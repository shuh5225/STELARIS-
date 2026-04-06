from flask import Flask, request, jsonify
import pickle
import requests
from urllib.parse import urlparse
import re

app = Flask(__name__)

model = None

class URLClassifier:
    """Simple ML model for URL classification"""
    def predict(self, features):
        # Simple heuristic-based classification
        # features: [url_length, dot_count, is_ip, slash_count, equals_count, path_length]
        if len(features) >= 6:
            url_length, dot_count, is_ip, slash_count, equals_count, path_length = features[:6]
            
            # Heuristics for detecting malicious URLs
            suspicious_score = 0
            
            # Unusually long URLs are often suspicious
            if url_length > 75:
                suspicious_score += 1
            
            # Multiple equals signs suggest parameter injection
            if equals_count > 3:
                suspicious_score += 2
            
            # IP-based URLs are sometimes suspicious
            if is_ip:
                suspicious_score += 1
            
            # Many slashes suggest directory traversal attempts
            if slash_count > 6:
                suspicious_score += 1
            
            if suspicious_score >= 3:
                return 'Phishing'
            elif suspicious_score >= 1:
                return 'Defacement'
        
        return 'Benign'

def load_model():
    global model
    try:
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
        print("✓ Model loaded successfully")
    except (FileNotFoundError, pickle.UnpicklingError, AttributeError) as e:
        print(f"⚠ Could not load model.pkl ({e}), using default classifier")
        model = URLClassifier()  

def extract_features(url):
    features = [
        len(url),
        url.count('.'),
        1 if re.match(r'\d+\.\d+\.\d+\.\d+', urlparse(url).netloc) else 0,
        url.count('/'),
        url.count('='),
        len(urlparse(url).path)
    ]
    return features 

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    url = data.get('url', '')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    features = extract_features(url)
    if model:
        prediction = model.predict(features)
    else:
        prediction = 'Benign'
    should_block = prediction in ['Phishing', 'Defacement']
    
    return jsonify({
        'url': url,
        'prediction': prediction,
        'block': should_block
    })

if __name__ == '__main__':
    load_model()
    app.run(debug=True, port=5001)
