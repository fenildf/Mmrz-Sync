#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cgi import parse_qs, escape
from wsgiref.simple_server import make_server
import time
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
    d = parse_qs(environ['QUERY_STRING'])
    read = parse_qs( getRequestBody(environ) )['q'][0]
    print unquote(read)
    write = start_response(status, response_headers)
    write("first write message\n")
    write("second write message\n")
    return "return message"

port  = 2603
httpd = make_server('', port, application)
print "Serving HTTP on port {0}...".format(port)

httpd.serve_forever()

