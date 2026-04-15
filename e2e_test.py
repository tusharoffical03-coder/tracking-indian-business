import asyncio
import pandas as pd
from scraper.maps_scraper import scrape_google_maps
from analyzer.site_auditor import audit_website
from analyzer.sales_expert import SalesExpert

async def run_e2e_flow(niche, location):
    print(f"--- Starting E2E Flow for {niche} in {location} ---")

    # 1. Scraping
    raw_leads = await scrape_google_maps(niche, location, max_results=3)

    enriched_leads = []
    expert = SalesExpert()

    for lead in raw_leads:
        print(f"Processing: {lead['business_name']}")

        # 2. Auditing
        audit_report = await audit_website(lead['website_url'])
        lead.update(audit_report)

        # 3. Pitch Generation
        pitch = expert.generate_pitch(lead, audit_report)
        lead['generated_pitch'] = pitch

        enriched_leads.append(lead)

    # 4. Save to final CSV
    df = pd.DataFrame(enriched_leads)
    df.to_csv("leads_final.csv", index=False)
    print(f"\n--- Flow Complete. Final data saved to leads_final.csv ---")
    print(df[['business_name', 'lead_score', 'website_status']])

if __name__ == "__main__":
    asyncio.run(run_e2e_flow("Coaching Center", "Janakpuri, Delhi"))
