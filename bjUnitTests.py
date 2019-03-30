import unittest
from deck import Deck
from card import Card
from blackjack import *

class TestAreBusted(unittest.TestCase):

    def testThreeFace(self):
        hand = BJHand()
        hand.addCard(Card(11, "H"))
        hand.addCard(Card(12, "D"))
        hand.addCard(Card(13, "S"))
        self.assertTrue(hand.areBusted())

    def testThreeAce(self):
        hand = BJHand()
        hand.addCard(Card(1, "S"))
        hand.addCard(Card(1, "H"))
        hand.addCard(Card(1, "C"))
        self.assertFalse(hand.areBusted())