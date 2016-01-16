import random
from enum import Enum

from colored import attr, bg, fg


class Suits(Enum):
    HEART = 1
    DIAMOND = 2
    SPADE = 3
    CLOVER = 4


class Colors(Enum):
    BLACK = 1
    RED = 2


class Card:
    def __init__(self, suit, rank):
        """
        suit:   Heart, Diamond, Club, Spade
        rank:   Ace through King
        hidden: card is face down or face up
        """
        suits = {
            Suits.HEART: "♡",
            Suits.DIAMOND: "♢",
            Suits.SPADE: "♤",
            Suits.CLOVER: "♧",
        }

        self._hidden = True
        self.rank = rank
        self._suit = suit
        self._suit_unicode = suits[suit]

        self._color = Colors.BLACK
        if self._suit in [Suits.HEART, Suits.DIAMOND]:
            self._color = Colors.RED

    def __str__(self):
        color = f"{attr('bold')}{fg('red')}{bg('white')}"
        if self._color == Colors.BLACK:
            color = f"{attr('bold')}{fg('black')}{bg('white')}"
        formatted_card = f"{color}{self._suit_unicode}{self.rank:>2}{attr(0)}"
        return f"[{formatted_card}]"

    def flip(self):
        self._hidden = not self._hidden

    def value(self):
        return (self._suit, self.rank)


class CardContainer:
    def __init__(self):
        self.deck = []
        self.size = 0

    def __str__(self):
        return ", ".join([str(card) for card in self.deck])

    def __getitem__(self, i):
        return self.deck[i]

    def __add__(self, x):
        """Used to combine decks"""
        for card in x:
            self.deck.append(card)
        return self

    def build_deck(self):
        """Initiate a shuffled deck of cards."""
        suits = [Suits.HEART, Suits.DIAMOND, Suits.SPADE, Suits.CLOVER]
        ranks = ["A"] + [str(i) for i in range(2, 11)] + ["J", "Q", "K"]

        self.deck = [Card(s, r) for s in suits for r in ranks]
        self.size = 52

    def shuffle(self):
        tmp = []

        l = len(self.deck)
        while l > 0:
            tmp.append(self.deck.pop(random.randrange(l)))
            l -= 1
        self.deck = tmp

    def is_empty(self):
        return self.size <= 0

    def draw(self):
        """Draw from the top of the deck (pop last)."""
        if self.is_empty():
            return None
        self.size -= 1
        return self.deck.pop()

    def return_card(self, card):
        """Return a card to the deck (push front)."""
        self.deck = [card] + self.deck
        self.size += 1
