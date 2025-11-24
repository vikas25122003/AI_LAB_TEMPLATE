import pandas as pd
import numpy as np
import time
from environment import GridWorld, ACTIONS

# ==========================================
# SIMULATION CONFIGURATION
# ==========================================
Q_TABLE_FILE = 'qtable.csv'
SIMULATION_EPISODES = 4

def simulate_agent():
    # Load Q-Table
    try:
        df = pd.read_csv(Q_TABLE_FILE)
        q_table = df.values
    except FileNotFoundError:
        print(f"Error: {Q_TABLE_FILE} not found. Run agent.py first.")
        return

    env = GridWorld()
    
    print(f"--- Starting Simulation for {SIMULATION_EPISODES} Episodes ---")
    print("Agent will always choose the best action (Exploitation).")
    
    for ep in range(SIMULATION_EPISODES):
        state_idx = env.reset()
        done = False
        total_reward = 0
        steps = 0
        
        print(f"\n=== Episode {ep + 1} ===")
        print(f"Start State: {env.index_to_state(state_idx)}")
        
        path = [env.index_to_state(state_idx)]
        
        while not done:
            # Always choose best action
            action_idx = np.argmax(q_table[state_idx])
            action_name = ACTIONS[action_idx]
            
            next_state_idx, reward, done = env.step(action_idx)
            
            print(f"Step {steps+1}: State {env.index_to_state(state_idx)} -> Action {action_name} -> Reward {reward} -> Next State {env.index_to_state(next_state_idx)}")
            
            total_reward += reward
            state_idx = next_state_idx
            steps += 1
            path.append(env.index_to_state(state_idx))
            
            if steps > 20: # Safety break for infinite loops if model is bad
                print("... Too many steps, stopping episode ...")
                break
                
        print(f"Episode Finished. Total Reward: {total_reward}")
        print(f"Path: {path}")

if __name__ == "__main__":
    simulate_agent()
