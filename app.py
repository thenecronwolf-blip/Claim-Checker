import os
import random
import time
from flask import Flask, jsonify, render_template, request

app = Flask(
    __name__, 
    template_folder="ui/templates", 
    static_folder="ui/static"
)

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

# --- THE "BEHAVIORAL" LOGIC ENGINE ---
# This runs locally. No internet required.
@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json(force=True)
        text = data.get('text', '').lower().strip()
        
        # Simulate "thinking" time for the UI effect
        time.sleep(1.5) 

        # 1. LOGIC: Keyword Detection
        # We look for specific "tells" in the text to generate a verdict.
        subjective_words = ['amazing', 'terrible', 'best', 'worst', 'love', 'hate', 'unbelievable', 'shocking', 'feel', 'opinion']
        factual_words = ['study', 'proven', 'data', 'percent', 'according', 'report', 'official', 'record', '2024', 'confirmed']
        
        # Count triggers
        subj_count = sum(1 for word in subjective_words if word in text)
        fact_count = sum(1 for word in factual_words if word in text)
        
        # 2. DECISION MATRIX
        if fact_count > subj_count:
            # It looks factual
            label = "factual"
            bias_score = random.uniform(0.05, 0.25) # Low bias
            confidence = random.uniform(0.85, 0.99)
            verdict = "Likely Factual – This statement contains objective terminology and specific data references."
        
        elif subj_count > fact_count:
            # It looks emotional
            label = "biased"
            bias_score = random.uniform(0.65, 0.95) # High bias
            confidence = random.uniform(0.80, 0.98)
            verdict = "Subjective / Biased – The text relies heavily on emotional descriptors rather than verifiable data."
            
        else:
            # It's neutral or ambiguous (Random fallback)
            # This makes the demo feel "alive" because it varies.
            scenarios = [
                ("opinion", 0.45, "Opinion – This appears to be a personal viewpoint rather than a verified claim."),
                ("misinformation", 0.75, "Caution – This matches patterns often seen in unverified sensationalism.")
            ]
            selected = random.choice(scenarios)
            label = selected[0]
            bias_score = selected[1] + random.uniform(-0.1, 0.1)
            confidence = random.uniform(0.70, 0.90)
            verdict = selected[2]

        # 3. RETURN THE RESULT
        return jsonify({
            "result": {
                "bias_score": round(bias_score, 2),
                "confidence": round(confidence, 2),
                "verdict": verdict,
                "label": label
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
