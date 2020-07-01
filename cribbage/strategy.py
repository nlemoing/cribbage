from typing import List, Tuple

class Strategy:
    """
    Strategy is an abstract base class for implementing cribbage strategies.
    It exposes two methods. The first, chooseHand, takes a hand of 6 cards and
    returns a hand of four as well as the two discarded cards. The second
    method is the pegging function, peg, which takes a hand and the sequence of
    previously played cards and returns a card to play next. 
    Besides that, anything goes!
    """
    def chooseHand(self, options: List[int], crib: bool) -> List[int]:
        """
        chooseHand expects an array of integers with length 6 that represents
        a set of 6 cards from which to choose a hand. It should return a list
        of 4 cards that are kept. The list should be made up of the same
        elements as were in the original list, but this can't be enforced here
        so we'll also do sanity checks when running simulations. It also has a
        parameter to indicate whether the crib belongs to the player.
        """
        pass

    def peg(self, hand: List[int], player: int, previousCards: List[List[Tuple[int]]]) -> int:
        """
        peg takes a hand and a set of previous cards that were played. Peg will
        only be called when a move is possible (e.g. a go is not forced). hand
        only contains cards that haven't been played yet, so whatever peg
        returns should be part of hand (we'll check!). previousCards is a list
        of previously played cards, grouped by 31s (each time 31 is reached, a
        new list is added). Each tuple is a pair containing a card and a player
        number.
        """
        pass
