# Data Schemas & Lead Scoring Logic

## 1. CSV Data Schema
The exported CSV will contain the following fields to provide a comprehensive view of the lead:

| Field | Description | Type |
|-------|-------------|------|
| `business_name` | Name of the clinic, agency, or center | String |
| `niche` | Skin Doctor, Real Estate, or Coaching | Category |
| `phone` | Contact number (prefixed with +91 if possible) | String |
| `website_url` | URL found on Google Maps | String |
| `google_rating` | Star rating (0.0 to 5.0) | Float |
| `review_count` | Total number of reviews | Integer |
| `website_status` | Active, Dead, Slow, or No Website | Category |
| `mobile_responsive`| Whether the site is usable on smartphones | Boolean |
| `has_whatsapp` | Is there a direct WhatsApp button? | Boolean |
| `has_booking` | Is there an online appointment/demo system? | Boolean |
| `lead_score` | Gold, Silver, or Bronze | Category |
| `generated_pitch` | The custom sales message for this lead | Text |

## 2. Lead Scoring Logic
Leads are categorized automatically based on the "Gap Analysis" performed by the Auditor.

### **Gold Lead (Priority: High)**
- **Criteria**: No website found OR Website is completely dead (404/DNS error).
- **Reasoning**: These businesses have zero digital presence or a broken one. They are the most likely to buy a new website.
- **Bonus**: If `google_rating` > 4.0 and `review_count` > 50, it's a "Super-Gold" lead because they are successful but digitally invisible.

### **Silver Lead (Priority: Medium)**
- **Criteria**: Website exists but is NOT mobile-responsive OR lacks a WhatsApp button.
- **Reasoning**: In the Indian market, mobile usability and WhatsApp are non-negotiable. If they lack these, they are losing customers daily.

### **Bronze Lead (Priority: Low)**
- **Criteria**: Website exists and is mobile-friendly, but lacks advanced features like a booking system or modern UI.
- **Reasoning**: These are "Upsell" opportunities. They have a basic setup but need professionalization.

## 3. Database Schema (Internal)
- `leads` table: Stores all the raw data from Maps and the Auditor.
- `pitches` table: Stores the history of generated messages and client responses.
- `settings` table: Stores API keys and scraping preferences.
