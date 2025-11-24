import pandas as pd
import numpy as np

# ==========================================
# CONFIGURATION
# ==========================================
OUTPUT_FILE = 'dataset.csv'
NUM_ROWS = 10
TARGET_NAME = 'travel_time' # The continuous value we want to predict

# Feature Configuration
# Define ranges for your numerical features here
# The KEYS here will become your COLUMN NAMES in the CSV
FEATURE_RANGES = {
    'distance': (500, 2000), # e.g., Square Footage
    'speed': (10, 50),        # e.g., Age of house
}

def generate_data():
    data = {}
    
    # 1. Generate Numerical Features
    # ------------------------------------------
    numerical_cols = []
    for feat_name, (min_val, max_val) in FEATURE_RANGES.items():
        data[feat_name] = np.random.uniform(min_val, max_val, NUM_ROWS)
        numerical_cols.append(feat_name)
    
    # 2. Generate Categorical Features (Optional)
    # ------------------------------------------
    # Useful to test encoding. Comment out if not needed.
    data['location'] = np.random.choice(['Urban', 'Suburban', 'Rural'], size=NUM_ROWS)

    df = pd.DataFrame(data)
    
    # 3. Generate Target Variable (Logic)
    # ------------------------------------------
    # We create a linear relationship: y = m1*x1 + m2*x2 ... + noise
    # We also add a simple effect for the categorical variable
    
    # Base price
    target_val = 10
    
    # Add feature effects dynamically
    for col in numerical_cols:
        target_val += np.random.uniform(1, 10) * df[col]
    
    # Add categorical effect
    # Urban adds 500, Suburban adds 200, Rural adds 0
    
    # Add random noise
    target_val += np.random.normal(0, 50, NUM_ROWS)
    
    df[TARGET_NAME] = target_val
    
    print(f"Generating regression dataset with {NUM_ROWS} rows...")
    print(df.head())
    
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Dataset saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_data()
