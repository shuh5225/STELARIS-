// Background service worker for Manifest V3
// Monitors navigation requests and calls Flask API

const FLASK_API_URL = 'http://localhost:5000/predict';

// Update rules dynamically based on API response
async function checkUrlAndUpdateRules(url) {
  try {
    const response = await fetch(FLASK_API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: url })
    });
    
    const result = await response.json();
    
    if (result.block) {
      // Add rule to block this URL
      chrome.declarativeNetRequest.updateDynamicRules({
        removeRuleIds: [result.url.hashCode()], // Use URL hash as rule ID
        addRules: [{
          id: result.url.hashCode(),
          priority: 1,
          action: {
            type: 'redirect',
            redirect: { regexSubstitution: '^https?://' + escapeRegex(urlparse(url).hostname) + '(:\\d+)?/?' }
          },
          condition: {
            urlFilter: url,
            resourceTypes: ['main_frame', 'sub_frame']
          }
        }]
      });
      
      console.log(`Blocked ${url} - ${result.prediction}`);
    }
  } catch (error) {
    console.error('API call failed:', error);
    // Fallback: allow navigation
  }
}

// Listen for navigation events
chrome.webNavigation.onBeforeNavigate.addListener((details) => {
  const url = details.url;
  
  // Check suspicious URLs (skip localhost, extensions, etc.)
  if (shouldCheckUrl(url)) {
    checkUrlAndUpdateRules(url);
  }
});

function shouldCheckUrl(url) {
  try {
    const parsed = new URL(url);
    // Skip safe domains and local
    const skipDomains = ['localhost', '127.0.0.1', 'chrome-extension://', 'chrome://'];
    return !skipDomains.some(domain => parsed.hostname.includes(domain));
  } catch {
    return false;
  }
}

// Utility functions
String.prototype.hashCode = function() {
  let hash = 0;
  for (let i = 0; i < this.length; i++) {
    const char = this.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32-bit integer
  }
  return Math.abs(hash);
};

function urlparse(urlStr) {
  try {
    return new URL(urlStr);
  } catch {
    return { hostname: urlStr };
  }
}

function escapeRegex(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

console.log('Malicious URL Blocker loaded');
