import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json(force=True)
    text = data.get('text', '')
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    Analyze this claim for bias and factual accuracy: "{text}"
    Return ONLY a JSON object with these keys: bias_score (0.0 to 1.0), confidence (0.0 to 1.0), and verdict (string).
    """
    
    response = model.generate_content(prompt)
    # ... parse the JSON response ...

import requests
from flask import Flask, jsonify, render_template, request

app = Flask(
    __name__, 
    template_folder="ui/templates", 
    static_folder="ui/static"
)

# Get a free API key from huggingface.com
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
    # ... setup code ...
    response = requests.post(HF_API_URL, headers=HF_HEADERS, json=payload)
    output = response.json()

    # If HF says it's loading, return that info to frontend IMMEDIATELY
    if isinstance(output, dict) and "error" in output and "loading" in output["error"].lower():
        estimated_time = output.get("estimated_time", 20.0)
        return jsonify({"error": "Model loading", "estimated_time": estimated_time}), 503

    if "labels" in output:
        # ... process your result ...
        return jsonify({"result": result})
    
    return jsonify({"error": "Unknown error"}), 500

else:
            # Handle model loading (Model is 500mb+, takes time to load on first hit)
            return jsonify({"error": "AI model is initializing. Please try again in 20 seconds."}), 503

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
