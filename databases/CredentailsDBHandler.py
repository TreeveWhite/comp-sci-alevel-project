from databases.SuperDBHandler import DataBaseHandler

class CredentailsDBHandler(DataBaseHandler):

    def __init__(self):
        super().__init__()
    
    def canLogin(self, givenUsername, givenPassword):
        sql = "SELECT players.playerid FROM players INNER JOIN credentials ON players.playerid = credentials.playerid WHERE username = %s AND password = %s"
        data = (givenUsername, givenPassword)
        playerid = self.run_SQL(sql, data)

        if playerid == []:
            playerid = None
        else:
            playerid = playerid[0]

        return playerid
    
    def addAccount(self, playerid, username, password):
        sql = """
        INSERT into credentials (playerid, username, password)
        VALUES(%s, %s, %s)
        """
        data = (playerid, username, password)

        self.run_SQL(sql, data)
    
    def addGuest(self, playerid):
        sql = """
        INSERT INTO credentials (playerid, username, password)
        VALUES(%s, %s, %s)
        """
        data = (playerid, "", "")
        self.run_SQL(sql, data)