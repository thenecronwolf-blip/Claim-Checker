import os
import requests
from flask import Flask, jsonify, render_template, request

app = Flask(
    __name__, 
    template_folder="ui/templates", 
    static_folder="ui/static"
)

# Option 1: Using the FASTER DistilBART model
HF_API_URL = "https://api-inference.huggingface.co/models/valhalla/distilbart-mnli-12-1"
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

        # Define the payload (This was missing in your snippet!)
        payload = {
            "inputs": text,
            "parameters": {"candidate_labels": ["factual", "biased", "opinion", "misinformation"]}
        }
        
        # Call Hugging Face
        response = requests.post(HF_API_URL, headers=HF_HEADERS, json=payload, timeout=20)
        output = response.json()

        # CHECK 1: Is the model loading?
        if isinstance(output, dict) and "error" in output and "loading" in str(output.get("error")).lower():
            # Send a specific 503 error so the frontend knows to wait
            estimated_time = output.get("estimated_time", 15.0)
            return jsonify({"error": "Model loading", "estimated_time": estimated_time}), 503

        # CHECK 2: Did we get a valid result?
        if isinstance(output, dict) and "labels" in output:
            top_label = output['labels'][0]
            confidence = round(output['scores'][0], 2)
            
            verdict_map = {
                "factual": "Likely Factual – The statement appears objective.",
                "biased": "Bias Detected – This text contains subjective language.",
                "opinion": "Opinion – This appears to be a personal view.",
                "misinformation": "Caution – This matches patterns of misinformation."
            }

            # Return the Clean Result
            result = {
                "bias_score": confidence if top_label != "factual" else 1 - confidence,
                "confidence": confidence,
                "verdict": verdict_map.get(top_label, "Analysis complete.")
            }
            return jsonify({"result": result})

        # Fallback if the API returns something unexpected
        return jsonify({"error": f"API Error: {output}"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
