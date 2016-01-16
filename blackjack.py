from deck import Deck
import time

def find_total(deck):
    """ Total is blackjack specific """
    total = 0
    for card in deck:
        if card.rank.isdigit():
            total += int(card.rank)
        elif card.rank in ["K", "Q", "J"]:
            total += 10

    # count Aces at the end
    for card in deck:
        if card.rank == "A":
            if total + 11 < 21:
                total += 11
            else:
                total += 1
    return total

def pretty_print(name, deck, total):
    print "{}: {}    <{:>3}>".format(name, deck, total)

def main():
    d = Deck()
    d.build_deck()
    d.shuffle()

    # new class, player can have money
    # goal to win all the money
    player = Deck()
    dealer = Deck()

    player.return2deck(d.draw())
    dealer.return2deck(d.draw())

    player.return2deck(d.draw())
    dealer.return2deck(d.draw())

    d_total = find_total(dealer)
    pretty_print("Dealer", dealer, d_total)

    print "Player phase"
    while True:
        p_total = find_total(player)
        pretty_print("Player", player, p_total)

        if p_total > 21:
            print "Player loses"
            return

        action = raw_input("> ")
        if action.startswith("bet"):
            pass
        elif action.startswith("hit"):
            print "Player draws..."
            player.return2deck(d.draw())
        elif action.startswith("stay"):
            break

    print "Dealer phase"
    while True:
        d_total = find_total(dealer)
        pretty_print("Dealer", dealer, d_total)
        if d_total > 21:
            print "Dealer busts! You win!"
            return

        if  d_total == p_total:
            "Draw, dealer wins"

        if d_total > p_total:
            print "Dealer wins!"
            break
        elif d_total < 21:
            # hit
            print "The Dealer hits..."
            time.sleep(2)
            dealer.return2deck(d.draw())

if __name__ == "__main__":
    main()
