from cribbage.simulate import peg, GameContext, PEG_POINTS
from cribbage.strategies import FirstStrategy
from cribbage.deck import RandomDeck
from typing import List

def pegging_setup(hands: List[List[int]], scores: List[int], point_cap: int = 121):
    # Use two strategies that always take the first option for repeatable tests
    strategies = [FirstStrategy(), FirstStrategy()]
    # Player 2 crib, player 1 starts
    gc = GameContext(1, point_cap, RandomDeck())
    
    
    peg(gc, strategies, hands)
    assert(gc.scores[0][PEG_POINTS] == scores[0])
    assert(gc.scores[1][PEG_POINTS] == scores[1])

def test_peg_1():
    ## P ## Card ## Total ## Points
    ## 1 ## J    ## 10    ## 0
    ## 2 ## 5    ## 15    ## 2
    ## 1 ## J    ## 25    ## 0
    ## 2 ## 6    ## 31    ## 2
    ## 1 ## 4    ## 4     ## 0
    ## 2 ## 6    ## 10    ## 0
    ## 1 ## 5    ## 15    ## 5
    ## 2 ## 3    ## 18    ## 4 + 1
    pegging_setup([[10, 23, 3, 4], [4, 5, 18, 2]], [5, 9])
    pegging_setup([[10, 23, 3, 4], [4, 5, 18, 2]], [0, 4], 3)

def test_peg_2():
    ## P ## Card ## Total ## Points
    ## 1 ## J    ## 10    ## 0
    ## 2 ## A    ## 11    ## 0
    ## 1 ## J    ## 21    ## 0
    ## 2 ## A    ## 22    ## 0
    ## 2 ## A    ## 23    ## 2
    ## 2 ## A    ## 24    ## 6 + 1
    ## 1 ## J    ## 10    ## 0
    ## 1 ## J    ## 20    ## 2 + 1
    pegging_setup([[10, 23, 36, 49], [0, 13, 26, 39]], [3, 9])
    pegging_setup([[10, 23, 36, 49], [0, 13, 26, 39]], [0, 9], 9)


def test_peg_3():
    ## P ## Card ## Total ## Points
    ## 1 ## J    ## 10    ## 0
    ## 2 ## K    ## 20    ## 0
    ## 1 ## Q    ## 30    ## 3 + 1
    ## 2 ## K    ## 10    ## 0
    ## 1 ## 5    ## 15    ## 2
    ## 2 ## 10   ## 25    ## 0 + 1
    ## 1 ## 7    ## 7     ## 0
    ## 2 ## 8    ## 15    ## 2 + 1
    pegging_setup([[10, 11, 4, 6], [12, 25, 9, 7]], [6, 4])
    pegging_setup([[10, 11, 4, 6], [12, 25, 9, 7]], [4, 0], 4)
