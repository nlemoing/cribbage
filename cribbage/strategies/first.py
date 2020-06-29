from typing import List, Tuple
from cribbage.strategy import Strategy

class FirstStrategy(Strategy):
    """
    FirstStrategy always picks the first available cards, which is useful for
    testing. It behaves similarly to RandomStrategy when the Deck is random.
    """

    def chooseHand(self, options: List[int]) -> List[int]:
        return options[:4]

    def peg(self, hand: List[int], player: int, previousCards: List[List[Tuple[int]]]) -> int:
        return hand[0]