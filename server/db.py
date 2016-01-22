#!/env/bin/python
# encoding: utf-8

import sqlite3

class MmrzDBManager:
    """
        table UNMMRZ:
        [0]word           -- char[255]
        [1]pronounce      -- char[255]
        [2]memTimes       -- int
        [3]remindTime     -- int
        [4]remindTimeStr  -- char[255]
        [5]wordID         -- int
    """

    def __init__(self):
        self.db = sqlite3.connect("./wordbook.db")
        self.c = self.db.cursor()

    def createDB(self):
        try:
            self.c.execute("create table UNMMRZ(word char[255], pronounce char[255], memTimes int, remindTime int, remindTimeStr char[255], wordID int)")
            self.db.commit()
        except:
            pass

    def insertDB(self, row):
        self.c.execute("insert into UNMMRZ values(?, ?, ?, ?, ?, ?)", row)

    def updateDB(self, row):
        self.c.execute("update UNMMRZ set memTimes = #{row[2]}, remindTime = #{row[3]}, remindTimeStr = '#{row[4]}' where wordID = '#{row[5]}'")

    def readDB(self):
        return self.c.execute("select * from UNMMRZ where memTimes < 9").fetchall()

    def readAllDB(self):
        return self.c.execute("select * from UNMMRZ").fetchall()

    def getMaxWordID(self):
        # format of maxWordID is like: maxWordID = [[33]], thus use maxWordID[0][0] to access it
        return self.c.execute("select max(wordID) from UNMMRZ").fetchall()[0][0] or 0

    def closeDB(self):
        self.db.commit()
        self.db.close()


