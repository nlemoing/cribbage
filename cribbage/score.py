from itertools import combinations

def scoreHand(hand, cutCard, crib = False):
    suit = lambda c: c // 13
    card = lambda c: c % 13
    valu = lambda c: 10 if card(c) >= 10 else card(c) + 1
    
    # Flush points
    flush = 0
    if all(suit(c) == suit(hand[0]) for c in hand):
        flush += 4
    if flush and suit(cutCard) == suit(hand[0]):
        flush += 1
    elif crib:
        flush = 0

    # Jack point
    jack = 0
    if any(card(c) == 10 and suit(c) == suit(cutCard) for c in hand):
        jack += 1

    fullHand = sorted(card(c) for c in hand + [cutCard]) 

    # Pair points
    pair = 0
    for i in range(4):
        for j in range(i + 1, 5):
            if fullHand[i] == fullHand[j]:
                pair += 2

    # Run points
    run = 0
    for runVal in range(5, 2, -1):
        for arr in combinations(fullHand, runVal):
            if all(arr[i] + 1 == arr[i+1] for i in range(len(arr) - 1)):
                run += runVal
        if run:
            break

    # Fifteen points
    fullHand = [valu(c) for c in fullHand]
    fifteen = 0
    total = sum(fullHand)
    
    if total == 15:
        fifteen += 2

    for i in range(5):
        if total - fullHand[i] == 15:
            fifteen += 2

    for i in range(4):
        for j in range(i + 1, 5):
            print(total, fullHand[i], fullHand[j])
            if fullHand[i] + fullHand[j] == 15:
                fifteen += 2
            if total - fullHand[i] - fullHand[j] == 15:
                fifteen += 2

    result = { 
        'flush': flush, 
        'jack': jack,
        'pair': pair,
        'run': run,
        'fifteen': fifteen
    }
    print(result)

    return sum(v for v in result.values())
