import random
from bot import Bot

MODELNAME = 'bot7'

name = 'Jogador' + str(random.randint(1, 10000000))
x = Bot(5000, 'Player ' + name, MODELNAME)
x.start()
