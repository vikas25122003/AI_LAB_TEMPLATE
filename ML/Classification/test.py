import pandas as pd
import pickle
import numpy as np

# ==========================================
# CONFIGURATION
# ==========================================
MODEL_FILE = 'model.pkl'
ENCODER_FILE = 'encoders.pkl'

# Define the features in the exact order they were trained on
# You must match the columns from your dataset.csv
FEATURE_NAMES = ['age', 'income', 'water_level']

def load_artifacts():
    try:
        with open(MODEL_FILE, 'rb') as f:
            model = pickle.load(f)
        with open(ENCODER_FILE, 'rb') as f:
            encoders = pickle.load(f)
        return model, encoders
    except FileNotFoundError:
        print("Error: Model or Encoders not found. Run train.py first.")
        return None, None

def get_user_input(encoders):
    user_data = {}
    print("\n--- Enter Feature Values ---")
    
    for feature in FEATURE_NAMES:
        val = input(f"{feature}: ")
        
        # Check if this feature needs encoding
        if feature in encoders:
            encoder = encoders[feature]
            try:
                # Transform input using the encoder
                # We wrap in list because transform expects an array
                encoded_val = encoder.transform([val])[0]
                user_data[feature] = encoded_val
            except ValueError:
                print(f"Error: Unknown category '{val}' for feature '{feature}'.")
                print(f"Valid options: {list(encoder.classes_)}")
                return None
        else:
            # Assume numerical
            try:
                user_data[feature] = float(val)
            except ValueError:
                print(f"Error: Expected number for '{feature}'.")
                return None
                
    # Convert to DataFrame with correct column order
    return pd.DataFrame([user_data], columns=FEATURE_NAMES)

def main():
    model, encoders = load_artifacts()
    if not model:
        return

    while True:
        print("\n=== Classification Test Interface ===")
        print("Type 'exit' to quit.")
        
        # Check if user wants to exit before asking for inputs
        # (A bit tricky inside the loop, so we'll handle exit inside get_user_input or just Ctrl+C)
        
        input_df = get_user_input(encoders)
        if input_df is None:
            continue
            
        prediction = model.predict(input_df)
        print(f"\n✅ Prediction: {prediction[0]}")
        
        cont = input("\nTest another? (y/n): ")
        if cont.lower() != 'y':
            break

if __name__ == "__main__":
    main()
