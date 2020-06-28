from itertools import combinations

suit = lambda c: c // 13
card = lambda c: c % 13
value = lambda c: 10 if card(c) >= 10 else card(c) + 1

def flush(hand, cutCard, crib):
    # Flush points
    flush = 0
    if all(suit(c) == suit(hand[0]) for c in hand):
        flush += 4
    if flush and suit(cutCard) == suit(hand[0]):
        flush += 1
    elif crib:
        flush = 0
    return flush

def jack(hand, cutCard):
    # Jack point
    jack = 0
    if any(card(c) == 10 and suit(c) == suit(cutCard) for c in hand):
        jack += 1
    return jack

def pair(hand, cutCard):
    fullHand = sorted(card(c) for c in hand + [cutCard]) 

    # Pair points
    pair = 0
    for i in range(4):
        for j in range(i + 1, 5):
            if fullHand[i] == fullHand[j]:
                pair += 2
    return pair

def run(hand, cutCard):
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

def fifteen(hand, cutCard):
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

def scoreHand(hand, cutCard, crib = False):

    result = { 
        'flush': flush(hand, cutCard, crib), 
        'jack': jack(hand, cutCard),
        'pair': pair(hand, cutCard),
        'run': run(hand, cutCard),
        'fifteen': fifteen(hand, cutCard),
    }

    return sum(v for v in result.values())
