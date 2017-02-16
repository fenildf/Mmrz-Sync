#!/env/bin/python
# encoding: utf-8

import sqlite3
import base64

class MmrzSyncDBManager:
    """
        table UNMMRZ:
        [0]word           -- char[255]
        [1]pronounce      -- char[255]
        [2]memTimes       -- int
        [3]remindTime     -- int
        [4]remindTimeStr  -- char[255]
        [5]wordID         -- int

        table FAVOURITE:
        [0]wordID         -- int
        [1]favourite      -- boolean (true: 1, false: 0)
        [2]memTimes       -- int
    """

    def __init__(self, dbName):
        self.db = sqlite3.connect("./USERDB/{0}.db".format(dbName))
        self.c = self.db.cursor()

    def create_USERS_DB(self):
        try:
            self.c.execute("create table USERS(username char[255], password char[255])")
            self.db.commit()
        except:
            pass

    def insert_USERS_DB(self, userInfo):
        self.c.execute("insert into USERS values(?, ?)", userInfo)

    def update_USERS_DB(self, userInfo):
        self.c.execute("update USERS set password = '{0}' where username = '{1}'".format(userInfo[1], userInfo[0]))

    def read_USERS_DB(self):
        return self.c.execute("select * from USERS").fetchall()



    def createDB(self):
        try:
            self.c.execute("create table UNMMRZ(word char[255], pronounce char[255], memTimes int, remindTime int, remindTimeStr char[255], wordID int)")
            self.c.execute("create table FAVOURITE(wordID int NOT NULL, favourite boolean, memTimes int)")
        except:
            pass

    def insertDB(self, row):
        self.c.execute("insert into UNMMRZ values(?, ?, ?, ?, ?, ?)", row)

    def updateDB(self, row):
        self.c.execute("update UNMMRZ set memTimes = {0}, remindTime = {1}, remindTimeStr = '{2}' where wordID = '{3}'".format(row[2], row[3], row[4], row[5]))

    def readDB(self):
        return self.c.execute("select * from UNMMRZ where memTimes < 8").fetchall()

    def readAllDB(self):
        return self.c.execute("select * from UNMMRZ").fetchall()

    def pruneDB(self):
        self.c.execute("delete from UNMMRZ")
        self.c.execute("VACUUM")

    def getMaxWordID(self):
        # format of maxWordID is like: maxWordID = [[33]], thus use maxWordID[0][0] to access it
        return self.c.execute("select max(wordID) from UNMMRZ").fetchall()[0][0] or 0

    def read_WORD_FAVOURITE_DB(self):
        return self.c.execute("select fav.wordID, fav.favourite from UNMMRZ mmrz LEFT JOIN FAVOURITE fav ON mmrz.wordID = fav.wordID where mmrz.memTimes < 8").fetchall()

    def insert_FAVOURITE_DB(self, row):
        self.c.execute("insert into FAVOURITE values(?, ?, ?)", row)

    def delete_FAVOURITE_DB(self, wordID):
        self.c.execute("DELETE FROM favourite WHERE wordID = {0}".format(wordID))

    def closeDB(self):
        self.db.commit()
        self.db.close()

# db = MmrzSyncDBManager("USERS")
# # userdict = dict(db.read_USERS_DB())
# # print userdict
# db.create_USERS_DB()
# db.insert_USERS_DB(["zhanglin", base64.b64encode("zhanglin")])
# db.insert_USERS_DB(["wuhong", "wuhong"])
# db.closeDB()


