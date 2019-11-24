class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.is_hidden = False

    def flip(self):
        """Flip this card face-down if face-up or face-up if face-down"""
        self.is_hidden = not self.is_hidden

    def print_card(self):
        """Print the card, or obscure it if face-down"""
        if self.is_hidden:
            print("??")
        else:
            print(self)

    def __repr__(self):
        """Convert the card object to a printable string"""
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
            val = str(val)
        return val + self.suit

    '''
    * @param c: The card we are comparing to 'self'
    * @return: 1 if self > c, -1 if c > self, 0 if self = c
    '''
    def compare_to(self, c):
        """Take 2 cards and evaluate which is a higher card"""
        if not isinstance(c, Card):
            raise ValueError("The passed object is not a card")
        elif c.value > self.value:
            return -1
        elif c.value < self.value:
            return 1
        else:
            return 0
