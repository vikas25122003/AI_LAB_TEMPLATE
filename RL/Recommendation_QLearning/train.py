from environment import RecommendationEnv, STATES, ACTIONS
from agent import QLearningAgent

# ==========================================
# TRAINING CONFIGURATION
# ==========================================
EPISODES = 50
ALPHA = 0.1
GAMMA = 0.0 # 0 because recommendation is usually immediate reward (no future steps)
EPSILON = 0.2
Q_TABLE_FILE = 'qtable.csv'

def train():
    env = RecommendationEnv()
    agent = QLearningAgent(STATES, ACTIONS, ALPHA, GAMMA, EPSILON)
    
    print(f"Starting training for {EPISODES} episodes...")
    
    for episode in range(EPISODES):
        state = env.reset()
        action = agent.choose_action(state)
        
        reward, done = env.step(action)
        
        # Update Q-Table
        agent.learn(state, action, reward)
        
        if (episode + 1) % 50 == 0:
            print(f"Episode {episode+1}: User={state}, Rec={action}, Reward={reward}")

    agent.save(Q_TABLE_FILE)
    print("\nFinal Q-Table:")
    print(agent.q_table)

if __name__ == "__main__":
    train()
