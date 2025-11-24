import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# Configuration
DATASET_FILE = 'dataset.csv'
MODEL_FILE = 'model.pkl'
ENCODER_FILE = 'encoders.pkl'
TARGET_COLUMN = 'survival_rate' # The column we want to predict

def train_model():
    # Load dataset
    try:
        df = pd.read_csv(DATASET_FILE)
    except FileNotFoundError:
        print(f"Error: {DATASET_FILE} not found. Run generate_dataset.py first.")
        return

    # Separate features and target
    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]

    # Preprocessing: Label Encoding for Categorical Features
    encoders = {}
    for col in X.columns:
        if X[col].dtype == 'object':
            print(f"Encoding categorical column: {col}")
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col])
            encoders[col] = le
    
    # Save encoders
    with open(ENCODER_FILE, 'wb') as f:
        pickle.dump(encoders, f)
    print(f"Encoders saved to {ENCODER_FILE}")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train classifier
    clf = DecisionTreeClassifier(random_state=42)
    print("Training Decision Tree Classifier...")
    clf.fit(X_train, y_train)

    # Evaluate
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.4f}")

    # Save model
    with open(MODEL_FILE, 'wb') as f:
        pickle.dump(clf, f)
    print(f"Model saved to {MODEL_FILE}")

if __name__ == "__main__":
    train_model()
