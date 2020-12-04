from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from os import curdir, listdir
from time import sleep
from datetime import datetime

from TemplateHandler import TemplateHandler

from databases.PlayersDBHandler import PlayersDBHandler
from databases.TablesDBHandler import TablesDBHandler
from databases.EventsDBHandler import EventsDBHandler
from databases.CredentailsDBHandler import CredentailsDBHandler
from databases.ChatsDBHandler import ChatsDBHandler

from gameState.PokerHandler import PokerHandler
from gameState.PokerMemory import ResponceTypes

PORT = 8080
#NGROK password: ngrokPassword!

class ServerHandler(BaseHTTPRequestHandler):

    playersDBHandler = PlayersDBHandler()
    tablesDBHandler = TablesDBHandler()
    chatsDBHandler = ChatsDBHandler()
    credentailsDBHandler = CredentailsDBHandler()
    eventsDBHandler = EventsDBHandler()

    templateHandler = TemplateHandler()

    def updateHome(self, loginMessage=""):
        currentUser = self.playersDBHandler.getPlayerName(self.cookie)
            
        tables = self.tablesDBHandler.getAllTablesNames()
        lobbyRefreshCount = self.tablesDBHandler.getTableRefreshCount(1)
        self.playersDBHandler.sendPlayerLobby(self.cookie, lobbyRefreshCount)
        
        self.templateHandler.updateHomePage(tables, currentUser, loginMessage)
    
    def updatePoker(self, tableID, tableName, hand):
        pokerHandler = PokerHandler()

        playerName = self.playersDBHandler.getPlayerName(self.cookie)
        allPlayersOnTable = self.tablesDBHandler.getAllPlayersOnTable(tableID)

        if playerName not in allPlayersOnTable:
            tableRefresh = self.tablesDBHandler.getTableRefreshCount(tableID)
            self.playersDBHandler.addPlayerToTable(self.cookie, tableID, tableRefresh)

        players = self.tablesDBHandler.getAllPlayersOnTable(tableID)
        allPlayersMoney = self.playersDBHandler.getAllPlayersMoney(players)
        money = self.playersDBHandler.getMoney(self.cookie)
        

        hand = self.tablesDBHandler.getHand(tableID)
        events = self.eventsDBHandler.getAllEventsForTableHand(tableID, hand)

        lastEvent = events[-1]
        for event in events:
            pokerHandler.completeEvent(event)
                    
        gamestate = pokerHandler.responce(self.cookie)
        handOver = False

        allPlayersInGameState = [*pokerHandler.memory.players, *pokerHandler.memory.foldedPlayers]
        for player in allPlayersInGameState:
            self.playersDBHandler.setMoney(player.name, player.money)

        for playerDetails in allPlayersMoney:
            playerDetails.append("black")
            for player in pokerHandler.memory.foldedPlayers:
                if playerDetails[0] == self.playersDBHandler.getPlayerName(player.name):
                    playerDetails[2] = "red"
                    break

        typeEvent, data = lastEvent.split(" ")
        structuredEvent = ""
        if typeEvent == "ADD":
            name = data.split(",")[0]
            joinedPlayer = self.playersDBHandler.getPlayerName(name)
            structuredEvent = f"{joinedPlayer} has joined the table."
        elif typeEvent == "READY":
            readiedUpPlayer = self.playersDBHandler.getPlayerName(data)
            structuredEvent = f"{readiedUpPlayer} has readied up to play."
        elif typeEvent == "FLOP":
            structuredEvent = "The Flop has been shown and a player is now betting."
        elif typeEvent == "TURN":
            structuredEvent = "The Turn has been shown and a player is now betting."
        elif typeEvent == "RIVER":
            structuredEvent = "The River has been shown and a player is now betting."
        elif typeEvent == "CARDS":
            structuredEvent = "You hand has been delt."
        elif typeEvent == "BET":
            if self.cookie == gamestate.currentPlayer and gamestate.message == ResponceTypes.NEEDBET:
                betNeeded = gamestate.details
                structuredEvent = f"The bet has been raised you need to either bet an extra &pound;{betNeeded} or raise higher."
            else:
                data = data.split(",")
                betPlayer = self.playersDBHandler.getPlayerName(data[0])
                amount = data[1]
                structuredEvent = f"{betPlayer} has just bet &pound;{amount}.\n You must now bet a minumum of &pound;{amount} or fold."

        if gamestate.message == ResponceTypes.NEEDPlAYERS or gamestate.message == ResponceTypes.WAITREADY:
            isReady = self.playersDBHandler.isPlayerReady(self.cookie, tableID, hand)
            self.templateHandler.updatePokerPageReadyUp(players, money, tableName, playerName, isReady, structuredEvent, hand)
        elif gamestate.message == ResponceTypes.NOTTURN:
            currentPlayerName = self.playersDBHandler.getPlayerName(gamestate.currentPlayer)
            self.templateHandler.updatePokerPageNotTurn(allPlayersMoney, money, tableName, playerName, currentPlayerName, gamestate.cards, gamestate.flop, gamestate.turn, gamestate.river, structuredEvent, gamestate.pot, hand)
        elif gamestate.message == ResponceTypes.DEALCARDS:
            self.tablesDBHandler.hideTable(tableID)
            for player in players:
                playerCookie = self.playersDBHandler.getPlayerCookie(player)
                cards = pokerHandler.dealCards(events, 2)
                self.eventsDBHandler.addEventCARDS(playerCookie, tableID, hand, cards)
            self.tablesDBHandler.incrementTableRefreshCount(tableID)
        elif gamestate.message == ResponceTypes.SHOWFLOP:
            flop = pokerHandler.dealCards(events, 3)
            added = self.eventsDBHandler.addEventFLOP(tableID, hand, flop)
            if added:
                self.tablesDBHandler.incrementTableRefreshCount(tableID)
        elif gamestate.message == ResponceTypes.SHOWTURN:
            turn = pokerHandler.dealCards(events, 1)[0]
            added = self.eventsDBHandler.addEventTURN(tableID, hand, turn)
            if added:
                self.tablesDBHandler.incrementTableRefreshCount(tableID)
        elif gamestate.message == ResponceTypes.SHOWRIVER:
            river = pokerHandler.dealCards(events, 1)[0]
            added = self.eventsDBHandler.addEventRIVER(tableID, hand, river)
            if added:
                self.tablesDBHandler.incrementTableRefreshCount(tableID)
        elif gamestate.message == ResponceTypes.NEXTBET:
            amountNeedBet = pokerHandler.memory.betAmount
            maxAmountBet = self.playersDBHandler.getMoney(self.cookie)
            self.templateHandler.updatePokerPageTurn(gamestate.cards, gamestate.flop, gamestate.turn, gamestate.river, playerName, allPlayersMoney, tableName, money, amountNeedBet, maxAmountBet, structuredEvent, gamestate.pot, hand)
        elif gamestate.message == ResponceTypes.NEEDBET:
            amountNeedBet = gamestate.details
            maxAmountBet = self.playersDBHandler.getMoney(self.cookie)
            self.templateHandler.updatePokerPageTurn(gamestate.cards, gamestate.flop, gamestate.turn, gamestate.river, playerName, allPlayersMoney, tableName, money, amountNeedBet, maxAmountBet, structuredEvent, gamestate.pot, hand)
        elif gamestate.message == ResponceTypes.WINNER:
            handOver = True
            handStrengths = gamestate.river
            if handStrengths != None:
                handStrengths = dict(map(lambda x: (self.playersDBHandler.getPlayerName(x[0]), x[1]), handStrengths.items()))
            winners = []
            for player in gamestate.currentPlayer:
                winners.append(self.playersDBHandler.getPlayerName(player))
                messages = self.chatsDBHandler.getAllChats(tableID)
                self.templateHandler.updatePokerPageWinner(handStrengths, winners, messages)

        return handOver         

    def do_GET(self):
        
        self.cookie = self.headers["Cookie"]
        print(self.cookie)

        if self.path == "/":

            if (self.cookie == 'None') or (self.cookie == None) or (int(self.cookie) not in self.playersDBHandler.getAllCookies()):
                guestCookie = self.playersDBHandler.addGuest()
                self.credentailsDBHandler.addGuest(guestCookie)
                self.cookie = guestCookie

            self.updateHome()

            self.path = "HTML/returnPage.html"
            self.contentType = "text/html"
            needToUpdate = True

        elif self.path == "/createAccount?":
            currentUser = self.playersDBHandler.getPlayerName(self.cookie)
            tables = self.tablesDBHandler.getAllTablesNames()
            self.templateHandler.updateCreationPage(tables, currentUser)

            self.path = "HTML/returnPage.html"
            self.contentType = "text/html"
            needToUpdate = True
        
        elif self.path.split("(")[0] == "/playPoker":
            tableName = self.path[11: len(self.path)-2].replace("%20", "_")
            tableID = self.tablesDBHandler.getTableID(tableName)

            hand = self.tablesDBHandler.getHand(tableID)
            playerMoney = self.playersDBHandler.getMoney(self.cookie)
            added = self.eventsDBHandler.addEventADD(self.cookie, tableID, hand, playerMoney)
            if added:
                self.tablesDBHandler.incrementTableRefreshCount(tableID)

            handEnded = self.updatePoker(tableID, tableName, hand)
            if handEnded and self.tablesDBHandler.getEndHandTime(tableID) == 0:
                self.tablesDBHandler.unhideTable(tableID)
                time = int(datetime.now().hour)*60*60 + int(datetime.now().minute)*60 + int(datetime.now().second)
                self.tablesDBHandler.addEndHandTime(tableID, time)
            elif handEnded:
                currentTime = int(datetime.now().hour)*60*60 + int(datetime.now().minute)*60 + int(datetime.now().second)
                endHandTime = self.tablesDBHandler.getEndHandTime(tableID)
                if currentTime - endHandTime >= 10:
                    self.tablesDBHandler.incrementHand(tableID)
                    self.tablesDBHandler.addEndHandTime(tableID, 0)
                    hand = self.tablesDBHandler.getHand(tableID)
                    self.eventsDBHandler.addEventADD(self.cookie, tableID, hand, playerMoney)
                    self.updatePoker(tableID, tableName, hand)

            needToUpdate = True
            self.path = "HTML/returnPage.html"
            self.contentType = "text/html"

        elif self.path.split("?")[0] == "/newTable":
            newTable = self.path.split("?")[1].split("&")[0].split("=")[1].replace("+", "_")
            smallBlind = self.path.split("?")[1].split("&")[1].split("=")[1].replace("+", "_")
            if newTable not in self.tablesDBHandler.getAllTablesNames():
                self.tablesDBHandler.makeNewTable(newTable, smallBlind)
                self.tablesDBHandler.incrementTableRefreshCount(1)

            needToUpdate = False
        
        elif self.path.split("/")[1] == "images":
            self.contentType = "image/jpg"
            self.path = curdir + self.path
            needToUpdate = True
        
        elif self.path == "/favicon.ico":
            self.path = curdir + "/images/icon/cornoricon.ico"
            self.contentType = "image/x-icon"
            needToUpdate = True
        
        elif self.path == "/refresh":
            try:
                needToUpdate = False
                tableID = self.playersDBHandler.getTablePlayerOn(self.cookie)
                
                while not needToUpdate:
                    sleep(1)     
                    tableRefresh = self.tablesDBHandler.getTableRefreshCount(tableID)              
                    if self.playersDBHandler.getTablePlayerOn(self.cookie) != tableID:
                        break
                    elif self.playersDBHandler.isUpdate(tableID, self.cookie, tableRefresh):
                        needToUpdate = True

                newCount = self.tablesDBHandler.getTableRefreshCount(tableID)
                self.playersDBHandler.changePlayerRefreshCount(self.cookie, newCount)

                self.contentType = "text/event-stream"
            except IndexError:
                print("127.0.0.1:", self.path, " --- ERROR --- old refresh attempting to excecute")
                needToUpdate = False

        if needToUpdate == True:
            
            if self.contentType == "text/html":
                with open(self.path) as f:
                    self.send_response(200)
                    self.send_header("Content-type", self.contentType)
                    self.send_header("Set-Cookie", self.cookie)
                    self.end_headers()
                    self.wfile.write(f.read().encode())

            elif self.contentType == "image/jpg" or self.contentType == "image/x-icon":
                with open(self.path, "rb") as file:
                    self.path = file.read()
                self.send_response(200)
                self.send_header("Content-type", self.contentType)
                self.send_header("Set-Cookie", self.cookie)
                self.send_header("Cache-Control", "public, max-age=31536000")
                self.end_headers()
                self.wfile.write(self.path)
            
            elif self.contentType == "text/event-stream":
                self.send_response(200)
                self.send_header("Content-type", self.contentType)
                self.end_headers()
                self.wfile.write("data: 1\n\n".encode())
        elif not needToUpdate:
            self.send_response(304)
            self.send_header("Content-Type", "text/html")
            self.send_header("Set-Cookie", self.cookie)
            self.end_headers()

    def do_POST(self):
        self.cookie = self.headers["Cookie"]
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        data = ""
        for item in post_data:
            data += str(chr(item))
    
        if self.path == "/login":
            username = data.split("&")[0].split("=")[1]
            password = data.split("&")[1].split("=")[1]

            loginMessage = "Login Failed"
            
            cookie = self.credentailsDBHandler.canLogin(username, password)
            if cookie != None:
                loginMessage = "Login Successful"
                self.cookie = cookie
            
            self.updateHome(loginMessage)
            self.path = "HTML/returnPage.html"

            needToUpdate = True
        
        elif self.path == "/newAccount":
            name = data.split("&")[0].split("=")[1]
            username = data.split("&")[1].split("=")[1]
            password = data.split("&")[2].split("=")[1]

            if not (name == username == password) or name != "" or username != "" or password != "":
                cookie = self.playersDBHandler.addAccount(name)
                self.credentailsDBHandler.addAccount(cookie, username, password)
                creationMessage = "Account Was Created<br>Return to home page to now login."
            
            else:
                creationMessage = "Invalid Credentials"

            currentUser = self.playersDBHandler.getPlayerName(self.cookie)
            tables = self.tablesDBHandler.getAllTablesNames()
            self.templateHandler.updateCreationPage(tables, currentUser, creationMessage)

            self.path = "HTML/returnPage.html"
            self.contentType = "text/html"
            needToUpdate = True

        elif self.path == "/readyUp":
            tableID = self.playersDBHandler.getTablePlayerOn(self.cookie)
            hand = self.tablesDBHandler.getHand(tableID)
            added = self.eventsDBHandler.addEventREADY(self.cookie, tableID, hand)
            if added:
                self.tablesDBHandler.incrementTableRefreshCount(tableID)

            needToUpdate = False
        
        elif self.path == "/bet":
            bet = data.split("=")[1]
            tableID = self.playersDBHandler.getTablePlayerOn(self.cookie)
            hand = self.tablesDBHandler.getHand(tableID)
            added = self.eventsDBHandler.addEventBET(self.cookie, tableID, hand, bet)
            if added:
                self.tablesDBHandler.incrementTableRefreshCount(tableID)
        
            needToUpdate = False
        
        elif self.path == "/fold":
            tableID = self.playersDBHandler.getTablePlayerOn(self.cookie)
            hand = self.tablesDBHandler.getHand(tableID)
            added = self.eventsDBHandler.addEventFOLD(self.cookie, tableID, hand)
            if added:
                self.tablesDBHandler.incrementTableRefreshCount(tableID)
        
            needToUpdate = False
        
        elif self.path == "/sendMessage":
            message = data.split("=")[1].replace("+", " ")
            tableID = self.playersDBHandler.getTablePlayerOn(self.cookie)
            self.chatsDBHandler.addChat(message, self.cookie, tableID)
            self.tablesDBHandler.incrementTableRefreshCount(tableID)

            needToUpdate = False
        
        elif self.path == "/exitGame":
            tableID = self.playersDBHandler.getTablePlayerOn(self.cookie)
            hand = self.tablesDBHandler.getHand(tableID)
            allEvents = self.eventsDBHandler.getAllEventsForTableHand(tableID, hand)
            self.playersDBHandler.clearPlayersEvents(self.cookie, tableID, allEvents)
            self.tablesDBHandler.incrementTableRefreshCount(tableID)

            self.send_response(301)
            self.send_header('Location','/')
            self.end_headers()

            needToUpdate = False

        if needToUpdate:
            with open(self.path) as f:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.send_header("Set-Cookie", self.cookie)
                self.end_headers()
                self.wfile.write(f.read().encode())

        elif not needToUpdate:
            self.send_response(304)
            self.send_header("Content-Type", "text/html")
            self.send_header("Set-Cookie", self.cookie)
            self.end_headers()

class Server:
    def __init__(self, port):
        self.server = ThreadingHTTPServer(("", port), ServerHandler)
        self.server.serve_forever()

if __name__ == "__main__":

    print("serving at port", PORT)
    try:
        server = Server(PORT)
    except:
        print("closing at port", PORT)