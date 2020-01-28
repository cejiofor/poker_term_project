#handEval.py
#Module written to assist in evaluating hands
#Final function gives a hand rank from 1-10, o for a folded hand

import random

def quadsTripsPairs(faces):
    #Returns the number of Four of a Kinds, Three of a Kinds and Pairs
    #in a given  hand in the form of a list
    numberPairs = 0
    numberTrips = 0
    numberQuads = 0
    alreadyCounted = []
    for face in range(len(faces)):
        if faces[face] not in alreadyCounted:
            count = faces.count(faces[face])
            if count == 4:
                numberQuads += 1
            elif count == 3:
                numberTrips += 1
            elif count == 2:
                numberPairs += 1
            alreadyCounted += [faces[face]]   
    return [numberQuads, numberTrips, numberPairs]

def find(sequence, key, startIndex=0):
    #Function copied from the findin elements section
    # in Lecture 4.1
    for i in range(startIndex, len(sequence)):
        if (sequence[i] == key):
            return i
    return -1
    
def isStraight(faces):
    #Determines of a list of faces is stiart by comaripng to a
    #List of posible faces in order
    possibleFaces = "23456789TJQKA"
    faceCards = list(possibleFaces)
    sortedFaces = []
    faceInCards = 0
    for card in faceCards:
        for face in range(len(faces)):
            if faces[face] == card:
                sortedFaces +=[card]
    for face in range(len(sortedFaces)-1):
        faceInCards = find(faceCards, sortedFaces[face])
        if sortedFaces[face] != 'A':
            if sortedFaces[face+1] != faceCards[faceInCards+1]:
                return False
    return True

    
def isRoyal(faces):
    #Determins if a hand is royal if all the faces in the hand are in the
    #possible Royal Faces
    royalFaces = "TJQKA"
    count = 0
    for char in royalFaces:
        if char in faces:
            count += 1
        else:
            count -= 1
    return count == len(faces)

def highCard(hand):
    #Determines of the high card of a hand by looking at the faces in the hand
    #and finding the one closest to the end of the possible faces in order
    possibleFaces = "23456789TJQKA"
    faceCards = list(possibleFaces)
    maxIndex = 0
    index = 0
    cardLocation = 0
    for card in range(len(hand)):
        index = find(faceCards, hand[card][0])
        if (index > maxIndex):
            maxIndex = index
            cardLocation = card
    return hand[cardLocation]
    
    
def isFlush(suits):
    #Deterinmnes if there is a flush by comparing every suit to teh first one
    # If they are all the same, returns True
    count = 0
    for suit in range(len(suits)):
        if suits[suit] != suits[0]:
            return False
    return True
            
def handRank(hand):
    listSuits = []
    listFaces = []
    RF = 10
    SF = 9
    Quad = 8
    FH = 7
    Flush = 6
    Strait = 5
    Trips = 4
    TwPr = 3
    for card in range(len(hand)):
        listSuits += [hand[card][1]]
        listFaces += [hand[card][0]]
    if listFaces[0] == 'f':
        return 0#Folded
    elif isStraight(listFaces) == True:
        if isFlush(listSuits) == True:
            if isRoyal(listFaces) == True:
                return RF#Royal Flush
            else:
                return SF#Straight Flush
        else:
            return Strait#Straight   
    elif  quadsTripsPairs(listFaces)[0] == 1:
        return Quad#Four of a Kind
    elif quadsTripsPairs(listFaces)[1] == 1:
        if quadsTripsPairs(listFaces)[2] == 1:
            return FH#Full House
        else:
            return Trips#Three of a Kind 
    elif isFlush(listSuits) == True:
        return Flush#Flush    
    elif quadsTripsPairs(listFaces)[2] == 2:
        return TwPr#Two Pairs
    elif quadsTripsPairs(listFaces)[2] == 1:
        return 2#Pair
    else:
        return 1# Nothing, use Highest card
