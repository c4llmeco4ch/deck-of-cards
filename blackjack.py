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
        for val in self.handValue:
            if c.value == 1: #deal with Aces counting as 11 first
                self.handValue.append(val + 11)
            if c.value <= 10:
                val += c.value
            else:
                val += 10
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
        self.stillIn = False

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
    
    

class BJPlayer:
    def __init__(self, name):
        self.money = 100
        self.hand = BJHand()
        self.name = name

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

def startGame():
    dealer = Dealer()
    while playerNumber <= 0:
        playerNumber = (int)(prompt("How many players would like a chair at the table?"+
                                    "\nMax 5"))
    for i in range(playerNumber):
        name = prompt("Player " + (str)(i) + ": Choose a name.")
        playerList.append(BJPlayer(name))
    del(i)

def dealHands(deck):
    for round in range(2):
        for player in playerList:
            player.dealCard(deck.dealCard())
        dealer.dealCard(deck.dealCard())
    dealer.hand[1].flip()
    del(round, player)

def playerLoop(player, dealer):
    while player.stillIn:
        if player.hand.handValue[0] == 21:
            print("Blackjack! You win!")
            return
        isValid == False
        print("Dealer is showing " + dealer.hand.hand[0].printCard())
        while not isValid:
            print(player.name + ": Your Hand is " + player.hand.toString())
            decision = input("Would you like to hit (\'h\') or stand (\'s\')? ")
            if decision == "h":
                player.dealCard(deck.dealCard())
                if player.hand.areBusted():
                    player.stillIn = False
                    return
                isValid = True
            elif decision == "s":
                player.stand()
                return
            else:
                print("Excuse me, sir. This is not a valid move. Try again.")

def dealerLoop(dealer):
    print("Dealer is showing " + dealer.hand.hand[0].printCard())
    dealer.hand.hand[1].flip()
    print("Dealer reveals his face-down card: " + dealer.hand.hand[1].printCard())
    if dealer.hand.handValue[0] == 21:
        print("Dealer has blackjack!")
        return -1
    playing = True
    while playing:
        True


   
deck = Deck()
deck.shuffle()
startGame()
dealHands(deck)
for player in playerList:
    playerLoop(player, dealer)
dealerStatus = dealerLoop(dealer)