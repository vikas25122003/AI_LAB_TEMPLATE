import pandas as pd
import pickle
import os
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# ==========================================
# CONFIGURATION
# ==========================================
DATASET_FILE = 'dataset.csv'
MODEL_FILE = 'model.pkl'
ENCODER_FILE = 'encoders.pkl'
SCALER_FILE = 'scaler.pkl'
TARGET_COLUMN = 'price'
SAMPLE_SIZE = 20 

def calculate_metrics():
    # 1. Load Data and Artifacts
    try:
        df = pd.read_csv(DATASET_FILE)
        with open(MODEL_FILE, 'rb') as f: model = pickle.load(f)
        
        encoders = {}
        if os.path.exists(ENCODER_FILE):
            with open(ENCODER_FILE, 'rb') as f: encoders = pickle.load(f)
            
        scaler = None
        if os.path.exists(SCALER_FILE):
            with open(SCALER_FILE, 'rb') as f: scaler = pickle.load(f)
            
    except FileNotFoundError as e:
        print(f"Error loading files: {e}")
        return

    # 2. Select Sample
    if SAMPLE_SIZE:
        df_sample = df.head(SAMPLE_SIZE)
    else:
        df_sample = df

    X = df_sample.drop(columns=[TARGET_COLUMN])
    y_true = df_sample[TARGET_COLUMN]

    # 3. Apply Preprocessing (Encoding)
    for col in X.columns:
        if col in encoders:
            X[col] = encoders[col].transform(X[col])

    # 4. Apply Preprocessing (Scaling)
    if scaler:
        X = scaler.transform(X)

    # 5. Predict
    y_pred = model.predict(X)

    # 6. Calculate Metrics
    mse = mean_squared_error(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)

    print("\n--- Regression Metrics ---")
    print(f"Mean Squared Error (MSE): {mse:.4f}")
    print(f"Mean Absolute Error (MAE): {mae:.4f}")
    print(f"R2 Score: {r2:.4f}")
    
    # Show side-by-side comparison for first few
    print("\n--- Sample Predictions ---")
    print(f"{'Actual':<15} | {'Predicted':<15}")
    print("-" * 35)
    for actual, pred in zip(y_true[:5], y_pred[:5]):
        print(f"{actual:<15.2f} | {pred:<15.2f}")

if __name__ == "__main__":
    calculate_metrics()
