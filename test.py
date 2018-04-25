import random
from bot import Bot

name = 'Jogador' + str(random.randint(1, 1000000))
x = Bot(8000, 'Player ' + name)
x.start()