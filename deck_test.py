from card import Card
from deck import Deck
import random
import unittest

class TestDealCardsFromDeck(unittest.TestCase):

    def testNoShuffleDeal(self):
        d = Deck()
        answer = d.dealCard()
        self.assertEqual(answer.value, 1)
        self.assertEqual(answer.suit, "H")
        self.assertFalse(d.isEmpty)
        self.assertEqual(d.size, 51)

    def testLastCard(self):
        d = Deck()
        for i in range(len(d.deck) - 1):
            d.dealCard()
        self.assertFalse(d.isEmpty)
        d.dealCard()
        self.assertTrue(d.isEmpty)
        self.assertIsNone(d.dealCard())

    def testShuffleMaintainsSize(self):
        d = Deck()
        d.shuffle()
        self.assertEqual(d.size, 52)