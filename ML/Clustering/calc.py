import pandas as pd
import pickle
import os
from sklearn.metrics import silhouette_score

# ==========================================
# CONFIGURATION
# ==========================================
DATASET_FILE = 'dataset.csv'
MODEL_FILE = 'model.pkl'
ENCODER_FILE = 'encoders.pkl'
SCALER_FILE = 'scaler.pkl'
IGNORE_COLS = ['true_cluster']

def calculate_metrics():
    # 1. Load
    try:
        df = pd.read_csv(DATASET_FILE)
        with open(MODEL_FILE, 'rb') as f: model = pickle.load(f)
        
        encoders = {}
        if os.path.exists(ENCODER_FILE):
            with open(ENCODER_FILE, 'rb') as f: encoders = pickle.load(f)
            
        scaler = None
        if os.path.exists(SCALER_FILE):
            with open(SCALER_FILE, 'rb') as f: scaler = pickle.load(f)
            
    except FileNotFoundError:
        print("Error loading files.")
        return

    # 2. Prepare Data (Same as training)
    X = df.drop(columns=[c for c in IGNORE_COLS if c in df.columns], errors='ignore')

    # Encode
    for col in X.columns:
        if col in encoders:
            X[col] = encoders[col].transform(X[col])

    # Scale
    if scaler:
        X_scaled = scaler.transform(X)
    else:
        X_scaled = X

    # 3. Predict Clusters
    labels = model.predict(X_scaled)

    # 4. Calculate Metrics
    # Silhouette Score: How similar an object is to its own cluster compared to other clusters.
    # Range: -1 to 1. Higher is better.
    score = silhouette_score(X_scaled, labels)
    
    # Inertia: Sum of squared distances of samples to their closest cluster center.
    # Lower is better (but depends on k).
    inertia = model.inertia_

    print("\n--- Clustering Metrics ---")
    print(f"Silhouette Score: {score:.4f}")
    print(f"Inertia: {inertia:.4f}")
    
    print("\n--- Cluster Counts ---")
    print(pd.Series(labels).value_counts().sort_index())

if __name__ == "__main__":
    calculate_metrics()
