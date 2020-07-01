from typing import List
from random import shuffle

class Deck:
    """
    A deck implements the deal method which produces two hands and a cut card.
    """
    def deal(self):
        pass

class RandomDeck(Deck):
    def __init__(self):
        self.deck = list(range(52))
    
    def deal(self) -> (List[int], List[int], int):
        shuffle(self.deck)
        return self.deck[:6], self.deck[6:12], self.deck[12]
