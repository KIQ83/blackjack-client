import utils
from enum import Enum

class Action(Enum):
    HIT = 0
    STAND = 1

class Input:

    INITIAL_USED_CARDS = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # 13 cards
    # Considering 6 decks being used
    INITIAL_POSSIBLE_CARDS = [24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24] # 13 cards

    def __init__(self, playerName):
        self.playerName = playerName
        self.dealerSum = 0
        self.playerSum = 0
        self.possibleCards = INITIAL_POSSIBLE_CARDS
        self.usedCards = INITIAL_USED_CARDS

    def cloneCards(self):
        cloned = Input(self.playerName)
        cloned.possibleCards = [x for x in self.possibleCards]
        cloned.usedCards = [x for x in self.usedCards]

    def applyTable(self, table):
        self.dealerSum = self.setDealerSum(table)
        self.playerSum =self.setPlayerSum(table)
        self.possibleCards = self.setPossibleCards(table)
        self.used = self.setUsedCards(table)

    def setDealerSum(self, table):
        dealer = table['dealer']
        dealerCards = utils.dealerCards(dealer)
        return utils.sumCards(dealerCards)

    def setPlayerSum(self, table):
        player = utils.findPlayer(table['players'], self.playerName)
        return utils.sumCards(player['pile'])

    def setPossibleCards(self, table):
        dealer = table['dealer']
        dealerCards = utils.dealerCards(dealer)
        for card in dealerCards:
            index = card['number']
            self.possibleCards[index] = max(self.possibleCards[index] - 1, 0)
        
        players = table['players']
        for player in players:
            playerCards = player['pile']
            for card in playerCards:
                index = card['number']
                self.possibleCards[index] = max(self.possibleCards[index] - 1, 0)

    def setUsedCards(self, table):
        dealer = table['dealer']
        dealerCards = utils.dealerCards(dealer)
        for card in dealerCards:
            index = card['number']
            self.disCards[index] = self.disCards[index] + 1

        players = table['players']
        for player in players:
            playerCards = player['pile']
            for card in playerCards:
                index = card['number']
                self.disCards[index] = self.disCards[index] + 1

    def format(self):
        input = []
        input.append(self.dealerSum)
        input.append(self.playerSum)
        input = input + self.possibleCards
        input = input + self.disCards
        input.append(self.action)
        print(input)