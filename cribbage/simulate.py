from cribbage.strategy import Strategy
from cribbage.score import scoreHand, scorePeg, value
from cribbage.io import formatCard
import pandas as pd
from random import shuffle

TURNS = 'turns'
WINNER = 'winner'
TOTAL_POINTS = 'total_points'
HAND_POINTS = 'hand_points'
CRIB_POINTS = 'crib_points'
PEG_POINTS = 'peg_points'

PEG_CAP = 31

def simulate(strat1: Strategy, strat2: Strategy, games: int, point_cap: int=121) -> pd.DataFrame:
    """
    The simulate function pits two strategies against each other. The two
    strategies will play the specified number of games up to the specified
    point cap, taking turns starting with the crib. Simulate returns a pandas
    DataFrame containing the result of each game.
    """
    return pd.DataFrame(game(strat1, strat2, game_number % 2, point_cap) for game_number in range(games))

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
    START_DICT = { k: 0 for k in (HAND_POINTS, CRIB_POINTS, PEG_POINTS) }
    scores = [pd.Series(START_DICT), pd.Series(START_DICT)]
    deck = list(range(52))
    turns = 0

    def printif(s: str = ""):
        if verbose:
            print(s)

    def add_points(player: int, game_section: str, points: int) -> bool:
        """
        add_points adds the specified number of points to the player's hand.
        It returns True if the player has surpassed the number of points
        required to win and False otherwise.
        """
        if game_section == HAND_POINTS:
            printif(f"Player {player + 1} scored {points} in their hand")
        elif game_section == CRIB_POINTS: 
            printif(f"Player {player + 1} scored {points} in their crib")

        scores[player][game_section] += points
        return sum(scores[player]) >= point_cap

    while True:
        printif()
        printif(f"Turn {turns + 1}: player {crib + 1}'s crib.")
        printif(f"Player 1 score: {sum(scores[0])}")
        printif(f"Player 2 score: {sum(scores[1])}")

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

        printif(f"\n{formatCard(cutCard)} was cut.")

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
        printif()
        while True:

            printif(f"Pegging: player {pegging_turn + 1} to play (total: {context_value()}).")

            if pegging_can_play(pegging_turn):

                # Get a card using the strategy and ensure it was in the player's hand
                strat = strat1 if pegging_turn == 0 else strat2
                card = strat.peg(
                    # Only provide options that will fit under the pegging cap
                    [c for c in pegging_hands[pegging_turn] if value(c) + context_value() <= PEG_CAP],
                    pegging_turn,
                    pegging_context
                )
                assert(card in pegging_hands[pegging_turn])

                # Remove the card from the hand and add it to the context
                pegging_hands[pegging_turn].remove(card)
                pegging_context[-1].append((card, pegging_turn))

                # Score based on the context
                play_score = scorePeg([c for c, _ in pegging_context[-1]])
                printif(f"Player {pegging_turn+1} played {formatCard(card)}, scoring {play_score}.")
                if add_points(pegging_turn, PEG_POINTS, play_score):
                    game_over = True
                    break
    
            elif not pegging_can_play(1 - pegging_turn):
                # The player whose turn it isn't gets to go, since when neither
                # player can play, the person whose turn it isn't played last.
                # They receive 2 points for reaching 31 exactly and 1 point
                # otherwise.
                printif(f"No one can play (total: {context_value()}). Player {2 - pegging_turn} to go.")

                if add_points(1 - pegging_turn, PEG_POINTS, 2 if context_value() == 31 else 1):
                    game_over = True
                    break
                
                printif()

                # Add a new pegging context
                pegging_context.append([])

            else:
                printif(f"Player {pegging_turn+1} could not play.")

            # Switch the turn 
            pegging_turn = 1 - pegging_turn

            if not any(len(h) for h in pegging_hands):
                # If players run out of cards to play and a go wasn't just given, add it here
                if context_value():
                    printif(f"No one can play (total: {context_value()}). Player {2 - pegging_turn} to go.")

                    if add_points(1 - pegging_turn, PEG_POINTS, 1):
                        game_over = True
                        break
                break

        if game_over:
            break

        # Score the hands here
        hand_points = [scoreHand(hand1, cutCard, 1 - crib), scoreHand(hand2, cutCard, crib)]
        crib_points  = scoreHand(crib_hand,  cutCard)
        
        # The person without the crib alwa gets the chance to score their 
        # hand first. We'll also check for a win condition after every addition
        # using the add_points hand. If any of them returns True, the
        # expression will short-circuit before the rest complete.
        printif()
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
        if scores[strat][WINNER]:
            printif(f"Game over. Player {strat + 1} wins!")

    result = pd.Series({ f'strat{p+1}_{k}': v for p, d in enumerate(scores) for k, v in d.iteritems() })
    result[TURNS] = turns
    return result
