from cribbage.strategies import RandomStrategy
from cribbage.simulate import simulate
from cribbage.constants import TOTAL_POINTS

def test_end_to_end():
    """
    This test simulates a game with two random strategies and ensures that the
    resulting dataframe contains data that makes sense (points are capped at
    the point cap, etc.). This doesn't do much to test whether the simulation
    code makes sense, but serves as a smoke test to make sure no glaring errors
    are happening.
    """
    strat1 = RandomStrategy()
    strat2 = RandomStrategy()
    games = 10
    point_cap = 100
    df = simulate(strat1, strat2, games, point_cap=point_cap)
    assert(len(df) == games)
    assert(df[f'strat1_{TOTAL_POINTS}'].max() <= point_cap)
    assert(df[f'strat2_{TOTAL_POINTS}'].max() <= point_cap)
