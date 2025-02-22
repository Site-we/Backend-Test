from flask import Flask, request, render_template, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

@app.route('/')
def index():
    return render_template('index.html')  # Load the frontend HTML page

@app.route('/fetch_source', methods=['POST'])
def fetch_source():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    # Ensure the URL has HTTP/HTTPS prefix
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise error for bad responses (4xx, 5xx)
        return jsonify({"source_code": response.text})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
