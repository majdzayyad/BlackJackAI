import random
import mdp
import value_iteration
import sys
from tqdm import tqdm
from Qlearning import QLearningAgent


class Deck:
    """
    A class that represents the cards in a deck that also have operations over these
    cards such as reset/renew the cards, pop a cord, shuffle them and get them.
    """

    def __init__(self, decks_num=1):
        self.__decks_num = decks_num
        self.__cards = [j for deck_num in range(self.__decks_num)
                        for i in range(4)
                        for j in range(2, 15)]
        # dictionary that maps the card number j to its number of appearances
        # in the deck.
        self.__card_dict = {j: self.__decks_num * 4 for j in range(2, 15)}

    def is_empty(self):
        if self.__cards:
            return False
        return True

    def renew(self):
        self.__cards = [j for deck_num in range(self.__decks_num)
                        for i in range(4)
                        for j in range(2, 15)]
        self.__card_dict = {j: self.__decks_num * 4 for j in range(2, 15)}

    def shuffle(self):
        random.shuffle(self.__cards)

    def pop(self):
        c = self.__cards.pop()
        self.__card_dict[c] -= 1
        return c

    def get_cards(self):
        return self.__cards[:]

    @property
    def card_dict(self):
        return self.__card_dict


class Dealer:
    """
    A class that represents the dealer in the casino.
    It has many operations such as update score, add cards to the hand
    and remove/clear the hand.
    """

    def __init__(self):
        self.__score = 0
        self.__hand = []

    def get_hand(self):
        return self.__hand[:]

    def update_score(self):
        self.__score += 1

    def get_score(self):
        return self.__score

    def add_cards(self, hand):
        for card in hand:
            self.__hand.append(card)

    def remove_cards(self):
        self.__hand = []

    def reset_score(self):
        self.__score = 0


class Player:
    """
    A class that represents the player that plays against the dealer.
    It has similar operations to the Dealer class.
    """

    def __init__(self):
        self.__score = 0
        self.__hand = []

    def get_hand(self):
        return self.__hand[:]

    def update_score(self):
        self.__score += 1

    def get_score(self):
        return self.__score

    def add_cards(self, hand):
        for card in hand:
            self.__hand.append(card)

    def remove_cards(self):
        self.__hand = []

    def reset_score(self):
        self.__score = 0


