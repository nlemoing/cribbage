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
        logger.info(f"Turn {self.turns}: player {self.crib + 1}'s crib.")
        logger.info(f"Player 1 score: {sum(self.scores[0])}")
        logger.info(f"Player 2 score: {sum(self.scores[1])}\n")

        if self.turns:
            self.crib = 1 - self.crib
        self.turns += 1
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
        if "J" in formatCard(cutCard) and game_context.add_points(crib, JACK_POINTS, 2):
            break

        # Set up pegging: no previous cards played, starting with the player
        # without the crib, and with both player
        pegging_context = [[]]
        pegging_turn = 1 - crib
        pegging_hands = [hand1.copy(), hand2.copy()]

        def context_value() -> int:
            """
            Returns the current total of the pegging context.
            """
            return sum(value(c) for c, _ in pegging_context[-1])

        def pegging_can_play(player: int) -> bool:
            """
            Returns whether a player is able to peg.
            """
            if not len(pegging_hands[player]):
                return False
            min_card = min(value(c) for c in pegging_hands[player])
            return context_value() + min_card <= PEG_CAP

        # While both players have cards remaining, peg
        game_over = False
        logger.info("Pegging\n")
        while True:

            ctx = context_value()
            logger.info(f"Player {pegging_turn + 1} to play (total: {ctx}).")

            if pegging_can_play(pegging_turn):

                # Get a card using the strategy and ensure it was in the player's hand
                strat = strat1 if pegging_turn == 0 else strat2
                card = strat.peg(
                    # Only provide options that will fit under the pegging cap
                    [c for c in pegging_hands[pegging_turn] if value(c) + ctx <= PEG_CAP],
                    pegging_turn,
                    pegging_context
                )
                assert(card in pegging_hands[pegging_turn])

                # Remove the card from the hand and add it to the context
                pegging_hands[pegging_turn].remove(card)
                pegging_context[-1].append((card, pegging_turn))

                # Score based on the context
                play_score = scorePeg([c for c, _ in pegging_context[-1]])
                logger.info(f"Player {pegging_turn + 1} played {formatCard(card)}.")
                if game_context.add_points(pegging_turn, PEG_POINTS, play_score):
                    game_over = True
                    break
    
            elif not pegging_can_play(1 - pegging_turn):
                # The player whose turn it isn't gets to go, since when neither
                # player can play, the person whose turn it isn't played last.
                # They receive 2 points for reaching 31 exactly and 1 point
                # otherwise.
                logger.info(f"No one can play (total: {ctx}). Go for Player {2 - pegging_turn}.\n")

                if game_context.add_points(1 - pegging_turn, PEG_POINTS, 2 if ctx == 31 else 1):
                    game_over = True
                    break

                # Add a new pegging context
                pegging_context.append([])

            else:
                logger.info(f"Player {pegging_turn+1} could not play.")

            # Switch the turn 
            pegging_turn = 1 - pegging_turn

            if not any(len(h) for h in pegging_hands):
                # If players run out of cards to play and a go wasn't just given, add it here
                if context_value():
                    logger.info(f"No one can play (total: {context_value()}). Player {2 - pegging_turn} to go.")

                    if game_context.add_points(1 - pegging_turn, PEG_POINTS, 1):
                        game_over = True
                break

        if game_over:
            break

        # Score the hands here
        hand_points = [scoreHand(hand1, cutCard, 1 - crib), scoreHand(hand2, cutCard, crib)]
        crib_points  = scoreHand(crib_hand,  cutCard)
        
        # The person without the crib always gets the chance to score their 
        # hand first. We'll also check for a win condition after every addition
        # using the add_points hand. If any of them returns True, the
        # expression will short-circuit before the rest complete.
        if game_context.add_points(1 - crib, HAND_POINTS, hand_points[1 - crib]) or \
           game_context.add_points(crib, HAND_POINTS, hand_points[crib]) or \
           game_context.add_points(crib, CRIB_POINTS, crib_points):
            break
    
    return game_context.finish_game()
