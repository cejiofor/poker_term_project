#poker.py
#poker.py
#Main file for Poker game

##Written By Christopher Ejiofor
##Written for Prinicple of Computing, 15-110 at Carnegie Mellon University
##Written under Professor David Kosbie and Mentor CA Kiraz Baysal

from Tkinter import *
import random
import handEval
import pokerAI
import tkSimpleDialog
import tkMessageBox

def mousePressed(event):
    #calls the replace card funtion to turn a click
    #into a card selection
    replaceCard(event.x, event.y)

def keyPressed(event):
    #Space bar to start the game
    if event.keysym == 'space' and canvas.data.screen==1:
        canvas.data.screen =2
        playDrawPoker()
    #r to resstart the game when the game is over with your current money amount
    elif event.keysym == 'r' and canvas.data.gameOver == True:
        canvas.data.roundCount = 1
        canvas.data.deck = getRandomDeck()
        canvas.data.player1 = getPlayerHand()
        canvas.data.player2 = getPlayerHand()
        canvas.data.player3 = getPlayerHand()
        canvas.data.gameOver = False
        canvas.data.bet = 0
        redrawAll()
        playDrawPoker()
        
           
def button1Pressed():
    canvas.data.screen=1
    redrawAll()
     
def button2Pressed():
    drawRules()
    
def button3Pressed():
    #destroys the button to end the wait_window() for clicking
    canvas.data.button3.destroy()

def getRandomDeck():
    ### getRandomDeck adatped from hw3, BlackJack problem ###
    ### returns a random deck list with card in the '2C' fortmat
    import time 
    prime1 = 583621
    prime2 = 329717
    prime3 = 611953
    seed = int(100*time.time()) % prime3
    deck = range(52)
    for i in range(52):
        seed = (((seed * prime1) + (seed * seed * prime2)) % prime3)
        j = i + (seed % (52 - i))
        temp = deck[j]
        deck[j] = deck[i]
        deck[i] = temp
    result = []
    #changed the for loop to make the deck a list
    for i in range(52):
        result += ["23456789TJQKA"[deck[i]%13] + "CDHS"[deck[i]/13]]
    return result


def getPlayerHand():
    # Gives a player a hand with 5 cards removed from the deck
    handLength = 5
    playerHand = [""]*handLength
    for card in xrange(handLength):
        playerHand[card] = canvas.data.deck[card]
        canvas.data.deck.remove(canvas.data.deck[card])
    return playerHand

def timerFired():
    redrawAll()

def redrawAll():
    canvas.delete(ALL)
    if(canvas.data.screen >= 1):
        # Draws the main game if screen is 1 or above
        drawBoard()
        drawPlayer1(canvas.data.player1)
        drawPlayer2(canvas.data.player2)
        drawPlayer3(canvas.data.player3)
    if canvas.data.screen==0:
        #draws the welcome screen
        drawWelcome()

def drawWelcome():
    #Draws the welmoce splash screen
    nameX = 900
    nameY = 650
    imageX = 300
    imageY = canvas.data.canvasHeight/2
    welcomeX = canvas.data.canvasWidth/2
    welcomeY = imageX/2
    canvas.data.image = PhotoImage(file='deck.gif')
    image = canvas.data.image
    name = "Christopher Ejiofor\n15-110 Spring 2011\nTerm Project"
    canvas.create_rectangle(0, 0, canvas.data.canvasWidth,
                            canvas.data.canvasHeight, fill="forest green")
    canvas.create_window(imageX, imageY, window=canvas.data.button1)
    canvas.create_window(canvas.data.canvasHeight,
                         imageY, window=canvas.data.button2)
    
    canvas.create_text(welcomeX, welcomeY, text="Welcome to Poker",anchor=N,
                       fill='dark red', font='ComicSans 42 bold underline')
    canvas.create_image(welcomeX,imageY,image= image)
    canvas.create_text(nameX, nameY, text=name ,
                       fill='dark red', font='ComicSans 14')
    

