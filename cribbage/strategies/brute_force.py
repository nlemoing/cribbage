from cribbage.strategies import HandScore
from cribbage.score import scoreHand

from typing import List
from statistics import mean

class BruteForce(HandScore):
    """
    The BruteForce strategy implements scoring by running through each possible
    cut card and scoring the resulting hand. Base classes differ in how they
    select a hand to choose.
    """
    def getScores(self, hand: List[int], discarded: List[int], crib: bool) -> List[int]:
        return [scoreHand(hand, cutCard) for cutCard in range(52) \
            if cutCard not in hand and cutCard not in discarded]

class ExpectedValue(BruteForce):
    """
    The expected value strategy scores a hand based on its expected value
    across all possible cut cards.
    """
    def score(self, hand: List[int], discarded: List[int], crib: bool) -> int:
        return mean(self.getScores(hand, discarded, crib))

class MaximizeCeiling(BruteForce):
    """
    The maximize ceiling strategy scores a hand based on the highest possible
    points it can gain across all cut cards.
    """
    def score(self, hand: List[int], discarded: List[int], crib: bool) -> int:
        return max(self.getScores(hand, discarded, crib))

class MaximizeFloor(BruteForce):
    """
    The maximize floor strategy scores a hand based on the minimum number of
    points that are guaranteed, regardless of cut card.
    """
    def score(self, hand: List[int], discarded: List[int], crib: bool) -> int:
        return min(self.getScores(hand, discarded, crib))
            