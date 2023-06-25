const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());
const fs = require('fs');

// Read the user thresholds and URLs from the JSON file
let thresholds = JSON.parse(fs.readFileSync('thresholds.json', 'utf8'));

// Collect all the URLs from all users
let urls = [];
for (let username in thresholds) {
    let user_urls = thresholds[username]['urls'];
    urls = urls.concat(user_urls);
}

(async () => {
    console.log("Starting scraping cycle...");
    const browser = await puppeteer.launch({ headless: "new" });
    const productDataArray = []; // Array to store product data

    for (const url of urls) {
        if (!url || typeof url !== 'string') {
            console.error(`Invalid URL: ${url}`);
            continue; // Skip this iteration of the loop
        }

        const page = await browser.newPage();
        await page.goto(url, { waitUntil: 'networkidle2' });

        let price;
        let productName;

        if (url.includes("g2a.com")) {
            try {
                await page.waitForSelector("span[data-locator='zth-price']", { timeout: 5000 });
                price = await page.evaluate(() =>
                    document.querySelector("span[data-locator='zth-price']").innerText.trim()
                );
            } catch (error) {
                console.error('Price element not found:', error);
            }

            // Split the URL on slashes and select the product name segment
            const urlParts = url.split("/");
            const productNameSegment = urlParts[urlParts.length - 1];
            productName = productNameSegment
                .split("-")
                .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
                .join(" ");
        } else if (url.includes("instant-gaming.com")) {
            price = await page.evaluate(() =>
                document.querySelector("meta[itemprop='price']").getAttribute('content')
            );

            productName = await page.evaluate(() =>
                document.querySelector("h1.game-title").innerText.trim()
            );
        } else if (url.includes("store.steampowered.com")) {
            price = await page.evaluate(() =>
                document.querySelector(".game_purchase_price.price").innerText.trim()
            );

            productName = await page.evaluate(() =>
                document.querySelector(".apphub_AppName").innerText.trim()
            );
        }

        const productData = {
            "product": productName,
            "price": price,
            "url": url
        };

        productDataArray.push(productData); // Add product data to the array

        await page.close();

        console.log("Scraped data: ", productData);
    }

    // Write the entire product data array to the JSON file
    try {
        // Write the entire product data array to the JSON file
        console.log("Writing to product-data.json... ", productDataArray);
        fs.writeFileSync('product-data.json', JSON.stringify(productDataArray));
        console.log("Data written successfully");
    } catch (error) {
        console.error('Error writing to file:', error);
    }

    // Close the browser
    await browser.close();
    console.log("Browser closed");
})();
