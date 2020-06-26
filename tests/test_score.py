from cribbage.score import scoreHand

def test_best_hand():
    assert(scoreHand([4, 30, 17, 36], 43) == 28)
    assert(scoreHand([4, 43, 17, 36], 30) == 29)

def test_runs():
    assert(scoreHand([0, 14, 28, 42], 43) == 7)
    assert(scoreHand([0, 14, 28, 42], 29) == 10)
    assert(scoreHand([10, 23, 36, 48], 50) == 15)
    assert(scoreHand([10, 23, 48, 50], 37) == 16)

def test_flush():
    assert(scoreHand([1, 3, 5, 20], 9) == 0)
    assert(scoreHand([1, 3, 5, 7], 22) == 4)
    assert(scoreHand([1, 3, 5, 7], 22, crib=True) == 0)
    assert(scoreHand([1, 3, 5, 7], 9) == 5)
    assert(scoreHand([1, 3, 5, 7], 9, crib=True) == 5)

def test_fifteens():
    assert(scoreHand([20, 33, 29, 16], 15) == 12)
    assert(scoreHand([45, 46, 32, 33], 21) == 24)
    assert(scoreHand([41, 28, 29, 30], 48) == 12)
    assert(scoreHand([44, 40, 13, 17], 26) == 4)

def test_pairs():
    assert(scoreHand([1, 16, 31, 46], 48) == 0)
    assert(scoreHand([1, 14, 31, 46], 48) == 2)
    assert(scoreHand([1, 14, 27, 46], 48) == 6)
    assert(scoreHand([1, 14, 27, 40], 48) == 12)
    