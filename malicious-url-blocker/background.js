// Background service worker for Manifest V3
// Monitors navigation requests and calls Flask API

const FLASK_API_URL = 'http://localhost:5001/predict';
const BLOCKED_URLS = new Set();

// Check URL with Flask API and block if necessary
async function checkUrlAndBlock(url, tabId, frameId) {
  try {
    const response = await fetch(FLASK_API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: url })
    });
    
    const result = await response.json();
    
    console.log(`[URL Check] ${url} - Prediction: ${result.prediction}, Block: ${result.block}`);
    
    if (result.block) {
      BLOCKED_URLS.add(url);
      
      // Create a blocking rule
      const ruleId = Math.abs(url.hashCode()) % 1000000;
      
      try {
        await chrome.declarativeNetRequest.updateDynamicRules({
          removeRuleIds: [ruleId],
          addRules: [{
            id: ruleId,
            priority: 1,
            action: {
              type: 'redirect',
              redirect: { url: chrome.runtime.getURL('blocked.html?url=' + encodeURIComponent(url) + '&reason=' + result.prediction) }
            },
            condition: {
              urlFilter: url,
              resourceTypes: ['main_frame']
            }
          }]
        });
        
        console.log(`✓ Blocked ${url} - Reason: ${result.prediction}`);
      } catch (ruleError) {
        console.error('Error creating block rule:', ruleError);
      }
    }
  } catch (error) {
    console.error('API call failed:', error);
  }
}

// Listen for web navigation events
chrome.webNavigation.onBeforeNavigate.addListener((details) => {
  const url = details.url;
  const tabId = details.tabId;
  const frameId = details.frameId;
  
  // Check suspicious URLs (skip localhost, extensions, etc.)
  if (shouldCheckUrl(url)) {
    checkUrlAndBlock(url, tabId, frameId);
  }
});

function shouldCheckUrl(url) {
  try {
    const parsed = new URL(url);
    // Skip safe domains and local
    const skipDomains = ['localhost', '127.0.0.1', 'chrome-extension://', 'chrome://', 'chrome-error://', 'about:'];
    return !skipDomains.some(domain => url.includes(domain));
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

console.log('✓ Malicious URL Blocker extension loaded and connected to Flask at ' + FLASK_API_URL);
