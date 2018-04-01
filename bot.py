from client import Player
import time
import random

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
    table = bot.tableState()
    printDealerShownCard(table['dealer'])
    player = findPlayer(table['players'], bot.name)
    printMyCards(player['pile'])
    while (player['state'] == 'Playing'):
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
        player = findPlayer(table['players'], bot.name)
        printMyCards(player['pile'])

    print("Ok, that's it for me. I finish my play")

def checkResult(bot):
    print("Checking results")
    table = bot.tableState()
    player = findPlayer(table['players'], bot.name)
    dealer = table['dealer']
    printFullDealer(dealer)
    printMyCards(player['pile'])
    winner = player['state'] == 'Winner'
    if (winner):
        print("Daddy, I won!")
    else:
        print("I lost.. I'll do better next time..")

def leaveGame(bot):
    print("That's it. I'm out")
    bot.close()

def findPlayer(playersList, playerName):
    for player in playersList:
        if player['name'] == playerName:
            return player

def printMyCards(cards):
    print("These are my cards:")
    printCards(cards)

def printDealerShownCard(dealer):
    print('Dealer has: ' + cardDisplay(dealer['shown']))

def printFullDealer(dealer):
    dealerCards = [dealer['shown'], dealer['hidden']]
    print('Dealer cards: ')
    printCards(dealerCards)

def printCards(cards):
    cardSum = sumCards(cards)
    cardsDisplay = ''
    for card in cards:
        cardsDisplay += cardDisplay(card) + ","
    print(cardsDisplay + " that gives a total of " + str(cardSum))


def cardDisplay(card):
    return str(getCardSymbol(card['number'])) + card['suit'] 

def getCardSymbol(cardIndex):
    if cardIndex == 0:
        return 'A'
    elif cardIndex == 10:
        return 'J'
    elif cardIndex == 11:
        return 'Q'
    elif cardIndex == 12:
        return 'K'
    else:
        return str(cardIndex + 1)

def getCardSumValue(cardIndex):
    # figure Cards are worth 10
    if cardIndex in (10, 13):
        return 10
    else:
        return cardIndex + 1

def sumCards(cards):
    cardValues = [getCardSumValue(card['number']) for card in cards]
    simpleSum = sum(cardValues)
    hasAce = containsAce([card['number'] for card in cards])
    # will use ace as 11 only if has ace and if sum does not exceed 21
    usableAce = hasAce and (simpleSum + 10) <= 21
    if usableAce:
        return simpleSum + 10
    else:
        return simpleSum

    
def containsAce(cardsIndexes):
    return 0 in cardsIndexes

numberOfGames = 2
bot = Player()

for x in range(0, numberOfGames):
    registerMyself(bot)
    awaitRegistering(bot)
    awaitForTurn(bot)
    play(bot)
    awaitGameFinish(bot)
    checkResult(bot)
    leaveGame(bot)




