import utils
import csv
from enum import Enum

# initially, 0 cards of each type were used
INITIAL_USED_CARDS = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # 13 cards
# Considering 6 decks being used, so there are 24 cards of each type
INITIAL_POSSIBLE_CARDS = [24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24] # 13 cards

# Enum class for representing each possible decision
class Action(Enum):
    HIT = 0
    STAND = 1

# The table State class representes the cumulate table state
# It represents all information the bot has stored for the table
# This means all the cards used, and all the cards that can still be used
class TableState:

    # The constructor just initialize the variables with the INITIAL constants
    def __init__(self):
        self.possibleCards = [x for x in INITIAL_POSSIBLE_CARDS]
        self.usedCards = [x for x in INITIAL_USED_CARDS]

    # Safe clone function (cloning the values, and not the pointers)
    def clone(self):
        cloned = TableState()
        cloned.possibleCards = [x for x in self.possibleCards]
        cloned.usedCards = [x for x in self.usedCards]
        return cloned

    # Updating the cumulate table state using a current table state
    def applyTable(self, table):
        self.setPossibleCards(table)
        self.setUsedCards(table)

    # Updates the vision the bot has on the possible cards
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
    
    # Updates the vision the bot has on the used cards
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

# The input class represents the vision the bot has of the table before making a decision
# It basically is the cumulate table state together with the player and the dealer's sum
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

    # calculates dealer sum based on dealer's cards
    def setDealerSum(self, table):
        dealer = table['dealer']
        dealerCards = utils.dealerCards(dealer)
        self.dealerSum = utils.sumCards(dealerCards)

    # calculates player sum based on the players cards
    def setPlayerSum(self, table):
        player = utils.findPlayer(table['players'], self.playerName)
        self.playerSum = utils.sumCards(player['pile'])

