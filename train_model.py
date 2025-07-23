import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# === 1. Create sample training data ===
data = {
    'amount': [100, 200, 5000, 7000, 150, 8000],
    'location': [0, 0, 1, 1, 0, 1],   # 0 = local, 1 = risky location
    'is_fraud': [0, 0, 1, 1, 0, 1]    # Label: 1 = fraud, 0 = normal
}

df = pd.DataFrame(data)

# === 2. Features & labels ===
X = df[['amount', 'location']]
y = df['is_fraud']

# === 3. Train RandomForest ===
model = RandomForestClassifier()
model.fit(X, y)

# === 4. Save the model to file ===
with open('fraud_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Model trained & saved as fraud_model.pkl")
