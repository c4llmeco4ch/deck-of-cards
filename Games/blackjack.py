from deck import ../Deck
from card import ../Card


class BJHand:
    def __init__(self):
        self.cardsInHand = []
        self.handValue = 0
        self.numOfCards = 0
        self.stillIn = False
    
    def addCard(self, c):
        self.cardsInHand.append(c)
        self.handValue += c.value
        self.numOfCards += 1
    
    def stay(self):
        self.stillIn = True

class BJPlayer:
    def __init__(self):
        self.money = 100
        self.hand = BJHand()
        
    def placeBet(self, m):
        if self.m > self.money:
            return False
        else:
            self.money -= m
    
    def receiveWinnings(self, m):
        self.money += m
    
    def dealtCard(self, c):
        self.hand.append(c)
    
    