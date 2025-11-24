from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

MODEL_FILE = 'model.pkl'
ENCODER_FILE = 'encoders.pkl'

# Load model
try:
    with open(MODEL_FILE, 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    model = None
    print(f"Warning: {MODEL_FILE} not found. Predictions will fail.")

# Load encoders
try:
    with open(ENCODER_FILE, 'rb') as f:
        encoders = pickle.load(f)
except FileNotFoundError:
    encoders = {}
    print(f"Warning: {ENCODER_FILE} not found.")

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
        if model:
            try:
                # Extract features from form
                # Ensure these match the input names in index.html and the order in training
                # We need to handle both numerical and categorical inputs
                
                # Example: Hardcoded list of features expected by the model
                # In a real scenario, you might store the feature names in a config file
                # For this template, we assume the form sends 'feature_1', 'feature_2', etc.
                
                # Let's dynamically grab keys from the form that start with 'feature_'
                # Or better, just grab all form values in order (risky if order changes)
                
                # Ideally, we know the feature names. Let's assume the user updates this list:
                feature_names = ['feature_1', 'feature_2', 'feature_3', 'feature_4', 'feature_cat']
                
                input_data = []
                for name in feature_names:
                    val = request.form.get(name)
                    
                    # Apply encoding if this feature has an encoder
                    if name in encoders:
                        try:
                            val = encoders[name].transform([val])[0]
                        except ValueError:
                            return render_template('index.html', prediction=f"Error: Unknown category '{val}' for {name}")
                    else:
                        val = float(val)
                    
                    input_data.append(val)
                
                # Reshape for prediction (1 sample, n features)
                features_array = np.array(input_data).reshape(1, -1)
                
                # Predict
                pred = model.predict(features_array)[0]
                prediction = f"Class {pred}"
            except Exception as e:
                prediction = f"Error: {str(e)}"
        else:
            prediction = "Model not loaded. Please train the model first."

    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
