import jinja2

class TemplateHandler:

    def updatePokerPageReadyUp(self, players, money, currentTable, name, isReady, lastEvent, hand):
        buttonIs = ""
        if isReady:
            buttonIs = "DISABLED"
        with open("HTML/pokerTemplateReadyUp.html", "r") as f:
            template = jinja2.Template(f.read())
            newPage = template.render(players=players, money=money, currentTable=currentTable, name=name, buttonIs=buttonIs, lastEvent=lastEvent, hand=hand)
        
        file = open("HTML/returnPage.html", "w").close()

        with open("HTML/returnPage.html", "w") as f:
            f.write(newPage)
    
    def updatePokerPageNotTurn(self, players, money, currentTable, name, currentPlayer, cards, flop, turn, river, lastEvent, pot, hand):
        tableCards = []
        playerCards = []

        for card in cards:
            playerCards.append(f"/images/cards/{card}")
        
        if flop == None:
            tableCards.append("/images/cards/BACK.jpg")
            tableCards.append("/images/cards/BACK.jpg")
            tableCards.append("/images/cards/BACK.jpg") 
        else:
            for card in flop:
                tableCards.append(f"/images/cards/{card}")
        
        if turn == None:
            tableCards.append("/images/cards/BACK.jpg")
        else:
            tableCards.append(f"/images/cards/{turn}")
        
        if river == None:
            tableCards.append("/images/cards/BACK.jpg")
        else:
            tableCards.append(f"/images/cards/{river}")
        
        with open("HTML/pokerTemplateNotTurn.html", "r") as f:
            template = jinja2.Template(f.read())
            newPage = template.render(players=players, money=money, currentTable=currentTable, name=name, currentPlayer=currentPlayer, tableCards=tableCards, playerCards=playerCards, lastEvent=lastEvent, pot=pot, hand=hand)
        
        file = open("HTML/returnPage.html", "w").close()

        with open("HTML/returnPage.html", "w") as f:
            f.write(newPage)
    
    def updatePokerPageWinner(self, playerStrengths, winners, messages):
        handStrengthsMeanings = {1: "High Card", 2: "Pair", 3: "Two Pair", 4: "Three of a Kind", 5: "Straight", 6: "Flush", 7: "Full House", 8: "Four of a Kind", 9: "Straight Flush", 10: "Royal Flush"}
        if playerStrengths == None:
            visualStrengths = [["All other players folded, so", "hand strength of 0"]]
        else:
            visualStrengths = []
            for player in playerStrengths.keys():
                visualStrengths.append([player, handStrengthsMeanings[playerStrengths[player]]])

        with open("HTML/pokerTemplateWinner.html", "r") as f:
            template = jinja2.Template(f.read())
            newPage = template.render(playerStrengths=visualStrengths, winners=winners, messages=messages)
        
        file = open("HTML/returnPage.html", "w").close()

        with open("HTML/returnPage.html", "w") as f:
            f.write(newPage)
    
    def updatePokerPageTurn(self, cards, flop, turn, river, playerName, players, currentTable, money, amountNeedBet, maxAmountBet, lastEvent, pot, hand):
        tableCards = []
        playerCards = []

        for card in cards:
            playerCards.append(f"/images/cards/{card}")
        
        if flop == None:
            tableCards.append("/images/cards/BACK.jpg")
            tableCards.append("/images/cards/BACK.jpg")
            tableCards.append("/images/cards/BACK.jpg") 
        else:
            for card in flop:
                tableCards.append(f"/images/cards/{card}")
        
        if turn == None:
            tableCards.append("/images/cards/BACK.jpg")
        else:
            tableCards.append(f"/images/cards/{turn}")
        
        if river == None:
            tableCards.append("/images/cards/BACK.jpg")
        else:
            tableCards.append(f"/images/cards/{river}")
        
        with open("HTML/pokerTemplateTurn.html", "r") as f:
            template = jinja2.Template(f.read())
            newPage = template.render(tableCards=tableCards, playerCards=playerCards, name=playerName, players=players, currentTable=currentTable, money=money, amountNeedBet=amountNeedBet, maxAmountBet=maxAmountBet, lastEvent=lastEvent, pot=pot, hand=hand)
        
        file = open("HTML/returnPage.html", "w").close()

        with open("HTML/returnPage.html", "w") as f:
            f.write(newPage)

    def updateHomePage(self, tables, currentUser, loginMessage=""):
        with open("HTML/homeTemplate.html", "r") as f:
            template = jinja2.Template(f.read())
            newPage = template.render(tables=tables, currentUser=currentUser, loginMessage=loginMessage)
        
        file = open("HTML/returnPage.html", "w").close()

        with open("HTML/returnPage.html", "w") as f:
            f.write(newPage)
    
    def updateCreationPage(self, tables, currentUser, creationMessage=""):
        with open("HTML/homeCreationTemplate.html", "r") as f:
            template = jinja2.Template(f.read())
            newPage = template.render(tables=tables, currentUser=currentUser, creationMessage=creationMessage)
        
        file = open("HTML/returnPage.html", "w").close()

        with open("HTML/returnPage.html", "w") as f:
            f.write(newPage)
