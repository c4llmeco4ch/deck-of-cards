from .card import Card
import random


class Deck:
    def __init__(self):
        self.deck = []
        self.size = 52
        self.isEmpty = False
        self.fill_deck()

    def fill_deck(self):
        """Fill the deck and place it in new deck order"""
        self.isEmpty = False
        self.size = 52
        suits = ["H", "C", "D", "S"]
        values = 13
        deck = []
        for s in suits:
            if s == "H" or s == "C":
                for v in range(1, values+1):
                    c = Card(v, s)
                    deck.append(c)
            else:
                for v in range(values, 0, -1):
                    c = Card(v, s)
                    deck.append(c)
        self.deck = deck

    def shuffle(self):
        """Shuffle the deck"""
        self.deck = self.randMerge(self.deck)

    def randMerge(self, d):
        """Perform merge sort,
        but randomly choose which elements are added,
        rather than adding in logical order
        """
        if len(d) <= 1:
            return d
        left = self.randMerge(d[:len(d)//2])
        right = self.randMerge(d[(len(d)//2):])
        mixedDeck = []
        while len(left) > 0 and len(right) > 0:
            which = random.randint(1, 3)
            if which == 1:
                mixedDeck.append(left.pop(0))
            else:
                mixedDeck.append(right.pop(0))
        if len(right) == 0:
            for c in left:
                mixedDeck.append(c)
        else:
            for c in right:
                mixedDeck.append(c)
        return mixedDeck

    # Print each card in an array-like format for readability
    def print_deck(self):
        """Print the deck in an easy-to-read format"""
        pDeck = "["
        for c in self.deck:
            pDeck += " ", c, " |"
            pDeck = pDeck[:len(pDeck) - 1] + "]"
        print(pDeck)

    def deal_card(self):
        """If the deck is not empty, remove the top card from the deck"""
        if not self.isEmpty:
            self.size -= 1
            if self.size == 0:
                self.isEmpty = True
            return self.deck.pop(0)
        else:
            print("No cards in the deck to deal")
            return None
