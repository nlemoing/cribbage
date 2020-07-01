from typing import List, Tuple
from cribbage.strategy import Strategy
from cribbage.io import formatCard

class HumanStrategy(Strategy):
    """
    HumanStrategy implements an interactive strategy that allows a person to
    select pegging and hand cards using IO inputs
    """

    def chooseHand(self, options: List[int], crib: bool) -> List[int]:
        print(f"It is {'' if crib else ' not'} your crib.")
        print("Choose your hand by typing the numbers corresponding to the cards you want, separated by spaces.")
        chosen = input("\n".join(f"{i}: {formatCard(options[i])}" for i in range(len(options))) + "\n")
        return [options[int(option)] for option in chosen.split(" ")] 

    def peg(self, hand: List[int], player: int, previousCards: List[List[Tuple[int]]]) -> int:
        print("Choose the card to play by typing the number corresponding to the card you want.")
        chosen = input("\n".join(f"{i}: {formatCard(hand[i])}" for i in range(len(hand))) + "\n")
        return hand[int(chosen)]
