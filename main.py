import os
import random
import state
import mdp
import value_iteration

deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] * 4
scores = [0,0]

def deal(deck):
    hand = []
    for i in range(2):
        random.shuffle(deck)
        card = deck.pop()
        if card == 11: card = "J"
        if card == 12: card = "Q"
        if card == 13: card = "K"
        if card == 14: card = "A"
        hand.append(card)
    return hand


def play_again():
    again = "y"
        #input("Do you want to play again? (Y/N) : ").lower()
    if again == "y":
        dealer_hand = []
        player_hand = []
        deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] * 4
        game(deck)
    else:
        print(scores)
        exit()


def total(hand):
    total = 0
    for card in hand:
        if card == "J" or card == "Q" or card == "K":
            total += 10
        elif card == "A":
            if total >= 11:
                total += 1
            else:
                total += 11
        else:
            total += card
    return total


def hit(hand):
    if not deck:
        print("--------------------------------------")
        print("Score:")
        print(f"AI won {scores[0]} games out of {scores[0]+scores[1]} total.")
        exit()
    card = deck.pop()
    if card == 11: card = "J"
    if card == 12: card = "Q"
    if card == 13: card = "K"
    if card == 14: card = "A"
    hand.append(card)
    return hand


def clear():
    if os.name == 'nt':
        os.system('CLS')
    if os.name == 'posix':
        os.system('clear')


def print_results(dealer_hand, player_hand):
    clear()
    print("The dealer has a " + str(dealer_hand) + " for a total of " + str(total(dealer_hand)))
    print("You have a " + str(player_hand) + " for a total of " + str(total(player_hand)))


def blackjack(dealer_hand, player_hand):
    if total(player_hand) == 21:
        print_results(dealer_hand, player_hand)
        print("Congratulations! You got a Blackjack!\n")
        play_again()
    elif total(dealer_hand) == 21:
        print_results(dealer_hand, player_hand)
        print("Sorry, you lose. The dealer got a blackjack.\n")
        play_again()


def score(dealer_hand, player_hand):
    if total(player_hand) == 21:
        print_results(dealer_hand, player_hand)
        scores[0]+=1
        print("Congratulations! You got a Blackjack!\n")
    elif total(dealer_hand) == 21:
        print_results(dealer_hand, player_hand)
        scores[1]+=1
        print("Sorry, you lose. The dealer got a blackjack.\n")
    elif total(player_hand) > 21:
        print_results(dealer_hand, player_hand)
        scores[1]+=1
        print("Sorry. You busted. You lose.\n")
    elif total(dealer_hand) > 21:
        print_results(dealer_hand, player_hand)
        scores[0]+=1
        print("Dealer busts. You win!\n")
    elif total(player_hand) < total(dealer_hand):
        print_results(dealer_hand, player_hand)
        scores[1]+=1
    # print ("Sorry. Your score isn't higher than the dealer. You lose.\n")
    elif total(player_hand) > total(dealer_hand):
        print_results(dealer_hand, player_hand)
        scores[0]+=1
        print("Congratulations. Your score is higher than the dealer. You win\n")

def to_val(card_list):
    cards = [card for card in card_list]
    for i, card in enumerate(card_list):
        if card == 'J' or card == 'Q' or card == 'K':
            cards[i] = 10
        if card == 'A':
            cards[i] = 11
    return cards



def game(deck):
    choice = None
    clear()
    dealer_hand = deal(deck)
    player_hand = deal(deck)
    while choice != "q":
        print("The dealer is showing a " + str(dealer_hand[0]))
        print("You have a " + str(player_hand) + " for a total of " + str(total(player_hand)))
        blackjack(dealer_hand, player_hand)
        #AI:
        cur_state = state.State(to_val(dealer_hand+player_hand), to_val(player_hand), to_val(dealer_hand)[0], deck, to_val(dealer_hand)[1], 0)
        m = mdp.MarkovDecisionProcess(cur_state)
        v = value_iteration.ValueIteration(m)


        choice = v.get_policy(cur_state)
        print(choice)
        if choice == None:
            choice = "Stand"
        while choice == "Hit":
            if sum(to_val(player_hand)) < 14:
                hit(player_hand)
                cur_state = state.State(to_val(dealer_hand+player_hand), to_val(player_hand), to_val(dealer_hand)[0], deck, to_val(dealer_hand)[1], 0)
                m = mdp.MarkovDecisionProcess(cur_state)
                v = value_iteration.ValueIteration(m)
                choice = v.get_policy(cur_state)
                if choice == "Stand":
                    break
            while total(dealer_hand) < 17:
                hit(dealer_hand)
            score(dealer_hand, player_hand)
            play_again()
        if choice == "Stand":
            while total(dealer_hand) < 17:
                hit(dealer_hand)
            score(dealer_hand, player_hand)
            play_again()


if __name__ == "__main__":
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] * 4
    game(deck)
