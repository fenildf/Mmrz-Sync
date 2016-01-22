#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cgi import parse_qs, escape
from wsgiref.simple_server import make_server
from urllib import unquote
import configparser
import json, sys

CONFIG_PATH   = sys.path[0] + '/version.ini'

universal_dict = {
    'occupied_client': 'NULL',
    'version_info': {"CLI": "CLI-0.0.0", "GUI": "GUI-0.0.0"},
    'message_str': 'message from Mmrz-Sync server'
}

def getVersion():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    CLI_VERSION = config['MMRZ_VER']['CLI_VERSION']
    GUI_VERSION = config['MMRZ_VER']['GUI_VERSION']

    return CLI_VERSION, GUI_VERSION

def getRequestBody(environ):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))

    except (ValueError):
        request_body_size = 0

    return environ['wsgi.input'].read(request_body_size)

def application(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    write = start_response(status, response_headers)

    if environ['REQUEST_METHOD'] == 'POST':

        return_dict = {}

        dict_from_client = parse_qs(getRequestBody(environ))
        word_rows_json = unquote(dict_from_client['word_rows'][0])
        word_rows = json.loads(word_rows_json)
        print word_rows

        return_dict['from_client'] = word_rows
        return_json = json.dumps(return_dict)

        return return_json

    if environ['REQUEST_METHOD'] == 'GET':
        received_param = parse_qs(environ['QUERY_STRING'])
        req_thing = received_param.get('req_thing')[0]

        print req_thing
        if req_thing == 'occupied_client':
            dict_for_return = universal_dict
            dict_for_return['lock'] = "Mac"
            json_for_return = json.dumps(dict_for_return)

            return json_for_return

        if req_thing == 'version_info':
            cli, gui = getVersion()
            dict_for_return = universal_dict
            dict_for_return['version_info'] = {"CLI": cli, "GUI": gui}
            json_for_return = json.dumps(dict_for_return)

            return json_for_return

        dict_for_return = universal_dict
        dict_for_return['message_str'] = "GET method end"
        json_for_return = json.dumps(dict_for_return)
        return json_for_return

    dict_for_return = universal_dict
    dict_for_return['message_str'] = "no GET/POST method end"
    json_for_return = json.dumps(dict_for_return)
    return json_for_return

port  = 2603
httpd = make_server('', port, application)
print "Serving HTTP on port {0}...".format(port)

httpd.serve_forever()

