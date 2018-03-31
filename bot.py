from client import Player
import time
import random

timeToMove = 5

bot = Player()
bot.start()
bot.register('Jao')

isPlaying = True
while (isPlaying):
    time.sleep(timeToMove)
    bot.updateMe()
    time.sleep(timeToMove)
    shouldStand = bool(random.getrandbits(1))
    print(shouldStand)
    if (shouldStand):
        isPlaying = False
        print('parou')
    else:
        bot.hit()
        print('hitou')

bot.stand()
print('standou')