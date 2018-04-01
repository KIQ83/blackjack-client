from client import Player
import time
import random

def registerMyself(bot):
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
    player = findPlayer(table['players'], bot.name)
    while (player['state'] == 'Playing'):
        print("These are my cards:" + str(player['pile']))
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

    print("Ok, that's it for me. I finish my play")

def checkResult(bot):
    table = bot.tableState()
    player = findPlayer(table['players'], bot.name)
    winner = player['state'] == 'Winner'
    if (winner):
        print("Daddy, I won!")
    else:
        print("I'll do better next time..")

def leaveGame(bot):
    print("That's it. I'm out")
    bot.close()

def findPlayer(playersList, playerName):
    for player in playersList:
        if player['name'] == playerName:
            return player

def sumCards(cards):
    print("sum")

def simpleSum(cards):
    print("Simple sum")

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




