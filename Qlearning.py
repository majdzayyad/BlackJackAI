import util
import random
class QLearningAgent:
    def __init__(self, alpha, discount):
        self.Qvalues = util.Counter()
        self.alpha = alpha
        self.discount = discount

        #initializing the qvalues of the state combinations
        #state = ((player hand, dealer card, ace or not), action)
        #state = (player_sum (int), dealer_card (str))
    def getQValue(self, state, action):
        return self.Qvalues[(state, action)]

    def getLegalActions(self, state):
        if state[0] >= 21:
            return ["Stand"]
        return ["Stand", "Hit"]

    def getValue(self, state):
        if len(self.getLegalActions(state)) == 0:
            return 0.0
        max_val = max([self.getQValue(state, action) for action in self.getLegalActions(state)])
        return max_val

    def getPolicy(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        if len(self.getLegalActions(state)) == 0:
            return None
        choices_list = []
        for action in self.getLegalActions(state):
            if self.getQValue(state, action) == self.getValue(state):
                choices_list.append(action)
        return random.choice(choices_list)

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        if util.flipCoin(self.epsilon):
            return random.choice(legalActions)
        action = self.getPolicy(state)
        return action

    def update(self, state, action, nextState, reward):
        res = ((1 - self.alpha) * self.Qvalues[(state, action)]) + self.alpha * (
                    reward + (self.discount * self.getValue(nextState)))
        self.Qvalues[(state, action)] = res
