from databases.SuperDBHandler import DataBaseHandler
import random

class PlayersDBHandler(DataBaseHandler):

    def __init__(self):
        super().__init__()
        self.clearGuests()

    def changePlayerRefreshCount(self, playerid, newCount):
        sql = "UPDATE players SET refreshCount = %s WHERE playerid = %s"
        data = (newCount, playerid, )
        self.run_SQL(sql, data)
    
    def getPlayerName(self, playerid):
        sql = "SELECT name FROM players WHERE playerid = %s"
        data = (playerid, )
        player = self.run_SQL(sql, data)

        return player[0]
    
    def getPlayerCookie(self, name):
        sql = "SELECT playerid FROM players WHERE name = %s"
        data = (name, )
        playerid = self.run_SQL(sql, data)

        return playerid[0]
    
    def getAllPlayersMoney(self, players):
        playersMoney = []
        for player in players:
            sql = "SELECT money FROM players WHERE name = %s"
            data = (player, )
            money = self.run_SQL(sql, data)
            playersMoney.append([player, money])

        return playersMoney
    
    def getTablePlayerOn(self, playerid):
        sql = "SELECT tableid FROM players WHERE playerid = %s"
        data = (playerid, )
        tableID = self.run_SQL(sql, data)

        return tableID[0]
    
    def getAllCookies(self):
        sql = "SELECT playerid FROM players"
        playerids = self.run_SQL(sql)

        return playerids

    def sendPlayerLobby(self, playerid, refreshCount):
        sql = "UPDATE players SET TableID = 1 WHERE playerid = %s"
        data = (playerid, )
        self.run_SQL(sql, data)
        sql = "UPDATE players SET refreshCount = %s WHERE playerid = %s"
        data = (playerid, refreshCount, )
        self.run_SQL(sql, data)

    def addGuest(self):
        cookie = str(random.randint(0, 1000))
        while cookie is self.getAllCookies():
            cookie = str(random.randint(0, 1000))
        name = "Guest" + cookie
        sql = """
        INSERT INTO players (playerid, name, tableid, Money, refreshCount)
        VALUES(%s, %s, %s, %s, %s)
        """
        data = (cookie, name, 1, 100, 0)
        self.run_SQL(sql, data)

        return cookie
    
    def addAccount(self, name):
        cookie = str(random.randint(0, 1000))
        while cookie is self.getAllCookies():
            cookie = str(random.randint(0, 1000))
        sql = """
        INSERT INTO players (playerid, name, tableid, Money, refreshCount)
        VALUES(%s, %s, %s, %s, %s)
        """
        data = (cookie, name, 1, 100, 0)
        self.run_SQL(sql, data)
        return cookie
    
    def getPlayerRefreshCount(self, playerid):
        sql = "SELECT refreshCount FROM players WHERE playerid = %s"
        data = (playerid, )
        count = self.run_SQL(sql, data)

        return count[0]
    
    def addPlayerToTable(self, playerid, tableID, refreshCount):
        sql = "UPDATE players SET tableid = %s WHERE playerid = %s"
        data = (tableID, playerid)
        self.run_SQL(sql, data)
        sql = "UPDATE players SET refreshCount = %s WHERE playerid = %s"
        data = (refreshCount, playerid)
        self.run_SQL(sql, data)
    
    def getMoney(self, playerid):
        sql = "SELECT money FROM players WHERE playerid = %s"
        data = (playerid, )
        money = self.run_SQL(sql, data)

        return money[0]
    
    def clearGuests(self):
        sql = """
        DELETE FROM players 
        WHERE playerid IN (SELECT playerid FROM credentials WHERE username = '')
        """
        self.run_SQL(sql)

    def isPlayerReady(self, playerid, tableid, hand):
        sql = "SELECT event, hand FROM events WHERE tableid = %s"
        data = (tableid, )
        events = self.run_SQL(sql, data, False)

        for event in events:
            tp, player = event[0].split(" ")
            if tp == "READY" and player == playerid and hand == event[1]:
                return True

        return False
    
    def clearPlayersEvents(self, playerid, tableID, events):
        eventsToClear = []
        for event in events:
            if str(event.split(" ")[1]) == str(playerid) or str(event.split(" ")[1].split(",")[0]) == str(playerid):
                eventsToClear.append(event)

        for event in eventsToClear:
            sql = "DELETE FROM events WHERE tableid = %s and event = %s"
            data = (tableID, event, )
            self.run_SQL(sql, data)
    
    def setMoney(self, playerid, money):
        sql = "UPDATE players SET money = %s WHERE playerid = %s"
        data = (money, playerid, )
        self.run_SQL(sql, data)
    
    def isUpdate(self, tableID, playerid, tableCount):
        if tableCount != self.getPlayerRefreshCount(playerid):
            return True
        else:
            return False