def drawRules():
    #draws the screen with the rules of the game
    canvas.delete(ALL)
    position = 150
    position2 = 620
    directions = "\t1. Press the Space Bar to Begin.\n\
                  2. After you press the space, you Give $5 to play\n\
                  3. Each is player dealt five cards, but you can\n\
                      only see your own cards\n\
                  4. Player 1 Bets an you then must match the bet,\n\
                      bet higher, or fold\n\
                  5. If you  didn't fold, you can trade-in \n\
                      cards for a better hand\n\
                  6. Click on the cards you want to trade, then click\n\
                      'Done Selecting'\n\
                  7. If you want to keep you hand, simply press the\n\
                      button as soon as it appears\n\
                  8. Another round of betting starts and repeats steps\n\
                      4-8 for a total of 3 rounds of betting\n\
                  7. At the end or the game,  the player with the\n\
                      highest hand wins the money in the pot\n\
                  8. See the chart to the right for winning hands\n\
                  9. at the end, if you would like to continue playing,\n\
                      press r for restart\n\
                  10. Click the button below to begin and enjoy!"
    
    image = PhotoImage(file="pokerHands.gif")
    canvas.data.image = image
    imageX= image.width()
    canvas.create_rectangle(0, 0, canvas.data.canvasWidth,
                            canvas.data.canvasHeight, fill="forest green")
    canvas.create_image(canvas.data.canvasWidth-imageX,
                        canvas.data.canvasHeight/2,anchor = W,
                        image=canvas.data.image)
    canvas.create_text(0, position, anchor=NW, text=directions,
                       font='ComicSans 14 bold')
    canvas.create_text(position2/3, position/3, anchor=NW, text="Playing Poker",
                       fill='white', font='ComicSans 24 bold underline')
    canvas.create_window(2*position, position2, window=canvas.data.button1)
    
    
    
def drawBoard():
    canvas.create_rectangle(0, 0, canvas.data.canvasWidth,
                            canvas.data.canvasHeight, fill="forest green")
    #Dealers corner
    majorAxis = 350
    minorAxis = 300
    dealPos = 15
    four = 4
    three = 3
    canvas.create_oval(canvas.data.canvasWidth/2-2*majorAxis/three,-minorAxis/2,
                       canvas.data.canvasWidth/2+2*majorAxis/three,minorAxis/2,
                       fill ='black')
    canvas.create_text(canvas.data.canvasWidth/2-dealPos,dealPos,
                       text="Betting Round: "+ str(canvas.data.roundCount),
                       fill="white", anchor=E, font= "ComicSans 14 bold")
    canvas.create_text(canvas.data.canvasWidth/2 +dealPos,dealPos,
                       text="Player Turn: "+ str(canvas.data.playerTurn),
                       fill="white", anchor=W, font= "ComicSans 14 bold")
    canvas.create_image(canvas.data.canvasWidth/2, minorAxis/four,
                        image=canvas.data.deckImage)
    
    drawBox()
    #moneyPot
    canvas.create_oval(canvas.data.canvasWidth/2 - majorAxis/2,
                       canvas.data.canvasHeight/2-minorAxis/three-dealPos,
                       canvas.data.canvasWidth/2 + majorAxis/2,
                       canvas.data.canvasHeight/2+minorAxis/three-dealPos,
                       fill ='black')
    canvas.create_text(canvas.data.canvasWidth/2,
                       canvas.data.canvasHeight/2-dealPos,
                       text=str(canvas.data.moneyPot), fill="white",
                       font= "ComicSans 28 bold")
    
    
