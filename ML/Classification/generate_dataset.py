import pandas as pd
import numpy as np
import random

# Configuration
OUTPUT_FILE = 'dataset.csv'
NUM_ROWS = 10
LABEL_NAME = 'survival_rate'
LABEL_TYPE = 'binary' # 'binary' or 'multiclass'
LABEL_NAMES = ['yes', 'no'] # For binary

# Feature Configuration
# Define ranges for your numerical features here
# The KEYS here will become your COLUMN NAMES in the CSV
FEATURE_RANGES = {
    'age': (0, 100),           # Column 'age'
    'income': (20000, 80000) # Column 'family_size'
}

def generate_data():
    data = {}
    
    # 1. Generate Numerical Features based on FEATURE_RANGES
    numerical_cols = []
    for feat_name, (min_val, max_val) in FEATURE_RANGES.items():
        data[feat_name] = np.random.uniform(min_val, max_val, NUM_ROWS)
        numerical_cols.append(feat_name)
    
    # 2. Add a categorical feature (Optional - you can remove or rename this)
    data['water_level'] = np.random.choice(['High', 'Medium', 'Low'], size=NUM_ROWS)

    df = pd.DataFrame(data)
    
    # 3. Generate Labels based on logic
    # We sum the numerical columns to create a synthetic rule
    linear_combo = df[numerical_cols].sum(axis=1) + np.random.normal(0, 0.5, NUM_ROWS)
    
    if LABEL_TYPE == 'binary':
        # If sum is above average, classify as 1, else 0
        threshold = linear_combo.mean()
        df[LABEL_NAME] = (linear_combo > threshold).astype(int)
    else:
        # Multiclass logic
        df[LABEL_NAME] = pd.qcut(linear_combo, len(LABEL_NAMES), labels=False)
        
    print(f"Generating dataset with {NUM_ROWS} rows...")
    print(f"Features: {list(data.keys())}")
    print(f"Labels: {df[LABEL_NAME].unique()}")
    
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Dataset saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_data()
