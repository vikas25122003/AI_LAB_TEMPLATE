import pandas as pd
import pickle
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder, StandardScaler
import matplotlib.pyplot as plt

# ==========================================
# CONFIGURATION
# ==========================================
DATASET_FILE = 'dataset.csv'
MODEL_FILE = 'model.pkl'
ENCODER_FILE = 'encoders.pkl'
SCALER_FILE = 'scaler.pkl'
K_CLUSTERS = 3 # Number of clusters to find

# Columns to IGNORE during training (e.g., ID, or the true label if it exists)
IGNORE_COLS = ['true_cluster'] 

def train_model():
    # 1. Load Dataset
    try:
        df = pd.read_csv(DATASET_FILE)
    except FileNotFoundError:
        print(f"Error: {DATASET_FILE} not found.")
        return

    # 2. Prepare Features
    # Drop columns we don't want to cluster on
    X = df.drop(columns=[c for c in IGNORE_COLS if c in df.columns], errors='ignore')

    # 3. Encoding Categorical Data
    # ------------------------------------------
    encoders = {}
    for col in X.columns:
        if X[col].dtype == 'object':
            print(f"Encoding categorical column: {col}")
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col])
            encoders[col] = le
            
    with open(ENCODER_FILE, 'wb') as f:
        pickle.dump(encoders, f)

    # 4. Scaling (CRITICAL for K-Means)
    # ------------------------------------------
    # K-Means calculates distances. If one feature is 0-1 and another is 0-1000,
    # the second feature will dominate. Scaling makes them equal.
    print("Scaling features...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    with open(SCALER_FILE, 'wb') as f:
        pickle.dump(scaler, f)

    # 5. Train K-Means
    # ------------------------------------------
    print(f"Training K-Means with k={K_CLUSTERS}...")
    kmeans = KMeans(n_clusters=K_CLUSTERS, random_state=42)
    kmeans.fit(X_scaled)

    # 6. Save Model
    with open(MODEL_FILE, 'wb') as f:
        pickle.dump(kmeans, f)
    print(f"Model saved to {MODEL_FILE}")
    
    # Optional: Print cluster centers (in scaled space)
    print("Cluster Centers (Scaled):")
    print(kmeans.cluster_centers_)

if __name__ == "__main__":
    train_model()
