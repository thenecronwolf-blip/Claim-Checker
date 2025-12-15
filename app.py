import os
import requests
from flask import Flask, jsonify, render_template, request

# Initialize Flask with explicit folder paths
app = Flask(
    __name__, 
    template_folder="ui/templates", 
    static_folder="ui/static"
)

# --- CONFIGURATION ---
# Using the updated Router URL to avoid "No longer supported" errors
HF_API_URL = "https://router.huggingface.co/models/valhalla/distilbart-mnli-12-1"
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
        # 1. Input Validation
        data = request.get_json(force=True)
        text = data.get('text', '').strip()

        if not text:
            return jsonify({"error": "Please enter some text!"}), 400

        # 2. Construct Payload
        payload = {
            "inputs": text,
            "parameters": {"candidate_labels": ["factual", "biased", "opinion", "misinformation"]}
        }
        
        # 3. Call Hugging Face API
        response = requests.post(HF_API_URL, headers=HF_HEADERS, json=payload, timeout=20)
        
        # 4. Handle Non-JSON Responses (like 404s or 503s from HF)
        try:
            output = response.json()
        except:
            # This catches the exact error you are seeing ("Not JSON")
            return jsonify({"error": f"External API Error: {response.text}"}), 500

        # 5. Handle Model Loading State
        if isinstance(output, dict) and "error" in output and "loading" in str(output.get("error")).lower():
            estimated_time = output.get("estimated_time", 15.0)
            return jsonify({"error": "Model loading", "estimated_time": estimated_time}), 503

        # 6. Process Success
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

        # 7. Catch-all for other API errors
        return jsonify({"error": f"API Error: {output}"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
