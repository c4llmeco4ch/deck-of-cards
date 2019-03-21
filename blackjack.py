from deck import Deck
from card import Card


class BJHand:
    def __init__(self):
        self.reset()
        self.busted = False

    '''
    * @param c: The Card being added to the hand
    * First, tack the card on the hand list
    * Then, update all current hand values
    * Also, if the card is an ace,
    * Add a new value where the ace is treated as an 11
    '''
    def addCard(self, c):
        self.hand.append(c)
        size = len(self.handValue)
        for pos in range(size):
            if c.value == 1: #deal with Aces counting as 11 first
                self.handValue.append(self.handValue[pos] + 11)
            if c.value <= 10:
                self.handValue[pos] += c.value
            else:
                self.handValue[pos] += 10
        self.numOfCards += 1
    
    '''
    * Set the player's best score, 
    * and pull him out of the dealing process
    '''
    def stand(self):
        best = 0
        for v in self.handValue:
            if v >= best:
                best = v
        del(v)
        self.handValue = best

    #Return a hand to its default state
    def reset(self):
        self.hand = []
        self.handValue = [0]
        self.numOfCards = 0
        self.stillIn = True

    '''
    * Iterate through each possible hand value in the player's hand
    * If a particular value is greater than 21, 
    * remove it from the list
    '''
    def areBusted(self):
        for val in self.handValue:
            if val > 21:
                self.handValue.remove(val)
        del(val)
        if len(self.handValue) <= 0:
            return True
        return False 

    def toString(self):
        currentHand = "| "
        for c in self.hand:
            currentHand += c.toString() + ", "
        currentHand = currentHand[:len(currentHand) - 2] + "|" 
        return currentHand
    
    '''
    * @param altHand: The other player's hand we are comparing 'self' to
    * @return 1: If self's value > altHand's value
    * @return 0: If self's value == altHand's value
    * @return -1: If self's value < altHand's value
    '''
    def compareTo(self, altHand):
        if self.handValue > altHand.handValue:
            return 1
        elif self.handValue == altHand.handValue:
            return 0
        else:
            return -1
    

class BJPlayer:
    def __init__(self, name):
        self.money = 100
        self.hand = BJHand()
        self.name = name
        self.bet = 0

    '''
    * @param m: The amount of money a player is betting on his hand
    * If the player cannot pay 'm' dollars, return false to show this inability
    * Otherwise, subtract that amount of money from the player's account
    '''
    def placeBet(self, m):
        if self.m > self.money:
            return False
        else:
            self.money -= m
            self.bet = m
    
    '''
    * @param m: The amount of money a player wins from a particular hand
    * Player 'self' adds 'm' money to his account
    '''
    def receiveWinnings(self, m):
        self.money += m
    
    #Player is dealt a card and adds it to his hand
    def dealCard(self, c):
        self.hand.addCard(c)
    
class Dealer:
    def __init__(self):
        self.hand = BJHand()

    '''
    * If a hand has a value that leaves it between 17 and 21
    * The dealer must stay
    * Otherwise, the dealer must hit
    '''    
    def decideToHit(self):
        for val in self.hand.handValue:
            if val >= 17 and val <= 21:
                return False
        del(val)
        return True

playerNumber = -1
playerList = []
dealer = Dealer()

def startGame():
    playerNumber = -1
    while playerNumber <= 0:
        playerNumber = (int)(input("How many players would like a chair at the table?"+
                                    "\nMax 5 "))
    for i in range(playerNumber):
        pName = input("Player " + (str)(i + 1) + ", choose a name: ")
        print(pName + " is your name")
        playerList.append(BJPlayer(pName))
    del(i)

def dealHands(deck):
    for round in range(2):
        for player in playerList:
            player.dealCard(deck.dealCard())
        dealer.hand.addCard(deck.dealCard())
    dealer.hand.hand[1].flip()
    del(round, player)

def playerLoop(player):
    while player.hand.stillIn:
        if len(player.hand.handValue) == 2 and player.hand.handValue[1] == 21:
            print("Blackjack! You win!")
            return
        isValid = False
        print("Dealer is showing " + dealer.hand.hand[0].toString())
        while not isValid:
            print(player.name + ": Your Hand is " + player.hand.toString())
            decision = input("Would you like to hit (\'h\') or stand (\'s\')? ")
            if decision == "h":
                player.dealCard(deck.dealCard())
                if player.hand.areBusted():
                    player.hand.stillIn = False
                    return
                isValid = True
            elif decision == "s":
                player.hand.stand()
                return
            else:
                print("Excuse me, sir. This is not a valid move. Try again.")

def dealerLoop():
    print("Dealer is showing " + dealer.hand.hand[0].toString())
    dealer.hand.hand[1].flip()
    print("Dealer reveals his face-down card: " + dealer.hand.hand[1].toString())
    if len(dealer.hand.handValue) == 2 and dealer.hand.handValue[1] == 21:
        print("Dealer has blackjack!")
        return -1
    playing = True
    while playing:
        playing = dealer.decideToHit()
        if playing:
            dealer.hand.addCard(deck.dealCard())
            print("Dealer now has " + dealer.hand.toString())
            if dealer.hand.areBusted():
                print("Dealer busted!")
                return 0
    dealer.hand.stand()
    print("Dealer stands at " + dealer.hand.handValue)
    return dealer.hand.handValue


   
deck = Deck()
deck.shuffle()
startGame()
dealHands(deck)
for player in playerList:
    playerLoop(player)
dealerStatus = dealerLoop()
if dealerStatus == 0:
    #All players who are still in win
    for player in playerList:
        if player.hand.stillIn:
            player.receiveWinnings(player.bet * 2)
            print(player.name + " wins!")
    del(player)
elif dealerStatus == -1:
    #Dealer hit blackjack, all players lose except those with BJ
    for player in playerList:
        if player.hand.stillIn:
            print("Sorry, " + player.name + ": dealer's blackjack means you lose.")
    del(player)
else:
    #Calculate who wins between dealers and players that are still in
    for playing in playerList:
        if player.hand.stillIn:
            winner = player.hand.compareTo(dealer.hand)
            if winner == 1:
                player.receiveWinnings(player.bet * 2)
                print("Congrats, " + player.name + ", you win $" + (str)(player.bet * 2))
            elif winner == 0:
                player.receiveWinnings(player.bet)
                print(player.name + ": You pushed and have received your bet back.")
            

