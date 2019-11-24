import pytest
from baseComponents import Card
from blackjack import BJHand, BJPlayer


# TODO: Add tests for dealerloop, update compare_to tests
class TestAreBusted:

    def test_three_face(self):
        hand = BJHand()
        hand.add_card(Card(11, "H"))
        hand.add_card(Card(12, "D"))
        hand.add_card(Card(13, "S"))
        assert hand.are_busted()

    def test_three_ace(self):
        hand = BJHand()
        hand.add_card(Card(1, "S"))
        hand.add_card(Card(1, "H"))
        hand.add_card(Card(1, "C"))
        assert not hand.are_busted()

    def test_normal_hand(self):
        hand = BJHand()
        hand.add_card(Card(4, "H"))
        hand.add_card(Card(5, "S"))
        hand.add_card(Card(6, "C"))
        assert not hand.are_busted()

    def test_long_busted_hand(self):
        hand = BJHand()
        hand.add_card(Card(2, "H"))
        hand.add_card(Card(3, "S"))
        hand.add_card(Card(5, "C"))
        hand.add_card(Card(1, "H"))
        hand.add_card(Card(1, "D"))
        hand.add_card(Card(5, "D"))
        hand.add_card(Card(4, "S"))
        hand.add_card(Card(1, "S"))
        assert hand.are_busted()

    def test_long_safe_hand(self):
        hand = BJHand()
        hand.add_card(Card(2, "H"))
        hand.add_card(Card(2, "S"))
        hand.add_card(Card(7, "C"))
        hand.add_card(Card(1, "H"))
        hand.add_card(Card(1, "D"))
        hand.add_card(Card(5, "D"))
        hand.add_card(Card(3, "S"))
        assert not hand.are_busted()

    def test_blackjack(self):
        hand = BJHand()
        hand.add_card(Card(1, "S"))
        hand.add_card(Card(12, "H"))
        assert not hand.are_busted()


class TestStanding:

    def test_dual_aces_are_twelve(self):
        hand = BJHand()
        hand.add_card(Card(1, "S"))
        hand.add_card(Card(1, "H"))
        hand.are_busted()
        hand.stand()
        assert 12 == hand.hand_value

    def test_four_aces_are_fourteen(self):
        hand = BJHand()
        hand.add_card(Card(1, "S"))
        hand.add_card(Card(1, "H"))
        hand.add_card(Card(1, "C"))
        hand.add_card(Card(1, "D"))
        hand.are_busted()
        hand.stand()
        assert 14 == hand.hand_value

    def test_ace_as_eleven(self):
        hand = BJHand()
        print("This hand has a value of: " + str(hand.hand_value[0]))
        hand.add_card(Card(1, "D"))
        hand.add_card(Card(2, "S"))
        hand.add_card(Card(3, "C"))
        hand.are_busted()
        hand.stand()
        assert 16 == hand.hand_value

    def test_ace_face_are_blackjack(self):
        hand = BJHand()
        hand.add_card(Card(13, "H"))
        hand.add_card(Card(1, "D"))
        hand.are_busted()
        hand.stand()
        assert 21 == hand.hand_value


class TestBets:

    def test_negative_bet(self):
        bjp = BJPlayer("Connor")
        assert not bjp.place_bet(-5)

    def test_too_high_bet(self):
        bjp = BJPlayer("Me")
        assert not bjp.place_bet(101)

    def test_exact_high_bet(self):
        bjp = BJPlayer("Me")
        assert bjp.place_bet(bjp.money)

    def test_exact_low_bet(self):
        bjp = BJPlayer("Me")
        assert bjp.place_bet(1)


class TestSplitAbility:

    def test_cant_split(self):
        one_hand = BJHand()
        assert not one_hand.can_split()
        one_hand.add_card(Card(5, "H"))
        one_hand.add_card(Card(10, "S"))
        assert not one_hand.can_split()
        twoHand = BJHand()
        twoHand.add_card(Card(3, "C"))
        twoHand.add_card(Card(3, "H"))
        twoHand.add_card(Card(3, "S"))
        assert not one_hand.can_split()

    def test_can_split(self):
        one_hand = BJHand()
        one_hand.add_card(Card(8, "C"))
        one_hand.add_card(Card(8, "H"))
        assert one_hand.can_split()


class TestHandComparisons:
    def test_face_cards(self):
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
        assert hand1.compare_to(hand2) == 0

        hand3 = BJHand()
        hand3.add_card(ten)
        hand3.add_card(king)
        hand3.stand()
        assert hand3.compare_to(hand2) == 0

    def test_aces(self):
        ace = Card(1, "S")
        hand1 = BJHand()
        for _ in range(3):
            hand1.add_card(ace)
        hand1.stand()
        hand2 = BJHand()
        hand2.add_card(Card(10, "C"))
        for _ in range(2):
            hand2.add_card(ace)
        hand2.stand()
        assert hand1.compare_to(hand2) == 1

    def test_blackjack(self):
        blackjack = BJHand()
        blackjack.hand_value = -1
        dealer_hand = BJHand()
        dealer_hand.hand_value = 21
        assert blackjack.compare_to(dealer_hand) == 1
