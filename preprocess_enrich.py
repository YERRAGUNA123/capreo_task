import pandas as pd
from enrichment import enrich_company
from lead_scoring import score_lead

df = pd.read_csv("sample_leads.csv")  # input: company name column
enriched_data = []

for company in df["company"]:
    enriched = enrich_company(company)
    score = score_lead(enriched.get("email", ""), enriched.get("linkedin", ""), enriched.get("website", ""))
    enriched_data.append({
        "company": company,
        **enriched,
        "score": score
    })

pd.DataFrame(enriched_data).to_csv("scored_leads.csv", index=False)
print("✅ Saved to scored_leads.csv")
