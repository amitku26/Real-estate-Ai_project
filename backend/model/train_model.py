# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestRegressor
# import pickle

# # Load your dataset
# data = pd.read_csv("../../data/real_estate_data.csv")
# X = data[["bhk", "area", "floodZone"]]
# y = data["price"]

# model = RandomForestRegressor()
# model.fit(X, y)

# with open("model.pkl", "wb") as f:
#     pickle.dump(model, f)




# 📁 backend/model/train_model.py
import pandas as pd 
from sklearn.ensemble import RandomForestRegressor 
import pickle

# Load your dataset (adjust path as needed)
data = pd.read_csv("../../data/real_estate_data.csv")

# Features and target
X = data[["bhk", "area", "floodZone"]]
y = data["price"]

# Train model
model = RandomForestRegressor()
model.fit(X, y)

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ model.pkl created successfully")
