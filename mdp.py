import itertools
import util

class MarkovDecisionProcess:
    def __init__(self, start, deck):
        self.actions = ["Hit", "Stand"]
        self.start = start
        self.deck = deck

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
        return ["Hit", "Stand"]

    def get_states_probs(self, state, action):
        """
        return a list of (next state, probability) pairs reachable by taking an action
        :param state: our state
        :param action: action we want to take
        :param initial_prob: probability we give to this state
        :return: list of (next state, probability) pairs
        """
        res = []
        if action == "Stand":
            return [((state[0],state[1],state[2]), 1)]

        elif action == "Hit":
            total = sum(self.deck.values())
            for card in self.deck:
                if self.deck[card] >= 0 and total > 0:
                    res.append(((state[0]+card, state[1], state[2]), self.deck[card]/total))
        return res

    def get_reward(self, state):
        if state[0] > 21:
            return -1
        if state[0] > 13:
            return 1
        return 0





