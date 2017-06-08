#!/env/bin/python
# encoding: utf-8

import pymongo
from ConfigManager import ConfigManager

# Database: Mmrz-Sync
# 
# Colletions:
# 1. memorize_state
#
# memorize_state:
# 1. username           -- string, 用户名
# 2. state_cached       -- bool, 是否有状态处于缓存中
# 3. rows_length        -- int, 特征值: rows长度
# 4. current_cursor     -- int, 特征值: 当前游标位置
# 5. data               -- list, rows_from_DB

class MongoDBManager:
    def __init__(self):
        configMgr = ConfigManager()
        config = configMgr.read_config_file()
        mongo_username = config["mongo_username"]
        mongo_password = config["mongo_password"]

        self.client = pymongo.MongoClient()
        self.client.admin.authenticate(mongo_username, mongo_password, mechanism="SCRAM-SHA-1")
        self.db = self.client["Mmrz-Sync"]

    def query_memorize_state(self, username):
        result = self.db.memorize_state.find(dict(username=username))

        if result.count() == 0:
            return dict(result)

        else:
            return result[0]

    def update_memorize_state(self, document={}):
        result = self.db.memorize_state.find(dict(username=document["username"]))

        # if not find, insert document
        if result.count() == 0:
            self.db.memorize_state.insert_one(document)
        # if find, update codument
        else:
            self.db.memorize_state.update({"username": document["username"]}, {"$set": document})

    def clear_state_cached_flag(self, username):
        result = self.db.memorize_state.find(dict(username=username))

        if result.count() == 0:
            return False
        else:
            document = result[0]
            document["state_cached"] = False
            self.db.memorize_state.update({"username": document["username"]}, {"$set": document})

            return True

    def closeDB(self):
        self.client.close()

if __name__ == '__main__':
    MDBManager = MongoDBManager()


