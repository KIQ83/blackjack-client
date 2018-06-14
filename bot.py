from client import Player
import time
import random
import utils
from input import Input
from input import Action
from input import TableState
from learning_model import LearningModel

# The sleep time decides the delay out bot takes before checking next responses from the server
sleepTime=0.01

# The bot contains logic for interacting to the blackjack server as a client
# The deep learning code IS NOT HERE. It is inside the learning_model.py and agent.py files
class Bot(object):

    playerName = None
    numberOfGames = 0
    bot = None
    # contains table state up to the last game played
    cumulateTableState = None
    # inputs used on the current game
    gameInputs = []

    currentDealerId = None

    def __init__(self, numberOfGames, playerName='SUPER_BOT', modelname='default'):
        self.modelname = modelname
        self.numberOfGames = numberOfGames
        self.playerName = playerName
        self.bot = Player()

        self.learning_model = LearningModel('./models/'+modelname+'/'+modelname+'.ckpt')

    # Register itself on the game server
    def registerMyself(self):
        print("--------------  NEW GAME --------------")
        print("Registering myself")
        self.bot.register(self.playerName)

    # Waits for other players to register themselves
    def awaitRegistering(self):
        print("Waiting for everyone to register..")
        table = self.bot.tableState()
        while (table == None or table['state'] == 'Registering'):
            time.sleep(sleepTime)
            print("Still waiting")
            table = self.bot.tableState()

    # Keeps waiting until it is it's turn to play
    def awaitForTurn(self):
        print("Waiting for my turn to play.")
        table = self.bot.tableState()
        while (table['currentPlayer'] != self.bot.name):
            print("Not my turn. It's " + str(table['currentPlayer']) + "'s turn now.")
            time.sleep(sleepTime)
            table = self.bot.tableState()

        print("My turn now. Time to shine")

    # Waits until the game is finished
    def awaitGameFinish(self):
        print("Waiting for game to Finish")
        table = self.bot.tableState()
        while (table['state'] != 'Finished'):
            time.sleep(sleepTime)
            print("Still waiting")
            table = self.bot.tableState()

    # Plays on it's turn, until it decided to stand or it get busted
    def play(self):
        print("Heart of the cards, don't disappoint me!")
        # Getting the current table state
        table = self.bot.tableState()
        utils.printDealerShownCard(table['dealer'])
        player = utils.findPlayer(table['players'], self.bot.name)
        utils.printMyCards(player['pile'])
        while (player['state'] == 'Playing'):
            # getting an input view from the table
            currentInput = Input(self.playerName, self.cumulateTableState.clone())
            currentInput.applyTable(table)

            # Uses our learning model to decide what action to take
            shouldStand = self.learning_model.decide(currentInput.playerSum, currentInput.dealerSum, currentInput.tableState.possibleCards)

            if (not shouldStand):
                print("HIT ME!")
                self.bot.hit()
                currentInput.action = Action.HIT
            else:
                print("I'll stand for now. Let's hope for the best")
                self.bot.stand()
                currentInput.action = Action.STAND

            self.gameInputs.append(currentInput)
            # The game server is a little slow. Lets give him some time before making next request
            time.sleep(sleepTime)
            table = self.bot.tableState()
            player = utils.findPlayer(table['players'], self.bot.name)
            utils.printMyCards(player['pile'])


            if (player['state'] == 'Playing'):
                # this means the player hit, and is not busted. Will feed partial reward
                self.learning_model.feed_reward(currentInput.playerSum, currentInput.dealerSum, currentInput.tableState.possibleCards, 0, 0, shouldStand, False, None)


        print("Ok, that's it for me. I finish my play")

    # Printing results and handling results
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

    # Handling results from previous game
    def handleInputs(self, isWinner, player, dealer):
        lastGameInput = self.gameInputs[-1]
        result = 'WIN'
        if (not isWinner):
            result = 'LOSS'

        dealerCards = []
        dealerCards.append(dealer['shown'])
        dealerCards.append(dealer['hidden'])
        dealerSum = utils.sumCards(dealerCards)
        playerSum = utils.sumCards(player['pile'])
        # storing result on csv file
        utils.saveWinRate(self.modelname, dealerSum, playerSum, dealer, result)
        # feeding reward to our model
        self.learning_model.feed_reward(lastGameInput.playerSum, lastGameInput.dealerSum, lastGameInput.tableState.possibleCards, playerSum, dealerSum, lastGameInput.action.value, True, isWinner)
  
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

    # Plays N games, always taking the same steps
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




