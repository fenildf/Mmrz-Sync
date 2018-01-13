#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import pickle
import time

''' Only work well in folder Mmrz-Sync/server '''

def each_file(target):
    for root, dirs, files in os.walk(target):
        for f in files:
            yield os.path.join(root, f)

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

    def load_json(self):
        fr = open(self.path, "rb")
        content = fr.read()
        fr.close()
        self.jsn = json.loads(content)

    def set_json(self, content):
        self.jsn = content

    def dump_json(self):
        fw = open(self.path, "wb")
        fw.write(json.dumps(self.jsn, indent=4))
        fw.close()

    def set_book_name(self, book_name):
        self.load_json()
        self.jsn["book_name"] = book_name
        self.dump_json()

    def set_total_lines(self, total_lines):
        self.load_json()
        self.jsn["total_lines"] = total_lines
        self.dump_json()

    def set_last_import_time(self):
        self.load_json()
        self.jsn["last_import_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.dump_json()

    def set_last_import_time_int(self):
        self.load_json()
        self.jsn["last_import_time_int"] = int(time.time())
        self.dump_json()

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

for f in each_file("./"):
    if ".pkl" in f:
        dirname  = os.path.dirname(f)
        username = dirname.split("/")[-1]
        basename = os.path.basename(f)

        pklMgr  = PickleManager(username)
        jsonMgr = JsonManager(username)
        pklMgr.load_pkl()
        jsonMgr.set_json(pklMgr.pkl)
        jsonMgr.dump_json()





