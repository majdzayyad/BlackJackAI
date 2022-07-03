import itertools
import state as s
import util

class MarkovDecisionProcess:
    def __init__(self, start):
        self.actions = ["Hit", "Stand"]
        self.start = start

    def get_start_state(self):
        return self.start

    def get_children(self, state):
        """
        function to get children states of a state
        :param state: state of game
        :return: list of all states that can be reached from the current state
        """
        res = []
        for action in self.get_possible_actions(state):
            for next_state, prob in self.get_states_probs(state, action):
                res.append(next_state)
        return res

    def get_states(self):
        """
        get all possible states of the game
        :return: list of all possible states
        """
        res = []
        state = self.start
        stack = util.Stack()
        stack.push(state)
        while not stack.isEmpty():
            state = stack.pop()
            for s in self.get_children(state):
                stack.push(s)
                res.append(s)
        return res


    def get_possible_actions(self, state):
        """
        list of possible actions that we can perform on the current states
        :param state: state
        :return: actions
        """
        if state.is_terminal():
            return []
        return ["Hit", "Stand"]

    def get_states_probs(self, state, action, initial_prob=1):
        """
        return a list of (next state, probability) pairs reachable by taking an action
        :param state: our state
        :param action: action we want to take
        :param initial_prob: probability we give to this state
        :return: list of (next state, probability) pairs
        """
        res = []
        if action == "Stand":
            next_state = state.copy()
            res.append((next_state, 1))

        elif action == "Hit":
            for i in range(len(state.get_deck())):
                new_state = state.copy()
                new_deck = state.get_deck().copy()
                new_deck.pop(i)
                new_shown = state.get_cards_shown().copy()
                new_shown.append(state.get_deck()[i])
                new_state.add_player_card(state.get_deck()[i])
                new_state.set_deck(new_deck)
                new_state.set_cards_shown(new_shown)
                prob = state.get_prob(state.get_deck()[i])
                res.extend(self.get_states_probs(new_state, "Stand", prob))
        return res

    def get_reward(self, state, action, next_state):
        """
        reward function for the reinforcement agent
        :param state: current state
        :param action: action taken to achieve next state
        :param next_state: the next state we achieve by taking the action
        :return: reward or penalty
        """
        if next_state == None or action == None:
            return state.get_hand_value()
        if next_state.get_hand_value() <= 21:
            if action == "Hit":
                return 1
            else:
                return 0
        else:
            return -1



