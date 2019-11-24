from abc import ABC, abstractmethod
class Hand(ABC):

    def __init__(self):
        self.cards = []
        self.numOfCards = 0
        super().__init__()

    def __repr__(self):
        """Convert this hand to a readable string"""
        current_hand = "| "
        for c in self.hand:
            current_hand += repr(c) + ", "
        current_hand = current_hand[:len(current_hand) - 2] + "|"
        return current_hand

    @abstractmethod
    def add_card(self, cardToAdd):
        pass

    @abstractmethod
    def reset(self):
        pass