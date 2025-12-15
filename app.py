import os
import requests
from flask import Flask, jsonify, render_template, request

app = Flask(
    __name__, 
    template_folder="ui/templates", 
    static_folder="ui/static"
)

# Get a free API key from huggingface.co
HF_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
HF_HEADERS = {"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}

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

@app.route('/health')
def health():
    return "OK", 200

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json(force=True)
        text = data.get('text', '').strip()

        if not text:
            return jsonify({"error": "Please enter some text!"}), 400

        # Hugging Face API Logic
        payload = {
            "inputs": text,
            "parameters": {"candidate_labels": ["factual", "biased", "opinion", "misinformation"]}
        }
        
        response = requests.post(HF_API_URL, headers=HF_HEADERS, json=payload, timeout=10)
        output = response.json()

        if isinstance(output, dict) and "labels" in output:
            top_label = output['labels'][0]
            confidence = round(output['scores'][0], 2)
            
            verdict_map = {
                "factual": "Likely Factual – The statement appears objective.",
                "biased": "Bias Detected – This text contains subjective language.",
                "opinion": "Opinion – This appears to be a personal view.",
                "misinformation": "Caution – This matches patterns of misinformation."
            }

            # WRAP IN "result" KEY FOR UI COMPATIBILITY
            return jsonify({
                "result": {
                    "bias_score": confidence if top_label != "factual" else 1 - confidence,
                    "confidence": confidence,
                    "verdict": verdict_map.get(top_label, "Analysis complete.")
                }
            })
        else:
            # Handle model loading (Model is 500mb+, takes time to load on first hit)
            return jsonify({"error": "AI model is initializing. Please try again in 20 seconds."}), 503

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