def drawBox():
    #Box for directions for each player
    majorAxis = 350
    minorAxis = 300
    buttonX = 500
    buttonY = 550
    maxRound = 4
    three = 3
    dealPos = 15
    canvas.create_rectangle(canvas.data.canvasWidth/2 - canvas.data.handLen/2,
                            canvas.data.canvasHeight/2+ minorAxis/three+dealPos,
                            canvas.data.canvasWidth/2 + canvas.data.handLen/2,
                            canvas.data.canvasHeight-majorAxis/three-dealPos,
                            fill="white")
    canvas.create_text(canvas.data.canvasWidth/2 -canvas.data.handLen/2+dealPos,
                       canvas.data.canvasHeight/2+ minorAxis/three+dealPos,
                       text=canvas.data.playerDialog, anchor=NW,
                       font="ComicSans 14 bold")
    b3 = Button(canvas, text="Done Selecting", command=button3Pressed)
    canvas.data.button3 = b3
    if canvas.data.roundCount<maxRound and canvas.data.isClicking==True:
        canvas.create_window(buttonX, buttonY, window = canvas.data.button3)
    
def drawPlayer1(player):
    #draw cards for the computer player 1 on the lefthand side of the screen
    boxSize = 110
    handX = 100
    cashX = 50 
    cashY = 650
    six = 6
    imageX = 20
    cardLen = canvas.data.cardLen
    canvasHeight = canvas.data.canvasHeight
    maxRound = 4
    canvas.create_rectangle(0, handX, boxSize, handX*six, fill="black")
    if canvas.data.roundCount == maxRound:
        for card in range(len(player)):
            canvas.data.cardPhotos1[card] = PhotoImage(file=player[card]+".gif")
            canvas.create_image(imageX,canvasHeight/six+cardLen*card,
                                anchor=NW, image=canvas.data.cardPhotos1[card])
    else:
        for card in range(len(player)):
            canvas.create_image(imageX, canvasHeight/six + cardLen*card,
                                anchor=NW, image=canvas.data.deckImage)
    canvas.create_text(cashX, cashY, text='$'+str(canvas.data.player1Cash),
                       fill='green', font="ComicSans 18 bold")

        
def drawPlayer2(player):
    #draws cards for player 2, the user, at the bottom of the screeen
    majorAxis = 350
    minorAxis = 300
    dealPos = 15
    cashX = 755
    cashY = 650
    three = 3
    canvas.create_rectangle(canvas.data.canvasWidth/2 - canvas.data.handLen/2,
                            canvas.data.canvasHeight - canvas.data.handWidth,
                            canvas.data.canvasWidth/2 + canvas.data.handLen/2,
                            canvas.data.canvasHeight, fill="black") 
    for card in range(len(player)):
        canvas.data.cardPhotos2[card] = PhotoImage(file=player[card]+".gif")
        canvas.create_image(canvas.data.canvasWidth/2 - canvas.data.handLen/2\
                            + canvas.data.cardWidth*card +dealPos,
                            canvas.data.canvasHeight-canvas.data.cardLen\
                            -dealPos/three, anchor=NW,
                            image=canvas.data.cardPhotos2[card])
    canvas.create_text(cashX, cashY, text='$'+str(canvas.data.player2Cash),
                       fill='green', font="ComicSans 18 bold")

        
def drawPlayer3(player):
    #Draws Cards for teh computer player 3 on teh righthand side of the screen
    major = 940
    minor = 300
    handX = 890
    handY = 100
    handX2 = 1000
    six = 6
    three = 3
    maxRound = 4
    imageX = 25
    handWidth = canvas.data.handWidth
    height = canvas.data.canvasHeight
    canvas.create_rectangle(handX,minor/three,handX2,minor*2,fill="black")
    if canvas.data.roundCount == maxRound:
        for card in range(len(player)):
            canvas.data.cardPhotos3[card] = PhotoImage(file=player[card]+".gif")
            canvas.create_image(canvas.data.canvasWidth-handWidth+imageX,
                                height/six+canvas.data.cardLen*card,
                                anchor=NW, image=canvas.data.cardPhotos3[card])
    else:
        for card in range(len(player)):
            canvas.create_image(canvas.data.canvasWidth-handWidth+imageX,
                                height/six + canvas.data.cardLen*card,
                                anchor=NW, image=canvas.data.deckImage)
    canvas.create_text(major, minor/six,
                       text='$'+str(canvas.data.player3Cash),
                       fill='green', font="ComicSans 18 bold")

