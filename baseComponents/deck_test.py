from .deck import Deck


class TestDealCardsFromDeck:

    def test_no_shuffle_deal(self):
        d = Deck()
        answer = d.deal_card()
        assert answer.value == 1
        assert answer.suit == 'H'
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


class TestPrintDeck:

    def test_no_shuffle_print(self):
        d = Deck()
        assert d.__str__() == ''.join(['[ AH | 2H | 3H | 4H | 5H | 6H |',
                                       ' 7H | 8H | 9H | 10H | JH | QH | KH |',
                                       ' AC | 2C | 3C | 4C | 5C | 6C |',
                                       ' 7C | 8C | 9C | 10C | JC | QC | KC |',
                                       ' KD | QD | JD | 10D | 9D | 8D | 7D |',
                                       ' 6D | 5D | 4D | 3D | 2D | AD |',
                                       ' KS | QS | JS | 10S | 9S | 8S | 7S |',
                                       ' 6S | 5S | 4S | 3S | 2S | AS ]'])
