# class for a single state of the game
class State():
    def __init__(self, cards_shown, player_cards, dealer_card, deck, dealer_card_hidden, terminal):
        self.cards_shown = cards_shown
        self.player_cards = player_cards
        self.dealer_card = dealer_card
        self.deck = deck
        self.terminal = terminal
        self.dealer_card_hidden = dealer_card_hidden
        self.dealer_value = dealer_card + dealer_card_hidden

    def get_hand_value(self):
        return sum([card for card in self.player_cards])

    def get_count(self):
        res = 0
        for card in self.cards_shown:
            if card <= 6:
                res += 1
            elif card == 10:
                res -= 1
        return res

    def get_prob(self, value):
        """
        probability of getting a card with the value of value
        :param value: value
        :return: probability
        """
        res = 0.0
        for c in self.deck:
            if c == value:
                res += 0.018
        return res

    def get_dealer_value(self):
        return self.dealer_value

    def get_deck(self):
        return self.deck

    def get_cards_shown(self):
        return self.cards_shown

    def add_player_card(self, card):
        self.player_cards.append(card)

    def set_cards_shown(self, cards):
        self.cards_shown = cards

    def set_deck(self, cards):
        self.deck = cards

    def add_dealer_value(self, val):
        self.dealer_value += val

    def set_terminal(self, t):
        self.terminal = t

    def is_terminal(self):
        return self.terminal or self.get_hand_value() > 21

    def copy(self):
        """
        :return: copy of the current state
        """
        return State(self.cards_shown.copy(), self.player_cards.copy(), self.dealer_card, self.deck.copy(), self.dealer_card_hidden, self.terminal)