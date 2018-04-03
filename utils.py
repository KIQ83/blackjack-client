def getCardSumValue(cardIndex):
    # figure Cards are worth 10
    if cardIndex in range(10, 13):
        return 10
    else:
        return cardIndex + 1

def containsAce(cardsIndexes):
    return 0 in cardsIndexes

def sumCards(cards):
    cardValues = [getCardSumValue(card['number']) for card in cards]
    simpleSum = sum(cardValues)
    hasAce = containsAce([card['number'] for card in cards])
    # will use ace as 11 only if has ace and if sum does not exceed 21
    usableAce = hasAce and (simpleSum + 10) <= 21
    if usableAce:
        return simpleSum + 10
    else:
        return simpleSum
    
def cardDisplay(card):
    return str(getCardSymbol(card['number'])) + card['suit'] 

def getCardSymbol(cardIndex):
    if cardIndex == 0:
        return 'A'
    elif cardIndex == 10:
        return 'J'
    elif cardIndex == 11:
        return 'Q'
    elif cardIndex == 12:
        return 'K'
    else:
        return str(cardIndex + 1)

def findPlayer(playersList, playerName):
    for player in playersList:
        if player['name'] == playerName:
            return player

def dealerCards(dealer):
    dealerCards = [dealer['shown']]
    if ('hidden' in dealer):
        dealerCards.append(dealer['hidden'])
    return dealerCards

def printMyCards(cards):
    print("These are my cards:")
    printCards(cards)

def printDealerShownCard(dealer):
    print('Dealer has: ' + cardDisplay(dealer['shown']))

def printFullDealer(dealer):
    dealerCards = [dealer['shown'], dealer['hidden']]
    print('Dealer cards: ')
    printCards(dealerCards)

def printCards(cards):
    cardSum = sumCards(cards)
    cardsDisplay = ''
    for card in cards:
        cardsDisplay += cardDisplay(card) + ","
    print(cardsDisplay + " that gives a total of " + str(cardSum))