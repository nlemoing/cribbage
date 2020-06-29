from cribbage.strategy import Strategy
from cribbage.score import scoreHand, scorePeg, value
from cribbage.io import formatCard
import pandas as pd
from random import shuffle
import logging
from typing import List

TURNS = 'turns'
WINNER = 'winner'
TOTAL_POINTS = 'total_points'
HAND_POINTS = 'hand_points'
CRIB_POINTS = 'crib_points'
PEG_POINTS = 'peg_points'
JACK_POINTS = 'jack_points'

PEG_CAP = 31

logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger('cribbage')

def simulate(strat1: Strategy, strat2: Strategy, games: int, point_cap: int=121) -> pd.DataFrame:
    """
    The simulate function pits two strategies against each other. The two
    strategies will play the specified number of games up to the specified
    point cap, taking turns starting with the crib. Simulate returns a pandas
    DataFrame containing the result of each game.
    """
    return pd.DataFrame(game(strat1, strat2, game_number % 2, point_cap) for game_number in range(games))

START_DICT = { k: 0 for k in (HAND_POINTS, CRIB_POINTS, PEG_POINTS, JACK_POINTS) }
class GameContext:
    def __init__(self, crib, point_cap):
        self.scores = [pd.Series(START_DICT), pd.Series(START_DICT)]
        self.deck = list(range(52))
        self.crib = crib
        self.turns = 0
        self.point_cap = point_cap
    
    def new_turn(self) -> (List[int], List[int], int):
        """
        new_turn handles the logic of going to the next turn. This includes
        updating the turn, switching the crib, dealing two hands of 6 and
        the cut card.
        """
        if self.turns:
            self.crib = 1 - self.crib
        self.turns += 1

        logger.info(f"Turn {self.turns}: player {self.crib + 1}'s crib.")
        logger.info(f"Player 1 score: {sum(self.scores[0])}")
        logger.info(f"Player 2 score: {sum(self.scores[1])}\n")

        shuffle(self.deck)
        return self.deck[0:6], self.deck[6:12], self.deck[12]

    def add_points(self, player: int, game_section: str, points: int) -> bool:
        """
        add_points adds the specified number of points to the player's hand.
        It returns True if the player has surpassed the number of points
        required to win and False otherwise.
        """
        if not points:
            return False

        if game_section == HAND_POINTS:
            logger.info(f"Player {player + 1} scored {points} in their hand.")
        elif game_section == CRIB_POINTS: 
            logger.info(f"Player {player + 1} scored {points} in their crib.")
        elif game_section == PEG_POINTS:
            logger.info(f"Player {player + 1} scored {points} by pegging.")
        elif game_section == JACK_POINTS:
            logger.info(f"Player {player + 1} scored {points} when the Jack was cut.")

        self.scores[player][game_section] += points
        return sum(self.scores[player]) >= self.point_cap

    def finish_game(self) -> pd.Series:
        """
        Perform all post-game cleanup and return a Series summarizing the game.
        """
        for strat in (0, 1):
            self.scores[strat][TOTAL_POINTS] = min(self.point_cap, sum(self.scores[strat]))
            self.scores[strat][WINNER] = self.scores[strat][TOTAL_POINTS] == self.point_cap
            if self.scores[strat][WINNER]:
                logger.info(f"\nGame over. Player {strat + 1} wins!")

        result = pd.Series({ f'strat{p+1}_{k}': v for p, d in enumerate(self.scores) for k, v in d.iteritems() })
        result[TURNS] = self.turns
        return result

