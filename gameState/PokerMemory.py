import enum

class Player:

    # Player Object

    def __init__(self, name, money):
        self.name = name
        self.folded = False
        self.money = money
        self.cards = []
        self.cardsUsedToMakeStrength = []
    
class Memory:

    # Class to hold all data about poker game

    def __init__(self):
        self.players = []
        self.playersReady = {}
        self.foldedPlayers = []
        self.bet = None
        self.river = None
        self.flop = None
        self.turn = None
        self.dealerCards = []
        self.events = []
        self.pot = 0
        self.betAmount = 0

class Forms(enum.Enum):
    ADD = 1
    READY = 2
    CARDS = 3
    BET = 4
    FLOP = 5
    TURN = 6
    RIVER = 7
    FOLD = 8


class ResponceTypes(enum.Enum):
    NEEDBET = 1
    NEXTBET = 2
    NEEDPlAYERS = 3
    DEALCARDS = 4
    SHOWFLOP = 5
    SHOWTURN = 6
    SHOWRIVER = 7
    WINNER = 8
    NOTTURN = 9
    WAITREADY = 10
