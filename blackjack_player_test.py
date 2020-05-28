from baseComponents import Card
from blackjack import BJPlayer
import pytest


# TODO: Add tests for dealerloop, update compare_to tests
class TestBets:

    @pytest.mark.parametrize('amount, expected',[
        (-5, False),
        (101, False),
        (100, True),
        (1, True)
    ])
    def test_bets(self, amount, expected):
        bjp = BJPlayer("Connor")
        assert bjp.place_bet(amount) == expected


class TestDealingCards:

    @pytest.mark.parametrize('cards, size, total', [
        ([2, 2, 4], 1, 8),
        ([10, 2, 5], 1, 17),
        ([13, 5, 3], 1, 18),
        ([12, 11, 1], 1, 21),
        ([12, 1, 1], 1, 12),
        ([5, 1, 1, 1, 4], 1, 12),
        ([1, 4, 1], 3, 16),
        ([1], 2, 11)
    ])
    def test_dealings(self, cards, size, total):
        p = BJPlayer('Me')
        for c in cards:
            p.deal_card(Card(c, 'H'), 0)
        p.hand[0].are_busted()
        assert len(p.hand[0].hand_value) == size
        p.hand[0].stand()
        assert p.hand[0].hand_value == total


class TestSplittingHands:

    def test_proper_splits(self):
        player = BJPlayer('Me')
        player.deal_card(Card(10, 'H'), 0)
        player.deal_card(Card(10, 'S'), 0)
        split = player.split_hand(Card(1, 'S'), Card(10,'C'), 0)
        assert len(split) == 2
        assert split[0].hand_value == [11, 21]
        assert split[1].hand_value == [20]
        assert split[1].can_split()

    def test_cascading_splits(self):
        pass