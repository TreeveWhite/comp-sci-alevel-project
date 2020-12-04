from gameState.PokerMemory import ResponceTypes

class Responce:

    def __init__(self, message, details, user, currentPlayer, cards, flop, turn, river, pot):
        self.message = message
        self.details = details
        self.currentPlayer = currentPlayer
        self.user = user

        self.cards = cards

        self.flop = flop

        self.turn = turn

        self.river = river

        self.pot = pot

        if (self.currentPlayer != self.user):
            if self.message == ResponceTypes.NEXTBET or self.message == ResponceTypes.NEEDBET:
                self.message = ResponceTypes.NOTTURN