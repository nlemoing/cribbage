import argparse
import pathlib
from cribbage.simulate import simulate, simulateHandChoice
from cribbage.strategies import strategies
from cribbage.constants import POINT_CAP
from cribbage.logger import logger, setLogLevel
from cribbage.analysis import analyze_game

STRATEGY_NAMES = tuple(strategies.keys())
STRATEGIES_MESSAGE = "\n\n".join(f"{k}: {v.__doc__}" for k, v in strategies.items())

parser = argparse.ArgumentParser(description=STRATEGIES_MESSAGE, formatter_class=argparse.RawTextHelpFormatter)

subparsers = parser.add_subparsers()

# Game parser
game = subparsers.add_parser("game", help="Play a crib game between two strategies")
game.add_argument("strategy1", help="Player 1 Strategy", choices=STRATEGY_NAMES)
game.add_argument("strategy2", help="Player 2 Strategy", choices=STRATEGY_NAMES)
game.add_argument("-pc", "--point-cap", help=f"Score to play the game to (default {POINT_CAP})", default=121)

def handle_game(args, output):
    df = simulate(
        strategies[args.strategy1],
        strategies[args.strategy2],
        args.iterations,
        args.point_cap,
    )
    df.to_csv(f'{output}/raw_game_data.csv')
    analysis = analyze_game(df)
    analysis.to_csv(f'{output}/game_analysis.csv')
game.set_defaults(func=handle_game)

# Hand choice parser
hand_choice = subparsers.add_parser("hand-choice", help="Choose a hand from 6 cards and score it based on a cut card")
hand_choice.add_argument("strategy", help="Strategy", choices=STRATEGY_NAMES)

def handle_hand_choice(args, output):
    df = simulateHandChoice(strategies[args.strategy], args.iterations)
    df.to_csv(f'{output}/raw_hand_data.csv')
hand_choice.set_defaults(func=handle_hand_choice)

parser.add_argument("-i", "--iterations", type=int, default=1, help="Number of iterations to run (default 1)")
parser.add_argument("-v", "--verbose", help="Print information about the game (useful for human strategies)",
                    action="store_true")
parser.add_argument("output", help="The output folder where analysis files are written")

def main():
    args = parser.parse_args()
    setLogLevel(args.verbose)
    path = pathlib.Path(args.output)
    path.mkdir(parents=True, exist_ok=True)
    args.func(args, path.resolve())
