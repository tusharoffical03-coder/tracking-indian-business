# Dashboard Design & User Flow

## 1. Visual Style
- **Theme**: Dark Mode (Professional/Tech look) with Gold and Electric Blue accents.
- **Vibe**: Clean, Data-driven, High-Professional.

## 2. Main Sections

### **A. Lead Command Center (Table View)**
- **Filters**: Niche (Dropdown), Lead Score (Buttons: Gold/Silver/Bronze), City.
- **Lead Row**:
    - Name & Rating.
    - Status Badge (e.g., "Gold: No Website").
    - Action Buttons: `[Analyze Site]` `[Generate Pitch]` `[Send to WhatsApp]`.

### **B. Sales Agent Chat Interface**
- A sidebar or popup chat window.
- **Input**: Paste a client's message (e.g., "I already have a developer").
- **Output**: The Agent suggests 3 potential replies (Friendly, Aggressive, Value-based).

### **C. Lead Deep-Dive (Modal/Panel)**
- Shows the full Auditor Report.
- "Gaps Found" list (e.g., No SSL, No WhatsApp button, Slow speed).
- A generated "Before/After" visual comparison (AI generated mockup).

### **D. Bulk Actions**
- `[Download CSV]`: Exports the current filtered list.
- `[Start Scraping]`: Opens a dialog to enter Niche and City.

## 3. User Flow
1. **Scraping**: User enters "Skin Doctor" and "South Delhi". The system starts fetching leads in the background.
2. **Reviewing**: User sees the table filling up. The "Lead Score" column highlights the best opportunities.
3. **Auditing**: User clicks "Analyze" on a Gold/Silver lead. The AI Auditor scans the site and populates the "Gaps" section.
4. **Pitching**: User clicks "Generate Pitch". The AI creates a message based on the gaps.
5. **Engagement**: User copies the pitch or clicks "Send WhatsApp" to open the WhatsApp Web interface with the message pre-filled.
6. **Objection Handling**: If the client replies with a doubt, the user uses the "Sales Expert Chat" to get a rebuttal.

## 4. Key Components (React)
- `LeadTable.tsx`: Custom sortable/filterable table.
- `AuditModal.tsx`: Visual representation of website health.
- `SalesBot.tsx`: Interactive chat for objection handling.
- `ExportButton.tsx`: Handles CSV generation.
