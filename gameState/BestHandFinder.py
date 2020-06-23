

class BestHandFinder:

    def isRoyalFlush(self, allCards):
        if self.isStraight(allCards)[0] and self.isFlush(allCards)[0]:
            cardsMag = [int(elem[0]) for elem in allCards]
            if (14 in cardsMag) and (13 in cardsMag) and (12 in cardsMag) and (11 in cardsMag) and (10 in cardsMag):
                return True, [10, 11, 12, 13, 14]
        
        return False, []
    
    def isStraightFlush(self, allCards):
        if self.isStraight(allCards)[0] and self.isFlush(allCards)[0]:
            cardsMagUsed = self.isStraight(allCards)[1]
            return True, cardsMagUsed
        else:
            return False, []

    def isFourKind(self, types):
        if 4 in types.values():
            cardsUsedmag = []
            for card in types:
                if types[card] == 4:
                    cardsUsedmag.append(int(card))
            return True, cardsUsedmag
        else:
            return False, []

    def isFullHouse(self, types):
        if self.isPair(types)[0] and self.isThreeKind(types)[0]:
            cardsMagUsed = [self.isThreeKind(types)[1], self.isPair(types)[1]]
            return True, cardsMagUsed
        else:
            return False, []

    def isFlush(self, allCards):
        suits = {}
        for card in allCards:
            if card[1] in suits.keys():
                suits[card[1]] += 1
            else:
                suits[card[1]] = 1
        highestNumSuit = max(suits.values())
        if highestNumSuit >= 5:
            cardsWithSuit = []
            suit = [key for (key, value) in suits.items() if value == highestNumSuit][0]
            for card in allCards:
                if card[1] == suit:
                    cardsWithSuit.append(int(card[0]))
            return True, cardsWithSuit
        else:
            return False, []

    def isStraight(self, allCards):
        magnitudes = [int(elem[0]) for elem in allCards]
        magnitudes.sort()
        numTests = 3 - (len(magnitudes) - len(set(magnitudes)))
        magnitudes = list(dict.fromkeys(magnitudes))

        for test in range(numTests):
            if magnitudes[test:test+5] == list(range(min(magnitudes[test:test+5]), max(magnitudes[test:test+5])+1)):
                return True, magnitudes[test:test+5]
            else:
                continue

        lowAceHand = [14, 2, 3, 4, 5]

        if [14, 2, 3, 4, 5] in magnitudes:
            return True, lowAceHand

        return False, []

    def isThreeKind(self, types):
        if 3 in types.values():
            cardsUsedmag = []
            for card in types:
                if types[card] == 3:
                    cardsUsedmag.append(int(card))
            return True, cardsUsedmag
        else:
            return False, []

    def isTwoPair(self, types):
        if  len([value for value in types.values() if value == 2]) == 2:
            cardsUsedmag = []
            for card in types:
                if types[card] == 2:
                    cardsUsedmag.append(int(card))
            return True, cardsUsedmag
        else:
            return False, [] 

    def isPair(self, types):
        if 2 in types.values():
            cardsUsedmag = []
            for card in types:
                if types[card] == 2:
                    cardsUsedmag.append(int(card))
            return True, cardsUsedmag
        else:
            return False, []
    
    def createFullBestHand(self, valuesToNotInclude, allCards, amountNeeded):
        allCardsMag = [int(elem[0]) for elem in allCards]
        for value in valuesToNotInclude:
            allCardsMag = list(filter((int(value)).__ne__, allCardsMag)) 

        highCards = []
        for i in range(amountNeeded):
            nextHighCard = max(list(set(allCardsMag)))
            highCards.append(nextHighCard)
            allCardsMag.remove(nextHighCard)

        return highCards

    def getTypes(self, allCards):
        types = {}
        for card in allCards:
            if card[0] in types.keys():
                types[card[0]] += 1
            else:
                types[card[0]] = 1

        return types

    def formatHand(self, hand):
        allCards = []
        for card in hand:
            card = card[:-4]
            newcards = [card[:-1], card[-1:]]
            if newcards[0] == "A":
                newcards[0] = "14"
            elif newcards[0] == "K":
                newcards[0] = "13"
            elif newcards[0] == "Q":
                newcards[0] = "12"
            elif newcards[0] == "J":
                newcards[0] = "11"
            allCards.append(newcards)
        
        return allCards

    def getHandStrength(self, hand):
        allCards = self.formatHand(hand)
        types = self.getTypes(allCards)

        isPair = self.isPair(types)
        isTwoPair = self.isTwoPair(types)
        isThreeKind = self.isThreeKind(types)
        isStraight = self.isStraight(allCards)
        isFlush = self.isFlush(allCards)
        isFullHouse = self.isFullHouse(types)
        isFourKind = self.isFourKind(types)
        isStraightFlush = self.isStraightFlush(allCards)
        isRoyalFlush = self.isRoyalFlush(allCards)

        if isRoyalFlush[0]:
            bestHand = isRoyalFlush[1]
            strength = 10
        elif isStraightFlush[0]:
            bestHand = isStraightFlush[1]
            strength = 9
        elif isFourKind[0]:
            cardsUsed = isFourKind[1]
            highOtherCards = self.createFullBestHand(cardsUsed, allCards, 1)
            bestHand = cardsUsed + highOtherCards
            strength = 8
        elif isFullHouse[0]:        
            bestHand = isFullHouse[1]
            strength = 7
        elif isFlush[0]:
            bestHand = isFlush[1]
            strength = 6
        elif isStraight[0]:
            bestHand = isStraight[1]
            strength = 5
        elif isThreeKind[0]:
            cardsUsed = isThreeKind[1]
            highOtherCards = self.createFullBestHand(cardsUsed, allCards, 2)
            bestHand = cardsUsed + highOtherCards
            strength = 4
        elif isTwoPair[0]:
            cardsUsed = isTwoPair[1]
            highOtherCards = self.createFullBestHand(cardsUsed, allCards, 1)
            bestHand = cardsUsed + highOtherCards
            strength = 3
        elif isPair[0]:
            cardsUsed = isPair[1]
            highOtherCards = self.createFullBestHand(cardsUsed, allCards, 3)
            bestHand = cardsUsed + highOtherCards
            strength = 2
        else:
            bestHand = self.createFullBestHand([], allCards, 5)
            strength = 1
        
        return strength, bestHand
    
    def getHighestHand(self, maxStages, playersWWS, startStage = 0):
        winnerFound = False
        stage = startStage
        while not winnerFound:
            highest = max([elem[stage] for elem in list(playersWWS.values())])
            playersWithHighest = []
            for player in playersWWS:
                if playersWWS[player][stage] == highest:
                    playersWithHighest.append(player)
            if len(playersWithHighest) == 1:
                winnerFound = True
                #One player has higher card than the others 
            elif stage == maxStages:
                winnerFound = True
                #Draw (all player have same magnitude of cards)
            else:
                stage += 1
        
        return playersWithHighest
    
    def getWinner(self, handStrengths, playerHands):
        maxHandStrength = max(handStrengths.values())
        playersWWS = {} #Players with winning strength

        for player in handStrengths:
            if handStrengths[player] == maxHandStrength:
                playersWWS[player] = playerHands[player]
        
        numPlayerWWS = len(playersWWS) #Number of players with winning strength

        if numPlayerWWS == 1:
            #one player has a higher hand strength
            winners = list(playersWWS.keys())
        elif maxHandStrength == 10:
            # players have royal flush
            winners = list(playersWWS.keys())
        elif maxHandStrength == 9:
            # players have straight Flush
            winners = self.getHighestHand(4, playersWWS, 4)
        elif maxHandStrength == 8:
            # players have four kind
            winners = self.getHighestHand(1, playersWWS)
        elif maxHandStrength == 7:
            # players have full house
            winners = self.getHighestHand(1, playersWWS)
        elif maxHandStrength == 6:
            # players have a flush
            winners = self.getHighestHand(4, playersWWS)
        elif maxHandStrength == 5:
            # players have straight
            winners = self.getHighestHand(4, playersWWS, 4)
        elif maxHandStrength == 4:
            # players have three kind
            winners = self.getHighestHand(2, playersWWS)
        elif maxHandStrength == 3:
            # players have 2 pair
            winners = self.getHighestHand(2, playersWWS)
        elif maxHandStrength == 2:
            # players have pair
            winners = self.getHighestHand(3, playersWWS)
        elif maxHandStrength == 1:
            # players have high card only
            winners = self.getHighestHand(4, playersWWS)

        return winners
