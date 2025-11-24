import pandas as pd
import numpy as np
import os

class QLearningAgent:
    def __init__(self, states, actions, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.states = states
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = pd.DataFrame(
            np.zeros((len(states), len(actions))), 
            index=states, 
            columns=actions
        )

    def choose_action(self, state, train=True):
        if train and np.random.uniform(0, 1) < self.epsilon:
            return np.random.choice(self.actions)
        else:
            # Exploit: Choose best action for current state
            state_values = self.q_table.loc[state]
            # Break ties randomly
            return np.random.choice(state_values[state_values == state_values.max()].index)

    def learn(self, state, action, reward, next_state=None):
        """
        Update Q-Value
        For recommendation (single step episodes), next_state is often irrelevant 
        or terminal, so Gamma term might be 0.
        """
        old_value = self.q_table.loc[state, action]
        
        # If there is a next state (multi-step), we look at max q there.
        # If single step, next_max is 0.
        next_max = 0
        if next_state is not None:
            next_max = self.q_table.loc[next_state].max()
            
        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
        self.q_table.loc[state, action] = new_value

    def save(self, filename):
        self.q_table.to_csv(filename)
        print(f"Q-Table saved to {filename}")

    def load(self, filename):
        if os.path.exists(filename):
            self.q_table = pd.read_csv(filename, index_col=0)
            print(f"Q-Table loaded from {filename}")
        else:
            print("No existing Q-Table found, starting fresh.")
