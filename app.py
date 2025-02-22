from flask import Flask, request, render_template, jsonify
import httpx  # Faster alternative to requests
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def fetch_page_source(url):
    try:
        # Ensure URL starts with http/https
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }

        # Fetch page content
        response = httpx.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Extract first vcloud.lol link
        match = re.search(r'https?://vcloud\.lol[^\s"<>]+', response.text)
        vcloud_link = match.group(0) if match else None

        return {"source_code": response.text, "vcloud_link": vcloud_link}

    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_source', methods=['POST'])
def fetch_source():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    result = fetch_page_source(url)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
