from flask import Flask
from flask_cors import CORS
from routes.predict import predict_bp
import os

app = Flask(__name__)
CORS(app)
app.register_blueprint(predict_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(port=5000, debug=True)

port = int(os.environ.get("PORT", 5000))  # Use 5000 locally as default
app.run(host="0.0.0.0", port=port)

