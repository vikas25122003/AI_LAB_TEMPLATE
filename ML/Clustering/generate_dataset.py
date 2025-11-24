import pandas as pd
import numpy as np
from sklearn.datasets import make_blobs

# ==========================================
# CONFIGURATION
# ==========================================
OUTPUT_FILE = 'dataset.csv'
NUM_ROWS = 10
NUM_CLUSTERS = 3 

# Feature Configuration
# Define ranges for your numerical features here
# The KEYS here will become your COLUMN NAMES in the CSV
FEATURE_RANGES = {
    'no_kills': (0, 1000),  # e.g., Annual Income
    'damage': (1, 100)    # e.g., Spending Score
}

def generate_data():
    # We use make_blobs to create distinct clusters
    # However, make_blobs creates data centered around 0 or random centers.
    # To respect our custom ranges, we will generate random data first, 
    # but that won't have clusters.
    
    # BETTER APPROACH for Clustering Template:
    # Use make_blobs to get the structure, then scale it to our desired ranges.
    
    feature_names = list(FEATURE_RANGES.keys())
    n_features = len(feature_names)
    
    data_blobs, labels = make_blobs(n_samples=NUM_ROWS, centers=NUM_CLUSTERS, n_features=n_features, random_state=42)
    
    # Scale to custom ranges
    # This is a bit manual but ensures the data looks like "Income" vs "Age" etc.
    for i, feat_name in enumerate(feature_names):
        feat_col = data_blobs[:, i]
        min_target, max_target = FEATURE_RANGES[feat_name]
        
        # Min-Max Scaling to target range
        min_orig = feat_col.min()
        max_orig = feat_col.max()
        
        # Formula: (x - min) / (max - min) * (new_max - new_min) + new_min
        if max_orig != min_orig:
            data_blobs[:, i] = (feat_col - min_orig) / (max_orig - min_orig) * (max_target - min_target) + min_target
        else:
            data_blobs[:, i] = min_target

    df = pd.DataFrame(data_blobs, columns=feature_names)
    
    # We can add a categorical column to show how to handle it (by encoding)
    # though K-Means purely on categorical data is tricky, usually we encode it.
    df['category'] = np.random.choice(['Attacker', 'Defender','AllRounder'], size=NUM_ROWS)
    
    # Note: In clustering, we usually don't have a 'target' label in real life.
    # But we'll save the true label for verification if we want.
    df['true_cluster'] = labels
    
    print(f"Generating clustering dataset with {NUM_ROWS} rows and {NUM_CLUSTERS} centers...")
    print(df.head())
    
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Dataset saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_data()
