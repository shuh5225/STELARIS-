# Malicious URL Blocker

## Backend Setup (Flask API)

1. Install dependencies:
```bash
pip install flask pickle5 requests
```

2. Train your ML model (Random Forest/XGBoost) and save as `model.pkl`:
```python
import pickle
model = ... # your trained model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
```

3. Run the Flask API:
```bash
cd malicious-url-blocker
python app.py
```
API runs on `http://localhost:5000`

## Browser Extension Setup

1. Open Chrome → `chrome://extensions/`
2. Enable **Developer mode** (top right)
3. Click **Load unpacked** → Select the `malicious-url-blocker` folder
4. Extension is now active!

## How it Works

1. **Feature Extraction**: `extract_features(url)` - Add your ML features here
2. **Model Prediction**: Loads `model.pkl` - Returns 'Phishing', 'Defacement', or 'Benign'
3. **Real-time Blocking**: Extension monitors all navigation requests
4. **API Integration**: Calls Flask `/predict` for each URL
5. **Dynamic Rules**: Blocks malicious URLs instantly

## Customization

**Update ML Features** in `app.py`:
```python
def extract_features(url):
    # Add your 20-50 features here
    features = [...]
    return features
```

**Test the API**:
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "http://phishingsite.com"}'
```

## Production Deployment

1. Deploy Flask API to Heroku/Vercel with CORS
2. Update `FLASK_API_URL` in `background.js`
3. Submit extension to Chrome Web Store
