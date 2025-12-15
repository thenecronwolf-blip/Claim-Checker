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
        data = request.get_json(force=True)  # force=True ignores Content-Type header issues
        text = data.get('text', '').strip() if data else ''

        if not text:
            return jsonify({"error": "No text provided – please enter a claim to analyze."}), 400

        # Your real Hugging Face analysis code here...
        # Temporary placeholder so you can test the flow
        result = {
            "bias_score": 0.72,
            "confidence": 0.89,
            "verdict": "Potential bias detected – review sources recommended"
        }

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": f"Something went wrong: {str(e)}"}), 500
