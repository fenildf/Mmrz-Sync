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
import socket
import base64
import pickle
import random
import time
import re
import os

def each_file(target):
    for root, dirs, files in os.walk(target):
        for f in files:
            yield os.path.join(root, f)

# pkl data format:
# pkl = {   
#     book_name: str,
#     total_lines: int,
#     last_import_time: str,
#     last_import_time_int: int,
# }

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

def cal_remind_time(memTimes, types):
    curTime = int(time.time())

    remindTime = {
        0: curTime + (60 * 5), # 5 minutes
        1: curTime + (60 * 30), # 30 minutes
        2: curTime + (60 * 60 * 12), # 12 hours
        3: curTime + (60 * 60 * 24), # 1 day
        4: curTime + (60 * 60 * 24 * 2), # 2 days
        5: curTime + (60 * 60 * 24 * 4), # 4 days
        6: curTime + (60 * 60 * 24 * 7), # 7 days
        7: curTime + (60 * 60 * 24 * 15), # 15 days
    }.get(memTimes, curTime)

    if types == "int":
        remindTime = remindTime
    elif types ==  "str":
        remindTime = time.strftime('%Y-%m-%d %H:%M:%S +0800', time.localtime(remindTime))

    return remindTime

def smart_import(path, username, quantity=100):
    if path == "":
        return

    if ".mmz" not in path and ".yb" not in path:
        return

    if ".mmz" in path:
        suffix = ".mmz"
    elif ".yb" in path:
        suffix = ".yb"
    else:
        suffix = ".*"

    fr = open("./WORDBOOK/{0}/data.pkl".format(username), "rb")
    pkl_data = pickle.load(fr)
    fr.close()

    fw = open("./WORDBOOK/{0}/data.pkl".format(username), "wb")
    pkl_data["last_import_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    pkl_data["last_import_time_int"] = int(time.time())
    pickle.dump(pkl_data, fw)
    fw.close()

    IMPORT_QUANTITY = quantity

    # split & count lines
    fr = open(path, "rb")
    content = fr.read()
    fr.close()
    content_list = content.split("\n")
    line_quantity = len(content_list)

    # get rand indexes & extract lines
    idx_range = line_quantity
    idx_amount = min(line_quantity, IMPORT_QUANTITY)
    rand_idxes = []
    extracted = []
    while len(rand_idxes) != idx_amount:
        rand_num = random.randint(1, line_quantity)
        if rand_num not in rand_idxes:
            extracted.append(content_list[rand_num - 1] + "\n")
            content_list[rand_num - 1] = ""

            rand_idxes.append(rand_num)

    # write back
    fw = open(path, "wb")
    fw.writelines([(line + "\n") for line in content_list if line != ""])
    fw.close

    dbMgr = MmrzSyncDBManager(username)

    for line in extracted:
        line = line.strip()

        if re.search("^[ |\t]*#.*", line) or line == "":
            continue # ignore comment line or null line

        if suffix == ".yb":
            line = line.replace(" ", "")
            mc = re.search("(.*)「(.*)」(.*)", line)
            if mc:
                if mc.group(2) == "":
                    wordInfo = [mc.group(1), mc.group(3)]
                else:
                    wordInfo = [mc.group(1), mc.group(2), mc.group(3)]
            else:
                print "load err"

        word          = wordInfo[0].decode("utf8")
        pronounce     = wordInfo[1].decode("utf8") if len(wordInfo) == 2 else "{0} -- {1}".format(wordInfo[1], wordInfo[2]).decode("utf8")
        memTimes      = 0
        remindTime    = cal_remind_time(memTimes, "int")
        remindTimeStr = cal_remind_time(memTimes, "str")
        wordID        = dbMgr.getMaxWordID() + 1

        row = [word, pronounce, memTimes, remindTime, remindTimeStr, wordID]
        dbMgr.insertDB(row)

    dbMgr.closeDB()

    return True

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
    username = request.params.get('username', None)

    fr = open("./WORDBOOK/{0}/data.pkl".format(username), "rb")
    pkl = pickle.load(fr)
    fr.close()

    fr = open("./WORDBOOK/{0}/{1}".format(username, pkl["book_name"]), "rb")
    lq = len(fr.read().split("\n"))
    fr.close()

    pkl["remained_words"] = lq
    pkl["import_rate"]    = (1 - round(float(lq) / float(pkl["total_lines"]), 4)) * 100

    days, hours, mins, secs = split_remindTime(int(time.time()) - pkl.get("last_import_time_int", 0))
    pkl["time_elapsed"]   = "{0}天{1}时{2}分".format(days, hours, mins)

    return pkl

@route('/ranking')
@view('ranking')
def ranking():
    db_info_list = []
    for path in each_file("./USERDB"):
        basename = os.path.basename(path)
        username = basename.replace(".db", "")

        if ".db" not in basename:
            continue

        if basename == "USERS.db":
            continue

        dbMgr = MmrzSyncDBManager(username)
        words = dbMgr.getMaxWordID()
        dbMgr.closeDB
        db_info_list.append([username, os.path.getmtime(path), words])

    db_info_list.sort(cmp = lambda u1, u2: cmp(u2[1], u1[1]))

    for user in db_info_list:
        user[1] = time.strftime('%Y-%m-%d %H:%M', time.localtime(user[1]))

    return dict(db_info_list = db_info_list)

@route('/wordbook')
@view('wordbook')
def show_wordbook():
    username = request.params.get('username', None)
    show_all = request.params.get('show_all', None)

    # username not available means username exist, connect it
    if not is_username_available(username):
        dbMgr = MmrzSyncDBManager(username)
        rows = dbMgr.readAllDB() if show_all == "yes" else dbMgr.readDB()
        word_quantity = len(dbMgr.readAllDB())
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

    return dict(rows=rows_for_return, word_quantity=word_quantity)

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

@post('/online_import/')
@post('/online_import')
def online_import():
    username = request.forms.get('username', None)
    password = request.forms.get('password', None)
    quantity = request.forms.get('quantity', None)
    quantity = int(quantity)

    dict_for_return = dict(universal_POST_dict)
    if not verify_login(username, password):
        dict_for_return['verified'] = False
        dict_for_return['message_str'] = "login failed"
        json_for_return = json.dumps(dict_for_return)
        return json_for_return
    else:
        dict_for_return['verified'] = True
        dict_for_return['message_str'] = "Online import success"
        json_for_return = json.dumps(dict_for_return)

        fr = open("./WORDBOOK/{0}/data.pkl".format(username), "rb")
        pkl = pickle.load(fr)
        fr.close()
        smart_import("./WORDBOOK/{0}/{1}".format(username, pkl["book_name"]), username, quantity)
        return json_for_return

@post('/mem_duration/')
@post('/mem_duration')
def mem_duration():
    return ""

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

# show serving IP (for debug)
myname = socket.getfqdn(socket.gethostname())
myaddr = socket.gethostbyname(myname)

print ""
print "Serving IP: " + myaddr
print ""

# run server
run(host='0.0.0.0', port=PORT)


