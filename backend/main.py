import os
from flask import Flask, request, jsonify, send_from_directory
from huggingface_hub import InferenceClient

HF_API_KEY = os.getenv("HF_API_KEY")
client = None  # We will initialize on first request

app = Flask(__name__, static_folder="../ui", static_url_path="")

# Serve frontend
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

# Lazy-loading HF model
def get_client():
    global client
    if client is None:
        client = InferenceClient(token=HF_API_KEY)
    return client

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    try:
        hf_client = get_client()
        result = hf_client.text_classification(
            model="distilbert-base-uncased-finetuned-sst-2-english",
            inputs=text
        )
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
