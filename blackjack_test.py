from baseComponents import Card
from blackjack import BJHand, BJPlayer
import pytest


# TODO: Add tests for dealerloop, update compare_to tests
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
