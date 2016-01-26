#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wsgiref.simple_server import make_server
from cgi import parse_qs, escape
from db import MmrzSyncDBManager
import configparser
import json, sys
import base64

"""
accept when POST:
{
    post_thing|
    "login_data": { "username": "", "password"(base64): "" }
}
------------------------------------------
return of POST:
{
    "verified": true/false,
    "message_str":  "" 
}
------------------------------------------
return when GET:
{
    req_thing|
    "occupied_client": "",
    "version_info": { "CLI": "", "GUI": ""},
    "message_str": "",
}
"""

CONFIG_PATH   = sys.path[0] + '/version.ini'

universal_POST_dict = {
    "verified": False,
    "message_str":  ""
}

universal_GET_dict = {
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

def verifyUserName(username):
    dbMgr = MmrzSyncDBManager("USERS")
    users = dict(dbMgr.read_USERS_DB())
    dbMgr.closeDB()

    return username in users

def verifyLogin(username, password):
    dbMgr = MmrzSyncDBManager("USERS")
    users = dict(dbMgr.read_USERS_DB())
    dbMgr.closeDB()
    
    return username in users and password == users[username]

def login_data(environ):
    dict_from_client = parse_qs(getRequestBody(environ))
    username = dict_from_client['username'][0]
    password_encrypted = dict_from_client['password'][0]
    password = password_encrypted # password = base64.b64decode(password_encrypted)

    dict_for_return = universal_POST_dict
    if verifyLogin(username, password):
        dict_for_return['verified'] = True
    else:
        dict_for_return['verified'] = False

    json_for_return = json.dumps(dict_for_return)
    return json_for_return

def sign_up(environ):
    dict_from_client = parse_qs(getRequestBody(environ))
    username = dict_from_client['username'][0]

    dict_for_return = universal_POST_dict
    if verifyUserName(username):
        dict_for_return['verified'] = True
    else:
        dict_for_return['verified'] = False

    json_for_return = json.dumps(dict_for_return)
    return json_for_return

def occupied_client(environ):
    dict_for_return = universal_GET_dict
    dict_for_return['lock'] = "Mac"
    json_for_return = json.dumps(dict_for_return)

    return json_for_return

def version_info(environ):
    cli, gui = getVersion()
    dict_for_return = universal_GET_dict
    dict_for_return['version_info'] = {"CLI": cli, "GUI": gui}
    json_for_return = json.dumps(dict_for_return)

    return json_for_return

def application(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    write = start_response(status, response_headers)

    if environ['REQUEST_METHOD'] == 'POST':
        received_param = parse_qs(environ['QUERY_STRING'])
        post_thing = received_param.get('post_thing')[0]

        if post_thing == 'login_data':
            return login_data(environ)

        if post_thing == 'sign_up':
            return sign_up(environ)

        return json.dumps(universal_POST_dict)

    if environ['REQUEST_METHOD'] == 'GET':
        received_param = parse_qs(environ['QUERY_STRING'])
        req_thing = received_param.get('req_thing')[0]

        print req_thing
        if req_thing == 'occupied_client':
            return occupied_client(environ)

        if req_thing == 'version_info':
            return version_info(environ)

        return json.dumps(universal_GET_dict)

    return "End of POST/GET"

if __name__ == '__main__':
    port  = 2603
    print "Serving HTTP on port {0}...".format(port)

    httpd = make_server('', port, application)
    httpd.serve_forever()


