import pandas as pd
import numpy as np
from environment import STATES, ACTIONS

# ==========================================
# CONFIGURATION
# ==========================================
Q_TABLE_FILE = 'qtable.csv'

def load_q_table():
    try:
        # The agent saves it as a CSV with index=True (User Types as index)
        df = pd.read_csv(Q_TABLE_FILE, index_col=0)
        return df
    except FileNotFoundError:
        print("Error: qtable.csv not found. Run train.py first.")
        return None

def main():
    q_table = load_q_table()
    if q_table is None:
        return

    print("Loaded Q-Table:")
    print(q_table)
    
    while True:
        print("\n=== Recommendation System Test ===")
        print("Available User Types:", STATES)
        
        user_type = input("Enter User Type: ")
        
        if user_type not in STATES:
            print("Invalid User Type.")
            continue
            
        # Look up in Q-Table
        # The Q-Table rows are User Types, Columns are Products
        if user_type in q_table.index:
            user_q_values = q_table.loc[user_type]
            best_product = user_q_values.idxmax()
            max_val = user_q_values.max()
            
            print(f"\n🎁 Recommended Product: {best_product}")
            print(f"Confidence (Q-Value): {max_val:.4f}")
        else:
            print("User type not found in Q-Table.")

        cont = input("\nTest another user? (y/n): ")
        if cont.lower() != 'y':
            break

if __name__ == "__main__":
    main()
