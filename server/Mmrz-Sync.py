#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Bottle.py official tutorial: http://bottlepy.org/docs/dev/tutorial.html

# GET mothod params: request.params
# POST mothod params: request.forms

from bottle import route, run, template, request
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

### routes
@route('/')
def index():
    return "Hello, world!!!"


@route('/version_info')
def version_info():
    cli, gui = read_version()

    version = {}
    version['version_info'] = {"CLI": cli, "GUI": gui}

    return json.dumps(version)


run(host='localhost', port=PORT)


