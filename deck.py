from card import Card
import random

class Deck:
  DEBUG = False
  def __init__(self):
    self.deck = []
    self.size = 52
    self.isEmpty = False
    self.fillDeck()

  def __init__(self, size):
    self.deck = []
    self.size = size
    self.isEmpty = False
    self.fillDeck()
  
  '''
  * Start with a blank deck
  * Fill the deck and place it in new deck order
  '''
  def fillDeck(self):
    suits = ["H", "C", "D", "S"]
    values = 13
    deck = []
    for i in range(deck.size/52):
      for s in suits:
        if s == "H" or s == "C":
          for v in range(1, values+1):
            c = Card(v, s)
            deck.append(c)
        else:
          for v in range (values,0, -1):
            c = Card(v, s)
            deck.append(c)
    self.deck = deck
  #End fillDeck

  def shuffle(self):
    self.deck = self.randMerge(self.deck)
  
  '''
  * Much like a regular merge sort, 
  * break down the problem as much as possible using recursion.
  * On the way up, however, use random numbers to choose sorting,
  * rather than using compareTo() or similar
  '''
  def randMerge(self, d):
    if len(d) <= 1:
      return d
    left = self.randMerge(d[:len(d)//2])
    if self.DEBUG:
      print("Left")
      print(left)
    right = self.randMerge(d[(len(d)//2):])
    if self.DEBUG:
      print("Right")
      print(right)
    mixedDeck = []
    while len(left) > 0 and len(right) > 0:
      which = random.randint(1,3)
      if which == 1:
        mixedDeck.append(left.pop(0))
      else:
        mixedDeck.append(right.pop(0))
    if self.DEBUG:
      print("Halfway through, one stack left")
    if len(right) == 0:
      if self.DEBUG:
        print("Adding left stack")
      for c in left:
        mixedDeck.append(c)
    else:
      if self.DEBUG:
        print("Adding right stack")
      for c in right:
        mixedDeck.append(c)
    return mixedDeck
  
  #Print each card in an array-like format for readability
  def printDeck(self):
    pDeck = "["
    for c in self.deck:
      pDeck += " " + c.toString() + " |"
    pDeck = pDeck[:len(pDeck) - 1] + "]"
    print(pDeck)

  #If the deck is not empty, remove the top card from the deck
  def dealCard(self):
    if not self.isEmpty:
      return self.deck.pop(0)
      if len(deck) == 0:
        self.isEmpty = True
    else:
      print("No cards in the deck to deal")
      return None
