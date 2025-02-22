from flask import Flask, request, render_template, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def fetch_page_source(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())  
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        source_code = driver.page_source  # Get fully rendered HTML
        driver.quit()

        # Extract first vcloud.lol link
        match = re.search(r'https?://vcloud\.lol[^\s"<>]+', source_code)
        vcloud_link = match.group(0) if match else None

        return source_code, vcloud_link

    except Exception as e:
        driver.quit()
        return None, str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_source', methods=['POST'])
def fetch_source():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    if not url.startswith(("http://", "https://")):
        url = "https://" + url  # Ensure correct format

    source_code, vcloud_link = fetch_page_source(url)

    if source_code is None:
        return jsonify({"error": f"Failed to fetch page: {vcloud_link}"}), 500

    return jsonify({"source_code": source_code, "vcloud_link": vcloud_link})

if __name__ == '__main__':
    app.run(debug=True)
