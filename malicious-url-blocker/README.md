# 🛡️ Malicious URL Blocker - Browser Extension

A Chrome browser extension that uses machine learning to detect and block malicious URLs in real-time. The extension intercepts navigation requests, sends them to a Flask backend for analysis, and prevents users from accessing dangerous websites.

## 🚀 Quick Start

### Backend Setup (Flask API)

The Flask backend runs on **port 5001** and provides URL classification.

#### 1. Install Python dependencies:
```bash
cd malicious-url-blocker
pip install -r requirements.txt
```

#### 2. Start the Flask server:
```bash
python3 app.py
```

You should see:
```
✓ Model loaded successfully
 * Running on http://127.0.0.1:5001
```

### Frontend Setup (Browser Extension)

#### 1. Open Chrome and go to `chrome://extensions/`

#### 2. Enable "Developer mode" (toggle in top-right corner)

#### 3. Click "Load unpacked" and select this folder (`malicious-url-blocker`)

#### 4. The extension should now appear in your extensions list with a shield icon ✓

### 📋 How It Works

1. **URL Interception**: When you navigate to a URL, the extension's background script intercepts it
2. **Flask API Call**: The URL is sent to the Flask backend at `http://localhost:5001/predict`
3. **Classification**: The ML model analyzes the URL and returns:
   - `Benign` - Safe to visit
   - `Phishing` - Credential harvesting attempt
   - `Defacement` - Website tampering/malware
4. **Blocking**: If malicious, the URL is blocked and redirected to a warning page
5. **Warning Page**: User sees details about the threat and can go home or back

### 🧪 Testing the API

**Test with a benign URL:**
```bash
curl http://localhost:5001/predict -X POST \
  -H "Content-Type: application/json" \
  -d '{"url":"http://example.com"}'
```

Response:
```json
{
    "url": "http://example.com",
    "prediction": "Benign",
    "block": false
}
```

**Test with a suspicious URL (many parameters):**
```bash
curl http://localhost:5001/predict -X POST \
  -H "Content-Type: application/json" \
  -d '{"url":"http://example.com/login?user=admin&pass=123&token=xyz&verify=true"}'
```

Response:
```json
{
    "url": "http://example.com/login?user=admin&pass=123&token=xyz&verify=true",
    "prediction": "Defacement",
    "block": true
}
```

### 📊 Classification Logic

The URL classifier uses heuristic-based analysis with the following signals:

| Signal | Suspicious Score |
|--------|------------------|
| URL length > 75 characters | +1 |
| More than 3 query parameters | +2 |
| IP-based URL | +1 |
| More than 6 path segments | +1 |

**Classification thresholds:**
- Score ≥ 3: **Phishing** (blocked)
- Score ≥ 1: **Defacement** (blocked)
- Score < 1: **Benign** (allowed)

### 📁 File Structure

```
malicious-url-blocker/
├── app.py                 # Flask backend server
├── background.js          # Extension background worker
├── blocked.html           # Warning page for blocked URLs
├── manifest.json          # Extension configuration
├── model.pkl             # Pickled ML model
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

### 🔧 Configuration

**To change the Flask port**, edit `app.py`:
```python
app.run(debug=True, port=5001)  # Change 5001 to desired port
```

Then update `background.js`:
```javascript
const FLASK_API_URL = 'http://localhost:5001/predict';  // Update port
```

### ⚠️ Important Notes

1. Flask must be running for the extension to work
2. The extension only works for `http://` and `https://` URLs
3. Local addresses (localhost, 127.0.0.1) are skipped
4. Chrome-specific URLs are skipped
5. The warning page displays in place of the blocked URL

### 🐛 Troubleshooting

**Extension not blocking URLs?**
- Check that Flask is running: `lsof -i :5001`
- Open Chrome DevTools (F12) → Extensions tab → Click on extension → Check console logs
- Verify Flask is responding: `curl http://localhost:5001/predict -X POST -d '{"url":"http://test.com"}'`

**Port 5001 already in use?**
```bash
# Find and kill the process
lsof -i :5001
kill -9 <PID>

# Or use a different port (don't forget to update both app.py and background.js)
```

**Model.pkl errors?**
- The extension will use a default heuristic classifier if model loading fails
- Check Flask logs for pickle errors

### 📝 License
This project is part of the STELARIS cybersecurity initiative.

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