def replaceCard(x, y):
    # Takes and x and y value location on the canvas
    # and detmines if there is a card at this location. If so, it adds that card
    # to the list of idecies that will be chaged for the player
    cardWidth = 72
    handStart = 300
    cardMargin = 80
    minY =600
    count = 0
    if y>minY and canvas.data.isClicking == True:
        for i in range(5):
            if handStart+cardMargin*i< x< handStart+cardWidth+cardMargin*i:
                canvas.data.removeCard += [i]
    for index in range(5):
        for card in range(len(canvas.data.removeCard)):
            if canvas.data.removeCard[card] == index:
                canvas.data.giveUp[index] = canvas.data.removeCard.count(index)
    
            
def playDrawPoker():
    #Larger Function that initiates the game of Poker
    ante = 5
    canvas.data.player1Cash -= ante
    canvas.data.player2Cash -= ante
    canvas.data.player3Cash -= ante
    canvas.data.moneyPot += ante*3
    redrawAll()
    maxRound = 4
    #repeats rounds for 3 turns
    while canvas.data.bet >= 0 and canvas.data.roundCount < maxRound:
        canvas.data.playerTurn = 1
        playAutoPlayer(canvas.data.player1, canvas.data.player1Cash)
        if (canvas.data.screen == 0):
            return #out of the loop if user cancels the game
        canvas.data.playerTurn = 2
        playPokerRound(canvas.data.player2, canvas.data.player2Cash)
        if (canvas.data.screen == 0):
            return
        canvas.data.playerTurn += 1 
        playAutoPlayer(canvas.data.player3, canvas.data.player3Cash)
        if (canvas.data.screen == 0):
            return
        canvas.data.roundCount += 1
    winPoker()
    canvas.data.gameOver = True
    
def winPoker():
    #Funtion that determines the winner of poker
    winPlay = [canvas.data.player1, canvas.data.player2, canvas.data.player3]
    winners = ['Player 1', 'Player 2', 'Player 3']
    maxPlayer = 0
    lastDialog4= "Winner is "+winners[maxPlayer]
    for player in range(len(winPlay)):
        playRank = handEval.handRank(winPlay[player]) 
        if playRank > handEval.handRank(winPlay[maxPlayer]):
            maxPlayer = player
            lastDialog4= "Winner is "+winners[maxPlayer]
        elif playRank == handEval.handRank(winPlay[maxPlayer]) and player !=0:
            print player, maxPlayer
            if breakTie(winPlay[maxPlayer],winPlay[player])==False:
                maxPlayer = player
                lastDialog4= "Winner is "+winners[player]
            else:
                lastDialog4= "Winner is "+winners[maxPlayer]  
    lastDialog = "Player 1, Your Hand is a: "+\
                 canvas.data.handType[handEval.handRank(canvas.data.player1)]
    lastDialog2= "Player 2, Your Hand is a: "+\
                 canvas.data.handType[handEval.handRank(canvas.data.player2)]
    lastDialog3= "Player 3, Your Hand is a: "+\
                 canvas.data.handType[handEval.handRank(canvas.data.player3)]
    canvas.data.playerDialog =lastDialog+'\n'+lastDialog2\
                               +'\n'+lastDialog3+'\n'+lastDialog4
    winningReward(winPlay, maxPlayer)
    redrawAll()

def breakTie(hand1, hand2):
    #Breaks a tie between two hands
    maxCards = [handEval.highCard(hand1), handEval.highCard(hand2)]
    highCard = handEval.highCard(maxCards)
    if highCard == handEval.highCard(hand1):
        return True
    else:
        return False

def winningReward(win, player):
    #Distributes the moneyPot funds to the winner accordingly
    reward = canvas.data.moneyPot
    canvas.data.moneyPot -= reward
    if win[player] == canvas.data.player1:
        canvas.data.player1Cash += reward
    elif win[player] == canvas.data.player2:
        canvas.data.player2Cash += reward
    elif win[player] == canvas.data.player3:
        canvas.data.player3Cash += reward
        
    