class Round:
    """
    A class that represents a whole round of games between a dealer and an AI.
    It supports MDP, Q-Learning and Random as an AI.
    It has many operations that can be casted on each player whether it is AI or a
    dealer such us returning the total of its hand, hitting a player, running one
    or multiple games including counting score.
    """

    def __init__(self, agent="mdp", games_num=1, decks_num=1):
        self.__games_num = games_num
        self.__decks_num = decks_num
        self.__deck = Deck(decks_num)
        self.__dealer = Dealer()
        self.__player = Player()
        self.__agent = agent
        self.__q = QLearningAgent(0.01, 0.5)
        # a flag for qlearning indicating whether we're in training mode or not.
        self.__is_training = True

    def set_q(self, q):
        self.__q = q

    def __total(self, hand):
        """
        Returns the total of the hand,
        it also counts 'A' as 11 if it's better for the hand or 1 if it's better for the hand.
        """
        total = 0
        As_num = 0
        for card in hand:
            if card == "J" or card == "Q" or card == "K":
                total += 10
            elif card == "A":
                As_num += 1
            else:
                total += card
        for i in range(As_num):
            if total >= 11:
                total += 1
            else:
                total += 11
        return total

    def __soft_17(self, hand):
        """
        Returns True if the hand has a soft 17 or False otherwise.
        """
        if self.__total(hand) != 17:
            return False
        total = 0
        As_num = 0
        for card in hand:
            if card == "J" or card == "Q" or card == "K":
                total += 10
            elif card == "A":
                As_num += 1
            else:
                total += card
        if not As_num:
            return False
        for i in range(As_num):
            if total >= 11:
                return False
            else:
                total += 11
        return True

    def __to_val(self, card_list):
        """
        Returns list of cards where it only consists numbers and not chars.
        Ace is converted to 11 or 1 according to what's better for the hand.
        """
        total = 0
        cards = [card for card in card_list]
        for i, card in enumerate(card_list):
            if card == 'J' or card == 'Q' or card == 'K':
                cards[i] = 10
                total += 10

        for i, card in enumerate(card_list):
            if card == 'A':
                if total >= 11:
                    cards[i] = 1
                    total += 1
                else:
                    cards[i] = 11
                    total += 11
        return cards

    def __deal(self):
        """
        Draws 2 cards from the deck.
        Returns a list of 2 cards.
        In case there there isn't enough cards in the deck/s, the deck/s is renewed.
        """
        hand = []
        for i in range(2):
            if self.__deck.is_empty():
                self.__deck.renew()
            self.__deck.shuffle()
            card = self.__deck.pop()
            if card == 11: card = "J"
            if card == 12: card = "Q"
            if card == 13: card = "K"
            if card == 14: card = "A"
            hand.append(card)
        return hand

    def __hit(self):
        """
        Draws one card from the deck and returns it.
        In case there there isn't enough cards in the deck/s, the deck/s is renewed.
        """
        if self.__deck.is_empty():
            self.__deck.renew()
        card = self.__deck.pop()
        if card == 11: card = "J"
        if card == 12: card = "Q"
        if card == 13: card = "K"
        if card == 14: card = "A"
        return card

    def __blackjack(self):
        """
        Returns True if there is a Blackjack, False otherwise.
        Updates the scores in case there is a blackjack and the dealer didn't get blackjack as well.
        """
        if self.__total(self.__player.get_hand()) == 21:
            # in case the dealer and the play got blackjack it's a tie.
            if self.__total(self.__dealer.get_hand()) != 21:
                self.__score()
            return True
        elif self.__total(self.__dealer.get_hand()) == 21:
            self.__score()
            return True
        return False

    def __score(self):
        """
        Updates the score of the AI/dealer according to the hands.
        Returns 1 in case the AI wins, 0 in case the dealer wins.
        """
        player = 0
        if self.__agent != "ql" or not self.__is_training:
            if self.__total(self.__player.get_hand()) == 21:
                self.__player.update_score()
                player = 1
            elif self.__total(self.__dealer.get_hand()) == 21:
                self.__dealer.update_score()
            elif self.__total(self.__player.get_hand()) > 21:
                self.__dealer.update_score()
            elif self.__total(self.__dealer.get_hand()) > 21:
                self.__player.update_score()
                player = 1
            elif self.__total(self.__player.get_hand()) < self.__total(
                    self.__dealer.get_hand()):
                self.__dealer.update_score()
            elif self.__total(self.__player.get_hand()) > self.__total(
                    self.__dealer.get_hand()):
                self.__player.update_score()
                player = 1
        return player

    def __clear_hands(self):
        """
        Clears both dealer and AI hands.
        """
        self.__dealer.remove_cards()
        self.__player.remove_cards()

    def __mdp_action(self):
        """
        Returns the choice of the MDP policy.
        """
        m = mdp.MarkovDecisionProcess((sum(
            self.__to_val(self.__player.get_hand())),
                                       self.__dealer.get_hand()[1],
                                       0),
            self.__deck.card_dict)
        v = value_iteration.ValueIteration(m)
        choice = v.get_policy((
            sum(self.__to_val(self.__player.get_hand())),
            self.__dealer.get_hand()[1], 0))
        return choice

    def game(self):
        """
        Runs a game of blackjack between the AI and the dealer.
        In case the AI is Q-Learning, it trains the agent before the actual game.
        The function draws 2 cards for each player.
        Using only the exposed card of the dealer hand and the 2 cards of the AI it manages to
        Learn or activate the mdp policies and random choice/policy.
        Starting by checking if there's blackjack then it plays according to the given policies.
        """
        self.__player.add_cards(self.__deal())
        self.__dealer.add_cards(self.__deal())

        if self.__blackjack():
            self.__clear_hands()
            return

        # AI:
        # Using AI policy to decide what to do: Stand/Hit
        if self.__agent == "mdp":
            choice = self.__mdp_action()

        elif self.__agent == "ql":
            state = (self.__total(self.__player.get_hand()),
                     self.__dealer.get_hand()[1], 0)
            choice = self.__q.getPolicy(state)

        # According to the decision we play:
        if self.__agent == "mdp":
            # if the AI decided to hit and the cards sum is still under 21:
            while choice == "Hit" and self.__total(
                    self.__player.get_hand()) < 21:
                self.__player.add_cards([self.__hit()])
                choice = self.__mdp_action()

        elif self.__agent == "ql":
            # if the AI decided to hit and the cards sum is still under 21:
            while choice == "Hit" and self.__total(
                    self.__player.get_hand()) < 21:
                self.__player.add_cards([self.__hit()])
                next_state = (self.__total(self.__player.get_hand()),
                              self.__dealer.get_hand()[1], 0)
                if self.__is_training:
                    # Updates Q-learning
                    self.__q.update(state, choice, next_state, 0)
                choice = self.__q.getPolicy(next_state)
                state = next_state

        # Dealer turn
        while self.__total(self.__dealer.get_hand()) < 17:
            self.__dealer.add_cards([self.__hit()])

        # Using soft_17 feature for the dealer - deactivate if needed
        if self.__soft_17(self.__dealer.get_hand()):
            self.__dealer.add_cards([self.__hit()])

        self.__score()

        player_score = self.__total(self.__player.get_hand())
        dealer_score = self.__total(self.__dealer.get_hand())

        if self.__agent == "ql" and self.__is_training:
            reward = 0
            # tie case
            if player_score > 21 and dealer_score > 21:
                reward = 0
            # losing case
            elif player_score > 21 and dealer_score <= 21:
                reward = -1
            # winning case
            elif player_score <= 21 and (
                    dealer_score > 21 or player_score > dealer_score):
                reward = 1
            # losing case
            elif dealer_score <= 21 and player_score < dealer_score:
                reward = -1

            # Updates Q-Learning
            self.__q.update(state, choice, state, reward)

        self.__clear_hands()

    def start(self):
        """
        Starts n games of blackjack.
        It Learns the Q-learning for x games in case it's chosen as the AI.
        Otherwise it Runs MDP on each games.
        """
        if self.__agent == "mdp":
            for i in tqdm(range(self.__games_num), desc='MDP Game Progress',
                          ascii=False, ncols=125):
                self.game()

        elif self.__agent == "ql":
            self.__is_training = True
            # train about 100k games
            for i in tqdm(range(100000), desc='Q-learning Learning Progress',
                          ascii=False, ncols=125):
                self.game()
            self.__is_training = False
            # stop training
            for i in tqdm(range(self.__games_num),
                          desc='Q-learning Game Progress',
                          ascii=False, ncols=125):
                self.game()

        print(
            f"Total games are: {self.__games_num}.\n"
            f"AI won {self.__player.get_score()} games.\n"
            f"Dealer won {self.__dealer.get_score()} games.\n"
            f"AI got tied with the dealer "
            f"{self.__games_num - self.__dealer.get_score() - self.__player.get_score()} times.\n"
            f"The percentage of AI wins excluding ties: " +
            "{:.2f}".format((self.__player.get_score() / (
                    self.__player.get_score() + self.__dealer.get_score())) * 100) +
            f"%")

        self.__clear_hands()


if __name__ == "__main__":
    AI_mode = sys.argv[1]
    AI_games_num = int(sys.argv[2])
    game = Round(AI_mode, AI_games_num)
    game.start()
