from cribbage.strategy import Strategy
from cribbage.score import scoreHand
import pandas as pd
from random import shuffle

TURNS = 'turns'
WINNER = 'winner'
TOTAL_POINTS = 'total_points'
HAND_POINTS = 'hand_points'
CRIB_POINTS = 'crib_points'
PEG_POINTS = 'peg_points'

def simulate(strat1: Strategy, strat2: Strategy, games: int, point_cap: int=121) -> pd.DataFrame:
    """
    The simulate function pits two strategies against each other. The two
    strategies will play the specified number of games up to the specified
    point cap, taking turns starting with the crib. Simulate returns a pandas
    DataFrame containing the result of each game.
    """
    return pd.DataFrame(game(strat1, strat2, game_number % 2, point_cap) for game_number in range(games))

def game(strat1: Strategy, strat2: Strategy, crib: int, point_cap: int) -> pd.Series:
    """
    This function takes care of actual game simulation. crib is 1 if strat2
    starts with the crib and 0 otherwise.
    It returns a pandas series with information about the game.
     - strat1_score: the score for strategy 1
     - strat1_hand: the number of points strat1 gained from their hand
     - strat1_crib: the number of points strat1 gained from their crib
     - strat1_peg: the number of points strat1 gained from pegging
     - ... all the same fields for strat2 ...
    """
    START_DICT = { k: 0 for k in (HAND_POINTS, CRIB_POINTS, PEG_POINTS) }
    scores = [pd.Series(START_DICT), pd.Series(START_DICT)]
    deck = list(range(52))
    turns = 0

    def add_points(player: int, game_section: str, points: int) -> bool:
        """
        add_points adds the specified number of points to the player's hand.
        It returns True if the player has surpassed the number of points
        required to win and False otherwise.
        """
        scores[player][game_section] += points
        return sum(scores[player]) >= point_cap

    while True:
        shuffle(deck)
        crib_hand = []
        options1, options2, cutCard = deck[0:6], deck[6:12], deck[12]

        # Choose strat1 hand
        hand1 = strat1.chooseHand(options1)
        assert(all(card in options1 for card in hand1))
        crib_hand.extend(card for card in options1 if card not in hand1)

        # Choose strat2 hand
        hand2 = strat2.chooseHand(options2)
        assert(all(card in options2 for card in hand2))
        crib_hand.extend(card for card in options2 if card not in hand2)

        # TODO: Do pegging here

        # Score the hands here
        hand_points = [scoreHand(hand1, cutCard), scoreHand(hand2, cutCard)]
        crib_points  = scoreHand(crib_hand,  cutCard)
        
        # The person without the crib alwa gets the chance to score their 
        # hand first. We'll also check for a win condition after every addition
        # using the add_points hand. If any of them returns True, the
        # expression will short-circuit before the rest complete.
        if add_points(1 - crib, HAND_POINTS, hand_points[1 - crib]) or \
           add_points(crib, HAND_POINTS, hand_points[crib]) or \
           add_points(crib, CRIB_POINTS, crib_points):
            break

        # Switch the crib and increment the turn counter
        crib = 1 - crib
        turns += 1
    
    for strat in (0, 1):
        scores[strat][TOTAL_POINTS] = min(point_cap, sum(scores[strat]))
        scores[strat][WINNER] = scores[strat][TOTAL_POINTS] == point_cap
    result = pd.Series({ f'strat{p+1}_{k}': v for p, d in enumerate(scores) for k, v in d.iteritems() })
    result[TURNS] = turns
    return result