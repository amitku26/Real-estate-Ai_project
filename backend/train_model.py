import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestRegressor

# Step 1: Dummy training dataset
# Columns: bhk, area, floodZone
data = {
    "bhk": [1, 2, 3, 4, 5],
    "area": [600, 900, 1200, 1500, 1800],
    "floodZone": [0, 1, 0, 2, 1],
    "price": [25, 45, 65, 85, 105]  # Price in Lakhs
}

df = pd.DataFrame(data)

# Step 2: Features and label
X = df[["bhk", "area", "floodZone"]]
y = df["price"]

# Step 3: Train the model
model = RandomForestRegressor()
model.fit(X, y)

# Step 4: Save the trained model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ model.pkl created successfully!")
#   hwfgwekwk