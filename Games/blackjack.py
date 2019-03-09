from deck import ../Deck
from card import ../Card


class BJHand:
    def __init__(self):
        self.reset()

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
            if c.value <= 10:
                val += c.value
            else:
                val += 10
            if c.value == 1:
                self.handValue.append(val + 11)
        self.numOfCards += 1
    
    '''
    * Set the player's best score, 
    * and pull him out of the dealing process
    '''
    def stay(self):
        self.stillIn = False
        best = 0
        for v in self.handValues:
            if v >= best:
                best = v
        self.handValues = best

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
        if len(self.handValue) <= 0:
            return True
        return False 
    
    

class BJPlayer:
    def __init__(self):
        self.money = 100
        self.hand = BJHand()

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
        return True

