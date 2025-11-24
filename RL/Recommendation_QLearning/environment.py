import numpy as np
import random

# ==========================================
# CONFIGURATION
# ==========================================
# States: Different types of users or contexts
STATES = ['white_town', 'PTU']

# Actions: Recommendations we can make
ACTIONS = ['high_acc', 'high_braking']

# Reward Logic (The "Truth" we want the agent to learn)
# Format: {State: {Action: Reward}}
# We can configure this to simulate how the world responds
REWARD_MAP = {
    'white_town': {
        'high_acc': 10,  # Loves cheap cars
        'high_braking': -5,      # Can't afford
       # Likes it but can't afford (mixed feeling)
    },
    'PTU': {
        'high_acc': 5,  # Loves cheap cars
        'high_braking': 10,      # Can't afford
       # Likes it but can't afford (mixed feeling)
    }
}

class RecommendationEnv:
    def __init__(self):
        self.states = STATES
        self.actions = ACTIONS
        self.current_state = None

    def reset(self):
        """Randomly selects a new user profile (State)"""
        self.current_state = random.choice(self.states)
        return self.current_state

    def step(self, action):
        """
        Returns (reward, done)
        In recommendation, usually one interaction is one episode (done=True immediately)
        """
        if self.current_state is None:
            raise Exception("Call reset() first")
            
        reward = REWARD_MAP[self.current_state].get(action, 0)
        
        # Add some randomness/noise to simulate real world inconsistency
        # e.g., sometimes a Family might actually buy a Sports Car
        if random.random() < 0.1: 
            reward += np.random.choice([-2, 2])
            
        return reward, True # Episode ends after recommendation
