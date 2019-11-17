from abc import ABC, abstractmethod
class Hand(ABC):

    def __init__(self):
        self.cards = []
        self.numOfCards = 0
        super.__init__()

    def __repr__(self):
        """Convert this hand to a readable string"""
        currentHand = "| "
        for c in self.hand:
            currentHand += repr(c) + ", "
        currentHand = currentHand[:len(currentHand) - 2] + "|"
        return currentHand

    @abstractmethod
    def addCard(self, cardToAdd):
        pass
