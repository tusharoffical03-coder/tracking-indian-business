# System Architecture: Indian Business Lead Automation

## Overview
This system is an automated lead generation and sales pipeline specifically designed for the Indian market, targeting Skin Doctors, Real Estate Developers, and Coaching Centers. It automates the process of finding businesses on Google Maps, analyzing their digital presence, and generating high-conversion sales pitches.

## System Components

### 1. Lead Scraper (The "Miner")
- **Function**: Scans Google Maps for specific keywords and locations.
- **Tech**: Python, Playwright/Selenium (for scraping), or Google Places API.
- **Inputs**: Niche (Skin Doctor, Real Estate, Coaching Center), City/Area.
- **Outputs**: Business Name, Phone Number, Address, Website URL, Rating, Review Count.

### 2. Website Auditor (The "Doctor")
- **Function**: Performs a deep health check of the business's website.
- **Analysis Criteria**:
    - **Availability**: Is the website online? (404/SSL check).
    - **Modernity**: Is it mobile-responsive? (Critical for India).
    - **Conversion Tools**: Does it have a WhatsApp button, booking form, or lead magnet?
    - **Performance**: Page load speed.
- **Tech**: Playwright (for rendering), Lighthouse API, OpenAI GPT-4o Vision (for UI/UX audit).

### 3. Sales Expert Agent (The "Closer")
- **Function**: Crafts personalized outreach messages and handles objections.
- **Capabilities**:
    - **Personalized Pitching**: Uses Audit data to highlight specific gaps.
    - **Objection Handling**: AI-powered bot to respond to common client concerns (e.g., "Too expensive", "Already have a site").
    - **Bot Integration**: A lead-qualification bot to gather business details automatically.
- **Tech**: OpenAI GPT-4o (Text-generation).

### 4. Professional Dashboard
- **Function**: A central hub to manage leads and monitor automation.
- **Features**:
    - **Lead Pipeline**: View leads as they move from "Scraped" to "Analyzed".
    - **CSV Export**: One-click download of all lead data.
    - **AI Chat Hub**: Interface to interact with the Sales Expert Agent.
- **Tech**: React.js, Tailwind CSS, FastAPI (Backend).

## Data Flow
1. **Trigger**: User selects a Niche and City on the Dashboard.
2. **Scraping**: The Miner fetches leads from Google Maps and stores them in the DB.
3. **Auditing**: The Auditor automatically visits each website found.
4. **Scoring**: Leads are categorized as Gold, Silver, or Bronze based on their digital gaps.
5. **Pitching**: The Closer generates a custom pitch for each lead.
6. **Action**: User exports the CSV or sends a message directly via WhatsApp integration.

## Proposed Tech Stack
- **Backend**: Python 3.10+, FastAPI.
- **Frontend**: React (Vite) + Tailwind CSS + Lucide Icons (for "High-Pro" look).
- **Automation**: Playwright (Web Scraping & Rendering).
- **AI Engine**: OpenAI API (GPT-4o).
- **Database**: SQLite (for development) or PostgreSQL.
