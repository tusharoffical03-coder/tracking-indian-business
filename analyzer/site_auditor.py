import asyncio
from playwright.async_api import async_playwright

async def audit_website(url):
    if not url or url == "":
        return {
            "website_status": "No Website",
            "mobile_responsive": False,
            "has_whatsapp": False,
            "has_booking": False,
            "lead_score": "Gold"
        }

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            # Set timeout for slow Indian sites
            await page.goto(url, timeout=30000, wait_until="networkidle")

            # 1. Check Mobile Responsiveness (Simple check for meta viewport)
            viewport_meta = await page.query_selector('meta[name="viewport"]')
            mobile_responsive = True if viewport_meta else False

            # 2. Check for WhatsApp button
            content = await page.content()
            has_whatsapp = "wa.me" in content or "whatsapp.com/send" in content or "api.whatsapp.com" in content

            # 3. Check for Booking System (Heuristic keywords)
            booking_keywords = ["book appointment", "book online", "appointment", "booking", "schedule"]
            has_booking = any(keyword in content.lower() for keyword in booking_keywords)

            # Determine Lead Score
            lead_score = "Bronze" # Default if site is good
            if not mobile_responsive or not has_whatsapp:
                lead_score = "Silver"

            await browser.close()
            return {
                "website_status": "Active",
                "mobile_responsive": mobile_responsive,
                "has_whatsapp": has_whatsapp,
                "has_booking": has_booking,
                "lead_score": lead_score
            }
        except Exception as e:
            await browser.close()
            return {
                "website_status": f"Error/Dead: {str(e)[:50]}",
                "mobile_responsive": False,
                "has_whatsapp": False,
                "has_booking": False,
                "lead_score": "Gold"
            }

if __name__ == "__main__":
    # Test with a dummy and a real-ish URL
    test_urls = ["", "https://www.google.com"]
    for url in test_urls:
        print(f"Auditing: {url}")
        report = asyncio.run(audit_website(url))
        print(report)
