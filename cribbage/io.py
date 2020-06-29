from cribbage.score import card, suit

SUITS = ["♥", "♦", "♠", "♣"]
CARDS = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]

def formatCard(c: int) -> str:
    """
    Accepts a card in integer form and returns its string representation.
    """
    return f"{CARDS[card(c)]}{SUITS[suit(c)]}"