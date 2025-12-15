import os
import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__, template_folder="ui/templates", static_folder="ui/static")

# Get a free API key from huggingface.co
HF_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
HF_HEADERS = {"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json(force=True)
        text = data.get('text', '').strip()

        if not text:
            return jsonify({"error": "Please enter some text!"}), 400

        # REAL LOGIC: Check the text against specific labels
        payload = {
            "inputs": text,
            "parameters": {"candidate_labels": ["factual", "biased", "opinion", "misinformation"]}
        }
        
        response = requests.post(HF_API_URL, headers=HF_HEADERS, json=payload)
        output = response.json()

        # Extract top label and score
        if "labels" in output:
            top_label = output['labels'][0]
            confidence = round(output['scores'][0], 2)
            
            # Map labels to user-friendly verdicts
            verdict_map = {
                "factual": "Likely Factual – The statement appears objective.",
                "biased": "Bias Detected – This text contains subjective language.",
                "opinion": "Opinion – This appears to be a personal view.",
                "misinformation": "Caution – This matches patterns of misinformation."
            }
            
            return jsonify({
                "bias_score": confidence if top_label != "factual" else 1 - confidence,
                "confidence": confidence,
                "verdict": verdict_map.get(top_label, "Analysis complete.")
            })
        else:
            return jsonify({"error": "AI model is warming up, try again in a moment."}), 503

    except Exception as e:
        return jsonify({"error": str(e)}), 500
