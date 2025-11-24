import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

# ==========================================
# CONFIGURATION
# ==========================================
DATASET_FILE = 'dataset.csv'
MODEL_FILE = 'model.pkl'
ENCODER_FILE = 'encoders.pkl'
SCALER_FILE = 'scaler.pkl'
TARGET_COLUMN = 'travel_time' # The column we want to predict

# TOGGLES
USE_SCALING = True # Set to False if you don't want to scale numerical features

def train_model():
    # 1. Load Dataset
    # ------------------------------------------
    try:
        df = pd.read_csv(DATASET_FILE)
    except FileNotFoundError:
        print(f"Error: {DATASET_FILE} not found.")
        return

    # 2. Separate Features (X) and Target (y)
    # ------------------------------------------
    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]

    # 3. Preprocessing: Encoding Categorical Data
    # ------------------------------------------
    # We use LabelEncoder for simplicity. 
    # For Regression, OneHotEncoding (pd.get_dummies) is often better theoretically,
    # but LabelEncoder is easier to manage for simple templates.
    encoders = {}
    for col in X.columns:
        if X[col].dtype == 'object':
            print(f"Encoding categorical column: {col}")
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col])
            encoders[col] = le
    
    # Save encoders for use in app.py
    with open(ENCODER_FILE, 'wb') as f:
        pickle.dump(encoders, f)

    # 4. Preprocessing: Scaling Numerical Data (Optional)
    # ------------------------------------------
    # Linear Regression often converges faster and coefficients are more interpretable with scaling.
    if USE_SCALING:
        print("Scaling numerical features...")
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
        
        # Save scaler
        with open(SCALER_FILE, 'wb') as f:
            pickle.dump(scaler, f)
    else:
        # If not using scaling, we might want to delete any old scaler file to avoid confusion
        import os
        if os.path.exists(SCALER_FILE):
            os.remove(SCALER_FILE)

    # 5. Split Data
    # ------------------------------------------
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 6. Train Model
    # ------------------------------------------
    model = LinearRegression()
    print("Training Linear Regression Model...")
    model.fit(X_train, y_train)

    # 7. Evaluate
    # ------------------------------------------
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Mean Squared Error: {mse:.4f}")
    print(f"R2 Score: {r2:.4f}")

    # 8. Save Model
    # ------------------------------------------
    with open(MODEL_FILE, 'wb') as f:
        pickle.dump(model, f)
    print(f"Model saved to {MODEL_FILE}")

if __name__ == "__main__":
    train_model()
