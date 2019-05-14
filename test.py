import random
from bot import Bot

# This is our best model so far, bot40
# Currently the best bot is named brunielle
MODELNAME = 'brunielle'

# Just creating a random player name to be registered at the game server
name = 'Jogador' + str(random.randint(1, 10000000))
# Will play for 50 thousand games
x = Bot(50000, 'Player ' + name, MODELNAME)
x.start()
