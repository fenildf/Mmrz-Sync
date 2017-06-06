#!/env/bin/python
# encoding: utf-8

import pymongo

# Database: Mmrz-Sync
# 
# Colletions:
# 1. memorize_state

class MongoDBManager:
    def __init__(self):
        self.client = pymongo.MongoClient()
        self.client.admin.authenticate("lane", "lane", mechanism="SCRAM-SHA-1")
        self.db = self.client["Mmrz-Sync"]

    def update_memorize_state(self, document={}):
        result = self.db.memorize_state.find(dict(username=document["username"]))

        # if not find, insert document
        if result.count() == 0:
            self.db.memorize_state.insert_many(document)
        # if find, update codument
        else:
            self.db.memorize_state.update({"username": document["username"]}, {"$set": document})

if __name__ == '__main__':
    MDBManager = MongoDBManager()


