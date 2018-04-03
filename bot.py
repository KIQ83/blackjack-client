from client import Player
import time
import random
import utils
from input import Input
from input import Action
from input import TableState

class Bot(object):

    playerName = None
    numberOfGames = 0
    bot = None
    # contains table state up to the last game played
    cumulateTableState = None
    # inputs used on the current game
    gameInputs = []

    def __init__(self, numberOfGames, playerName = 'MDNS_BOT'):
        self.numberOfGames = numberOfGames
        self.playerName = playerName
        self.bot = Player()
        self.cumulateTableState = TableState()

    def registerMyself(self):
        print("--------------  NEW GAME --------------")
        print("Registering myself")
        self.bot.register(self.playerName)

    def awaitRegistering(self):
        print("Waiting for everyone to register..")
        table = self.bot.tableState()
        while (table == None or table['state'] == 'Registering'):
            time.sleep(1)
            print("Still waiting")
            table = self.bot.tableState()

    def awaitForTurn(self):
        print("Waiting for my turn to play.")
        table = self.bot.tableState()
        while (table['currentPlayer'] != self.bot.name):
            print("Not my turn. It's " + str(table['currentPlayer']) + "'s turn now.")
            time.sleep(1)
            table = self.bot.tableState()

        print("My turn now. Time to shine")

    def awaitGameFinish(self):
        print("Waiting for game to Finish")
        table = self.bot.tableState()
        while (table['state'] != 'Finished'):
            time.sleep(1)
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

            shouldStand = bool(random.getrandbits(1))
            if (shouldStand):
                print("I'll stand for now. Let's hope for the best")
                self.bot.stand()
                currentInput.action = Action.STAND
            else:
                print("HIT ME!")
                self.bot.hit()
                currentInput.action = Action.HIT

            # The game server is a little slow. Lets give him some time
            self.gameInputs.append(currentInput)
            time.sleep(1)
            table = self.bot.tableState()
            player = utils.findPlayer(table['players'], self.bot.name)
            utils.printMyCards(player['pile'])

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

        self.handleInputs(isWinner)

    def handleInputs(self, isWinner):
        lastGameInput = self.gameInputs[-1]
        if (not isWinner):
            lastGameInput.invertAction()

        for gameInput in self.gameInputs:
            gameInput.format()

    def prepareForNextGame(self):
        table = self.bot.tableState()
        self.cumulateTableState.applyTable(table)
        self.gameInputs = []

    def leaveGame(self):
        print("That's it. I'm out")
        self.bot.close()

    def start(self):
        for _ in range(0, self.numberOfGames):
            self.registerMyself()
            self.awaitRegistering()
            self.awaitForTurn()
            self.play()
            self.awaitGameFinish()
            self.processResult()
            self.prepareForNextGame()
            self.leaveGame()




