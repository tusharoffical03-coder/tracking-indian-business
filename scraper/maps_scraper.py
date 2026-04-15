import asyncio
import pandas as pd
from playwright.async_api import async_playwright
import urllib.parse
import re

async def scrape_google_maps(niche, location, max_results=10):
    query = f"{niche} in {location}"
    search_url = f"https://www.google.com/maps/search/{urllib.parse.quote(query)}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print(f"Searching for: {query}")
        await page.goto(search_url)

        try:
            await page.wait_for_selector('div[role="feed"]', timeout=10000)
        except:
            print("No feed found or timeout.")
            await browser.close()
            return []

        leads = []
        for _ in range(2):
            await page.mouse.wheel(0, 2000)
            await asyncio.sleep(2)

        items = await page.query_selector_all('div[role="article"]')

        for item in items[:max_results]:
            try:
                # Click item to open the side panel which contains phone numbers
                await item.click()
                await asyncio.sleep(2) # Wait for panel to load

                name = ""
                title_el = await item.query_selector('div.fontHeadlineSmall')
                if title_el:
                    name = await title_el.inner_text()

                # Search for phone number in the side panel
                phone = "Not Found"
                # Heuristic: Phone numbers in India usually start with +91 or are 10 digits
                panel_text = await page.content()
                phone_match = re.search(r'(\+91\s?|0)?[6-9]\d{4}\s?\d{5}', panel_text)
                if phone_match:
                    phone = phone_match.group(0).replace(" ", "")

                website = ""
                links = await item.query_selector_all('a')
                for link in links:
                    href = await link.get_attribute('href')
                    if href and not "google.com" in href:
                        website = href
                        break

                rating = 0.0
                rating_el = await item.query_selector('span.MW4etd')
                if rating_el:
                    rating_text = await rating_el.inner_text()
                    rating = float(rating_text)

                leads.append({
                    "business_name": name,
                    "niche": niche,
                    "phone": phone,
                    "website_url": website,
                    "google_rating": rating
                })
                print(f"Found: {name} | Phone: {phone} | Website: {website}")
            except Exception as e:
                print(f"Error extracting item: {e}")
                continue

        await browser.close()
        return leads

if __name__ == "__main__":
    results = asyncio.run(scrape_google_maps("Skin Doctor", "South Delhi", max_results=3))
    print(results)
