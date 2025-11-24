import pandas as pd
import pickle
import numpy as np

# ==========================================
# CONFIGURATION
# ==========================================
MODEL_FILE = 'model.pkl'
ENCODER_FILE = 'encoders.pkl'
SCALER_FILE = 'scaler.pkl'

# Define the features in the exact order they were trained on
FEATURE_NAMES = ['no_kills', 'damage', 'category']

def load_artifacts():
    try:
        with open(MODEL_FILE, 'rb') as f:
            model = pickle.load(f)
        with open(ENCODER_FILE, 'rb') as f:
            encoders = pickle.load(f)
        with open(SCALER_FILE, 'rb') as f:
            scaler = pickle.load(f)
        return model, encoders, scaler
    except FileNotFoundError:
        print("Error: Model, Encoders, or Scaler not found. Run train.py first.")
        return None, None, None

def get_user_input(encoders):
    user_data = {}
    print("\n--- Enter Feature Values ---")
    
    for feature in FEATURE_NAMES:
        val = input(f"{feature}: ")
        
        if feature in encoders:
            encoder = encoders[feature]
            try:
                encoded_val = encoder.transform([val])[0]
                user_data[feature] = encoded_val
            except ValueError:
                print(f"Error: Unknown category '{val}' for feature '{feature}'.")
                print(f"Valid options: {list(encoder.classes_)}")
                return None
        else:
            try:
                user_data[feature] = float(val)
            except ValueError:
                print(f"Error: Expected number for '{feature}'.")
                return None
                
    return pd.DataFrame([user_data], columns=FEATURE_NAMES)

def main():
    model, encoders, scaler = load_artifacts()
    if not model:
        return

    while True:
        print("\n=== Clustering Test Interface ===")
        
        input_df = get_user_input(encoders)
        if input_df is None:
            continue
            
        # Apply Scaling (K-Means almost always uses scaling)
        input_scaled = scaler.transform(input_df)
        
        cluster_id = model.predict(input_scaled)[0]
        print(f"\n✅ Assigned Cluster: {cluster_id}")
        
        # Optional: Print cluster center info if you want
        # center = model.cluster_centers_[cluster_id]
        # print(f"Cluster Center: {center}")
        
        cont = input("\nTest another? (y/n): ")
        if cont.lower() != 'y':
            break

if __name__ == "__main__":
    main()
