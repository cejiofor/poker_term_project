# pokerAI.py
# Methods for how the computer player should funtion witch given hand inputs

import handEval

def deleteIndex(player, combo):
    #Given a player's hand and a specfict combinatoin of a possible hand
    # creates a list of indices that are to be deleted from the hand
    giveUp = [0]*5
    for card in range(len(player)):
        if handEval.find(combo, player[card])== -1:
            giveUp[card] += 1
    return giveUp

def isAlmostStraight(firstHalf, secdHalf):
    #Determins if a hand is close to being striaght, but there is one card
    # missign in between to halfs of a hand that is added will make the hand
    # a striaght
    if handEval.isStraight(firstHalf) and handEval.isStraight(secdHalf) == True:
        faceCards = list("23456789TJQKA")
        faceInCards = handEval.find(faceCards, secdHalf[0][0])
        last = len(firstHalf)-1
        if firstHalf[last][0]!= faceCards[faceInCards-2]:
            return False
        return True

def combinations(iterable, r, combos):
    # A fucthion that when given and iterable(hand) creates a list of hand
    # combinations of length r in the list combos
    # Adapted form itertools.combinations found at
    # http://docs.python.org/library/itertools.html
    # Then edited inputs and return values to better fit purpose of pokerA!
    pool = list(iterable)
    n = len(pool)
    if r > n:
        return
    indices = range(r)
    combos += [list(pool[i] for i in indices)]
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        combos += [list(pool[i] for i in indices)]
        
def sortHand(hand):
    #Given a hand, returns the hand sorted by face value
    possibleFaces = '23456789TJQKA'
    faceCards = list(possibleFaces)
    sortHand = []
    for card in faceCards:
        for face in range(len(hand)):
            if hand[face][0] == card:
                sortHand +=[hand[face]]
    return sortHand
            
def handOptionList(handCombo):
    # Gives a list of Optional hands that tell 1. The possible handRank
    #that can be possible using the comboination from handCombo[i] with the
    #combination having a length of maxLength
    maxHand = 0
    maxLength = 0
    handOptions = []
    for i in range(len(handCombo)):
        tempPlay = handCombo[i]
        for index in range(1,len(tempPlay)):
            if isAlmostStraight(tempPlay[:index], tempPlay[index:]) == True:
                maxHand = min(handEval.handRank(tempPlay[:index]),handEval.handRank(tempPlay[index:]))
                maxLength = len(handCombo[i])
                handOptions +=[[maxHand, maxLength, handCombo[i]]]
            elif handEval.handRank(tempPlay) >= maxHand and len(handCombo[i]) > maxLength:
                maxHand = handEval.handRank(tempPlay)
                maxLength = len(handCombo[i])
                handOptions +=[[maxHand, maxLength, handCombo[i]]]
    return handOptions
 
def giveUpData(handOptions, player):
    #Parses over the options of possible hands and returns the
    #giveUp list of indexes that wouls give the best hand
    five = 5
    giveUp = [0]*five
    four = 4
    three= 3
    for i in range(len(handOptions)):
        combo = handOptions[i][2]
        maxCombo = handOptions[0][0]
        maxComboLen = len(combo)
        if handOptions[i][0] >= maxCombo and maxComboLen == four:
            giveUp = deleteIndex(player, combo)
        elif handOptions[i][0] >= maxCombo and maxComboLen == three:
            giveUp = deleteIndex(player, combo)
    return giveUp
