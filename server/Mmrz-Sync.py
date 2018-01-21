#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Bottle.py official tutorial: http://bottlepy.org/docs/dev/tutorial.html

# GET mothod params: request.params
# POST mothod params: request.forms

from bottle import route, run, template, view, static_file
from bottle import post, get, request, redirect
from bs4 import BeautifulSoup
from SQLiteDBManager import TikTimeDBManager, MmrzSyncDBManager
from MongoDBManager import MongoDBManager
from MmrzLog import log
from MmrzCode import *
import requests
import MmrzMail
import chardet
import bottle
import urllib, urllib2
import gzip, StringIO
import configparser
import json, sys
import socket
import base64
import random
import shutil
import datetime, time, math
import re
import os

static_file_verion = 'v=1057'

def each_file(target):
    for root, dirs, files in os.walk(target):
        for f in files:
            yield os.path.join(root, f)

# jsn data format:
# jsn = {   
#     book_name: str,
#     total_lines: int,
#     last_import_time: str,
#     last_import_time_int: int,
# }
class JsonManager:
    def __init__(self, username):
        self.path = "./WORDBOOK/{0}/data.json".format(username)

        if not os.path.exists(self.path):
            tmp_json = {}
            tmp_json["book_name"] = ""
            tmp_json["total_lines"] = 0
            tmp_json["last_import_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            tmp_json["last_import_time_int"] = int(time.time())

            fw = open(self.path, "wb")
            fw.write(json.dumps(tmp_json))
            fw.close()

    def load_jsn(self):
        fr = open(self.path, "rb")
        content = fr.read()
        fr.close()
        jsn = json.loads(content)
        for k, v in jsn.items():
            if type(v) == type(u""):
                jsn[k] = v.encode("utf-8")
        self.jsn = jsn

    def dump_jsn(self):
        fw = open(self.path, "wb")
        fw.write(json.dumps(self.jsn, indent=4))
        fw.close()

    def set_book_name(self, book_name):
        self.load_jsn()
        self.jsn["book_name"] = book_name
        self.dump_jsn()

    def set_total_lines(self, total_lines):
        self.load_jsn()
        self.jsn["total_lines"] = total_lines
        self.dump_jsn()

    def set_last_import_time(self):
        self.load_jsn()
        self.jsn["last_import_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.dump_jsn()

    def set_last_import_time_int(self):
        self.load_jsn()
        self.jsn["last_import_time_int"] = int(time.time())
        self.dump_jsn()

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
    "message_str":  "",
}

universal_GET_dict = {
    'occupied_client': 'NULL',
    'version_info': {"CLI": "CLI-0.0.0", "GUI": "GUI-0.0.0"},
    'message_str': 'message from Mmrz-Sync server',
}

universal_ROUTE_dict = {
    'static_file_version': static_file_verion,
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

def get_timestamp_token_from_db(username):
    try:
        dbMgr = MongoDBManager()
        userData = dbMgr.query_memorize_state(username)
        timestamp_token = userData.get('timestamp_token', sys.maxint)
        dbMgr.closeDB()
    except:
        timestamp_token = sys.maxint

    return timestamp_token

def make_lexicon_dict():
    """
    lexicon_dict[0]: lexicon_name
    lexicon_dict[1]: lexicon_line
    """

    lexicon_path = "./LEXICONS/"

    if not os.path.exists(lexicon_path):
        lexicon_dict = {
            "lexicon_1": ("fake1.voc", 3584),
            "lexicon_2": ("fake2.voc", 2812),
        }
    else:
        lexicon_dict = {}
        lexicon_list = sorted(os.listdir(lexicon_path))
        for i in range(len(lexicon_list)):
            file_path  = lexicon_path + lexicon_list[i]
            file_lines = get_file_lines(file_path)
            lexicon_dict["lexicon_{0}".format(i)] = (lexicon_list[i], file_lines)

    return lexicon_dict

def clean_lexicon_in_user_folder(username):
    target_folder = "./WORDBOOK/{0}/".format(username)

    for path in each_file(target_folder):
        ext = os.path.basename(path).split(".")[-1].lower()
        if ext in ("mmz", "voc", "yb"):
            os.remove(path)

    return None

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

def smart_import(path, username, quantity=100, is_smart=True):
    if path == "":
        return

    if ".mmz" not in path and ".voc" not in path and ".yb" not in path:
        return

    if ".mmz" in path:
        suffix = ".mmz"
    elif ".voc" in path:
        suffix = ".voc"
    elif ".yb" in path:
        suffix = ".yb"
    else:
        suffix = ".*"

    jsnMgr = JsonManager(username)
    jsnMgr.load_jsn()
    jsnMgr.set_last_import_time()
    jsnMgr.set_last_import_time_int()
    jsnMgr.dump_jsn()

    IMPORT_QUANTITY = quantity

    # split & count lines
    fr = open(path, "rb")
    content = fr.read()
    fr.close()

    content_list = filter(lambda x: x not in ['', '\r', '\n', '\r\n'], content.split("\n"))
    line_quantity = len(content_list)

    # get rand indexes & extract lines
    idx_range = line_quantity if is_smart else IMPORT_QUANTITY # 随机数取值范围
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

        if suffix == ".yb" or suffix == ".voc":
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

def query_hujiang(key_word):
    """
    return value:
    1. OK: list object
    2. NG: [] null list
    """

    if not key_word:
        return []

    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
        'Accept-Encoding': 'gzip, deflate, sdch',
        }

    url = "https://m.hujiang.com/d/dict_jp_api.ashx?type=jc&w={0}".format(urllib.quote(key_word))

    proxies = {}
    response = requests.get(url, headers=headers, verify=False, proxies=proxies)
    try:
        defines = response.json()
    except:
        return []

    for i in range(len(defines)):
        Comment = defines[i]["Comment"]
        comments = re.findall("<br/>([^a-zA-Z]+)<br/>", Comment)

        # 如果未找到前后<br>包裹的字符串, 则找出以<br>结尾的第一个字符串
        if not comments:
            comments = re.findall("^([^a-zA-Z]+?)<br/>", Comment)

        # 仍未找到, 则找出两个<br>间的内容, 不考虑是否含有英文字符
        if not comments:
            mc = re.search("<br/>(.+?)<br/>", Comment)
            if mc:
                comments = mc.groups(1)

        tmp = ", ".join(comments)

        # 如果tmp为空, 则取出原有完整的样子
        # tmp = Comment if not tmp else tmp

        # 取出包含【】的所有内容
        # mch = re.search(u"(【.+?】)", tmp)
        # tmp = mch.group(1) if mch else tmp

        # 常规清洗处理
        tmp = re.sub(u"\（.+?\）",   "", tmp)
        tmp = re.sub(u"\(.+?\)",  "", tmp)
        tmp = re.sub(u"。+?",     "", tmp)

        defines[i]["Comment"] = tmp

        defines[i]["PronounceJp"] = re.sub("\[|\]", "", defines[i]["PronounceJp"])

    return defines

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

@route('/layer/<filename:path>')
def server_static_img(filename):
    return static_file(filename, root='./static/layer')

@route('/')
def index():
    if request.params.get('req_thing') == "version_info":
        return version_info()

    username = request.get_cookie('username')
    password = request.get_cookie('password')
    password = urllib.unquote(password) if password else None

    return dictionary()

@route('/login')
@view('login')
def login():
    return dict(universal_ROUTE_dict)

@route('/signup')
@view('signup')
def signup():
    return dict(universal_ROUTE_dict)

@route('/memorize')
@view('mmrz')
def mmrz():
    username = request.get_cookie('username')
    password = request.get_cookie('password')
    password = urllib.unquote(password) if password else None

    if not verify_login(username, password):
        redirect('/')

    # need_https = "localhost" not in request.url
    need_https = False

    return_dict = dict(universal_ROUTE_dict)
    return_dict.update(dict(need_https=need_https))
    return return_dict

@route('/setting')
@view('setting')
def setting():
    username = request.get_cookie('username')
    password = request.get_cookie('password')
    password = urllib.unquote(password) if password else None

    if not verify_login(username, password):
        redirect('/')

    dbMgr = MmrzSyncDBManager("USERS")
    users = dbMgr.read_USERS_DB_DICT()
    dbMgr.closeDB()

    return_dict = dict(universal_ROUTE_dict)
    return_dict.update({"username": username, "mailAddr": "" if users[username]["mailAddr"] == None else users[username]["mailAddr"]})
    return return_dict

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
    return dict(universal_ROUTE_dict)

@route('/individual')
@view('individual')
def individual():
    username = request.get_cookie('username')
    password = request.get_cookie('password')
    password = urllib.unquote(password) if password else None

    if not verify_login(username, password):
        redirect('/')

    user_folder = "./WORDBOOK/{0}/".format(username)
    user_jsn = "{0}/data.json".format(user_folder)

    if not os.path.exists(user_folder):
        os.mkdir(user_folder)

    if not os.path.exists(user_jsn):
        jsnMgr = JsonManager(username)
        
        jsnMgr.load_jsn()
        jsnMgr.set_book_name("--")
        jsnMgr.set_total_lines("--")
        jsnMgr.set_last_import_time()
        jsnMgr.set_last_import_time_int()
        jsnMgr.dump_jsn()

    jsnMgr = JsonManager(username)
    jsnMgr.load_jsn()
    jsn = jsnMgr.jsn

    if not jsn["book_name"] == "--":
        fr = open("./WORDBOOK/{0}/{1}".format(username, jsn["book_name"]), "rb")
        content = fr.read()
        fr.close()

        lq = len(filter(lambda x: x not in ['', '\r', '\n', '\r\n'], content.split("\n")))

        jsn["remained_words"] = lq
        jsn["import_rate"]    = (1 - round(float(lq) / float(jsn["total_lines"]), 4)) * 100

        days, hours, mins, secs = split_remindTime(int(time.time()) - jsn.get("last_import_time_int", 0))
        jsn["time_elapsed"]   = "{0}天{1}时{2}分".format(days, hours, mins)
    else:
        jsn["book_name"] = "--"
        jsn["total_lines"] = "--"
        jsn["last_import_time"] = "--"
        jsn["last_import_time_int"] = "--"
        jsn["remained_words"] = "--"
        jsn["import_rate"] = "--"
        jsn["time_elapsed"] = "--"

    return_dict = dict(universal_ROUTE_dict)
    return_dict.update(jsn)
    return return_dict

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

    return_dict = dict(universal_ROUTE_dict)
    return_dict.update(dict(db_info_list = db_info_list, date = date, week = week, month = month, year = year))
    return return_dict

@route('/dict')
def dict_short():
    query = request.urlparts.query
    url = '/dictionary?{0}'.format(query) if query else '/dictionary'
    redirect(url)

@route('/dictionary')
@view('dictionary')
def dictionary():
    username = request.get_cookie('username')
    password = request.get_cookie('password')
    password = urllib.unquote(password) if password else None

    key_word = request.params.get('key_word', None)

    verified = verify_login(username, password)

    if not key_word:
        defines = None
    else:
        defines = query_hujiang(key_word)

    return_dict = dict(universal_ROUTE_dict)
    return_dict.update(dict(defines=defines, verified=verified, key_word=key_word))
    return return_dict

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

        count = dbMgr.select_UNMMRZ_COUNT(times)
        page_max = int(math.ceil(count/float(page_size)))

        params = [times, page_size, page - 1]
        rows = dbMgr.select_UNMMRZ_DATA_BY_PAGE(params)

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

    return_dict = dict(universal_ROUTE_dict)
    return_dict.update(dict(rows=rows_for_return, page_max=page_max, word_quantity=word_quantity, rows_start=rows_start))
    return return_dict

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

    return_dict = dict(universal_ROUTE_dict)
    return_dict.update(dict(rows=rows_for_return))
    return return_dict

@route('/layer_edit')
@view('layer_edit')
def layer_edit():
    return dict(universal_ROUTE_dict)

@route('/layer_select')
@view('layer_select')
def layer_select():
    lexicon_dict = make_lexicon_dict()

    return_dict = dict(universal_ROUTE_dict)
    return_dict.update(dict(lexicon_dict=lexicon_dict))
    return return_dict

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
        dbMgr.insert_USERS_DB([username, password, "", "", "000000", 0, 0, 0])
        dbMgr.closeDB()
        dict_for_return['verified'] = True
        dict_for_return['mmrz_code'] = MMRZ_CODE_Signup_OK
        dict_for_return['message_str'] = "Signed up"

        # notify to wechat when new user signed up
        text = urllib.quote("New user notification: {0}".format(username))
        urllib2.urlopen("http://zhanglintc.work:8000/send?text={0}".format(text))

    json_for_return = json.dumps(dict_for_return)
    return json_for_return

@post('/select_lexicon/')
@post('/select_lexicon')
def select_lexicon():
    username = request.get_cookie('username')
    password = request.get_cookie('password')
    password = urllib.unquote(password) if password else None

    dict_for_return = dict(universal_POST_dict)
    if not verify_login(username, password):
        dict_for_return['verified'] = False
        dict_for_return['mmrz_code'] = MMRZ_CODE_Universal_Verification_Fail
        dict_for_return['message_str'] = "verify failed"
    else:
        lexicon_id = request.forms.get('lexicon_id')
        lexicon_dict = make_lexicon_dict()
        lexicon_name = lexicon_dict[lexicon_id][0]
        dict_for_return['verified'] = True
        try:
            clean_lexicon_in_user_folder(username)
            shutil.copy2('./LEXICONS/{0}'.format(lexicon_name), './WORDBOOK/{0}/{1}'.format(username, lexicon_name))
            jsnMgr = JsonManager(username)

            jsnMgr.load_jsn()
            jsnMgr.set_book_name(lexicon_name)
            jsnMgr.set_total_lines(get_file_lines('./LEXICONS/{0}'.format(lexicon_name)))
            jsnMgr.set_last_import_time()
            jsnMgr.set_last_import_time_int()
            jsnMgr.dump_jsn()

            dict_for_return['mmrz_code'] = MMRZ_CODE_Universal_OK
            dict_for_return['message_str'] = "select_lexicon OK"
        except:
            dict_for_return['mmrz_code'] = MMRZ_CODE_Universal_Error
            dict_for_return['message_str'] = "select_lexicon failed"

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
    filename = request.forms.get('filename', None)
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
        name, ext = os.path.splitext(filename)

        for path in each_file(target_folder):
            ext = os.path.basename(path).split(".")[-1].lower()
            if ext in ("mmz", "voc", "yb"):
                os.remove(path)

        wordfile_path = target_folder + filename
        wordfile.save(wordfile_path)
    
        jsnMgr = JsonManager(username)
        jsnMgr.load_jsn()
        jsnMgr.set_book_name(filename)
        jsnMgr.set_total_lines(get_file_lines(wordfile_path))
        jsnMgr.set_last_import_time()
        jsnMgr.set_last_import_time_int()
        jsnMgr.dump_jsn()

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

@post('/is_state_cache_available/')
@post('/is_state_cache_available')
def is_state_cache_available():
    username = request.forms.get('username', None)
    password = request.forms.get('password', None)

    dict_for_return = dict(universal_POST_dict)
    if not verify_login(username, password):
        dict_for_return['mmrz_code'] = MMRZ_CODE_Universal_Verification_Fail
        json_for_return = json.dumps(dict_for_return)

        return json_for_return

    else:
        dbMgr = MongoDBManager()
        userData = dbMgr.query_memorize_state(username)
        dbMgr.closeDB()

        state_cached = userData.get('state_cached', False)
        dict_for_return['mmrz_code'] = MMRZ_CODE_Universal_OK
        dict_for_return['state_cached'] = state_cached
        json_for_return = json.dumps(dict_for_return)

        return json_for_return

@post('/query_timestamp_token/')
@post('/query_timestamp_token')
def query_timestamp_token():
    username = request.get_cookie('username')
    password = request.get_cookie('password')
    password = urllib.unquote(password) if password else None

    dict_for_return = dict(universal_POST_dict)
    if not verify_login(username, password):
        dict_for_return['mmrz_code'] = MMRZ_CODE_Universal_Verification_Fail
        json_for_return = json.dumps(dict_for_return)

        return json_for_return

    else:
        timestamp_token = get_timestamp_token_from_db(username)
        dict_for_return['mmrz_code'] = MMRZ_CODE_Universal_OK
        dict_for_return['timestamp_token'] = timestamp_token
        json_for_return = json.dumps(dict_for_return)

        return json_for_return

@post('/verify_eiginvalue/')
@post('/verify_eiginvalue')
def verify_eiginvalue():
    username = request.forms.get('username', None)
    password = request.forms.get('password', None)

    dict_for_return = dict(universal_POST_dict)
    if not verify_login(username, password):
        dict_for_return['mmrz_code'] = MMRZ_CODE_Universal_Verification_Fail
        json_for_return = json.dumps(dict_for_return)

        return json_for_return

    else:
        dbMgr = MongoDBManager()
        userData = dbMgr.query_memorize_state(username)
        dbMgr.closeDB()

        rows_length_fromDB = userData.get('rows_length', 0)
        current_cursor_fromDB = userData.get('current_cursor', 0)
        rows_length_from_client = request.forms.get('rows_length', 0)
        current_cursor_from_client = request.forms.get('current_cursor', 0)

        if rows_length_from_client == rows_length_fromDB and current_cursor_from_client == current_cursor_fromDB:
            dict_for_return["mmrz_code"] = MMRZ_CODE_SaveState_Same_Eigenvalue
        else:
            dict_for_return["mmrz_code"] = MMRZ_CODE_SaveState_Diff_Eigenvalue

        return json.dumps(dict_for_return)

@post('/save_current_state/')
@post('/save_current_state')
def save_current_state():
    username = request.forms.get('username', None)
    password = request.forms.get('password', None)

    timestamp_token_from_client = request.forms.get('timestamp_token', 0)
    timestamp_token_from_db = get_timestamp_token_from_db(username)
    timestamp_token_from_client = float(timestamp_token_from_client)
    timestamp_token_from_db = float(timestamp_token_from_db)

    dict_for_return = dict(universal_POST_dict)
    if not verify_login(username, password):
        dict_for_return['mmrz_code'] = MMRZ_CODE_Universal_Verification_Fail

        json_for_return = json.dumps(dict_for_return)
        return json_for_return
    else:
        current_state = request.forms.get('current_state', "[]")
        current_state = json.loads(current_state)
        rows_length_from_client = request.forms.get('rows_length', 0)
        current_cursor_from_client = request.forms.get('current_cursor', 0)
        max_size_this_turn_from_client = request.forms.get('max_size_this_turn', 0)
        timestamp_token = time.time()

        # not save state if state length is 0
        if len(current_state) == 0:
            dict_for_return['mmrz_code'] = MMRZ_CODE_Universal_Error # this error code better changed to something like: MMRZ_CODE_State_Length_Zero
            json_for_return = json.dumps(dict_for_return)
            return json_for_return

        document = {
            "username": username,
            "state_cached": True,
            "rows_length": rows_length_from_client,
            "current_cursor": current_cursor_from_client,
            "max_size_this_turn": max_size_this_turn_from_client,
            "timestamp_token": timestamp_token,
            "data": current_state,
        }

        if timestamp_token_from_client + 4.9 < timestamp_token_from_db:
            dict_for_return['message_str'] = "save_current_state: timestamp too old"
        else:
            dbMgr = MongoDBManager()
            dbMgr.update_memorize_state(document)
            dbMgr.closeDB()
            dict_for_return['message_str'] = timestamp_token
            dict_for_return['message_str'] = "save_current_state: save OK"

        dict_for_return['mmrz_code'] = MMRZ_CODE_SaveState_Save_OK
        dict_for_return['timestamp_token'] = timestamp_token

        json_for_return = json.dumps(dict_for_return)
        return json_for_return

@post('/save_current_state_partially/')
@post('/save_current_state_partially')
def save_current_state_partially():
    username = request.get_cookie('username')
    password = request.get_cookie('password')
    password = urllib.unquote(password) if password else None

    need_move = request.forms.get('need_move', None)
    need_move = json.loads(need_move)
    current_cursor_from_client = request.forms.get('current_cursor', None)
    last_cursor_from_client = request.forms.get('last_cursor', None)

    timestamp_token_from_client = request.forms.get('timestamp_token', 0)
    timestamp_token_from_db = get_timestamp_token_from_db(username)
    timestamp_token_from_client = float(timestamp_token_from_client)
    timestamp_token_from_db = float(timestamp_token_from_db)

    dict_for_return = dict(universal_POST_dict)
    if not verify_login(username, password):
        dict_for_return['mmrz_code'] = MMRZ_CODE_Universal_Verification_Fail
        dict_for_return['message_str'] = "save_current_state_partially verify failed"

        json_for_return = json.dumps(dict_for_return)
        return json_for_return
    else:
        dbMgr = MongoDBManager()
        userData = dbMgr.query_memorize_state(username)
        userData['current_cursor'] = current_cursor_from_client
        timestamp_token = time.time()
        state_cached = userData.get('state_cached', False)
        if state_cached:
            last_cursor_from_client = int(last_cursor_from_client)
            # need_move is False means remember or pass
            if not need_move:
                del userData['data'][last_cursor_from_client]
            # need_move is True means firstTimeFail
            else:
                userData['data'][last_cursor_from_client][6] = True
        else:
            pass

        userData['timestamp_token'] = timestamp_token
        if timestamp_token_from_client + 4.9 < timestamp_token_from_db:
            dict_for_return['message_str'] = "save_current_state_partially timestamp too old"
        else:
            dict_for_return['message_str'] = "save_current_state_partially save OK"
            dbMgr.update_memorize_state(userData)

        dbMgr.closeDB()
        dict_for_return['mmrz_code'] = MMRZ_CODE_Universal_OK
        dict_for_return['timestamp_token'] = timestamp_token
        dict_for_return['state_cached'] = state_cached

        json_for_return = json.dumps(dict_for_return)
        return json_for_return

@post('/restore_remote_saved_state/')
@post('/restore_remote_saved_state')
def restore_remote_saved_state():
    username = request.forms.get('username', None)
    password = request.forms.get('password', None)

    dict_for_return = dict(universal_POST_dict)
    if not verify_login(username, password):
        dict_for_return['mmrz_code'] = MMRZ_CODE_Universal_Verification_Fail

        json_for_return = json.dumps(dict_for_return)
        return json_for_return
    else:
        dbMgr = MongoDBManager()
        userData = dbMgr.query_memorize_state(username)
        dbMgr.closeDB()

        dict_for_return['mmrz_code'] = MMRZ_CODE_Restore_State_OK
        dict_for_return['current_cursor'] = int(userData['current_cursor'])
        dict_for_return['max_size_this_turn'] = int(userData['max_size_this_turn'])
        dict_for_return['data'] = userData['data']
        json_for_return = json.dumps(dict_for_return)

        return json_for_return

@post('/clear_state_cached_flag_and_eiginvalue/')
@post('/clear_state_cached_flag_and_eiginvalue')
def clear_state_cached_flag_and_eiginvalue():
    username = request.forms.get('username', None)
    password = request.forms.get('password', None)

    dict_for_return = dict(universal_POST_dict)
    if not verify_login(username, password):
        dict_for_return['mmrz_code'] = MMRZ_CODE_Universal_Verification_Fail

        json_for_return = json.dumps(dict_for_return)
        return json_for_return
    else:
        dbMgr = MongoDBManager()
        dbMgr.clear_state_cached_flag_and_eiginvalue(username)
        dbMgr.closeDB()

        dict_for_return['mmrz_code'] = MMRZ_CODE_Universal_OK

        json_for_return = json.dumps(dict_for_return)
        return json_for_return

@post('/is_word_exist/')
@post('/is_word_exist')
def is_word_exist():
    username = request.forms.get('username', None)
    password = request.forms.get('password', None)

    # wordInfo = request.forms.get('wordInfo', None)

    word      = request.forms.get('word', None)
    pronounce = request.forms.get('pronounce', None)

    dict_for_return = dict(universal_POST_dict)
    if not verify_login(username, password):
        dict_for_return['mmrz_code'] = MMRZ_CODE_Universal_Verification_Fail
        dict_for_return['message_str'] = "/is_word_exist verify failed"

        json_for_return = json.dumps(dict_for_return)
        return json_for_return
    else:
        dbMgr = MmrzSyncDBManager(username)
        exist, wordID = dbMgr.is_word_exist(word, pronounce)

        dict_for_return['exist'] = exist
        dict_for_return['message_str'] = "/is_word_exist verify OK"

        json_for_return = json.dumps(dict_for_return)
        return json_for_return

@post('/update_row/')
@post('/update_row')
def update_row():
    username = request.forms.get('username', None)
    password = request.forms.get('password', None)

    update_whole_row = request.forms.get('update_whole_row', False)

    timestamp_token_from_client = request.forms.get('timestamp_token', 0)
    timestamp_token_from_db = get_timestamp_token_from_db(username)
    timestamp_token_from_client = float(timestamp_token_from_client)
    timestamp_token_from_db = float(timestamp_token_from_db)

    dict_for_return = dict(universal_POST_dict)
    if not verify_login(username, password):
        dict_for_return['verified'] = False
        dict_for_return['message_str'] = "login failed"
        json_for_return = json.dumps(dict_for_return)
        return json_for_return
    else:
        row = request.forms['row']
        row = json.loads(row)
        if timestamp_token_from_client + 4.9 < timestamp_token_from_db:
            dict_for_return['need_reload'] = True
            dict_for_return['message_str'] = "timestamp too old"
        else:
            dbMgr = MmrzSyncDBManager(username)
            dbMgr.createDB()
            dbMgr.updateDB(row, update_whole_row)
            dbMgr.closeDB()
            dict_for_return['need_reload'] = False
            dict_for_return['message_str'] = "Update row success"
        dict_for_return['verified'] = True
        json_for_return = json.dumps(dict_for_return)
        return json_for_return

@post('/online_import/')
@post('/online_import')
def online_import():
    username = request.forms.get('username', None)
    password = request.forms.get('password', None)

    is_smart = request.forms.get('is_smart', None)
    is_smart = json.loads(is_smart)

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

        jsnMgr = JsonManager(username)
        jsnMgr.load_jsn()
        jsn = jsnMgr.jsn
        added = smart_import("./WORDBOOK/{0}/{1}".format(username, jsn["book_name"]), username, quantity, is_smart)
        dict_for_return['added'] = added

        json_for_return = json.dumps(dict_for_return)
        return json_for_return

@post('/change_one_word_status/')
@post('/change_one_word_status')
def change_one_word_status():
    username = request.get_cookie('username')
    password = request.get_cookie('password')
    password = urllib.unquote(password) if password else None

    word      = request.forms.get('word', None)
    pronounce = request.forms.get('pronounce', None)

    dict_for_return = dict(universal_POST_dict)
    if not verify_login(username, password):
        dict_for_return['verified'] = False
        dict_for_return['mmrz_code'] = MMRZ_CODE_Universal_Verification_Fail
        dict_for_return['message_str'] = "/change_one_word_status verify failed"
        json_for_return = json.dumps(dict_for_return)
        return json_for_return
    else:
        dict_for_return['verified'] = True
        dbMgr = MmrzSyncDBManager(username)

        exist, wordID = dbMgr.is_word_exist(word, pronounce)
        if exist:
            dbMgr.deleteDB_by_wordID(wordID)

            dict_for_return['mmrz_code'] = MMRZ_CODE_Word_Remove_OK
            dict_for_return['message_str'] = "/change_one_word_status remove OK"
        else:
            word          = word.decode("utf8")
            pronounce     = pronounce.decode("utf8")
            memTimes      = 0
            remindTime    = cal_remind_time(memTimes, "int")
            remindTimeStr = cal_remind_time(memTimes, "str")
            wordID        = dbMgr.getMaxWordID() + 1

            row = [word, pronounce, memTimes, remindTime, remindTimeStr, wordID]
            dbMgr.insertDB(row)

            dict_for_return['mmrz_code'] = MMRZ_CODE_Word_Save_OK
            dict_for_return['message_str'] = "/change_one_word_status save OK"

        dbMgr.closeDB()
        json_for_return = json.dumps(dict_for_return)
        return json_for_return

@post('/report_word_mistake/')
@post('/report_word_mistake')
def report_word_mistake():
    word      = request.forms.get('word', None)
    pronounce = request.forms.get('pronounce', None)

    f = open("./mistake_report.json", "ab")
    f.close()

    fr = open("./mistake_report.json", "rb")
    content = fr.read().replace('\r\n', '\n')
    fr.close()

    dict_for_return = dict(universal_POST_dict)
    this_word = "{0} {1}".format(word, pronounce)
    word_list = content.split('\n')
    if '' in word_list:
        word_list.remove('')
    if this_word in word_list:
        dict_for_return['mmrz_code'] = MMRZ_CODE_Universal_Error
    else:
        word_list.append(this_word)
        content = "\n".join(word_list)
        fw = open("./mistake_report.json", "wb")
        fw.write(content)
        fw.close()
        dict_for_return['mmrz_code'] = MMRZ_CODE_Universal_OK

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

    now = int(time.time())
    last_change_time = int(users[username]["mailModTime"])
    mail_change_period = (now - last_change_time) / 60 / 60 / 24 # by day

    last_send_time = users[username]["mailSendTime"]
    mail_send_period = (now - last_send_time) / 60 # by minute

    mailAddr_from_client = mailAddr
    mailAddr_from_db = users[username]["mailAddr"]

    # mail address remain the same
    if mailAddr_from_client == mailAddr_from_db or not mailAddr_from_client:
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

@get('/get_next_approximate_words_count/')
@get('/get_next_approximate_words_count')
def get_next_approximate_words_count():
    username = request.params.get('username', None)

    if not is_username_available(username):
        dbMgr = MmrzSyncDBManager(username)
        rows = dbMgr.readUnMemDB()
        dbMgr.closeDB()

        if not rows:
            return ""

        rows = sorted(rows, key=lambda row: row[3]) # from small to big
        words_count = 1
        for i in range(len(rows) - 1):
            remindTime_next = rows[i + 1][3]
            remindTime_this = rows[i][3]

            if remindTime_next - remindTime_this <= 30 * 60:
                words_count += 1
            else:
                break

        words_count_string = "大约 {0} 个单词".format(words_count)

    else:
        words_count_string = "数据获取错误"

    return words_count_string

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
# run(host='0.0.0.0', port=PORT)
run(host='0.0.0.0', port=PORT, server='paste')


