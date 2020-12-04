from gameState.PokerMemory import Player, Memory, Forms, ResponceTypes
from gameState.BetRound import BetRound
from gameState.BestHandFinder import BestHandFinder
from gameState.Responce import Responce

import random

class PokerHandler:

    # Class that will handle all the logs and carry out the poker Game.

    def __init__(self):
        self.memory = Memory()
        self.betRound = BetRound(round=1)
        self.bestHandFinder = BestHandFinder()
        self.allCards = ["AS.jpg", "2S.jpg", "3S.jpg", "4S.jpg", "5S.jpg", "6S.jpg", "7S.jpg", "8S.jpg", "9S.jpg", "10S.jpg", "JS.jpg", "QS.jpg", "KS.jpg", 
                    "AC.jpg", "2C.jpg", "3C.jpg", "4C.jpg", "5C.jpg", "6C.jpg", "7C.jpg", "8C.jpg", "9C.jpg", "10C.jpg", "JC.jpg", "QC.jpg", "KC.jpg",
                    "AD.jpg", "2D.jpg", "3D.jpg", "4D.jpg", "5D.jpg", "6D.jpg", "7D.jpg", "8D.jpg", "9D.jpg", "10D.jpg", "JD.jpg", "QD.jpg", "KD.jpg",
                    "AH.jpg", "2H.jpg", "3H.jpg", "4H.jpg", "5H.jpg", "6H.jpg", "7H.jpg", "8H.jpg", "9H.jpg", "10H.jpg", "JH.jpg", "QH.jpg", "KH.jpg"]
        

    def completeEvent(self, event):
        self.addEventToMem(event)
        form, data = event.split(" ")
        form = Forms[form]

        if form.value == 1: # ADD
            name, money = data.split(",")
            self.addPlayerToMem(name, money)
        elif form.value == 2:  # READY
            self.memory.playersReady[data] = True
        elif form.value == 3: # CARDS
            self.addPlayerCardsToMem(data)
        elif form.value == 4: # BET
            name, bet = data.split(",")
            self.memory.pot += int(bet)
            for player in self.memory.players:
                if player.name == name:
                    player.money = int(player.money) - int(bet)
            self.betRound.addBet(name, bet)
            self.memory.betAmount = max(self.betRound.playersBet.values())
        elif form.value == 5: # FLOP
            round = self.betRound.round
            self.betRound = BetRound(round+1)
            self.memory.flop = data.split(",")
        elif form.value == 6: # TURN
            round = self.betRound.round
            self.betRound = BetRound(round+1)
            self.memory.turn = data
        elif form.value == 7: # RIVER
            round = self.betRound.round
            self.betRound = BetRound(round+1)
            self.memory.river = data
        elif form.value == 8: # Fold
            for player in self.memory.players:
                if player.name == data:
                    playerIndex = self.memory.players.index(player)
            self.memory.players[playerIndex].folded = True
            self.memory.foldedPlayers.append(self.memory.players[playerIndex])
            self.memory.players.pop(playerIndex)

    def responce(self, user):
        """
        This function works backwards through possible stages game.
        Its starts by checking if the game is finished
        Working backwards to checking if players join have joined the table.
        """
        userCards = (self.memory.players[[i if user == x.name else -1 for i,x in enumerate(self.memory.players)][0]]).cards
        eventsSorted = self.sortEvents()

        if len(self.memory.players) == 1 and len(self.memory.foldedPlayers) > 0:
            winner = [self.memory.players[0].name]
            self.distrobutePot(winner, self.memory.pot)
            responce = Responce(ResponceTypes.WINNER, "", user, winner, userCards, None, None, None, self.memory.pot)

        elif self.betRound.round == 4 and len(self.betRound.playersBet) > 1:
            #Check if its 4th betting round and a player has bet. Gets next player to bet.
            betResp = self.getBetRoundResponce(eventsSorted)
            if betResp[0] == ResponceTypes.WINNER:
                winners, handStrengths = self.workOutWinner()
                self.distrobutePot(winners, self.memory.pot)
                responce = Responce(betResp[0], "", user, winners, userCards, None, None, handStrengths, self.memory.pot)
            else:
                responce = Responce(betResp[0], betResp[2], user, betResp[1], userCards, self.memory.flop, self.memory.turn, self.memory.river, self.memory.pot)

        elif eventsSorted[7] == 1:
            #checks if river has been shown and gets first player to bet in 4th betting round.
            nextBetPlayer = self.betRound.whoBetNext(self.memory.players)
            responce = Responce(ResponceTypes.NEXTBET, "", user, nextBetPlayer, userCards, self.memory.flop, self.memory.turn, self.memory.river, self.memory.pot)

        elif self.betRound.round == 3 and len(self.betRound.playersBet) > 1:
            #Check if its 3nd betting round and a player has bet. Gets next player to bet.
            betResp = self.getBetRoundResponce(eventsSorted)
            responce = Responce(betResp[0], betResp[2], user, betResp[1], userCards, self.memory.flop, self.memory.turn, self.memory.river, self.memory.pot)

        elif eventsSorted[6] == 1:
            #checks if turn has been shown and gets first player to bet in 3rd betting round.
            nextBetPlayer = self.betRound.whoBetNext(self.memory.players)
            responce = Responce(ResponceTypes.NEXTBET, "", user, nextBetPlayer, userCards, self.memory.flop, self.memory.turn, self.memory.river, self.memory.pot)

        elif self.betRound.round == 2 and len(self.betRound.playersBet) > 1:
            #Check if its 2nd betting round and a player has bet. Gets next player to bet.
            betResp = self.getBetRoundResponce(eventsSorted)
            responce = Responce(betResp[0], betResp[2], user, betResp[1], userCards, self.memory.flop, self.memory.turn, self.memory.river, self.memory.pot)

        elif eventsSorted[5] == 1:
            #checks if the flop has been shown and if it has then gets first player to bet in betting round 2.
            nextBetPlayer = self.betRound.whoBetNext(self.memory.players)
            responce = Responce(ResponceTypes.NEXTBET, "", user, nextBetPlayer, userCards, self.memory.flop, self.memory.turn, self.memory.river, self.memory.pot)

        elif eventsSorted[4] >= 1:
            #gets next player to bet if all bets are places then next cards is told to show.
            betResp = self.getBetRoundResponce(eventsSorted)
            responce = Responce(betResp[0], betResp[2], user, betResp[1], userCards, self.memory.flop, self.memory.turn, self.memory.river, self.memory.pot)

        elif eventsSorted[3] == len(self.memory.players):
            #If all the players have cards the first player to bet is chosen.   
            nextBetPlayer = self.betRound.whoBetNext(self.memory.players)
            responce = Responce(ResponceTypes.NEXTBET, "", user, nextBetPlayer, userCards, self.memory.flop, self.memory.turn, self.memory.river, self.memory.pot)
 
        elif eventsSorted[1] >= 2:  
            #are there more than 2 players?
            if eventsSorted[2] == len(self.memory.players):
                responce = Responce(ResponceTypes.DEALCARDS, None, user, None, userCards, self.memory.flop, self.memory.turn, self.memory.river, self.memory.pot)     
            else:
                responce = Responce(ResponceTypes.WAITREADY, None, user, None, userCards, self.memory.flop, self.memory.turn, self.memory.river, self.memory.pot)

        elif eventsSorted[1] < 2:
            #There are less than 2 players.
            responce = Responce(ResponceTypes.NEEDPlAYERS, None, user, None, userCards, self.memory.flop, self.memory.turn, self.memory.river, self.memory.pot)         

        return responce

    def getBetRoundResponce(self, events):
        areAllBetsSame, whoNot, amount = self.betRound.areBetsSame()
        if not areAllBetsSame:
            #checks who has not bet enough.
            betRoundResponce =  [ResponceTypes.NEEDBET, whoNot, amount]
        else:
            if all(x.name in self.betRound.playersBet.keys() for x in self.memory.players):
                #all players have bet the correct amount so shows the flop.
                if events[5] == 0:
                    respType = ResponceTypes.SHOWFLOP
                elif events[6] == 0:
                    respType = ResponceTypes.SHOWTURN
                elif events[7] == 0:
                    respType = ResponceTypes.SHOWRIVER
                else:
                    respType = ResponceTypes.WINNER
                betRoundResponce = [respType, "", ""]
            else:
                #finds which player needs to bet next.
                nextBetPlayer = self.betRound.whoBetNext(self.memory.players)
                betRoundResponce = [ResponceTypes.NEXTBET, nextBetPlayer, ""]

        return betRoundResponce

    def sortEvents(self):
        dictEvents = {1: 0, 2: 0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}
        for event in self.memory.events:
            for form in Forms:
                if form.name in event:
                    dictEvents[form.value] += 1

        return dictEvents

    def addPlayerToMem(self, name, money):
        newPlayer = Player(name, money)
        self.memory.players.append(newPlayer)
        self.memory.playersReady[name] = False

    def addEventToMem(self, log):
        self.memory.events.append(log)
    
    def addPlayerCardsToMem(self, data):
        name = data.split(",")[0]
        playerCards = data[len(name)+1:len(data)]

        for player in self.memory.players:
            if player.name == name:
                player.cards = playerCards.split(",")
                break

    def workOutWinner(self):
        self.memory.flop.extend([self.memory.river, self.memory.turn])
        cardsOnTable = self.memory.flop

        handStrengths = {}
        playerHands = {}

        for player in self.memory.players:
            strength, bestHand = self.bestHandFinder.getHandStrength(player.cards + cardsOnTable)
            handStrengths[player.name] = strength
            playerHands[player.name] = bestHand
        
        winners = self.bestHandFinder.getWinner(handStrengths, playerHands)

        return winners, handStrengths
    
    def distrobutePot(self, winners, pot):
        amountWinners = len(winners)
        amountToGive = pot / amountWinners
        for player in self.memory.players:
            for winner in winners:
                if player.name == winner:
                    player.money = int(player.money) + int(amountToGive)

    def dealCards(self, events, amountCards):
        cardsUsed = []
        
        for event in events:
            tp = event.split(" ")[0]
            cards = event.split(" ")[1].split(",")

            if (tp == "CARDS") or (tp == "FLOP") or (tp == "RIVER") or (tp == "TURN"):
                for card in cards:
                    cardsUsed.append(card)

        avaliableCards = [x for x in self.allCards if x not in cardsUsed]
        returnCards = []

        for i in range(amountCards):
            chosenCard = random.choice(avaliableCards)
            returnCards.append(chosenCard)
            avaliableCards.remove(chosenCard)

        return returnCards
