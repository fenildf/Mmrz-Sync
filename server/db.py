#!/env/bin/python
# encoding: utf-8

import sqlite3
import base64

class TikTimeDBManager:
    """
        table TIKTIME:
        [0]username      -- char[255] NOT NULL
        [1]stampTime     -- largeint NOT NULL
        [2]uniqMinute    -- largeint
        [3]uniqHour      -- largeint
        [4]uniqDate      -- largeint
        [5]theYear       -- int
        [6]theMonth      -- int
        [7]theDate       -- int
        [8]theHour       -- int
        [9]theWeek       -- int
        [10]theDay       -- int
    """

    def __init__(self):
        self.db = sqlite3.connect("tikTime.db")
        self.c = self.db.cursor()

    def insertDB(self, tikInfo):
        self.c.execute("insert into TIKTIME values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", tikInfo)

    def getUniqMinuteList(self, username):
        uniqMinutes = self.c.execute("select uniqMinute from TIKTIME where username == '{0}'".format(username)).fetchall()
        for i in range(len(uniqMinutes)):
            uniqMinutes[i] = uniqMinutes[i][0]

        return uniqMinutes

    def closeDB(self):
        self.db.commit()
        self.db.close()

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
            self.c.execute("create table FAVOURITE(wordID int NOT NULL, favourite boolean, memTimes int)")
            self.c.execute("create table UNMMRZ(word char[255], pronounce char[255], memTimes int, remindTime int, remindTimeStr char[255], wordID int)")
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

    def read_FAVOURITE_DB(self):
        return self.c.execute("select fav.wordID, mmrz.word, mmrz.pronounce, fav.favourite from FAVOURITE fav LEFT JOIN UNMMRZ mmrz ON mmrz.wordID = fav.wordID").fetchall()

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