def getBet(player):
    #Function gets the bet for the user, or allows the user fold
    if not canvas.data.doGetBet:
        return False
    betString = ""
    message = "How Much will you Bet? (enter 0 to fold)?"
    title = "Place Your Bet"
    newBet = tkSimpleDialog.askstring(title, message)
    if newBet != None:
        while newBet == '' or newBet == None:
            betString = "Bet must bet at least " +str(canvas.data.bet)
            newBet = tkSimpleDialog.askstring(title, betString)
        if newBet == '0':
            player[0] = 'fold'
            canvas.data.isBet = True 
            return True
        else: 
            for i in range(len(newBet)):
                while (newBet[0] not in "0123456789") or\
                      (int(newBet) < canvas.data.bet):
                    betString = "Bet must bet at least " +str(canvas.data.bet)
                    newBet = tkSimpleDialog.askstring(title, betString) 
            canvas.data.bet = int(newBet)
        canvas.data.isBet = True
        return True
    return False

def playPokerRound(player, cash):
    #plays one round of poker with a given player and cash amount
    #as long as the player hasn't folded
    if player[0] != 'fold':
        canvas.data.isBet = False
        canvas.data.doGetBet = True
        fullText = "Player "+str(canvas.data.playerTurn)+'\n'
        canvas.data.playerDialog = fullText+"Place Your Bet"    
        redrawAll()
        canvas.data.giveUp = [0]*len(canvas.data.giveUp)
        canvas.data.removeCard = []
        turn = canvas.data.playerTurn
        #Enters the loop if user clicks cancel
        while canvas.data.doGetBet and not getBet(player) :
            message = "This will stop your game, are you sure?"
            title = "No Bet Input"
            if (tkMessageBox.askyesno(title, message)):
                canvas.data.doGetBet = False
                init()
                redrawAll()
                break
        if(canvas.data.isBet) and player[0] != 'fold':
            canvas.data.player2Cash -= canvas.data.bet
            canvas.data.moneyPot += canvas.data.bet
            redrawAll()
            lastTrade = 3
            if canvas.data.roundCount < lastTrade:
                canvas.data.playerDialog = fullText+\
                                           "Select The Cards You Wish to Trade"
                canvas.data.isClicking = True
                redrawAll()
                canvas.data.button3.wait_window()
                cardsGivenUp(player)
            redrawAll()

def cardsGivenUp(player):
    #determins what cards are given up, reomves them
    #adds the to the end of the deck and retireves an approporiate number
    #of new cards from the deck
    for i in range(len(canvas.data.giveUp)):
        if canvas.data.giveUp[i] > 0:
            canvas.data.deck.append(player[i])
            player.remove(player[i])
            player.insert(i, canvas.data.deck[0])
            canvas.data.deck.pop(0)
    canvas.data.isClicking = False
    
def playAutoPlayer(player, playerCash):
    #Plays a round for the comuter with a giver player and cash amount
    newBet = canvas.data.bet
    if canvas.data.roundCount ==1:
        newBet = 10 #Bets $10 the first round
    if canvas.data.playerTurn == 1:    
        cash = canvas.data.player1Cash
    else:
        cash = canvas.data.player3Cash
    trips = 4
    lastTrade = 3
    if handEval.handRank(player) > trips:
        #calls topHand if th hand held is a straight or better
        autoTopHands(player,cash)
        button3Pressed()
    else:
        canvas.data.bet = newBet
        canvas.data.moneyPot += canvas.data.bet
        cash -= canvas.data.bet
        if canvas.data.playerTurn == 1:    
            canvas.data.player1Cash=cash
        else:
            canvas.data.player3Cash=cash
        sortedHand = pokerAI.sortHand(player)
        handCombos = []
        #uses previous unrelated variable names to get lengths of 4,3
        pokerAI.combinations(sortedHand, trips, handCombos)  
        pokerAI.combinations(sortedHand, lastTrade, handCombos)
        pokerAI.combinations(sortedHand, 2, handCombos)
        options = pokerAI.handOptionList(handCombos)
        giveUp = pokerAI.giveUpData(options, player)
        canvas.data.giveUp = giveUp
        if canvas.data.bet > 0 and canvas.data.roundCount < lastTrade:
            canvas.data.isClicking = True
            redrawAll()
            cardsGivenUp(player)
        
