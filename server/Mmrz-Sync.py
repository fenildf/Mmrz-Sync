#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Bottle.py official tutorial: http://bottlepy.org/docs/dev/tutorial.html

# GET mothod params: request.params
# POST mothod params: request.forms

from bottle import route, run, template
from bottle import post, get, request
from db import MmrzSyncDBManager
import configparser
import json, sys
import base64

PORT = 3516 # 2603
CONFIG_PATH = sys.path[0] + '/version.ini'

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
@post('/log_in')
def log_in():
    username = request.forms['username']
    password = request.forms['password']

    dict_for_return = dict(universal_POST_dict)
    if verify_login(username, password):
        dict_for_return['verified'] = True
        dict_for_return['message_str'] = "logged in"
    else:
        dict_for_return['verified'] = False
        dict_for_return['message_str'] = "username or password not correct"

    json_for_return = json.dumps(dict_for_return)
    return json_for_return

### gets
@get('/')
def index():
    return "Hello, world!!!"

@get('/version_info')
def version_info():
    cli, gui = read_version()

    version = {}
    version['version_info'] = {"CLI": cli, "GUI": gui}

    return json.dumps(version)

@get('/database_info')
def database_info(environ):
    dbMgr = MmrzSyncDBManager("wordbook")
    rows = dbMgr.readAllDB()
    dbMgr.closeDB()

    return json.dumps(rows)


run(host='localhost', port=PORT)


