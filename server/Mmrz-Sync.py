#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Bottle.py official tutorial: http://bottlepy.org/docs/dev/tutorial.html

# GET mothod params: request.params
# POST mothod params: request.forms

from bottle import route, run, template
from bottle import post, get, request
from db import MmrzSyncDBManager
import bottle
import configparser
import json, sys
import base64

# Refer to: http://stackoverflow.com/questions/16865997/python-bottle-module-causes-error-413-request-entity-too-large
# There was a bug:
# If a client post something with a very large parameter, it will be encountered a "broken pipe" problem.
# The line below can change the Bottle's acceptable max-size of request.
# So this bug is no longer exist.
bottle.BaseRequest.MEMFILE_MAX = 1024 * 1024

bottle.debug(True)

PORT = 2603
CONFIG_PATH = sys.path[0] + '/version.ini'

POST_PARAMS = request.forms
GET_PARAMS  = request.params

universal_POST_dict = {
    "verified": False,
    "message_str":  ""
}

universal_GET_dict = {
    'occupied_client': 'NULL',
    'version_info': {"CLI": "CLI-0.0.0", "GUI": "GUI-0.0.0"},
    'message_str': 'message from Mmrz-Sync server'
}

### universal functions
def read_version():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    CLI_VERSION = config['MMRZ_VER']['CLI_VERSION']
    GUI_VERSION = config['MMRZ_VER']['GUI_VERSION']

    return CLI_VERSION, GUI_VERSION

def is_username_available(username):
    dbMgr = MmrzSyncDBManager("USERS")
    users = dict(dbMgr.read_USERS_DB())
    dbMgr.closeDB()

    return not username in users

def verify_login(username, password):
    dbMgr = MmrzSyncDBManager("USERS")
    users = dict(dbMgr.read_USERS_DB())
    dbMgr.closeDB()

    return username in users and password == users[username]

### posts
@post('/log_in/')
@post('/log_in')
def log_in():
    username = POST_PARAMS.get('username', None)
    password = POST_PARAMS.get('password', None)

    dict_for_return = dict(universal_POST_dict)
    if verify_login(username, password):
        dict_for_return['verified'] = True
        dict_for_return['message_str'] = "logged in"
    else:
        dict_for_return['verified'] = False
        dict_for_return['message_str'] = "username or password not correct"

    json_for_return = json.dumps(dict_for_return)
    return json_for_return

@post('/sign_up/')
@post('/sign_up')
def sign_up():
    username = POST_PARAMS.get('username', None)
    password = POST_PARAMS.get('password', None)

    dict_for_return = dict(universal_POST_dict)
    if is_username_available(username):
        dbMgr = MmrzSyncDBManager("USERS")
        dbMgr.insert_USERS_DB([username, password])
        dbMgr.closeDB()
        dict_for_return['verified'] = True
        dict_for_return['message_str'] = "Signed up"
    else:
        dict_for_return['verified'] = False
        dict_for_return['message_str'] = "Username not available"

    json_for_return = json.dumps(dict_for_return)
    return json_for_return

@post('/upload_wordbook/')
@post('/upload_wordbook')
def upload_wordbook():
    username = POST_PARAMS.get('username', None)
    password = POST_PARAMS.get('password', None)

    dict_for_return = dict(universal_POST_dict)
    if not verify_login(username, password):
        dict_for_return['verified'] = False
        dict_for_return['message_str'] = "login failed"
        json_for_return = json.dumps(dict_for_return)
        return json_for_return
    else:
        rows = POST_PARAMS.get('wordbook', None)
        rows = json.loads(rows)
        dbMgr = MmrzSyncDBManager(username)
        dbMgr.createDB()
        dbMgr.pruneDB()
        for row in rows:
            dbMgr.insertDB(row)
        dbMgr.closeDB()

        dict_for_return['verified'] = True
        dict_for_return['message_str'] = "upload done"
        json_for_return = json.dumps(dict_for_return)
        return json_for_return

### gets
@get('/')
def index():
    req_thing = GET_PARAMS.get('req_thing', None)
    if req_thing == "version_info":
        return version_info()

    else:
        return "Hello, world!!!"

@get('/version_info/')
@get('/version_info')
def version_info():
    cli, gui = read_version()

    version = {}
    version['version_info'] = {"CLI": cli, "GUI": gui}

    return json.dumps(version)

@get('/database_info/')
@get('/database_info')
def database_info():
    username = GET_PARAMS.get('username', None)

    dbMgr = MmrzSyncDBManager(username)
    rows = dbMgr.readAllDB()
    dbMgr.closeDB()

    return json.dumps(rows)

@get('/download_wordbook/')
@get('/download_wordbook')
def download_wordbook():
    username = GET_PARAMS.get('username', None)
    password = GET_PARAMS.get('password', None)

    dict_for_return = dict(universal_POST_dict)
    if not verify_login(username, password):
        dict_for_return['verified'] = False
        dict_for_return['message_str'] = "login failed"
        dict_for_return['wordbook'] = []
        json_for_return = json.dumps(dict_for_return)
        return json_for_return
    else:
        dbMgr = MmrzSyncDBManager(username)
        dbMgr.createDB()
        rows = dbMgr.readAllDB()
        dict_for_return['verified'] = True
        dict_for_return['message_str'] = "Download success"
        dict_for_return['wordbook'] = rows
        json_for_return = json.dumps(dict_for_return)
        return json_for_return


run(host='0.0.0.0', port=PORT)


