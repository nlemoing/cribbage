from itertools import combinations
from bisect import insort
from typing import List, Tuple

suit = lambda c: c // 13
card = lambda c: c % 13
value = lambda c: 10 if card(c) >= 10 else card(c) + 1

def flush(hand: List[int], cutCard: int, crib: bool) -> int:
    # Flush points
    flush = 0
    if all(suit(c) == suit(hand[0]) for c in hand):
        flush += 4
    if flush and suit(cutCard) == suit(hand[0]):
        flush += 1
    elif crib:
        flush = 0
    return flush

def jack(hand: List[int], cutCard: int):
    # Jack point
    jack = 0
    if any(card(c) == 10 and suit(c) == suit(cutCard) for c in hand):
        jack += 1
    return jack

def pair(hand: List[int], cutCard: int) -> int:
    fullHand = sorted(card(c) for c in hand + [cutCard]) 

    # Pair points
    pair = 0
    for i in range(4):
        for j in range(i + 1, 5):
            if fullHand[i] == fullHand[j]:
                pair += 2
    return pair

def run(hand: List[int], cutCard: int) -> int:
    fullHand = sorted(card(c) for c in hand + [cutCard]) 

    # Run points
    run = 0
    for runVal in range(5, 2, -1):
        for arr in combinations(fullHand, runVal):
            if all(arr[i] + 1 == arr[i+1] for i in range(len(arr) - 1)):
                run += runVal
        if run:
            break
    return run

def fifteen(hand: List[int], cutCard: int) -> int:
    # Fifteen points
    fullHand = [value(c) for c in hand + [cutCard]]
    fifteen = 0
    total = sum(fullHand)
    
    if total == 15:
        fifteen += 2

    for i in range(5):
        if total - fullHand[i] == 15:
            fifteen += 2

    for i in range(4):
        for j in range(i + 1, 5):
            if fullHand[i] + fullHand[j] == 15:
                fifteen += 2
            if total - fullHand[i] - fullHand[j] == 15:
                fifteen += 2
    return fifteen

def scoreHand(hand: List[int], cutCard: int, crib: bool = False):

    result = { 
        'flush': flush(hand, cutCard, crib), 
        'jack': jack(hand, cutCard),
        'pair': pair(hand, cutCard),
        'run': run(hand, cutCard),
        'fifteen': fifteen(hand, cutCard),
    }

    return sum(v for v in result.values())

def scorePeg(cards_played: List[int]) -> int:
    """
    Accepts a list of cards played and scores it according to pegging rules.
    """
    # Pegging only depends on the card, not the suit, so we can remove it.
    cards_played = [card(c) for c in cards_played]

    # Pair points. Check the last two cards. If they match, check the last
    # three, then the last four if those match.
    pair_points = 0
    for pair in range(1, 4):
        if len(cards_played) < pair + 1 or cards_played[-1] != cards_played[-pair - 1]:
            break
        # Add 2 for the first pair, 4 more for the second and 6 more for third.
        # 1 Pair  = 2         = 2
        # 2 Pairs = 2 + 4     = 6
        # 3 Pairs = 2 + 4 + 6 = 12
        pair_points += 2 * pair

    # Run points. Start with the last two cards played in sorted order. Then,
    # go through the remaining cards in reverse order while checking if the
    # resulting array makes a run.
    run_points = 0
    current_run = sorted(cards_played[-2:])
    for i in range(len(cards_played) - 3, -1, -1):
        insort(current_run, cards_played[i])
        # If each element in the array is off by 1, it's a run and set run
        # points accordingly
        if all(current_run[i] + 1 == current_run[i + 1] \
            for i in range(len(current_run) - 1)):
                run_points = len(current_run)
    
    # Fifteen points. Add up the value of the cards played, see if it's 15.
    fifteen_points = 2 if sum(value(c) for c in cards_played) == 15 else 0

    return pair_points + run_points + fifteen_points
