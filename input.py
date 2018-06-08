import utils
import csv
from enum import Enum

# initially, 0 cards of each type were used
INITIAL_USED_CARDS = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # 13 cards
# Considering 6 decks being used, so there are 24 cards of each type
INITIAL_POSSIBLE_CARDS = [24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24] # 13 cards

class Action(Enum):
    HIT = 0
    STAND = 1

class TableState:

    def __init__(self):
        self.possibleCards = [x for x in INITIAL_POSSIBLE_CARDS]
        self.usedCards = [x for x in INITIAL_USED_CARDS]

    def clone(self):
        cloned = TableState()
        cloned.possibleCards = [x for x in self.possibleCards]
        cloned.usedCards = [x for x in self.usedCards]
        return cloned

    def applyTable(self, table):
        self.setPossibleCards(table)
        self.setUsedCards(table)

    def setPossibleCards(self, table):
        dealer = table['dealer']
        dealerCards = utils.dealerCards(dealer)
        for card in dealerCards:
            index = card['number']
            self.possibleCards[index] = self.possibleCards[index] - 1
        
        players = table['players']
        for player in players:
            playerCards = player['pile']
            for card in playerCards:
                index = card['number']
                self.possibleCards[index] = self.possibleCards[index] - 1

    def setUsedCards(self, table):
        dealer = table['dealer']
        dealerCards = utils.dealerCards(dealer)
        for card in dealerCards:
            index = card['number']
            self.usedCards[index] = self.usedCards[index] + 1

        players = table['players']
        for player in players:
            playerCards = player['pile']
            for card in playerCards:
                index = card['number']
                self.usedCards[index] = self.usedCards[index] + 1

class Input:

    def __init__(self, playerName, tableState):
        self.playerName = playerName
        self.dealerSum = 0
        self.playerSum = 0
        self.tableState = tableState

    def applyTable(self, table):
        self.setDealerSum(table)
        self.setPlayerSum(table)
        self.tableState.applyTable(table)

    def setDealerSum(self, table):
        dealer = table['dealer']
        dealerCards = utils.dealerCards(dealer)
        self.dealerSum = utils.sumCards(dealerCards)

    def setPlayerSum(self, table):
        player = utils.findPlayer(table['players'], self.playerName)
        self.playerSum = utils.sumCards(player['pile'])

