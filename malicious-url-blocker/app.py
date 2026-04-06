from flask import Flask, request, jsonify
import pickle
import requests
from urllib.parse import urlparse
import re

app = Flask(__name__)

model = None

def load_model():
    global model
    try:
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
        print("Model loaded successfully")
    except FileNotFoundError:
        print("model.pkl not found. Please train and save your model.")

        model = lambda x: 'Benign'  

def extract_features(url):
      [
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
        prediction = model(features)
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
    app.run(debug=True, port=5000)
