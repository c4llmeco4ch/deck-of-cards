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

class TestStanding(unittest.TestCase):

    def testDualAces(self):
        hand = BJHand()
        hand.addCard(Card(1, "S"))
        hand.addCard(Card(1, "H"))
        self.assertEqual(12, hand.stand(), "Two aces should equal 12, but don't")

    def testFourAces(self):
        hand = BJHand()
        hand.addCard(Card(1, "S"))
        hand.addCard(Card(1, "H"))
        hand.addCard(Card(1, "C"))
        hand.addCard(Card(1, "D"))
        self.assertEqual(14, hand.stand(), "Four aces should equal 14, but don't")

    def testAceAsEleven(self):
        hand = BJHand()
        hand.addCard(Card(1, "D"))
        hand.addCard(Card(2, "S"))
        hand.addCard(Card(3, "C"))
        self.assertEqual(16, hand.stand(), "5 + 11 <= 21, so Ace should count as 11")
    
    def testBlackJack(self):
        hand = BJHand()
        hand.addCard(Card(13, "H"))
        hand.addCard(Card(1, "D"))
        self.assertEqual(21, hand.stand(), "Blackjack returns 21")