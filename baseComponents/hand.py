from abc import ABC, abstractmethod


class Hand(ABC):

    def __init__(self):
        self.cards = []
        self.numOfCards = 0
        super().__init__()

    def __repr__(self):
        """Convert this hand to a readable string"""
        return ''.join('| ', ', '.join(c for c in self.hand), '|')

    @abstractmethod
    def add_card(self, cardToAdd):
        pass

    @abstractmethod
    def reset(self):
        pass
