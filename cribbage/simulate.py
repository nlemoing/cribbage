from cribbage.strategy import Strategy
from cribbage.game import game
from cribbage.constants import POINT_CAP
import pandas as pd

def simulate(strat1: Strategy, strat2: Strategy, games: int, point_cap: int=POINT_CAP) -> pd.DataFrame:
    """
    The simulate function pits two strategies against each other. The two
    strategies will play the specified number of games up to the specified
    point cap, taking turns starting with the crib. Simulate returns a pandas
    DataFrame containing the result of each game.
    """
    return pd.DataFrame(game(strat1, strat2, game_number % 2, point_cap) for game_number in range(games))
