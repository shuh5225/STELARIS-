import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Create dummy model for testing
X_train = np.random.rand(1000, 6)  # 1000 samples, 6 features
y_train = np.random.choice(['Benign', 'Phishing', 'Defacement'], 1000)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save dummy model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Dummy model.pkl created for testing!")
print("Features used: [url_length, num_dots, has_ip, num_slashes, num_equals, path_length]")
print("Replace with your real trained model.")
