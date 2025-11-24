from flask import Flask, render_template, request
import pickle
import numpy as np
import os

app = Flask(__name__)

# ==========================================
# CONFIGURATION
# ==========================================
MODEL_FILE = 'model.pkl'
ENCODER_FILE = 'encoders.pkl'
SCALER_FILE = 'scaler.pkl'

def load_artifacts():
    model, encoders, scaler = None, {}, None
    if os.path.exists(MODEL_FILE):
        with open(MODEL_FILE, 'rb') as f: model = pickle.load(f)
    if os.path.exists(ENCODER_FILE):
        with open(ENCODER_FILE, 'rb') as f: encoders = pickle.load(f)
    if os.path.exists(SCALER_FILE):
        with open(SCALER_FILE, 'rb') as f: scaler = pickle.load(f)
    return model, encoders, scaler

model, encoders, scaler = load_artifacts()

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
        if model:
            try:
                # 1. Define Features (Must match training order!)
                feature_names = ['feature_1', 'feature_2', 'category']
                
                input_data = []
                for name in feature_names:
                    val = request.form.get(name)
                    
                    # 2. Encode
                    if name in encoders:
                        try:
                            val = encoders[name].transform([val])[0]
                        except ValueError:
                            return render_template('index.html', prediction=f"Error: Unknown category '{val}'")
                    else:
                        val = float(val)
                    input_data.append(val)
                
                # 3. Scale
                features_array = np.array(input_data).reshape(1, -1)
                if scaler:
                    features_array = scaler.transform(features_array)
                
                # 4. Predict Cluster
                cluster_id = model.predict(features_array)[0]
                prediction = f"Belongs to Cluster #{cluster_id}"
                
            except Exception as e:
                prediction = f"Error: {str(e)}"
        else:
            prediction = "Model not loaded."

    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
