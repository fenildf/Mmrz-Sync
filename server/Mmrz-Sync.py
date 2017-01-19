#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Bottle.py official tutorial: http://bottlepy.org/docs/dev/tutorial.html

# GET mothod params: request.params
# POST mothod params: request.forms

from bottle import route, run, template, view, static_file
from bottle import post, get, request, redirect
from db import MmrzSyncDBManager
import bottle
import configparser
import json, sys
import base64
import time

# Refer to: http://stackoverflow.com/questions/16865997/python-bottle-module-causes-error-413-request-entity-too-large
# There was a bug:
# If a client post something with a very large parameter, it will be encountered a "broken pipe" problem.
# The line below can change the Bottle's acceptable max-size of request.
# So this bug is no longer exist.
bottle.BaseRequest.MEMFILE_MAX = 1024 * 1024

bottle.debug(True)

PORT = 2603
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

def split_remindTime(remindTime, adjust=False):
    if adjust:
        remindTime += 59

    if remindTime > 0:
        days  = remindTime / (60 * 60 * 24)
        hours = remindTime % (60 * 60 * 24) / (60 * 60)
        mins  = remindTime % (60 * 60 * 24) % (60 * 60) / 60
        secs  = remindTime % (60 * 60 * 24) % (60 * 60) % 60
    else:
        days = hours = mins = secs = 0

    return days, hours, mins, secs

### static files
@route('/<filename>')
def server_static(filename):
    return static_file(filename, root='./static')

@route('/css/<filename>')
def server_static_css(filename):
    return static_file(filename, root='./static/css')

@route('/js/<filename>')
def server_static_js(filename):
    return static_file(filename, root='./static/js')

@route('/')
def index():
    req_thing = request.params.get('req_thing', None)
    if req_thing == "version_info":
        return version_info()

    else:
        redirect('/login')

@route('/login')
@view('login')
def login():
    return {}

@route('/signup')
@view('signup')
def signup():
    return {}

@route('/memorize')
@view('mmrz')
def mmrz():
    return {}

@route('/individual')
@view('individual')
def individual():
    return {}

@route('/wordbook')
@view('wordbook')
def show_wordbook():
    username = request.params.get('username', None)

    # username not available means username exist, connect it
    if not is_username_available(username):
        dbMgr = MmrzSyncDBManager(username)
        rows = dbMgr.readAllDB()
        dbMgr.closeDB()
    # else user name not exist, redirect to /
    else:
        redirect('/') 

    rows_for_return = []
    tail_of_8_times = []
    rows = sorted(rows, key=lambda row: row[3]) # from small to big
    for row in rows:
        row = list(row)

        word          = row[0]
        pronounce     = row[1]
        memTimes      = row[2]
        remindTime    = row[3]
        remindTimeStr = row[4]
        wordID        = row[5]

        remindTime -= int(time.time())
        days, hours, mins, secs = split_remindTime(remindTime, True)
        remindTimeStr = "{0}d-{1}h-{2}m".format(days, hours, mins)
        row[4] = remindTimeStr

        if memTimes >= 8:
            tail_of_8_times.append(row)
        else:
            rows_for_return.append(row)

    rows_for_return += tail_of_8_times

    return dict(rows=rows_for_return)

### posts
@post('/log_in/')
@post('/log_in')
def log_in():
    username = request.forms.get('username', None)
    password = request.forms.get('password', None)

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
    username = request.forms.get('username', None)
    password = request.forms.get('password', None)

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
    username = request.forms.get('username', None)
    password = request.forms.get('password', None)

    dict_for_return = dict(universal_POST_dict)
    if not verify_login(username, password):
        dict_for_return['verified'] = False
        dict_for_return['message_str'] = "login failed"
        json_for_return = json.dumps(dict_for_return)
        return json_for_return
    else:
        rows = request.forms['wordbook']
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

@post('/unmemorized_words/')
@post('/unmemorized_words')
def unmemorized_words():
    username = request.params.get('username', None)
    password = request.params.get('password', None)

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
        rows = dbMgr.readDB()
        dbMgr.closeDB()
        dict_for_return['verified'] = True
        dict_for_return['message_str'] = "Download success"
        dict_for_return['wordbook'] = rows
        json_for_return = json.dumps(dict_for_return)
        return json_for_return

@post('/update_row/')
@post('/update_row')
def update_row():
    username = request.forms.get('username', None)
    password = request.forms.get('password', None)

    dict_for_return = dict(universal_POST_dict)
    if not verify_login(username, password):
        dict_for_return['verified'] = False
        dict_for_return['message_str'] = "login failed"
        json_for_return = json.dumps(dict_for_return)
        return json_for_return
    else:
        row = request.forms['row']
        row = json.loads(row)
        dbMgr = MmrzSyncDBManager(username)
        dbMgr.createDB()
        dbMgr.updateDB(row)
        dbMgr.closeDB()
        dict_for_return['verified'] = True
        dict_for_return['message_str'] = "Update row success"
        json_for_return = json.dumps(dict_for_return)
        return json_for_return

### gets
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
    username = request.params.get('username', None)

    dbMgr = MmrzSyncDBManager(username)
    rows = dbMgr.readAllDB()
    dbMgr.closeDB()

    return json.dumps(rows)

@get('/get_shortest_remind/')
@get('/get_shortest_remind')
def get_shortest_remind():
    username = request.params.get('username', None)

    if not is_username_available(username):
        dbMgr = MmrzSyncDBManager(username)
        rows = dbMgr.readDB()
        dbMgr.closeDB()

        if len(rows) == 0:
            return "单词本中没有数据"

        rows = sorted(rows, key=lambda row: row[3]) # from small to big
        word          = rows[0][0]
        pronounce     = rows[0][1]
        memTimes      = rows[0][2]
        remindTime    = rows[0][3]
        remindTimeStr = rows[0][4]
        wordID        = rows[0][5]

        remindTime -= int(time.time())
        days, hours, mins, secs = split_remindTime(remindTime, True)
        remindTimeStr = "{0}d-{1}h-{2}m".format(days, hours, mins)
        remindTimeStr = "下次背诵 {0} 后开始".format(remindTimeStr)
    else:
        remindTimeStr = "数据获取错误"

    return remindTimeStr

@get('/download_wordbook/')
@get('/download_wordbook')
@post('/download_wordbook/')
@post('/download_wordbook')
def download_wordbook():
    username = request.params.get('username', None)
    password = request.params.get('password', None)

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
        dbMgr.closeDB()
        dict_for_return['verified'] = True
        dict_for_return['message_str'] = "Download success"
        dict_for_return['wordbook'] = rows
        json_for_return = json.dumps(dict_for_return)
        return json_for_return


run(host='0.0.0.0', port=PORT)


