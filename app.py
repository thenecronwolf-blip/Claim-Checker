from flask import Flask, jsonify, render_template

app = Flask(
    __name__,
    template_folder="ui/templates",
    static_folder="ui/static"
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/health")
def health():
    return jsonify({"status": "ok"})
