import random
from bot import Bot

name = 'Jogador' + str(random.randint(1, 10000000))
x = Bot(10, 'Player ' + name)
x.start()