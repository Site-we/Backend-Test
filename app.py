from flask import Flask, request, render_template, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_final_download_link(url):
    try:
        chrome_options = Options()
        chrome_options.binary_location = "/usr/bin/chromium-browser"  # Set Chromium path
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Step 1: Load the original page
        driver.get(url)
        time.sleep(3)  # Wait for full page load

        # Step 2: Extract vcloud.lol link
        match = re.search(r'https?://vcloud\.lol[^\s"<>]+', driver.page_source)
        vcloud_link = match.group(0) if match else None

        if not vcloud_link:
            driver.quit()
            return {"error": "No vcloud.lol link found"}

        # Step 3: Load the vcloud.lol link
        driver.get(vcloud_link)
        time.sleep(3)  # Wait for full page load

        # Step 4: Click "Generate Download Link" button
        try:
            button = driver.find_element(By.XPATH, "//button[contains(text(), 'Generate Download Link')]")
            ActionChains(driver).move_to_element(button).click().perform()
            time.sleep(3)  # Wait for link to generate
        except:
            driver.quit()
            return {"error": "Generate Download Link button not found"}

        # Step 5: Extract the final download URL
        match = re.search(r'https?://[^\s"<>]+', driver.page_source)
        final_download_link = match.group(0) if match else None

        driver.quit()

        if final_download_link:
            return {"vcloud_link": vcloud_link, "final_download_link": final_download_link}
        else:
            return {"error": "No final download link found"}

    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_download_link', methods=['POST'])
def fetch_download_link():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    result = get_final_download_link(url)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
