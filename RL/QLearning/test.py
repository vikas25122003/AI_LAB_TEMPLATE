import numpy as np
import pandas as pd
from environment import ACTIONS, GRID_SIZE

# ==========================================
# CONFIGURATION
# ==========================================
Q_TABLE_FILE = 'qtable.csv'

def load_q_table():
    try:
        # Try loading as CSV first (if saved by pandas)
        df = pd.read_csv(Q_TABLE_FILE, header=None)
        return df.values
    except:
        try:
            # Try loading as npy (if saved by numpy)
            return np.load('qtable.npy')
        except:
            print("Error: Could not load Q-Table.")
            return None

def get_best_action(q_table, state_idx):
    # Get Q-values for this state
    q_values = q_table[state_idx]
    # Find index of max value
    best_action_idx = np.argmax(q_values)
    return ACTIONS[best_action_idx], q_values

def main():
    q_table = load_q_table()
    if q_table is None:
        return

    print(f"Loaded Q-Table with shape: {q_table.shape}")
    
    while True:
        print("\n=== Q-Learning Agent Test ===")
        print(f"Grid Size: {GRID_SIZE}x{GRID_SIZE}")
        
        try:
            row = int(input(f"Enter Row (0-{GRID_SIZE-1}): "))
            col = int(input(f"Enter Col (0-{GRID_SIZE-1}): "))
            
            if row < 0 or row >= GRID_SIZE or col < 0 or col >= GRID_SIZE:
                print("Invalid coordinates.")
                continue
                
            # Convert (row, col) to state index
            state_idx = row * GRID_SIZE + col
            
            action, values = get_best_action(q_table, state_idx)
            
            print(f"\n🤖 Best Action: {action}")
            print(f"Q-Values: {values}")
            
        except ValueError:
            print("Please enter valid integers.")
        
        cont = input("\nTest another state? (y/n): ")
        if cont.lower() != 'y':
            break

if __name__ == "__main__":
    main()
