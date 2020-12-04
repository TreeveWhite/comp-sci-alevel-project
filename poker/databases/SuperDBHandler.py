import psycopg2


class DataBaseHandler():
    
    """
    Class to cobtrol all 4 tables used in the system.
    > Players
    > Credentials
    > Events
    > Tables

    All tables are held on a postgreSQL server and accessed using the psycopy2 Lib.
    """

    def __init__(self):
        self.db = "dbname='postgres' user=postgres password='password' host='localhost' port= '5432'"   
        self.con = psycopg2.connect(self.db)
        self.con.autocommit = True
        self.cursor = self.con.cursor()
    
    def generateTables(self):
        sql = "CREATE TABLE IF NOT EXISTS players (playerid INTEGER, name TEXT, tableid INTEGER, money INTEGER, refreshCount INTEGER, PRIMARY KEY (playerid))"
        self.run_SQL(sql)
        sql = "CREATE TABLE IF NOT EXISTS credentials (playerid INTEGER, username TEXT, password TEXT, PRIMARY KEY (playerid))"
        self.run_SQL(sql)
        sql = "CREATE TABLE IF NOT EXISTS tables (tableid INTEGER, name TEXT, hand INTEGER, refreshCount INTEGER, hidetable INTEGER, endHandTime INTEGER, smallBlind INTEGER, PRIMARY KEY (tableid))"
        self.run_SQL(sql)
        sql = "CREATE TABLE IF NOT EXISTS events (eventid SERIAL, tableid INTEGER, hand INTEGER, event TEXT, PRIMARY KEY (eventid))"
        self.run_SQL(sql)
        sql = "CREATE TABLE IF NOT EXISTS chats (chatid SERIAL, message TEXT, playerid INTEGER, tableid INTEGER, PRIMARY KEY(chatid))"
        self.run_SQL(sql)
        
        sqlForPlayers = """
        INSERT INTO players(playerid, name, tableid, money, refreshCount)
        VALUES(%s, %s, %s, %s, %s)
        """
        sqlForCredentials = """
        INSERT INTO credentials(playerid, username, password)
        VALUES(%s, %s, %s)
        """
        data = (1, "Treeve", 1, 1000, 0)
        self.run_SQL(sqlForPlayers, data)
        data = (1, "admin", "password")
        self.run_SQL(sqlForCredentials, data)

        data = (2, "Reece", 1, 1000, 0)
        self.run_SQL(sqlForPlayers, data)
        data = (2, "reece", "ilovenita")
        self.run_SQL(sqlForCredentials, data)

        data = (3, "Louis", 1, 1000, 0)
        self.run_SQL(sqlForPlayers, data)
        data = (3, "louis", "wusheen")
        self.run_SQL(sqlForCredentials, data)
        
        sql = """
        INSERT INTO tables(tableid, name, hand, refreshCount, hidetable)
        VALUES(%s, %s, %s, %s, %s)
        """
        data = (1, "Lobby", 0, 0, 1)
        self.run_SQL(sql, data)

    
    def deleteTables(self):
        try:
            sql = "DROP TABLE players"
            self.run_SQL(sql)
        except:
            print("")
        try:
            sql = "DROP TABLE tables"
            self.run_SQL(sql)
        except:
            print("")
        try:
            sql = "DROP TABLE events"
            self.run_SQL(sql)
        except:
            print("")
        try:
            sql = "DROP TABLE credentials"
            self.run_SQL(sql)
        except:
            print("")
        try:
            sql = "DROP TABLE chats"
            self.run_SQL(sql)
        except:
            print("")

    def run_SQL(self, sql, data=(), doFormat=True):
        #Runs any SQL statement and returns the responce in an Array.
        self.cursor.execute(sql, data)
        try:
            returnData = self.cursor.fetchall()
            formatedData = self.formatReturnData(returnData, doFormat)
            return formatedData
        except:
            return None
        
    def formatReturnData(self, data, doFormat):
        formatedData = []
        if doFormat:
            for item in data:
                formatedData.append(item[0])
        else:
            formatedData = data

        return formatedData
