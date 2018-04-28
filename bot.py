from client import Player
import time
import random
import utils
from input import Input
from input import Action
from input import TableState
from learning_model import learning_model

class Bot(object):

    playerName = None
    numberOfGames = 0
    bot = None
    # contains table state up to the last game played
    cumulateTableState = None
    # inputs used on the current game
    gameInputs = []

    currentDealerId = None

    def __init__(self, numberOfGames, playerName = 'SUPER_BOT'):
        self.numberOfGames = numberOfGames
        self.playerName = playerName
        self.bot = Player()
        self.learning_model = learning_model('/tmp/bot.ckpt')

    def registerMyself(self):
        print("--------------  NEW GAME --------------")
        print("Registering myself")
        self.bot.register(self.playerName)

    def awaitRegistering(self):
        print("Waiting for everyone to register..")
        table = self.bot.tableState()
        while (table == None or table['state'] == 'Registering'):
            time.sleep(0.1)
            print("Still waiting")
            table = self.bot.tableState()

    def awaitForTurn(self):
        print("Waiting for my turn to play.")
        table = self.bot.tableState()
        while (table['currentPlayer'] != self.bot.name):
            print("Not my turn. It's " + str(table['currentPlayer']) + "'s turn now.")
            time.sleep(0.1)
            table = self.bot.tableState()

        print("My turn now. Time to shine")

    def awaitGameFinish(self):
        print("Waiting for game to Finish")
        table = self.bot.tableState()
        while (table['state'] != 'Finished'):
            time.sleep(0.1)
            print("Still waiting")
            table = self.bot.tableState()

    def play(self):
        print("Heart of the cards, don't disappoint me!")
        table = self.bot.tableState()
        utils.printDealerShownCard(table['dealer'])
        player = utils.findPlayer(table['players'], self.bot.name)
        utils.printMyCards(player['pile'])
        while (player['state'] == 'Playing'):
            currentInput = Input(self.playerName, self.cumulateTableState.clone())
            currentInput.applyTable(table)

            shouldHit = self.learning_model.decide(currentInput.playerSum, currentInput.dealerSum)

            # playing agains the decided action
            if (not shouldHit):
                print("HIT ME!")
                self.bot.hit()
                currentInput.action = Action.HIT
            else:
                print("I'll stand for now. Let's hope for the best")
                self.bot.stand()
                currentInput.action = Action.STAND

            # The game server is a little slow. Lets give him some time
            self.gameInputs.append(currentInput)
            time.sleep(0.1)
            table = self.bot.tableState()
            player = utils.findPlayer(table['players'], self.bot.name)
            utils.printMyCards(player['pile'])

            # this means the player hit, and is not busted
            if (player['state'] == 'Playing'):
                self.learning_model.feed_reward(currentInput.playerSum, currentInput.dealerSum, 0, 0, shouldHit, False, None)


        print("Ok, that's it for me. I finish my play")

    def processResult(self):
        print("Checking results")
        table = self.bot.tableState()
        player = utils.findPlayer(table['players'], self.bot.name)
        dealer = table['dealer']
        utils.printFullDealer(dealer)
        utils.printMyCards(player['pile'])
        isWinner = player['state'] == 'Winner'
        if (isWinner):
            print("Daddy, I won!")
        else:
            print("I lost.. I'll do better next time..")

        self.handleInputs(isWinner, player, dealer)

    def handleInputs(self, isWinner, player, dealer):
        lastGameInput = self.gameInputs[-1]
        result = 'WIN'
        if (not isWinner):
            lastGameInput.invertAction()
            result = 'LOSS'

        for gameInput in self.gameInputs:
            gameInput.format()

        dealerCards = []
        dealerCards.append(dealer['shown'])
        dealerCards.append(dealer['hidden'])
        dealerSum = utils.sumCards(dealerCards)
        playerSum = utils.sumCards(player['pile'])
        self.saveWinRate(dealerSum, playerSum, dealer, result)

        self.learning_model.feed_reward(lastGameInput.playerSum, lastGameInput.dealerSum, playerSum, dealerSum, lastGameInput.action.value, True, isWinner)


    def saveWinRate(self, dealerSum, playerSum, dealer, result):
        # keeping track of win rates
        f = open('win_rates.csv','a')
        input = [dealer['id'], dealerSum, playerSum, result]
        print(str(input))
        f.write(str(dealer['id']) + "," + str(dealerSum) + ',' + str(playerSum) + "," + result + '\n')
        f.close()
         

    def prepareForNextGame(self):
        table = self.bot.tableState()
        self.cumulateTableState.applyTable(table)
        self.gameInputs = []

    def leaveGame(self):
        print("That's it. I'm out")
        self.bot.close()

    # we want to check if there is a new dealer, with new cards
    def assertTable(self):
        table = self.bot.tableState()
        if (self.currentDealerId == None or self.currentDealerId != table['dealer']['id']):
            print("New Dealer!! Welcome to the table my friend!")
            # new Dealer! Will reset cards counting
            self.cumulateTableState = TableState()
            self.currentDealerId = table['dealer']['id']

    def start(self):
        for _ in range(0, self.numberOfGames):
            self.registerMyself()
            self.awaitRegistering()
            self.awaitForTurn()

            self.assertTable()
            self.play()
            
            self.awaitGameFinish()
            self.processResult()
            self.prepareForNextGame()
            self.leaveGame()




