from deck import Deck
import re
import time

class Player():
    def __init__(self, name, cash):
        self.name  = name
        self.cash  = cash
        self.total = 0
        self.hand  = Deck()

    def __str__(self):
        return "{} (${:>5}): <{:>3}> | {}".format(self.name, self.cash, self.total, self.hand)

    def __add__(self, card):
        self.hand.return_card(card)
        self._find_total()
        return self

    def _find_total(self):
        """ Total is blackjack specific """
        total = 0
        for card in self.hand:
            if card.rank.isdigit():
                total += int(card.rank)
            elif card.rank in ["K", "Q", "J"]:
                total += 10

        for card in self.hand:
            if card.rank == "A":
                if total + 11 < 21:
                    total += 11
                else:
                    total += 1
        self.total = total

    def discard(self):
        tmp = self.hand
        self.hand  = Deck()
        self.total = 0
        return tmp

    def wager(self, cash):
        # wager more than you have
        if cash > self.cash:
            self.cash = 0
            return self.cash

        # or not
        else:
            self.cash -= cash
            return cash

def main():
    draw_pile = Deck()
    draw_pile.build_deck()
    draw_pile.shuffle()

    # for when you run out of cards in your deck
    discard_pile = Deck()

    # goal to win all the money, start with 10k each
    player = Player("Player", 10000)
    dealer = Player("Dealer", 10000)
    current_pot = 0

    while player.cash > 0 and dealer.cash > 0:

        print "The current standings"
        print "Player: ${:>5}, Dealer: ${:>5}".format(player.cash, dealer.cash)
        print "Commands: bet, hit, hold"

        # make sure to get the right bet amount
        action = raw_input("> ")
        bet_regex = re.compile("bet\s*(\d*)")
        while bet_regex.match(action).group(1) == "":
            action = raw_input("> ")

        # we know it's a number because of the regex
        cash = bet_regex.match(action).group(1)
        current_pot += player.wager(int(cash))
        current_pot += dealer.wager(int(cash))

        # each participant draws 2 cards, in a circle
        player += draw_pile.draw()
        dealer += draw_pile.draw()

        player += draw_pile.draw()
        dealer += draw_pile.draw()
        print dealer
        print player

        print "(Player phase)"
        while True:
            print player

            if player.total > 21:
                print "---  Player busts. Dealer wins the hand. ---"
                discard_pile += player.discard()
                discard_pile += dealer.discard()
                dealer.cash += current_pot
                current_pot = 0
                break

            action = raw_input("> ")
            if action.startswith("hit"):
                print "Player draws..."
                player += draw_pile.draw()

            elif action.startswith("stay"):
                break

        if current_pot == 0:
            continue
        print "(Dealer phase)"
        while True:
            print dealer
            if dealer.total > 21:
                print "--- Dealer busts! Player wins the hand! ---"
                discard_pile += player.discard()
                discard_pile += dealer.discard()
                player.cash += current_pot
                current_pot = 0
                break

            if  dealer.total == player.total:
                "--- Draw. Dealer wins the hand. ---"
                discard_pile += player.discard()
                discard_pile += dealer.discard()
                dealer.cash += current_pot
                current_pot = 0
                break

            elif dealer.total > player.total:
                print "--- Dealer wins the hand. ---"
                discard_pile += player.discard()
                discard_pile += dealer.discard()
                dealer.cash += current_pot
                current_pot = 0
                break
            elif dealer.total < 21:
                print "The Dealer hits..."
                time.sleep(2)
                dealer += draw_pile.draw()

    if player.cash > dealer.cash:
        print "Congratulations Player, you won all the money"
        return
    else:
        print "Sorry, Dealer wins this time."
        return

if __name__ == "__main__":
    main()

