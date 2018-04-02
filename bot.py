from client import Player
import time
import random
import utils

def registerMyself(bot):
    print("--------------  NEW GAME --------------")
    print("Registering myself")
    bot.register('KIQ')

def awaitRegistering(bot):
    print("Waiting for everyone to register..")
    table = bot.tableState()
    while (table == None or table['state'] == 'Registering'):
        time.sleep(1)
        print("Still waiting")
        table = bot.tableState()

def awaitForTurn(bot):
    print("Waiting for my turn to play.")
    table = bot.tableState()
    while (table['currentPlayer'] != bot.name):
        print("Not my turn. It's " + str(table['currentPlayer']) + "'s turn now.")
        time.sleep(1)
        table = bot.tableState()

    print("My turn now. Time to shine")

def awaitGameFinish(bot):
    print("Waiting for game to Finish")
    table = bot.tableState()
    while (table['state'] != 'Finished'):
        time.sleep(1)
        print("Still waiting")
        table = bot.tableState()

def play(bot):
    print("Heart of the cards, don't disappoint me!")
    table = bot.tableState(True)
    printDealerShownCard(table['dealer'])
    player = utils.findPlayer(table['players'], bot.name)
    printMyCards(player['pile'])
    while (player['state'] == 'Playing'):
        # tableAtualInput = input.fromTable()
        # inputAtual = input.juntarInformacoes(tableAtual, acumulado)
        shouldStand = bool(random.getrandbits(1))
        if (shouldStand):
            print("I'll stand for now. Let's hope for the best")
            bot.stand()
        else:
            print("HIT ME!")
            bot.hit()

        # The game server is a little slow. Lets give him some time
        time.sleep(1)
        table = bot.tableState()
        player = utils.findPlayer(table['players'], bot.name)
        printMyCards(player['pile'])

    print("Ok, that's it for me. I finish my play")

def checkResult(bot):
    print("Checking results")
    table = bot.tableState()
    player = utils.findPlayer(table['players'], bot.name)
    dealer = table['dealer']
    printFullDealer(dealer)
    printMyCards(player['pile'])
    winner = player['state'] == 'Winner'
    if (winner):
        print("Daddy, I won!")
    else:
        print("I lost.. I'll do better next time..")

    # tableAtualInput = input.fromTable()
    # inputAtual = input.juntarInformacoes(tableAtual, acumulado)

def leaveGame(bot):
    print("That's it. I'm out")
    bot.close()

def printMyCards(cards):
    print("These are my cards:")
    printCards(cards)

def printDealerShownCard(dealer):
    print('Dealer has: ' + utils.cardDisplay(dealer['shown']))

def printFullDealer(dealer):
    dealerCards = [dealer['shown'], dealer['hidden']]
    print('Dealer cards: ')
    printCards(dealerCards)

def printCards(cards):
    cardSum = utils.sumCards(cards)
    cardsDisplay = ''
    for card in cards:
        cardsDisplay += utils.cardDisplay(card) + ","
    print(cardsDisplay + " that gives a total of " + str(cardSum))

numberOfGames = 1
bot = Player()

# acumulado = Input(numeroDeDecks=6) // isso aqui inicializou todas as variaveis, menos a de decisao

for x in range(0, numberOfGames):
    # inputAtual = acumulado
    registerMyself(bot)
    awaitRegistering(bot)
    awaitForTurn(bot)
    play(bot)
    awaitGameFinish(bot)
    checkResult(bot)
    leaveGame(bot)
    # acumulado = inputAtual




