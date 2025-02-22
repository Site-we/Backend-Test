from flask import Flask, request, render_template, jsonify
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_source', methods=['POST'])
def fetch_source():
    data = request.json
    source_code = data.get("source_code")

    if not source_code:
        return jsonify({"error": "No source code provided"}), 400

    # Extract first vcloud.lol link
    match = re.search(r'https?://vcloud\.lol[^\s"<>]+', source_code)
    vcloud_link = match.group(0) if match else None

    return jsonify({"source_code": source_code, "vcloud_link": vcloud_link})

if __name__ == '__main__':
    app.run(debug=True)
