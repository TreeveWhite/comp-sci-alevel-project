

class BetRound:
    def __init__(self, round):
        self.playersBet = {}
        self.round = round
    
    def addBet(self, name, bet):
        if name in self.playersBet.keys():
            self.playersBet[name] += int(bet)
        else:
            self.playersBet[name] = int(bet)
    
    def areBetsSame(self):
        if len(set(self.playersBet.values())) == 1 and len(self.playersBet) >= 0:
            areSame = True
            playerNeedToBetMore = None
            amount = 0
        else:
            playerNeedToBetMore, amount = self.needsToRaise()
            areSame = False
        return areSame, playerNeedToBetMore, amount
    
    def needsToRaise(self):
        max = 0
        for value in self.playersBet.values():
            if int(value) > int(max):
                max = value
        for value in self.playersBet.values():
            if int(value) < int(max):
                lowBet = value
        for name, bet in self.playersBet.items():
            if bet == lowBet:
                break
        amountToBet = int(max) - int(lowBet)
        return [name, amountToBet]

    def whoBetNext(self, players):
        for player in players:
            if not (player.name in self.playersBet.keys()):
                return player.name