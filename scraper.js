const puppeteer = require('puppeteer');
const fs = require('fs');

const urls = [
    "https://www.g2a.com/sea-of-thieves-deluxe-edition-pc-steam-account-account-global-i10000145411033",
    "https://www.instant-gaming.com/en/967-buy-sea-of-thieves-pc-xbox-one-xbox-series-x-s-pc-xbox-one-xbox-series-x-s-game-microsoft-store/",
    "https://www.instant-gaming.com/en/11555-buy-microsoft-store-sea-of-thieves-pc-xbox-one-xbox-series-x-s-xbox-one-pc-xbox-series-x-s-game-microsoft-store-europe/"
];

(async () => {
    const browser = await puppeteer.launch({ headless: false });
    const productDataArray = []; // Array to store product data

    for (const url of urls) {
        const page = await browser.newPage();
        await page.goto(url, { waitUntil: 'networkidle2' });

        let price;
        let productName;

        if (url.includes("g2a.com")) {
            price = await page.evaluate(() =>
                document.querySelector(
                    "div[class='PaymentsRadiostyles__PriceWrapper-sc-gqqzhy-0 htjcnt'] span[class='sc-iqAclL sc-crzoAE dJFpVb frbZCR sc-bqGGPW fIHClq']"
                ).innerText.trim()
            );

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
        }

        const productData = {
            "product": productName,
            "price": price,
            "url": url
        };

        productDataArray.push(productData); // Add product data to the array

        await page.close();
    }

    // Write the entire product data array to the JSON file
    fs.writeFileSync('product-data.json', JSON.stringify(productDataArray));

    await browser.close();
})();
