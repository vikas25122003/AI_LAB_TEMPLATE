import pandas as pd
import pickle
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# Configuration
DATASET_FILE = 'dataset.csv'
MODEL_FILE = 'model.pkl'
ENCODER_FILE = 'encoders.pkl'
TARGET_COLUMN = 'survival_rate'
SAMPLE_SIZE = 10 # Set to None to use full dataset

def calculate_metrics():
    # Load dataset
    try:
        df = pd.read_csv(DATASET_FILE)
    except FileNotFoundError:
        print(f"Error: {DATASET_FILE} not found.")
        return

    # Load model
    try:
        with open(MODEL_FILE, 'rb') as f:
            model = pickle.load(f)
    except FileNotFoundError:
        print(f"Error: {MODEL_FILE} not found.")
        return

    # Load encoders
    try:
        with open(ENCODER_FILE, 'rb') as f:
            encoders = pickle.load(f)
    except FileNotFoundError:
        encoders = {}
        print(f"Warning: {ENCODER_FILE} not found.")

    # Select data
    if SAMPLE_SIZE:
        print(f"Using first {SAMPLE_SIZE} rows for calculation...")
        df_sample = df.head(SAMPLE_SIZE)
    else:
        print("Using full dataset for calculation...")
        df_sample = df

    X = df_sample.drop(columns=[TARGET_COLUMN])
    y_true = df_sample[TARGET_COLUMN]

    # Apply encoding to features
    for col in X.columns:
        if col in encoders:
            X[col] = encoders[col].transform(X[col])

    # Predict
    y_pred = model.predict(X)

    # Calculate metrics
    # Note: For multiclass, average='weighted' or 'macro' might be needed for precision/recall/f1
    # Assuming binary or handling automatically for simple cases
    
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, average='weighted', zero_division=0)
    rec = recall_score(y_true, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
    cm = confusion_matrix(y_true, y_pred)

    print("\n--- Metrics ---")
    print(f"Accuracy:  {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall:    {rec:.4f}")
    print(f"F1 Score:  {f1:.4f}")
    print("\nConfusion Matrix:")
    print(cm)

if __name__ == "__main__":
    calculate_metrics()
