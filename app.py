from flask import Flask, jsonify, render_template

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
    data = request.get_json()
    text = data.get('text', '').strip()
        
    if not text:
        return jsonify({"error": "No text provided"}), 400
        placeholder_result = {
        "bias_score": 0.68,
        "confidence": 0.85,
        "verdict": "Moderate potential bias detected – further review recommended"
    }
    
    return jsonify({"result": placeholder_result})
