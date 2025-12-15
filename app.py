import os
import requests
from flask import Flask, jsonify, render_template, request

app = Flask(
    __name__, 
    template_folder="ui/templates", 
    static_folder="ui/static"
)

# --- CONFIGURATION ---
# We use the official Facebook model on the new Router URL.
# This model is 100% guaranteed to exist.
HF_API_URL = "https://router.huggingface.co/models/facebook/bart-large-mnli"
HF_HEADERS = {"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}

# --- PAGE ROUTES ---
@app.route("/")
def home():
    return render_template("index.html")

@app.route('/examples')
def examples():
    return render_template('examples.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/docs')
def docs():
    return render_template('docs.html')

@app.route('/donate')
def donate():
    return render_template('donate.html')

@app.route('/health')
def health():
    return "OK", 200

# --- API ROUTES ---
@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json(force=True)
        text = data.get('text', '').strip()

        if not text:
            return jsonify({"error": "Please enter some text!"}), 400

        payload = {
            "inputs": text,
            "parameters": {"candidate_labels": ["factual", "biased", "opinion", "misinformation"]}
        }
        
        # Call Hugging Face API
        response = requests.post(HF_API_URL, headers=HF_HEADERS, json=payload, timeout=20)
        
        # Handle Non-JSON Responses
        try:
            output = response.json()
        except:
            return jsonify({"error": f"External API Error: {response.text}"}), 500

        # Handle Model Loading State (503)
        if isinstance(output, dict) and "error" in output and "loading" in str(output.get("error")).lower():
            estimated_time = output.get("estimated_time", 15.0)
            return jsonify({"error": "Model loading", "estimated_time": estimated_time}), 503

        # Process Success
        if isinstance(output, dict) and "labels" in output:
            top_label = output['labels'][0]
            confidence = round(output['scores'][0], 2)
            
            verdict_map = {
                "factual": "Likely Factual – The statement appears objective.",
                "biased": "Bias Detected – This text contains subjective language.",
                "opinion": "Opinion – This appears to be a personal view.",
                "misinformation": "Caution – This matches patterns of misinformation."
            }

            result = {
                "bias_score": confidence if top_label != "factual" else 1 - confidence,
                "confidence": confidence,
                "verdict": verdict_map.get(top_label, "Analysis complete.")
            }
            return jsonify({"result": result})

        return jsonify({"error": f"API Error: {output}"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
