from databases.SuperDBHandler import DataBaseHandler
import random

class TablesDBHandler(DataBaseHandler):

    def __init__(self):
        super().__init__()
        self.clearTables()
    
    def incrementTableRefreshCount(self, tableID):
        currentCount = self.getTableRefreshCount(tableID)
        newCount = currentCount + 1
        
        sql = "UPDATE tables SET refreshCount = %s WHERE tableid = %s"
        data = (newCount, tableID, )
        self.run_SQL(sql, data)
    
    def getAllTableIDs(self):
            sql = "SELECT tableid FROM Tables"
            tableIDs = self.run_SQL(sql)

            return tableIDs
    
    def getAllTablesNames(self):
        sql = "SELECT name FROM Tables WHERE hidetable = 0"
        tableNames = self.run_SQL(sql)

        return tableNames

    def getAllPlayersOnTable(self, tableID):
        sql = "SELECT name FROM players WHERE tableid = %s"
        data = (tableID, )
        players = self.run_SQL(sql, data)

        return players
    
    def getTableID(self, tableName):
        sql = "SELECT tableid FROM tables WHERE name = %s"
        data = (tableName, )
        tableID = self.run_SQL(sql, data)

        return tableID[0]
    
    def getTableName(self, tableid):
        sql = "SELECT name FROM tables WHERE tableid = %s"
        data = (tableid, )
        tableName = self.run_SQL(sql, data)

        return tableName[0]
    
    def hideTable(self, tableID):
        sql = "UPDATE tables SET hidetable = 1 WHERE tableid = %s"
        data = (tableID, )
        self.run_SQL(sql, data)
    
    def unhideTable(self, tableID):
        sql = "UPDATE tables SET hidetable = 0 WHERE tableid = %s"
        data = (tableID, )
        self.run_SQL(sql, data)
    
    def getTableRefreshCount(self, tableID):
        sql = "SELECT refreshCount FROM tables WHERE tableid = %s"
        data = (tableID, )
        count = self.run_SQL(sql, data)

        return count[0]
    
    def makeNewTable(self, tableName, smallBlind):
        sql = """
        INSERT INTO tables (tableid, hand, name, refreshCount, hidetable, endHandTime, smallBlind)
        VALUES(%s, %s, %s, %s, %s, %s, %s)
        """
        tableID = str(random.randint(0, 1000))
        while tableID is self.getAllTableIDs():
            tableID = str(random.randint(0, 1000))
        data = (tableID, 1, tableName, 0, 0, 0, smallBlind)
        self.run_SQL(sql, data)

    def clearTables(self):
        sql = "DELETE FROM tables WHERE NOT tableid = 1"
        self.run_SQL(sql)
    
    def getHand(self, tableID):
        sql = "SELECT hand FROM tables WHERE tableid = %s"
        data = (tableID, )
        hand = self.run_SQL(sql, data)[0]

        return hand
    
    def incrementHand(self, tableID):
        currentHand = self.getHand(tableID)
        newHand = int(currentHand) + 1
        sql = "UPDATE tables SET hand = %s WHERE tableid = %s"
        data = (newHand, tableID)
        
        self.run_SQL(sql, data)
    
    def addEndHandTime(self, tableid, endTime):
        sql = "UPDATE tables SET endHandTime = %s WHERE tableid = %s"
        data = (endTime, tableid)
        self.run_SQL(sql, data)
    
    def getEndHandTime(self, tableid):
        sql = "SELECT endHandTime FROM tables WHERE tableid = %s"
        data = (tableid, )
        
        endTime = int(self.run_SQL(sql, data)[0])
        return endTime