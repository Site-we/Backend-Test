const express = require("express");
const puppeteer = require("puppeteer");

const app = express();
app.use(express.json());

app.post("/fetch_source", async (req, res) => {
    let url = req.body.url;
    if (!url) {
        return res.status(400).json({ error: "No URL provided" });
    }

    if (!url.startsWith("http")) {
        url = "https://" + url;
    }

    try {
        const browser = await puppeteer.launch({ headless: "new" });  // Start headless browser
        const page = await browser.newPage();
        await page.goto(url, { waitUntil: "networkidle2", timeout: 10000 });

        const sourceCode = await page.content();  // Get full page source

        // Extract first vcloud.lol link
        const vcloudLink = await page.evaluate(() => {
            const match = document.body.innerHTML.match(/https?:\/\/vcloud\.lol[^\s"<>]+/);
            return match ? match[0] : null;
        });

        await browser.close();
        res.json({ source_code: sourceCode, vcloud_link: vcloudLink });

    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.listen(3000, () => console.log("Server running on port 3000"));
