#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cgi import parse_qs, escape
from wsgiref.simple_server import make_server
import time, json
from urllib import unquote

def getRequestBody(environ):
# the environment variable CONTENT_LENGTH may be empty or missing
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))

    except (ValueError):
        request_body_size = 0

    request_body = environ['wsgi.input'].read(request_body_size)

    return request_body


def application(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    write = start_response(status, response_headers)

    if environ['REQUEST_METHOD'] == 'POST':
        print "POST method"

        return_dict = {}

        dict_from_client = parse_qs(getRequestBody(environ))
        word_rows_json = unquote(dict_from_client['word_rows'][0])
        word_rows = json.loads(word_rows_json)
        print word_rows

        return_dict['from_client'] = word_rows
        return_json = json.dumps(return_dict)

        return return_json

    if environ['REQUEST_METHOD'] == 'GET':
        print "GET method"

        return_dict = {}

        return_dict['lock'] = "Mac"
        return_json = json.dumps(return_dict)

        return return_json


    return "WTF?"

port  = 2603
httpd = make_server('', port, application)
print "Serving HTTP on port {0}...".format(port)

httpd.serve_forever()