def autoTopHands(player, cash):
    #If a hand is so high, the computer keeps the hand and bets
    #According to how hight his hand is
    newBet = canvas.data.bet
    SF = 9
    Quad = 8
    FH = 7
    Flush = 6
    Strait = 5
    if canvas.data.roundCount ==1:
        newBet = 10
    if handEval.handRank(player) >= SF:
        canvas.data.bet = cash
        canvas.data.moneyPot += canvas.data.bet
        cash -= canvas.data.bet
    elif handEval.handRank(player) == Quad or FH:
        canvas.data.bet = newBet+30
        canvas.data.moneyPot += canvas.data.bet
        cash -= canvas.data.bet
    elif handEval.handRank(player) == Flush:
        canvas.data.bet = newBet+10
        canvas.data.moneyPot += canvas.data.bet
        cash -= canvas.data.bet
    elif handEval.handRank(player) == Strait:
        canvas.data.bet = newBet
        canvas.data.moneyPot += canvas.data.bet
        cash -= canvas.data.bet
    if canvas.data.playerTurn == 1:    
        cash = canvas.data.player1Cash
    else:
        cash = canvas.data.player3Cash
    
    
    
def init():
    b1 = Button(canvas, text="Play the Game", command=button1Pressed)
    canvas.data.button1 = b1
    b2 = Button(canvas, text="Learn the Rules", command=button2Pressed)
    canvas.data.button2 = b2
    b3 = Button(canvas, text="Done Selecting", command=button3Pressed)
    canvas.data.button3 = b3
    canvas.data.playerDialog = "Press the Space bar to Start"
    canvas.data.playerTurn = 1
    canvas.data.deckImage = PhotoImage(file="deckImage.gif")
    canvas.data.handLen = 425
    canvas.data.handWidth = 115
    canvas.data.cardWidth = 80
    canvas.data.cardLen = 96
    canvas.data.deck = getRandomDeck()
    canvas.data.player1 = getPlayerHand()
    canvas.data.player2 = getPlayerHand()
    canvas.data.player3 = getPlayerHand()
    canvas.data.player1Cash = 500
    canvas.data.player2Cash = 500
    canvas.data.player3Cash = 500
    canvas.data.moneyPot = 0
    canvas.data.roundCount = 1
    canvas.data.bet = 0
    canvas.data.handType = ['Fold','High Card','Pair','Two Pair',
                            'Three of a Kind','Straight', 'Flush','Full House',
                            'Four of a Kind','Straight Flush', 'Royal Flush']
    canvas.data.cardPhotos1 = [PhotoImage(file="AC.gif")]*5
    canvas.data.cardPhotos2 = [PhotoImage(file="AC.gif")]*5
    canvas.data.cardPhotos3 = [PhotoImage(file="AC.gif")]*5
    canvas.data.image = PhotoImage(file="pokerHands.gif")
    canvas.data.screen = 0
    canvas.data.giveUp = [0]*5
    canvas.data.removeCard = []
    canvas.data.isClicking = False
    canvas.data.gameOver = False
    
    

########### copy-paste below here ###########

def run():
    # create the root and the canvas
    global canvas
    root = Tk()
    canvasWidth = 1000            
    canvasHeight = 700
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
    canvas.pack()
    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.canvasWidth = canvasWidth
    canvas.data.canvasHeight = canvasHeight
    init()
    # set up events
    root.bind("<Button-1>", mousePressed)
    root.bind("<Key>", keyPressed)
    timerFired()
    # and launch the app
    root.mainloop()  

run()
