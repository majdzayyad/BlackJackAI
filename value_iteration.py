import util as util
#value Iteration agent
class ValueIteration:
    def __init__(self, mdp, discount=0.127, iterations=10):
        """
        constructor to initialize the counter for the value iteration agent
        :param mdp: the mdp of the game
        :param discount: discount value
        :param iterations: number of iterations to perform
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # where all the values of each state will be stored

        for it in range(iterations):
            v_next = util.Counter()
            for s in self.mdp.get_children(self.mdp.get_start_state()):
                max_sum = 0
                v_s = 0
                act = None
                nex = None
                action = None
                for a in self.mdp.get_possible_actions(s):
                    curr_sum = sum([(self.values[pair[0]] * pair[1]) for pair in self.mdp.get_states_probs(s, a)])
                    if curr_sum > max_sum:
                        max_sum = curr_sum
                        v_s = (self.discount * max_sum)
                        action = a
                v_next[s] = v_s + self.mdp.get_reward(s, action, None)
            self.values = v_next

    def get_value(self, state): # get value of current state
        return self.values[state]

    def get_q_value(self, state, action):
        """
        get q value of current state when action is applied to it
        :param state:
        :param action:
        :return: value in value iteration dictionary
        """
        res = self.mdp.get_reward(state, action, None)
        if action == None:
            return res
        return res + sum(
            [self.values[pair[0]] * pair[1] for pair in self.mdp.get_states_probs(state, action)])

    def get_policy(self, state):
        """
        get the best possible action to take on this state base on our value iterations
        :param state:
        :return: best possible action
        """
        if state.is_terminal():
            return "Stand"
        return max([a for a in self.mdp.get_possible_actions(state)], key= lambda x: self.get_q_value(state, x))
