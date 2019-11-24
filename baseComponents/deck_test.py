from .deck import Deck
import pytest


class TestDealCardsFromDeck:

    def test_no_shuffle_deal(self):
        d = Deck()
        answer = d.deal_card()
        assert answer.value == 1
        assert answer.suit == "H"
        assert not d.is_empty
        assert d.size == 51

    def test_last_card(self):
        d = Deck()
        for i in range(len(d.deck) - 1):
            d.deal_card()
        assert not d.is_empty
        d.deal_card()
        assert d.is_empty
        assert d.deal_card() is None

    def test_shuffle_maintains_size(self):
        d = Deck()
        d.shuffle()
        assert d.size == 52
