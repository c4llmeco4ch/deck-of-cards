import unittest
from deck import Deck
from card import Card
from blackjack import *

class TestAreBusted(unittest.TestCase):

    def test_ThreeFace(self):
        hand = BJHand()
        hand.addCard(Card(11, "H"))
        hand.addCard(Card(12, "D"))
        hand.addCard(Card(13, "S"))
        self.assertTrue(hand.areBusted())

    def test_ThreeAce(self):
        hand = BJHand()
        hand.addCard(Card(1, "S"))
        hand.addCard(Card(1, "H"))
        hand.addCard(Card(1, "C"))
        self.assertFalse(hand.areBusted())

    def test_NormalHand(self):
        hand = BJHand()
        hand.addCard(Card(4, "H"))
        hand.addCard(Card(5, "S"))
        hand.addCard(Card(6, "C"))
        self.assertFalse(hand.areBusted())

    def test_LongBustedHand(self):
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
    
    def test_LongSafeHand(self):
        hand = BJHand()
        hand.addCard(Card(2, "H"))
        hand.addCard(Card(2, "S"))
        hand.addCard(Card(7, "C"))
        hand.addCard(Card(1, "H"))
        hand.addCard(Card(1, "D"))
        hand.addCard(Card(5, "D"))
        hand.addCard(Card(3, "S"))
        self.assertFalse(hand.areBusted())

    def test_BlackJack(self):
        hand = BJHand()
        hand.addCard(Card(1, "S"))
        hand.addCard(Card(12, "H"))
        self.assertFalse(hand.areBusted())

class TestStanding(unittest.TestCase):

    def test_DualAces(self):
        hand = BJHand()
        hand.addCard(Card(1, "S"))
        hand.addCard(Card(1, "H"))
        hand.areBusted()
        hand.stand()
        self.assertEqual(12, hand.handValue, "Two aces should equal 12, but don't")

    def test_FourAces(self):
        hand = BJHand()
        hand.addCard(Card(1, "S"))
        hand.addCard(Card(1, "H"))
        hand.addCard(Card(1, "C"))
        hand.addCard(Card(1, "D"))
        hand.areBusted()
        hand.stand()
        self.assertEqual(14, hand.handValue, "Four aces should equal 14, but don't")

    def test_AceAsEleven(self):
        hand = BJHand()
        print("This hand has a value of: " + str(hand.handValue[0]))
        hand.addCard(Card(1, "D"))
        hand.addCard(Card(2, "S"))
        hand.addCard(Card(3, "C"))
        hand.areBusted()
        hand.stand()
        self.assertEqual(16, hand.handValue, "5 + 11 <= 21, so Ace should count as 11")
    
    def test_BlackJack(self):
        hand = BJHand()
        hand.addCard(Card(13, "H"))
        hand.addCard(Card(1, "D"))
        hand.areBusted()
        hand.stand()
        self.assertEqual(21, hand.handValue, "Blackjack returns 21")

class TestBets(unittest.TestCase):

    def test_NegativeBet(self):
        bjp = BJPlayer("Connor")
        self.assertFalse(bjp.placeBet(-5))

    def test_TooHighBet(self):
        bjp = BJPlayer("Me")
        self.assertFalse(bjp.placeBet(101))

    def test_ExactHighBet(self):
        bjp = BJPlayer("Me")
        self.assertTrue(bjp.placeBet(bjp.money))

class TestSplitting(unittest.TestCase):

    def test_CantSplit(self):
        oneHand = BJHand()
        self.assertFalse(oneHand.canSplit())
        oneHand.addCard(Card(5,"H"))
        oneHand.addCard(Card(10, "S"))
        self.assertFalse(oneHand.canSplit())
        twoHand = BJHand()
        twoHand.addCard(Card(3, "C"))
        twoHand.addCard(Card(3, "H"))
        twoHand.addCard(Card(3, "S"))
        self.assertFalse(oneHand.canSplit())
    
    def test_CanSplit(self):
        oneHand = BJHand()
        oneHand.addCard(Card(8, "C"))
        oneHand.addCard(Card(8, "H"))
        self.assertTrue(oneHand.canSplit())