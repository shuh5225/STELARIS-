from flask import Flask, request, jsonify
import pickle
import requests
from urllib.parse import urlparse
import re

app = Flask(__name__)

# Placeholder for ML model (save your trained model as 'model.pkl')
model = None

def load_model():
    global model
    try:
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
        print("Model loaded successfully")
    except FileNotFoundError:
        print("model.pkl not found. Please train and save your model.")
        # Return a dummy model for testing
        model = lambda x: 'Benign'  # Placeholder

def extract_features(url):
    """
    Placeholder for feature extraction.
    Replace this with your ML feature extraction logic (e.g., URL length, domain age, etc.).
    Returns a feature vector expected by your model.
    """
    # Example dummy features: [url_length, num_dots, has_ip, etc.]
    features = [
        len(url),
        url.count('.'),
        1 if re.match(r'\d+\.\d+\.\d+\.\d+', urlparse(url).netloc) else 0,
        url.count('/'),
        url.count('='),
        len(urlparse(url).path)
    ]
    return features  # Return list or array of numerical features

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    url = data.get('url', '')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    # Extract features (replace with your logic)
    features = extract_features(url)
    
    # Predict (replace with your model prediction)
    if model:
        prediction = model(features)
    else:
        prediction = 'Benign'  # Fallback
    
    # Determine if should block
    should_block = prediction in ['Phishing', 'Defacement']
    
    return jsonify({
        'url': url,
        'prediction': prediction,
        'block': should_block
    })

if __name__ == '__main__':
    load_model()
    app.run(debug=True, port=5000)
