import unittest
from baseComponents import Card
from blackjack import BJHand, BJPlayer


# TODO: Add tests for dealerloop, update compare_to tests
class TestAreBusted(unittest.TestCase):

    def test_ThreeFace(self):
        hand = BJHand()
        hand.add_card(Card(11, "H"))
        hand.add_card(Card(12, "D"))
        hand.add_card(Card(13, "S"))
        self.assertTrue(hand.are_busted())

    def test_ThreeAce(self):
        hand = BJHand()
        hand.add_card(Card(1, "S"))
        hand.add_card(Card(1, "H"))
        hand.add_card(Card(1, "C"))
        self.assertFalse(hand.are_busted())

    def test_NormalHand(self):
        hand = BJHand()
        hand.add_card(Card(4, "H"))
        hand.add_card(Card(5, "S"))
        hand.add_card(Card(6, "C"))
        self.assertFalse(hand.are_busted())

    def test_LongBustedHand(self):
        hand = BJHand()
        hand.add_card(Card(2, "H"))
        hand.add_card(Card(3, "S"))
        hand.add_card(Card(5, "C"))
        hand.add_card(Card(1, "H"))
        hand.add_card(Card(1, "D"))
        hand.add_card(Card(5, "D"))
        hand.add_card(Card(4, "S"))
        hand.add_card(Card(1, "S"))
        self.assertTrue(hand.are_busted())

    def test_LongSafeHand(self):
        hand = BJHand()
        hand.add_card(Card(2, "H"))
        hand.add_card(Card(2, "S"))
        hand.add_card(Card(7, "C"))
        hand.add_card(Card(1, "H"))
        hand.add_card(Card(1, "D"))
        hand.add_card(Card(5, "D"))
        hand.add_card(Card(3, "S"))
        self.assertFalse(hand.are_busted())

    def test_BlackJack(self):
        hand = BJHand()
        hand.add_card(Card(1, "S"))
        hand.add_card(Card(12, "H"))
        self.assertFalse(hand.are_busted())


class TestStanding(unittest.TestCase):

    def test_DualAces(self):
        hand = BJHand()
        hand.add_card(Card(1, "S"))
        hand.add_card(Card(1, "H"))
        hand.are_busted()
        hand.stand()
        self.assertEqual(12, hand.hand_value, "Two aces should equal 12")

    def test_FourAces(self):
        hand = BJHand()
        hand.add_card(Card(1, "S"))
        hand.add_card(Card(1, "H"))
        hand.add_card(Card(1, "C"))
        hand.add_card(Card(1, "D"))
        hand.are_busted()
        hand.stand()
        self.assertEqual(14, hand.hand_value, "Four aces should equal 14")

    def test_AceAsEleven(self):
        hand = BJHand()
        print("This hand has a value of: " + str(hand.hand_value[0]))
        hand.add_card(Card(1, "D"))
        hand.add_card(Card(2, "S"))
        hand.add_card(Card(3, "C"))
        hand.are_busted()
        hand.stand()
        self.assertEqual(16, hand.hand_value, "5 + 11 <= 21, Ace counts as 11")

    def test_BlackJack(self):
        hand = BJHand()
        hand.add_card(Card(13, "H"))
        hand.add_card(Card(1, "D"))
        hand.are_busted()
        hand.stand()
        self.assertEqual(21, hand.hand_value, "Blackjack returns 21")


class TestBets(unittest.TestCase):

    def test_NegativeBet(self):
        bjp = BJPlayer("Connor")
        self.assertFalse(bjp.place_bet(-5))

    def test_TooHighBet(self):
        bjp = BJPlayer("Me")
        self.assertFalse(bjp.place_bet(101))

    def test_ExactHighBet(self):
        bjp = BJPlayer("Me")
        self.assertTrue(bjp.place_bet(bjp.money))


class TestSplitAbility(unittest.TestCase):

    def test_CantSplit(self):
        one_hand = BJHand()
        self.assertFalse(one_hand.can_split())
        one_hand.add_card(Card(5, "H"))
        one_hand.add_card(Card(10, "S"))
        self.assertFalse(one_hand.can_split())
        twoHand = BJHand()
        twoHand.add_card(Card(3, "C"))
        twoHand.add_card(Card(3, "H"))
        twoHand.add_card(Card(3, "S"))
        self.assertFalse(one_hand.can_split())

    def test_CanSplit(self):
        one_hand = BJHand()
        one_hand.add_card(Card(8, "C"))
        one_hand.add_card(Card(8, "H"))
        self.assertTrue(one_hand.can_split())


class TestHandComparisons(unittest.TestCase):
    def test_FaceCards(self):
        jack = Card(11, "H")
        queen = Card(12, "S")
        king = Card(13, "D")
        ten = Card(10, "C")

        hand1 = BJHand()
        hand1.add_card(jack)
        hand1.add_card(queen)
        hand1.stand()
        hand2 = BJHand()
        hand2.add_card(ten)
        hand2.add_card(Card(5, "C"))
        hand2.add_card(Card(2, "S"))
        hand2.add_card(Card(3, "D"))
        hand2.stand()
        self.assertTrue(hand1.compare_to(hand2) == 0)

        hand3 = BJHand()
        hand3.add_card(ten)
        hand3.add_card(king)
        hand3.stand()
        self.assertTrue(hand3.compare_to(hand2) == 0)

    def test_Aces(self):
        ace = Card(1, "S")
        hand1 = BJHand()
        for _ in range(3):
            hand1.add_card(ace)
        hand1.stand()
        hand2 = BJHand()
        hand2.add_card(Card(10, "C"))
        for _ in range(2):
            hand2.add_card(ace)
        self.assertTrue(hand1.compare_to(hand2) == 1)

    def test_BlackJack(self):
        black_jack = BJHand()
        black_jack.hand_value = -1
        dealer_hand = BJHand()
        dealer_hand.hand_value = 21
        self.assertTrue(black_jack.compare_to(dealer_hand) == 1)
