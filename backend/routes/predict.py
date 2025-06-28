from flask import Blueprint, request, jsonify
import pickle
from utils.risk_score import compute_risk_score

predict_bp = Blueprint("predict", __name__)

with open("model/model.pkl", "rb") as f:
    model = pickle.load(f)

@predict_bp.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    try:
        features = [[data["bhk"], data["area"], data["floodZone"]]]
        price = model.predict(features)[0]
        risk = compute_risk_score(data["floodZone"])
        return jsonify({"predicted_price": round(price, 2), "risk_score": risk})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
