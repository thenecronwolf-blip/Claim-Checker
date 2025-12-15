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
