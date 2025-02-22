from flask import Flask, request, render_template, jsonify
import requests
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Custom headers to mimic a real browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://google.com",  # Some websites check for a valid referer
    "Connection": "keep-alive"
}

@app.route('/')
def index():
    return render_template('index.html')  # Load the frontend HTML page

@app.route('/fetch_source', methods=['POST'])
def fetch_source():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    if not url.startswith(("http://", "https://")):
        url = "https://" + url  # Ensure URL has correct format

    try:
        session = requests.Session()
        response = session.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()  # Handle HTTP errors

        source_code = response.text

        # Search for the first occurrence of a vcloud.lol link
        match = re.search(r'https?://vcloud\.lol[^\s"<>]+', source_code)
        vcloud_link = match.group(0) if match else None

        return jsonify({"source_code": source_code, "vcloud_link": vcloud_link})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch page: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
