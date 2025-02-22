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
    chrome_options.add_argument("--headless")  # Run Chrome in the background
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    try:
        service = Service(ChromeDriverManager().install())  
        driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.get(url)
        source_code = driver.page_source  # Get fully rendered HTML
        driver.quit()

        # Extract first vcloud.lol link
        match = re.search(r'https?://vcloud\.lol[^\s"<>]+', source_code)
        vcloud_link = match.group(0) if match else None

        return {"source_code": source_code, "vcloud_link": vcloud_link}

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

    if not url.startswith(("http://", "https://")):
        url = "https://" + url  # Ensure correct format

    result = fetch_page_source(url)

    return jsonify(result)  # Always return JSON format

if __name__ == '__main__':
    app.run(debug=True)
