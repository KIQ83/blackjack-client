import random
from bot import Bot

MODELNAME = 'bot1'

name = 'Jogador' + str(random.randint(1, 10000000))
x = Bot(1000, 'Player ' + name, MODELNAME)
x.start()