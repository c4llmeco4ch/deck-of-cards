from deck import Deck
import unittest


class TestDealCardsFromDeck(unittest.TestCase):

    def test_NoShuffleDeal(self):
        d = Deck()
        answer = d.dealCard()
        self.assertEqual(answer.value, 1)
        self.assertEqual(answer.suit, "H")
        self.assertFalse(d.isEmpty)
        self.assertEqual(d.size, 51)

    def test_LastCard(self):
        d = Deck()
        for i in range(len(d.deck) - 1):
            d.dealCard()
        self.assertFalse(d.isEmpty)
        d.dealCard()
        self.assertTrue(d.isEmpty)
        self.assertIsNone(d.dealCard())

    def test_ShuffleMaintainsSize(self):
        d = Deck()
        d.shuffle()
        self.assertEqual(d.size, 52)
