import random
from bot import Bot

MODELNAME = 'bot41'

name = 'Jogador' + str(random.randint(1, 10000000))
x = Bot(50000, 'Player ' + name, MODELNAME)
x.start()