def game(strat1: Strategy, strat2: Strategy, crib: int, point_cap: int, verbose: bool = False) -> pd.Series:
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
    if verbose:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARN)

    game_context = GameContext(crib, point_cap)

    while True:
        options1, options2, cutCard = game_context.new_turn()
        crib_hand = []

        # Choose strat1 hand
        hand1 = strat1.chooseHand(options1)
        assert(all(card in options1 for card in hand1))
        crib_hand.extend(card for card in options1 if card not in hand1)

        # Choose strat2 hand
        hand2 = strat2.chooseHand(options2)
        assert(all(card in options2 for card in hand2))
        crib_hand.extend(card for card in options2 if card not in hand2)

        logger.info(f"{formatCard(cutCard)} was cut.\n")
        if "J" in formatCard(cutCard) and game_context.add_points(game_context.crib, JACK_POINTS, 2):
            break

        if peg(game_context, [strat1, strat2], [hand1.copy(), hand2.copy()], game_context.crib):
            break

        # Score the hands here
        hand_points = [
            scoreHand(hand1, cutCard, 1 - game_context.crib),
            scoreHand(hand2, cutCard, game_context.crib)
        ]
        crib_points  = scoreHand(crib_hand,  cutCard)
        
        # The person without the crib always gets the chance to score their 
        # hand first. We'll also check for a win condition after every addition
        # using the add_points hand. If any of them returns True, the
        # expression will short-circuit before the rest complete.
        if game_context.add_points(1 - game_context.crib, HAND_POINTS, hand_points[1 - game_context.crib]) or \
           game_context.add_points(game_context.crib, HAND_POINTS, hand_points[game_context.crib]) or \
           game_context.add_points(game_context.crib, CRIB_POINTS, crib_points):
            break
    
    return game_context.finish_game()

class PeggingContext:
    def __init__(self, crib: int):
        self.ctx = [[]]
        self.ctx_value = 0
        self.turn = 1 - crib

    def switch_turn(self):
        self.turn = 1 - self.turn

    def total(self) -> int:
        return self.ctx_value

    def cards_played(self) -> List[int]:
        """
        Get the cards played in the current play for scoring.
        """
        return [c for c, _ in self.ctx[-1]]

    def add(self, card):
        """
        Adds a card to the current play and updates the total value.
        """
        self.ctx[-1].append((card, self.turn))
        self.ctx_value += value(card)

    def reset(self):
        """
        Resets the current play.
        """
        self.ctx_value = 0
        self.ctx.append([])

    def can_play(self, hand: List[int]) -> List[int]:
        """
        Takes a hand and returns a list of cards that are playable given the context
        """
        return [c for c in hand if self.total() + value(c) <= PEG_CAP]

def peg(game_context: GameContext, strategies: List[Strategy], hands: List[List[int]], crib: int) -> bool:
    pegging_context = PeggingContext(crib)

    # While both players have cards remaining, peg
    logger.info("Pegging\n")
    while any(len(hand) for hand in hands):

        logger.info(f"Player {pegging_context.turn + 1} to play (total: {pegging_context.total()}).")

        # Get a list of options for the active player and if they have options,
        # allow them to choose
        options = pegging_context.can_play(hands[pegging_context.turn]) 
        if len(options):
            # Get a card using the strategy and ensure it was in the player's hand
            strategy = strategies[pegging_context.turn]
            card = strategy.peg(options, pegging_context.turn, pegging_context.ctx)
            assert(card in hands[pegging_context.turn])

            # Remove the card from the hand and add it to the context
            hands[pegging_context.turn].remove(card)
            pegging_context.add(card)

            # Score based on the context
            play_score = scorePeg(pegging_context.cards_played())
            logger.info(f"Player {pegging_context.turn + 1} played {formatCard(card)}.")
            if game_context.add_points(pegging_context.turn, PEG_POINTS, play_score):
                return True

        # After the first player has played, check if both players cannot play.
        # If not, then add a go for the player who just played.
        if not any(pegging_context.can_play(hand) for hand in hands):
            ctx = pegging_context.total()
            logger.info(f"No one can play (total: {ctx}). Go for Player {pegging_context.turn + 1}.\n")
            if game_context.add_points(pegging_context.turn, PEG_POINTS, 2 if ctx == 31 else 1):
                return True

            # Add a new pegging context
            pegging_context.reset()

        # Switch the turn 
        pegging_context.switch_turn()
    return False
