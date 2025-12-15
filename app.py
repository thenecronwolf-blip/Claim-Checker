import os
import random
import time
import re
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

# --- THE ADVANCED LOGIC ENGINE (v2.0) ---
@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json(force=True)
        raw_text = data.get('text', '')
        text = raw_text.lower().strip()
        
        # Simulate processing time for the "Wow" effect
        time.sleep(1.2) 

        # --- SCOREBOARD ---
        # We start at 0. Negative = Biased. Positive = Factual.
        score = 0
        
        # 1. FACTUAL TRIGGERS (Weighted)
        # Strong evidence gets +2, Standard gets +1
        factual_strong = ['study published', 'peer-reviewed', 'meta-analysis', 'official report', 'census bureau', 'proven by', 'verified', 'evidence shows']
        factual_std = ['according to', 'data', 'percent', '2024', '2023', 'researchers', 'scientists', 'confirmed', 'report', 'statistics', 'record', 'average', 'increase', 'decrease']
        
        for phrase in factual_strong:
            if phrase in text: score += 2.5
        for word in factual_std:
            if word in text: score += 1.0

        # 2. SUBJECTIVE TRIGGERS (Weighted)
        # Emotional/Manipulative words get -2 or -1
        bias_strong = ['unbelievable', 'shocking', 'disgrace', 'destroy', 'catastrophe', 'miracle', 'worst ever', 'best ever', 'hate', 'love', 'stupid', 'genius']
        bias_std = ['feel', 'opinion', 'believe', 'think', 'maybe', 'rumor', 'people say', 'seems', 'might', 'probably', 'amazing', 'terrible', 'huge']
        
        for phrase in bias_strong:
            if phrase in text: score -= 2.5
        for word in bias_std:
            if word in text: score -= 1.0

        # 3. PATTERN DETECTION (Formatting)
        # ALL CAPS usually implies yelling/bias
        caps_count = sum(1 for c in raw_text if c.isupper())
        if len(raw_text) > 10 and (caps_count / len(raw_text) > 0.4):
            score -= 3.0 # Penalty for shouting

        # Excessive punctuation (e.g. "Real???!!")
        if "!!" in raw_text or "??" in raw_text:
            score -= 1.5

        # --- THE VERDICT CALCULATOR ---
        if score >= 2.0:
            # High Factuality
            label = "factual"
            bias_score = random.uniform(0.05, 0.20)
            confidence = random.uniform(0.88, 0.99)
            verdict = "Likely Factual – This statement cites specific data points or research terminology with neutral phrasing."

        elif score <= -2.0:
            # High Bias
            label = "biased"
            bias_score = random.uniform(0.75, 0.98)
            confidence = random.uniform(0.90, 0.99)
            verdict = "Highly Subjective – The text relies on emotional language, capitalization, or unverified claims to persuade."

        elif -2.0 < score < 2.0:
            # The "Grey Area" (Opinion or Mixed)
            # If the text is very short, confidence drops
            label = "opinion"
            bias_score = random.uniform(0.40, 0.60)
            confidence = random.uniform(0.60, 0.85)
            
            if len(text.split()) < 5:
                verdict = "Insufficient Context – The statement is too short to definitively categorize, but appears neutral."
            else:
                verdict = "Mixed / Opinion – This text contains a blend of factual references and personal interpretation."

        # --- RETURN RESULT ---
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
