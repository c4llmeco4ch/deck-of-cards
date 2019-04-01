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

    def testNormalHand(self):
        hand = BJHand()
        hand.addCard(Card(4, "H"))
        hand.addCard(Card(5, "S"))
        hand.addCard(Card(6, "C"))
        self.assertFalse(hand.areBusted())

    def testLongBustedHand(self):
        hand = BJHand()
        hand.addCard(Card(2, "H"))
        hand.addCard(Card(3, "S"))
        hand.addCard(Card(5, "C"))
        hand.addCard(Card(1, "H"))
        hand.addCard(Card(1, "D"))
        hand.addCard(Card(5, "D"))
        hand.addCard(Card(4, "S"))
        hand.addCard(Card(1, "S"))
        self.assertTrue(hand.areBusted())
    
    def testLongSafeHand(self):
        hand = BJHand()
        hand.addCard(Card(2, "H"))
        hand.addCard(Card(2, "S"))
        hand.addCard(Card(7, "C"))
        hand.addCard(Card(1, "H"))
        hand.addCard(Card(1, "D"))
        hand.addCard(Card(5, "D"))
        hand.addCard(Card(3, "S"))
        self.assertFalse(hand.areBusted())

    def testBlackJack(self):
        hand = BJHand()
        hand.addCard(Card(1, "S"))
        hand.addCard(Card(12, "H"))
        self.assertFalse(hand.areBusted())