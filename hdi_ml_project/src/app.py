from flask import Flask, render_template, request
import pickle
import numpy as np
import os

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Load the pickle model
model_path = 'hdi_model.pkl'
if os.path.exists(model_path):
    with open(model_path, 'rb') as f:
        ml_model = pickle.load(f)
else:
    ml_model = None

def get_development_tier(score):
    if score >= 0.800: return "Very High Human Development (Scenario 1)"
    elif score >= 0.700: return "High Human Development"
    elif score >= 0.550: return "Medium Human Development (Scenario 2)"
    else: return "Low Human Development (Scenario 3)"

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction_text = None
    tier_text = None
    
    if request.method == 'POST':
        if ml_model is None:
            return render_template('index.html', error="Model file missing. Run training process first.")
            
        try:
            # Extract inputs from web form
            inputs = [
                float(request.form['life_expectancy']),
                float(request.form['mean_schooling']),
                float(request.form['expected_schooling']),
                float(request.form['gni_per_capita'])
            ]
            
            # Machine Learning Inference Prediction
            features = [np.array(inputs)]
            predicted_score = ml_model.predict(features)[0]
            predicted_score = round(float(predicted_score), 3)
            
            prediction_text = f"Predicted HDI Score: {predicted_score}"
            tier_text = f"Classification: {get_development_tier(predicted_score)}"
            
        except Exception as e:
            prediction_text = f"Error processing prediction input details: {str(e)}"
            
    return render_template('index.html', prediction=prediction_text, tier=tier_text)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
