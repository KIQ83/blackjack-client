import utils

def parse(table, playerName):
    print(table)
    type = table['type']
    if (type == 'Table'):
       return toArray(table, playerName) 
    return []

def toArray(table, playerName):
    input = []
    input = setSums(input, table, playerName)
    input = setCardsCount(input, table)
    return input
    

def setSums(input, table, playerName):
    # dealer
    dealer = table['dealer']
    dealerCards = utils.dealerCards(dealer)
    dealerSum = utils.sumCards(dealerCards)
    input.append(dealerSum)

    # player sum
    player = utils.findPlayer(table['players'], playerName)
    playerSum = utils.sumCards(player['pile'])
    input.append(playerSum)

    return input

def setCardsCount(input, table):
    # ongame
    ongame = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # 13 cards

    dealer = table['dealer']
    dealerCards = utils.dealerCards(dealer)
    for card in dealerCards:
        index = card['number']
        ongame[index] = ongame[index] + 1
    
    players = table['players']
    for player in players:
        playerCards = player['pile']
        for card in playerCards:
            index = card['number']
            ongame[index] = ongame[index] + 1

    return input + ongame

    # # on game
    # ongame = []
    # for _ in range(0, 13):
    #     input.append(24)

def setAction(input, table, hit = False):
    return input.append(hit)