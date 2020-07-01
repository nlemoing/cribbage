from .random import *
from .first import *
from .human import *
from .hand_score import *
from .brute_force import *

strategies = {
    'random': RandomStrategy(),
    'first': FirstStrategy(),
    'human': HumanStrategy(),
    'expected_value': ExpectedValue(),
    'maximize_ceiling': MaximizeCeiling(),
    'maximize_floor': MaximizeFloor(),
}
