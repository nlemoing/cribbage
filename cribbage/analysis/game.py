import pandas as pd
import numpy as np

from cribbage.constants import TURNS, CRIB, WINNER

def analyze_game(df: pd.DataFrame):
    """
    Takes in a DataFrame of games and produces analysis of those games.
    It also provides results split out by victor and starting crib.
    For each game group, it produces the following columns:
      - games: number of games played
      - turns: average number of turns it takes to complete a game
      - strat(1|2)_wins: the number of wins for each strategy
      - average_victory_margin: average margin of victory for the winning
            player
      - strat(1|2)_(hand|crib|peg)_points_pct: percentage of points (relative
            to total) coming from each game section
    """
    rows = (
        ('total', np.repeat(True, len(df.index))),
        ('strat1_victory', df[f'strat1_{WINNER}'] == 1),
        ('strat2_victory', df[f'strat2_{WINNER}'] == 1),
        ('strat1_crib', df[CRIB] == 0),
        ('strat2_crib', df[CRIB] == 1)
    )
    def _analyze(row_name: str, mask: pd.Series):
        _df = df[mask]
        return pd.Series({
            'games': len(_df.index),
            'turns': _df[TURNS].mean(),
            'average_victory_margin': abs(_df['strat1_total_points'] - _df['strat2_total_points']).mean(),
            'strat1_wins': _df[f'strat1_{WINNER}'].sum(),
            'strat2_wins': _df[f'strat2_{WINNER}'].sum(),
            'strat1_peg_points': (_df['strat1_peg_points'] / _df['strat1_total_points']).mean(),
            'strat2_peg_points': (_df['strat2_peg_points'] / _df['strat2_total_points']).mean(),
            'strat1_hand_points': (_df['strat1_hand_points'] / _df['strat1_total_points']).mean(),
            'strat2_hand_points': (_df['strat2_hand_points'] / _df['strat2_total_points']).mean(),
            'strat1_crib_points': (_df['strat1_crib_points'] / _df['strat1_total_points']).mean(),
            'strat2_crib_points': (_df['strat2_crib_points'] / _df['strat2_total_points']).mean(),
        }, name=row_name)
    return pd.DataFrame(_analyze(row_name, mask) for row_name, mask in rows)

