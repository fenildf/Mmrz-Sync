#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Bottle.py official tutorial: http://bottlepy.org/docs/dev/tutorial.html

# GET mothod params: request.params
# POST mothod params: request.forms

from bottle import route, run, template, view, static_file
from bottle import post, get, request, redirect
from bs4 import BeautifulSoup
from db import TikTimeDBManager, MmrzSyncDBManager
from MmrzCode import *
import MmrzMail
import chardet
import bottle
import urllib, urllib2
import gzip, StringIO
import configparser
import json, sys
import socket
import base64
import pickle
import random
import datetime, time, math
import re
import os

def each_file(target):
    for root, dirs, files in os.walk(target):
        for f in files:
            yield os.path.join(root, f)

class PickleManager:
    def __init__(self, username):
        self.path = "./WORDBOOK/{0}/data.pkl".format(username)

        if not os.path.exists(self.path):
            tmp_pkl = {}
            tmp_pkl["book_name"] = ""
            tmp_pkl["total_lines"] = 0
            tmp_pkl["last_import_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            tmp_pkl["last_import_time_int"] = int(time.time())

            fw = open(self.path, "wb")
            pickle.dump(tmp_pkl, fw)
            fw.close()

    def load_pkl(self):
        fr = open(self.path, "rb")
        self.pkl = pickle.load(fr)
        fr.close()

    def dump_pkl(self):
        fw = open(self.path, "wb")
        pickle.dump(self.pkl, fw)
        fw.close()

    def set_book_name(self, book_name):
        self.load_pkl()
        self.pkl["book_name"] = book_name
        self.dump_pkl()

    def set_total_lines(self, total_lines):
        self.load_pkl()
        self.pkl["total_lines"] = total_lines
        self.dump_pkl()

    def set_last_import_time(self):
        self.load_pkl()
        self.pkl["last_import_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.dump_pkl()

    def set_last_import_time_int(self):
        self.load_pkl()
        self.pkl["last_import_time_int"] = int(time.time())
        self.dump_pkl()

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
bottle.BaseRequest.MEMFILE_MAX = 1024 * 1024 * 5 # max size: 5 MB

bottle.debug(True)

PORT = 2603
CONFIG_PATH = sys.path[0] + '/version.ini'

universal_POST_dict = {
    "verified": False,
    "mmrz_code": MMRZ_CODE_Universal_Error,
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

def get_file_lines(path):
    fr = open(path, "rb")
    content = fr.read()
    fr.close()

    return len(filter(lambda x: x not in ['', '\r', '\n', '\r\n'], content.split("\n")))

def generate_verify_code():
    veryCode = ""

    # 6 bit length
    for i in range(6):
        veryCode += str(random.randint(0, 9))

    return veryCode

def is_username_available(username):
    dbMgr = MmrzSyncDBManager("USERS")
    users = dict([row[:2] for row in dbMgr.read_USERS_DB()])
    dbMgr.closeDB()

    return not username in users

def validate_username(username):
    if not 3 <= len(username) <= 20:
        return False

    if re.search("[^A-Za-z0-9]", username):
        return False

    return True

def validate_password(password):
    if not 3 <= len(password) <= 255:
        return False

    return True

def verify_login(username, password):
    dbMgr = MmrzSyncDBManager("USERS")
    users = dict([row[:2] for row in dbMgr.read_USERS_DB()])
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
        0: curTime + (60 * 0), # back end import always 0 minute, request from @smilebin818
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

    content_list = filter(lambda x: x not in ['', '\r', '\n', '\r\n'], content.split("\n"))
    line_quantity = len(content_list)

    # get rand indexes & extract lines
    idx_range = line_quantity # 随机数取值范围
    idx_amount = min(idx_range, IMPORT_QUANTITY) # 需要导入的数量
    rand_idxes = []
    extracted = []
    while len(rand_idxes) != idx_amount:
        rand_num = random.randint(1, idx_range)
        if rand_num not in rand_idxes:
            extracted.append(content_list[rand_num - 1] + "\n")
            content_list[rand_num - 1] = ""

            rand_idxes.append(rand_num)

    # write back
    fw = open(path, "wb")
    fw.writelines([(line + "\n") for line in content_list if line != ""])
    fw.close

    dbMgr = MmrzSyncDBManager(username)

    added = 0
    for line in extracted:
        line = line.strip()

        if re.search("^[ |\t]*#.*", line) or line == "":
            continue # ignore comment line or null line

        if suffix == ".mmz":
            wordInfo = line.split()
            if len(wordInfo) not in (2, 3):
                print "load err"
                continue

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
                continue

        word          = wordInfo[0].decode("utf8")
        pronounce     = wordInfo[1].decode("utf8") if len(wordInfo) == 2 else "{0} -- {1}".format(wordInfo[1], wordInfo[2]).decode("utf8")
        memTimes      = 0
        remindTime    = cal_remind_time(memTimes, "int")
        remindTimeStr = cal_remind_time(memTimes, "str")
        wordID        = dbMgr.getMaxWordID() + 1

        row = [word, pronounce, memTimes, remindTime, remindTimeStr, wordID]
        dbMgr.insertDB(row)
        added += 1

    dbMgr.closeDB()

    return added

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

@route('/img/<filename>')
def server_static_img(filename):
    return static_file(filename, root='./static/img')

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

@route('/setting')
@view('setting')
def setting():
    username = request.params.get('username', None)

    dbMgr = MmrzSyncDBManager("USERS")
    users = dbMgr.read_USERS_DB_DICT()
    dbMgr.closeDB()

    return {"username": username, "mailAddr": users[username]["mailAddr"] or "请输入邮箱"}

@route('/verify_email')
def verify_email():
    username = request.params.get('username', None)
    veriCode = request.params.get('veriCode', None)

    dbMgr = MmrzSyncDBManager("USERS")
    users = dbMgr.read_USERS_DB_DICT()

    now = int(time.time())
    veriCode_from_client = veriCode
    veriCode_from_db = users[username]["veriCode"]
    deadline = users[username]["deadline"]
    if veriCode_from_client == veriCode_from_db:
        if now < deadline:
            dbMgr.update_USERS_DB_mailAddr(username, users[username]["mail_new"])
            dbMgr.update_USERS_DB_mail_new(username, "")
            dbMgr.update_USERS_DB_mailModTime(username)

            message = "恭喜, 邮箱验证成功"
        else:
            message = "验证码已过期, 请重新发送验证码"
    else:
        message = "验证码无效, 请重试"

    dbMgr.closeDB()

    return message

@route('/chart')
@view('chart')
def chart():
    return {}

@route('/individual')
@view('individual')
def individual():
    username = request.params.get('username', None)

    user_folder = "./WORDBOOK/{0}/".format(username)
    user_pkl = "{0}/data.pkl".format(user_folder)

    if not os.path.exists(user_folder):
        os.mkdir(user_folder)

    if not os.path.exists(user_pkl):
        pklMgr = PickleManager(username)
        
        pklMgr.load_pkl()
        pklMgr.set_book_name("--")
        pklMgr.set_total_lines("--")
        pklMgr.set_last_import_time()
        pklMgr.set_last_import_time_int()
        pklMgr.dump_pkl()

    fr = open("./WORDBOOK/{0}/data.pkl".format(username), "rb")
    pkl = pickle.load(fr)
    fr.close()


    if not pkl["book_name"] == "--":
        fr = open("./WORDBOOK/{0}/{1}".format(username, pkl["book_name"]), "rb")
        content = fr.read()
        fr.close()

        lq = len(filter(lambda x: x not in ['', '\r', '\n', '\r\n'], content.split("\n")))

        pkl["remained_words"] = lq
        pkl["import_rate"]    = (1 - round(float(lq) / float(pkl["total_lines"]), 4)) * 100

        days, hours, mins, secs = split_remindTime(int(time.time()) - pkl.get("last_import_time_int", 0))
        pkl["time_elapsed"]   = "{0}天{1}时{2}分".format(days, hours, mins)
    else:
        pkl["book_name"] = "--"
        pkl["total_lines"] = "--"
        pkl["last_import_time"] = "--"
        pkl["last_import_time_int"] = "--"
        pkl["remained_words"] = "--"
        pkl["import_rate"] = "--"
        pkl["time_elapsed"] = "--"


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

        if "journal.db" in basename:
            continue

        dbMgr = MmrzSyncDBManager(username)
        words = dbMgr.getMaxWordID()
        dbMgr.closeDB()
        tikMgr = TikTimeDBManager()
        minutes = tikMgr.getMiniutesByWeek(username, time.time())
        tikMgr.closeDB()
        db_info_list.append([username, os.path.getmtime(path), words, minutes])

    db_info_list.sort(cmp = lambda u1, u2: cmp(u2[1], u1[1]))

    for user in db_info_list:
        user[1] = time.strftime('%Y-%m-%d %H:%M', time.localtime(user[1]))

    Year, Week, Day = datetime.date.fromtimestamp(int(time.time())).isocalendar()
    date  = time.strftime('%Y年%m月%d日', time.localtime())
    week  = "第{1}周".format(Year, Week)
    month = "{0}月".format(time.localtime()[1])
    year  = "{0}年".format(Year)


    return dict(db_info_list = db_info_list, date = date, week = week, month = month, year = year)

@route('/wordbook')
@view('wordbook')
def show_wordbook():
    username = request.params.get('username', None)
    page = int(request.params.get('page', 1))
    # show_all = request.params.get('show_all', None)

    # username not available means username exist, connect it
    if not is_username_available(username):
        dbMgr = MmrzSyncDBManager(username)

        # times TODO
        times = 'all'
        page_size = 200

        count = dbMgr.selete_UNMMRZ_COUNT(times)
        page_max = int(math.ceil(count/float(page_size)))

        params = [times, page_size, page - 1]
        rows = dbMgr.selete_UNMMRZ_DATA_BY_PAGE(params)

        word_quantity = len(dbMgr.readAllDB())
        dbMgr.closeDB()
    # else user name not exist, redirect to /
    else:
        redirect('/') 

    rows_for_return = []
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

        rows_for_return.append(row)

    rows_start = (page - 1) * 200

    return dict(rows=rows_for_return, page_max=page_max, word_quantity=word_quantity, rows_start=rows_start)

@route('/favoritebook')
@view('favoritebook')
def show_favoritebook():
    username = request.params.get('username', None)

    # username not available means username exist, connect it
    if not is_username_available(username):
        dbMgr = MmrzSyncDBManager(username)
        rows = dbMgr.read_FAVOURITE_DB()
        dbMgr.closeDB()

    # else user name not exist, redirect to /
    else:
        redirect('/') 

    rows_for_return = []
    for row in rows:
        row = list(row)

        wordID        = row[0]
        word          = row[1]
        pronounce     = row[2]
        favourite     = row[3]

        rows_for_return.append(row)

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
    if not is_username_available(username):
        dict_for_return['verified'] = False
        dict_for_return['mmrz_code'] = MMRZ_CODE_Username_Not_Available_Error
        dict_for_return['message_str'] = "Username not available"

    elif not validate_username(username):
        dict_for_return['verified'] = False
        dict_for_return['mmrz_code'] = MMRZ_CODE_Username_Not_Valid
        dict_for_return['message_str'] = "Username not valid"

    elif not validate_password(password):
        dict_for_return['verified'] = False
        dict_for_return['mmrz_code'] = MMRZ_CODE_Password_Not_Valid
        dict_for_return['message_str'] = "Password not valid"

    else:
        dbMgr = MmrzSyncDBManager("USERS")
        dbMgr.insert_USERS_DB([username, password])
        dbMgr.closeDB()
        dict_for_return['verified'] = True
        dict_for_return['mmrz_code'] = MMRZ_CODE_Signup_OK
        dict_for_return['message_str'] = "Signed up"

    json_for_return = json.dumps(dict_for_return)
    return json_for_return

@post('/update_password/')
@post('/update_password')
def update_password():
    username = request.forms.get('username', None)
    password = request.forms.get('password', None)
    new_pass = request.forms.get('new_pass', None)

    dict_for_return = dict(universal_POST_dict)
    if not verify_login(username, password):
        dict_for_return['verified'] = False
        dict_for_return['message_str'] = "login failed"
        json_for_return = json.dumps(dict_for_return)
        return json_for_return
    else:
        dbMgr = MmrzSyncDBManager("USERS")
        dbMgr.update_USERS_DB([username, new_pass])
        dbMgr.closeDB()

        dict_for_return['verified'] = True
        dict_for_return['message_str'] = "password updated"
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

@post('/upload_lexicon/')
@post('/upload_lexicon')
def upload_lexicon():
    username = request.forms.get('username', None)
    password = request.forms.get('password', None)
    wordfile = request.files.get('wordfile', None)

    dict_for_return = dict(universal_POST_dict)
    if not wordfile:
        dict_for_return['verified'] = False
        dict_for_return['message_str'] = "word file not specified"
        json_for_return = json.dumps(dict_for_return)
        return json_for_return

    if not verify_login(username, password):
        dict_for_return['verified'] = False
        dict_for_return['message_str'] = "login failed"
        json_for_return = json.dumps(dict_for_return)
        return json_for_return
    else:
        target_folder = "./WORDBOOK/{0}/".format(username)
        name, ext = os.path.splitext(wordfile.filename)

        for path in each_file(target_folder):
            ext = os.path.basename(path).split(".")[-1].lower()
            if ext in ("mmz", "yb"):
                os.remove(path)

        wordfile.save(target_folder)

        wordfile_path = target_folder + wordfile.filename
        pklMgr = PickleManager(username)
        pklMgr.load_pkl()
        pklMgr.set_book_name(wordfile.filename)
        pklMgr.set_total_lines(get_file_lines(wordfile_path))
        pklMgr.set_last_import_time()
        pklMgr.set_last_import_time_int()
        pklMgr.dump_pkl()

        with open(wordfile_path, "rb") as fr:
            content = ""; idx = 0
            for line in fr:
                idx += 1
                content += line

                if idx == 50:
                    break

        encoding = chardet.detect(content)['encoding'].lower()

        dict_for_return['verified'] = True
        dict_for_return['message_str'] = "upload done"
        dict_for_return['encoding'] = encoding
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
        dict_for_return['wordfavourite'] = []
        json_for_return = json.dumps(dict_for_return)
        return json_for_return
    else:
        timeStamp = int(time.time())

        dbMgr = MmrzSyncDBManager(username)
        dbMgr.createDB()
        rows = dbMgr.readDB(timeStamp)
        fav  = dbMgr.read_WORD_FAVOURITE_DB(timeStamp)
        dbMgr.closeDB()
        dict_for_return['verified'] = True
        dict_for_return['message_str'] = "Download success"
        dict_for_return['wordbook'] = rows
        dict_for_return['wordfavourite'] = fav
        json_for_return = json.dumps(dict_for_return)
        return json_for_return

@post('/update_word_favourite/')
@post('/update_word_favourite')
def update_word_favourite():
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

        is_favourite = row[1]
        if is_favourite == 0:
            dbMgr.delete_FAVOURITE_DB(row[0])
            dict_for_return['message_str'] = "取消收藏成功！"
        else:
            count = dbMgr.insert_CHECK_FAVOURITE_DB(row[0])
            if count == 0 :
                dbMgr.insert_FAVOURITE_DB(row)
                dict_for_return['message_str'] = "收藏成功！"
            else:
                dict_for_return['message_str'] = "已在别处进行过收藏！"

        dbMgr.closeDB()
        dict_for_return['verified'] = True
        dict_for_return['verified_info'] = row
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

        fr = open("./WORDBOOK/{0}/data.pkl".format(username), "rb")
        pkl = pickle.load(fr)
        fr.close()
        added = smart_import("./WORDBOOK/{0}/{1}".format(username, pkl["book_name"]), username, quantity)
        dict_for_return['added'] = added

        json_for_return = json.dumps(dict_for_return)
        return json_for_return

@post('/tik_tik/')
@post('/tik_tik')
def tik_tik():
    username = request.forms.get('username', None)

    if not username:
        return "username is None"

    localtime  = time.localtime()
    timeStamp  = int(time.time()) # 唯一秒数
    Year, Week, Day = datetime.date.fromtimestamp(timeStamp).isocalendar()
    uniqMinute = timeStamp / 60  # 唯一分钟数
    uniqHour   = uniqMinute / 60 # 唯一小时数
    uniqDate   = uniqHour / 24   # 唯一天数
    theYear    = localtime[0]    # 年: 2017年
    theMonth   = localtime[1]    # 月份: 2 (2017年2月)
    theDate    = localtime[2]    # 天数: 22 (2月22)
    theHour    = localtime[3]    # 小时数: 17 (17点)
    theWeek    = Week            # 周数: 8 (第八周)
    theDay     = Day             # 周几: 3 (周3)


    tikMgr = TikTimeDBManager()
    tikInfo = [username, timeStamp, uniqMinute, uniqHour, uniqDate, theYear, theMonth, theDate, theHour, theWeek, theDay]
    if uniqMinute != tikMgr.getMaxUniqMinute(username):
        tikMgr.insertDB(tikInfo)
    else:
        pass
    tikMgr.closeDB()

    return "tik_tik: OK"

@post('/send_verification_mail/')
@post('/send_verification_mail')
def send_verification_mail():
    username = request.forms.get('username', None)
    mailAddr = request.forms.get('mailAddr', None)

    dict_for_return = dict(universal_POST_dict)

    dbMgr = MmrzSyncDBManager("USERS")
    users = dbMgr.read_USERS_DB_DICT()

    now = time.time()
    last_change_time = users[username]["mailModTime"]
    mail_change_period = (now - last_change_time) / 60 / 60 / 24 # by day

    last_send_time = users[username]["mailSendTime"]
    mail_send_period = (now - last_send_time) / 60 # by minute

    mailAddr_from_client = mailAddr
    mailAddr_from_db = users[username]["mailAddr"]

    # mail address remain the same
    if mailAddr_from_client == mailAddr_from_db:
        dict_for_return["mmrz_code"] = MMRZ_CODE_Email_Address_Not_Changed

    # mail address changed
    else:
        # mail address can be changed every 7 days
        if mail_change_period <= 7:
            dict_for_return["mmrz_code"] = MMRZ_CODE_Email_Modification_Frequency_Limit_Error
        # mail address not was changed 7 days ago or even longer
        else:
            # verification mail can be send every 5 minutes
            if mail_send_period <= 5:
                dict_for_return["mmrz_code"] = MMRZ_CODE_Email_Send_Frequency_Limit_Error
            else:
                dict_for_return["mmrz_code"] = MMRZ_CODE_Email_Send_OK
                veriCode = generate_verify_code()

                dbMgr.update_USERS_DB_mail_new(username, mailAddr_from_client)
                dbMgr.update_USERS_DB_veriCode(username, veriCode)
                dbMgr.update_USERS_DB_deadline(username)
                dbMgr.update_USERS_DB_mailSendTime(username)

                MmrzMail.send_mail(username = username, p_veriCode = veriCode, p_to = mailAddr)

    json_for_return = json.dumps(dict_for_return)

    dbMgr.closeDB()

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
        rows = dbMgr.getNearestRemindRow()
        maxID = dbMgr.getMaxWordID()
        dbMgr.closeDB()

        if maxID == 0:
            return "新用户请先导入单词"

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

@get('/get_hujiang_tts/')
@get('/get_hujiang_tts')
def get_hujiang_tts():
    key_word = request.params.get('key_word', None)
    job_id   = request.params.get('job_id', None)

    if not key_word:
        return "key_word is null"

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, sdch',
    }

    url = "http://dict.hjenglish.com/jp/jc/" + urllib.quote(key_word)

    req = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(req)
    compressedData = response.read()

    compressedStream = StringIO.StringIO(compressedData)
    gzipper = gzip.GzipFile(fileobj=compressedStream)
    html = gzipper.read()

    soup = BeautifulSoup(html, "html.parser")

    ret_info = {
        "found": False,
        "message_str": "",
        "tts_url": "",
        "job_id": job_id,
    }

    jpSound_list = soup.select('span[class=jpSound]')
    if len(jpSound_list) < 1:
        ret_info["found"] = False
        ret_info["message_str"] = "jpSound not found"
        return json.dumps(ret_info)

    jpSound = str(jpSound_list[0])
    mc = re.search("GetTTSVoice\(\"(.*?)\"\)", jpSound)
    if not mc:
        ret_info["found"] = False
        ret_info["message_str"] = "tts_url not found"
        return json.dumps(ret_info)

    tts_url = mc.group(1)
    ret_info["found"] = True
    ret_info["message_str"] = "tts_url is found"
    ret_info["tts_url"] = tts_url
    return json.dumps(ret_info)

@get('/get_weekly_mmrz_time/')
@get('/get_weekly_mmrz_time')
def get_weekly_mmrz_time():
    username  = request.params.get('username', None)

    tikMgr = TikTimeDBManager()
    weekly_data = tikMgr.getMiniutesDetailsByWeek(username, int(time.time()))
    tikMgr.closeDB()

    return json.dumps(weekly_data)

@get('/get_ranking_info/')
@get('/get_ranking_info')
def get_ranking_info():
    period  = request.params.get('period', None)

    rank_info = []
    tikMgr = TikTimeDBManager()

    if period == "day":
        rank_info = tikMgr.getDailyRanking(int(time.time()))
    elif period == "week":
        rank_info = tikMgr.getWeeklyRanking(int(time.time()))
    elif period == "month":
        rank_info = tikMgr.getMonthlyRanking(int(time.time()))
    elif period == "year":
        rank_info = tikMgr.getYearlyRanking(int(time.time()))
    else:
        rank_info = []

    tikMgr.closeDB()

    # append 5 users in the end
    rank_info += [("None", 0) for i in range(5)]

    return json.dumps(rank_info)

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

# user gevent
# import gevent; from gevent import monkey; monkey.patch_all()

# run server
run(host='0.0.0.0', port=PORT, server='paste')


