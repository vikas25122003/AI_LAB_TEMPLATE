import numpy as np
import pandas as pd
from environment import GridWorld, ACTIONS, GRID_SIZE

# ==========================================
# Q-LEARNING CONFIGURATION
# ==========================================
ALPHA = 0.1       # Learning Rate
GAMMA = 0.9       # Discount Factor
EPSILON = 0.1     # Exploration Rate
EPISODES = 1000   # Number of training episodes
Q_TABLE_FILE = 'qtable.csv'

def train_agent():
    env = GridWorld()
    num_states = GRID_SIZE * GRID_SIZE
    num_actions = len(ACTIONS)
    
    # Initialize Q-Table with zeros
    q_table = np.zeros((num_states, num_actions))
    
    print(f"Starting training for {EPISODES} episodes...")
    
    for episode in range(EPISODES):
        state_idx = env.reset()
        done = False
        
        while not done:
            # Epsilon-Greedy Strategy
            if np.random.uniform(0, 1) < EPSILON:
                # Explore: Random action
                action_idx = np.random.randint(0, num_actions)
            else:
                # Exploit: Best known action
                # Add some noise to break ties randomly instead of always taking the first one
                values = q_table[state_idx]
                action_idx = np.random.choice(np.flatnonzero(values == values.max()))
            
            # Take action
            next_state_idx, reward, done = env.step(action_idx)
            
            # Q-Learning Update Rule
            # Q(s,a) = Q(s,a) + alpha * (R + gamma * max(Q(s', a')) - Q(s,a))
            
            old_value = q_table[state_idx, action_idx]
            next_max = np.max(q_table[next_state_idx])
            
            new_value = (1 - ALPHA) * old_value + ALPHA * (reward + GAMMA * next_max)
            q_table[state_idx, action_idx] = new_value
            
            state_idx = next_state_idx
            
        if (episode + 1) % 100 == 0:
            print(f"Episode {episode + 1}/{EPISODES} completed.")

    # Save Q-Table to CSV
    # Rows are States, Columns are Actions
    df = pd.DataFrame(q_table, columns=ACTIONS)
    df.to_csv(Q_TABLE_FILE, index=False)
    print(f"Training complete. Q-Table saved to {Q_TABLE_FILE}")

if __name__ == "__main__":
    train_agent()
