import random
from bot import Bot

MODELNAME = 'bot2'

name = 'Jogador' + str(random.randint(1, 10000000))
x = Bot(100000, 'Player ' + name, MODELNAME)
x.start()
