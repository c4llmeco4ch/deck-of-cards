from .card import Card
import random


class Deck:
    def __init__(self):
        self.deck = []
        self.size = 52
        self.is_empty = False
        self.fill_deck()

    def fill_deck(self):
        """Fill the deck and place it in new deck order"""
        self.is_empty = False
        self.size = 52
        suits = ['H', 'C', 'D', 'S']
        values = 13
        deck = []
        for s in suits:
            if s == 'H' or s == 'C':
                for v in range(1, values+1):
                    c = Card(v, s)
                    deck.append(c)
            else:
                for v in range(values, 0, -1):
                    c = Card(v, s)
                    deck.append(c)
        self.deck = deck

    def shuffle(self):
        """Shuffle the deck 4 times"""
        for _ in range(4):
            self.deck = self.random_merge(self.deck)

    def random_merge(self, d):
        """Perform merge sort,
        but randomly choose which elements are added,
        rather than adding in logical order
        """
        if len(d) <= 1:
            return d
        left = self.random_merge(d[:len(d)//2])
        right = self.random_merge(d[(len(d)//2):])
        mixed_deck = []
        while len(left) > 0 and len(right) > 0:
            which = random.randint(1, 3)
            if which == 1:
                mixed_deck.append(left.pop(0))
            else:
                mixed_deck.append(right.pop(0))
        if len(right) == 0:
            for c in left:
                mixed_deck.append(c)
        else:
            for c in right:
                mixed_deck.append(c)
        return mixed_deck

    # Print each card in an array-like format for readability
    def print_deck(self):
        """Print the deck in an easy-to-read format"""
        pDeck = '['
        for c in self.deck:
            pDeck = ''.join([pDeck,' ', c.__repr__(), ' |'])
        pDeck = pDeck[:len(pDeck) - 1] + ']'
        print(pDeck)

    def deal_card(self):
        """If the deck is not empty, remove the top card from the deck"""
        if not self.is_empty:
            self.size -= 1
            if self.size == 0:
                self.is_empty = True
            return self.deck.pop(0)
        else:
            print('No cards in the deck to deal')
            return None
