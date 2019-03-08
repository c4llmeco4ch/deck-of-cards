class Card:
  def __init__(self, value, suit):
    self.value = value
    self.suit = suit
    self.isHidden = False
  
  #Flip this card face-down hiding it from one or more players
  def faceDown(self):
    self.isHidden = True
  
  #Flip this card face up, revealing it to all players
  def faceUp(self):
    self.isHidden = False

  def printCard(self):
    card = self.toString()
    print(card)

  def toString(self):
    val = self.value
    if val == 1:
      val = "A"
    elif val == 11:
      val = "J"
    elif val == 12:
      val = "Q"
    elif val == 13:
      val = "K"
    else:
      val = (str)(val)
    return val + self.suit

  '''
  * @param c: The card we are comparing to 'self'
  * @return: 1 if self > c, -1 if c > self, 0 if self = c
  * Take 2 cards and evaluate which is a higher card
  '''
  def compareTo(self, c):
    if c.type != Card:
      raise ValueError("The passed object is not a card")
    elif c.getValue > self.getValue():
      return -1
    elif c.getValue < self.getValue():
      return 1
    else: 
      return 0
