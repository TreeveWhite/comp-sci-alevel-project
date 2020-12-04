from databases.SuperDBHandler import DataBaseHandler

class ChatsDBHandler(DataBaseHandler):

    def __init__(self):
        super().__init__()
        self.clearChats()

    def clearChats(self):
        sql = "DELETE FROM chats"
        self.run_SQL(sql)
    
    def addChat(self, chat, playerid, tableid):
        chat = chat.replace("%21", "!")
        chat = chat.replace("%3F", "?")
        chat = chat.replace("%2C", ",")

        sql = """
        INSERT INTO chats(message, playerid, tableid)
        VALUES(%s, %s, %s)"""
        data = (chat, playerid, tableid, )
        self.run_SQL(sql, data)
    
    def getAllChats(self, tableid):
        sql = "SELECT chats.message, players.name FROM chats INNER JOIN players ON players.playerid = chats.playerid WHERE chats.tableid = %s"
        data = (tableid, )
        self.cursor.execute(sql, data)
        chats = self.cursor.fetchall()
        return chats