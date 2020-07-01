from cribbage.strategies import FirstStrategy

from itertools import combinations
from typing import List, Tuple

class HandScore(FirstStrategy):
    """
    HandScore is a strategy that assigns a score to each combination of four
    cards from the options given. It expects a score method, which takes a 4
    card hand and a boolean indicating whose crib it is, and returns an 
    integer.
    """
    def chooseHand(self, options: List[int], crib: bool) -> List[int]:
        """
        chooseHand depends on the score method, which is up to the base class
        to implement.
        """
        return max(
            (list(x) for x in combinations(options, 4)),
            key=lambda x: self.score(
                x,
                [c for c in options if c not in x],
                crib
            )
        )

    def score(self, hand: List[int], discarded: List[int], crib: bool) -> int:
        """
        Score takes a hand and returns an integer used to score it. This is
        used by chooseHand to select the combination with the highest score.
        """
        pass