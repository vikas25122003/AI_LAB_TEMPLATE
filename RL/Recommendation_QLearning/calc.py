from environment import RecommendationEnv, STATES, ACTIONS
from agent import QLearningAgent
import pandas as pd

Q_TABLE_FILE = 'qtable.csv'
SIMULATION_STEPS = 5

def calculate_step_by_step():
    env = RecommendationEnv()
    agent = QLearningAgent(STATES, ACTIONS)
    agent.load(Q_TABLE_FILE)
    
    print(f"\n--- Simulating {SIMULATION_STEPS} Recommendations ---")
    
    for i in range(SIMULATION_STEPS):
        print(f"\n[Step {i+1}]")
        
        # 1. New User Arrives
        state = env.reset()
        print(f"Context/State: {state}")
        
        # 2. Agent Checks Q-Table
        q_values = agent.q_table.loc[state]
        print(f"Agent Q-Values for {state}:")
        print(q_values.to_dict())
        
        # 3. Agent Decides
        action = agent.choose_action(state, train=False) # Exploit only
        print(f"Action Chosen: {action}")
        
        # 4. Environment Responds
        reward, done = env.step(action)
        print(f"Reward Received: {reward}")
        
        # 5. Calculation Check
        # Q_new = (1-alpha)*Q_old + alpha*(Reward)
        # We show what the update WOULD be if we were training
        alpha = 0.1
        old_q = q_values[action]
        new_q = (1 - alpha) * old_q + alpha * reward
        print(f"Hypothetical Update: {old_q:.2f} -> {new_q:.2f}")

if __name__ == "__main__":
    calculate_step_by_step()
