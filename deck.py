import random

class Card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.hidden = True

    def __str__(self):
        return "[{}{:>3}]".format(self.suit, self.rank)

    def flip(self):
        self.hidden = not self.hidden

    def value(self):
        return (self.suit, self.rank)


class Deck():
    def __init__(self):
        """ just in case you want an empty pile to put cards into """
        self.deck = []
        self.size = 0

    def __str__(self):
        return ", ".join([ str(card) for card in self.deck])

    def __getitem__(self, i):
        return self.deck[i]

    def __add__(self, x):
        # list concat
        for card in x:
            self.deck.append(card)
        return self

    def build_deck(self):
        """ regular ol' deck of playing cards """
        suits = ["H", "D", "S", "C"]
        ranks = ["A"] + [ str(i) for i in range(2, 11) ] + ["J", "Q", "K"]

        self.deck = [ Card(s, r) for s in suits for r in ranks ]
        self.size = 52

    def shuffle(self):
        """ self explanitory """
        tmp = []

        l = len(self.deck)
        while l > 0:
            tmp.append(self.deck.pop(random.randrange(l)))
            l -= 1
        self.deck = tmp

    def is_empty(self):
        """ tells if the deck is empty """
        return self.size <= 0

    def draw(self):
        """ draw from the top of the deck / pop last """
        if self.is_empty():
            return None
        self.size -= 1
        return self.deck.pop()

    def return_card(self, card):
        """
        push front operation

        Useful for rebuilding new decks from scratch
        """
        self.deck = [card] + self.deck
        self.size += 1

