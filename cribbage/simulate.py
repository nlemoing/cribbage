from cribbage.strategy import Strategy
from cribbage.game import game
from cribbage.constants import POINT_CAP
from cribbage.deck import RandomDeck
from cribbage.score import scoreHand
import pandas as pd

def simulate(strat1: Strategy, strat2: Strategy, games: int, point_cap: int=POINT_CAP) -> pd.DataFrame:
    """
    The simulate function pits two strategies against each other. The two
    strategies will play the specified number of games up to the specified
    point cap, taking turns starting with the crib. Simulate returns a pandas
    DataFrame containing the result of each game.
    """
    return pd.DataFrame(game(strat1, strat2, game_number % 2, point_cap) for game_number in range(games))

def simulateHandChoice(strat: Strategy, iterations: int) -> pd.DataFrame:
    """
    The simulateHandChoice function evaluates how a chosen strategy peforms
    by dealing several hands and scoring them based on the cut card. It returns
    a pandas DataFrame with the chosen hand, discarded cards, cut card, and the
    score of each hand. Points in the crib are not accounted for here because
    those depend on the choices from another strategy.
    """
    deck = RandomDeck()
    fields = [f'hand_{i+1}' for i in range(4)] + ['discarded_1', 'discarded_2', 'cutCard', 'score']
    def _score():
        hand, _, cutCard = deck.deal()
        options = strat.chooseHand(hand)
        discarded = [c for c in hand if c not in options]
        return pd.Series(options + discarded + [cutCard, scoreHand(options, cutCard)], index=fields)
    return pd.DataFrame(_score() for _ in range(iterations))
