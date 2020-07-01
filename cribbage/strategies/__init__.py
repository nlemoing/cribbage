from .random import *
from .first import *
from .human import *

strategies = {
    'random': RandomStrategy(),
    'first': FirstStrategy(),
    'human': HumanStrategy(),
}
