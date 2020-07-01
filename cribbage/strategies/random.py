from random import choice, sample
from typing import List, Tuple
from cribbage.strategy import Strategy

class RandomStrategy(Strategy):
    """
    RandomStrategy chooses how to peg and its hand using random chance,
    making it the easiest strategy to implement (and also the worst).
    """

    def chooseHand(self, options: List[int], crib: bool) -> List[int]:
        return sample(options, 4)

    def peg(self, hand: List[int], player: int, previousCards: List[List[Tuple[int]]]) -> int:
        return choice(hand)
