# Caprae AI Readiness Challenge – Lead Scorer Tool

##  Objective
Build a smarter lead generation tool in 5 hours that improves on SaaSquatchLeads by focusing on **lead quality**, not just scraping volume.

##  Features Implemented
- CSV input for company names
- For each company:
  - Validates email (via regex or API)
  - Checks LinkedIn and website presence
  - Scores leads based on data reliability
- Clean UI built using Streamlit
- Exportable scored leads table (CSV)

##  Scoring Formula
Score = (Email valid × 0.5) + (LinkedIn found × 0.3) + (Website alive × 0.2)

##  Business Value
- Prioritizes reachable and real leads
- Filters junk (fake domains, empty LinkedIns)
- Boosts email outreach success
- Saves time for Caprae's investment team

##  Future Enhancements
- CRM integrations
- Founder activity analysis
- Keyword tags (e.g., "AI", "Fintech")

##  Submitted by
Yerra Guna Shekhar  
Email: guna.datascientist@gmail.com
