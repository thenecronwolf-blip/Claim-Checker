from flask import Flask, jsonify, render_template, request

app = Flask(
    __name__,
    template_folder="ui/templates",
    static_folder="ui/static"
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/health', endpoint='health_check')  # Explicit unique endpoint
def health():
    return "OK", 200
@app.route('/examples')
def examples():
    return render_template('examples.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/docs')
def docs():
    return render_template('docs.html')
@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json(force=True)
        text = data.get('text', '').strip() if data else ''

        if not text:
            return jsonify({"error": "Please enter some text to analyze!"}), 400

        # Fun varying result based on input (replace with real HF later)
        length = len(text)
        bias_score = round(0.3 + (length % 70) / 100, 2)
        confidence = round(0.7 + (length % 40) / 100, 2)

        verdicts = [
            "Low potential bias – appears balanced",
            "Moderate potential bias detected",
            "Potential bias detected – review sources recommended",
            "High potential bias – strong language noted"
        ]
        verdict = verdicts[length % len(verdicts)]

        result = {
            "bias_score": bias_score,
            "confidence": confidence,
            "verdict": verdict
        }

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": f"Analysis error: {str(e)}"}), 500
