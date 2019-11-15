import unittest
from card import Card
from blackjack import BJHand, BJPlayer


# TODO: Add tests for dealerloop, update compareTo tests
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
        self.assertEqual(12, hand.handValue, "Two aces should equal 12")

    def test_FourAces(self):
        hand = BJHand()
        hand.addCard(Card(1, "S"))
        hand.addCard(Card(1, "H"))
        hand.addCard(Card(1, "C"))
        hand.addCard(Card(1, "D"))
        hand.areBusted()
        hand.stand()
        self.assertEqual(14, hand.handValue, "Four aces should equal 14")

    def test_AceAsEleven(self):
        hand = BJHand()
        print("This hand has a value of: " + str(hand.handValue[0]))
        hand.addCard(Card(1, "D"))
        hand.addCard(Card(2, "S"))
        hand.addCard(Card(3, "C"))
        hand.areBusted()
        hand.stand()
        self.assertEqual(16, hand.handValue, "5 + 11 <= 21, Ace counts as 11")

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


class TestSplitAbility(unittest.TestCase):

    def test_CantSplit(self):
        oneHand = BJHand()
        self.assertFalse(oneHand.canSplit())
        oneHand.addCard(Card(5, "H"))
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


class TestHandComparisons(unittest.TestCase):
    def test_FaceCards(self):
        jack = Card(11, "H")
        queen = Card(12, "S")
        king = Card(13, "D")
        ten = Card(10, "C")

        hand1 = BJHand()
        hand1.addCard(jack)
        hand1.addCard(queen)
        hand1.stand()
        hand2 = BJHand()
        hand2.addCard(ten)
        hand2.addCard(Card(5, "C"))
        hand2.addCard(Card(2, "S"))
        hand2.addCard(Card(3, "D"))
        hand2.stand()
        self.assertTrue(hand1.compareTo(hand2) == 0)

        hand3 = BJHand()
        hand3.addCard(ten)
        hand3.addCard(king)
        hand3.stand()
        self.assertTrue(hand3.compareTo(hand2) == 0)

    def test_Aces(self):
        ace = Card(1, "S")
        hand1 = BJHand()
        for _ in range(3):
            hand1.addCard(ace)
        hand1.stand()
        hand2 = BJHand()
        hand2.addCard(Card(10, "C"))
        for _ in range(2):
            hand2.addCard(ace)
        self.assertTrue(hand1.compareTo(hand2) == 1)

    def test_BlackJack(self):
        blackJack = BJHand()
        blackJack.handValue = -1
        dealerHand = BJHand()
        dealerHand.handValue = 21
        self.assertTrue(blackJack.compareTo(dealerHand) == 1)
