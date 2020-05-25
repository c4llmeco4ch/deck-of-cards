from baseComponents import Card
from blackjack import BJHand
import pytest

class TestHandComparisons:

    @pytest.mark.parametrize('hand1, hand2, comp_val', [
        ([11, 12], [10, 5, 2, 3], 0),
        ([10, 13], [10, 5, 2, 3], 0),
        ([10, 11], [1, 10], -1)
    ])
    def test_face_cards(self, hand1, hand2, comp_val):
        our_hand = BJHand()
        for c in hand1:
            our_hand.add_card(Card(c, 'H'))
        deal_hand = BJHand()
        for val in hand2:
            deal_hand.add_card(Card(val, 'S'))
        our_hand.stand()
        deal_hand.stand()
        assert our_hand.compare_to(deal_hand) == comp_val

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


class TestHaveBlackjack:
    
    @pytest.mark.parametrize('cards, expected', 
        [
            ([1, 10], True),
            ([1, 11], True),
            ([1, 12], True),
            ([1, 13], True),
            ([10, 10, 1], False),
            ([1, 1, 9], False),
            ([1], False),
            ([], False)
        ]
    )
    def test_for_blackjack(self, cards, expected):
        h = BJHand()
        for c in cards:
            h.add_card(Card(c, 'H'))
        assert h.have_blackjack() == expected


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
