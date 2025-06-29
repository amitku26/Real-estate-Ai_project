# from flask import Flask
# from flask_cors import CORS
# from routes.predict import predict_bp
# import os

# app = Flask(__name__)
# CORS(app)
# app.register_blueprint(predict_bp, url_prefix="/api")

# if __name__ == "__main__":
#     app.run(port=5000, debug=True)

# port = int(os.environ.get("PORT", 5000))  # Use 5000 locally as default
# app.run(host="0.0.0.0", port=port)




from flask import Flask, request, jsonify
import pickle
import numpy as np
import os
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin access

# Load the trained model
try:
    with open("model/model.pkl", "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    raise RuntimeError("❌ model.pkl not found! Please place it in the backend folder.")

# Dummy risk scoring logic
def compute_risk_score(area, floodZone):
    risk = int((floodZone + (10000 - area) / 1000) * 10)
    return min(100, max(0, risk))

# Route for prediction
@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json()
    bhk = data.get("bhk")
    area = data.get("area")
    floodZone = data.get("floodZone")

    if bhk is None or area is None or floodZone is None:
        return jsonify({"error": "Missing input data"}), 400

    input_features = np.array([[bhk, area, floodZone]])
    predicted_price = model.predict(input_features)[0]
    risk_score = compute_risk_score(area, floodZone)

    return jsonify({
        "predicted_price": round(predicted_price, 2),
        "risk_score": risk_score
    })

# Run the app (important for Render)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use the PORT env variable if provided
    app.run(host="0.0.0.0", port=port)
