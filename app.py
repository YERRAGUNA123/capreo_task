# app.py
import streamlit as st
import pandas as pd
from enrichment import enrich_company
from lead_scoring import score_lead
import requests
from bs4 import BeautifulSoup
import os
from PIL import Image
import pytesseract
import base64
from io import BytesIO

st.set_page_config(page_title="Caprae AI Lead Scorer", layout="wide")
st.title("Caprae AI Lead Scorer")


st.markdown("###  Upload or Scrape Startups")
option = st.selectbox("Choose input method", ["Scrape from Web", "Upload File", "Upload Image"])


SCRAPE_SOURCES = {
    "Y Combinator Startups": "https://en.wikipedia.org/wiki/List_of_Y_Combinator_startups",
    "Unicorn Startups": "https://en.wikipedia.org/wiki/List_of_unicorn_startup_companies",
    "Crunchbase Sample": "https://raw.githubusercontent.com/datasets/crunchbase-companies/master/data/companies.csv",
    "TechCrunch Startups": "https://techcrunch.com/startups/"
}

def scrape_yc_and_unicorn():
    companies = []
    for name, url in SCRAPE_SOURCES.items():
        try:
            if 'crunchbase' in url:
                df = pd.read_csv(url)
                companies += df['name'].dropna().tolist()
            elif 'techcrunch' in url:
                page = requests.get(url, timeout=10)
                soup = BeautifulSoup(page.text, 'html.parser')
                for article in soup.select("article h2"):
                    companies.append(article.get_text(strip=True))
            else:
                page = requests.get(url, timeout=10)
                soup = BeautifulSoup(page.text, 'html.parser')
                for ul in soup.select("div.mw-parser-output > ul"):
                    for li in ul.find_all("li"):
                        company = li.get_text().split("–")[0].strip()
                        if company and len(company) < 60:
                            companies.append(company)
        except Exception as e:
            print(f"Error scraping {url}: {e}")

    unique_companies = sorted(set(companies))
    df = pd.DataFrame(unique_companies, columns=["company"])
    df.to_csv("sample_leads.csv", index=False)
    return df

def extract_from_image(image):
    img = Image.open(image)
    text = pytesseract.image_to_string(img)
    companies = [line.strip() for line in text.splitlines() if line.strip()]
    df = pd.DataFrame(sorted(set(companies)), columns=["company"])
    df.to_csv("sample_leads.csv", index=False)
    return df

def upload_file(uploaded):
    df = pd.read_csv(uploaded) if uploaded.name.endswith(".csv") else pd.read_excel(uploaded)
    df = df.rename(columns={df.columns[0]: "company"})
    df.to_csv("sample_leads.csv", index=False)
    return df

if option == "Scrape from Web":
    if st.button("Scrape Startups from Multiple Sources"):
        df = scrape_yc_and_unicorn()
        st.success(f"Scraped {len(df)} unique companies from multiple sources.")
        st.dataframe(df)

elif option == "Upload File":
    uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])
    if uploaded_file:
        df = upload_file(uploaded_file)
        st.success(f"Uploaded {len(df)} companies.")
        st.dataframe(df)

elif option == "Upload Image":
    image = st.file_uploader("Upload screenshot (PNG/JPG)", type=["png", "jpg", "jpeg"])
    if image and st.button("Extract Companies"):
        df = extract_from_image(image)
        st.success(f"Extracted {len(df)} companies from image.")
        st.dataframe(df)

# Step 2: Enrich and Score
st.markdown("### Enrich & Score Companies")
def enrich_and_score():
    df = pd.read_csv("sample_leads.csv")
    enriched = []
    for company in df["company"]:
        info = enrich_company(company)
        info["company"] = company
        info["score"] = score_lead(info.get("email"), info.get("linkedin"), info.get("website"))
        enriched.append(info)
    result_df = pd.DataFrame(enriched)
    result_df.to_csv("scored_leads.csv", index=False)
    return result_df

if st.button("Run Enrichment & Scoring"):
    if not os.path.exists("sample_leads.csv"):
        st.warning("Please upload or scrape companies first.")
    else:
        result_df = enrich_and_score()
        st.success("Leads enriched and scored!")
        st.dataframe(result_df.sort_values(by="score", ascending=False), use_container_width=True)
        st.download_button("Download Results as CSV", result_df.to_csv(index=False), file_name="scored_leads.csv")


st.markdown("##  Search for a Lead")
search_name = st.text_input("Enter company name")

if os.path.exists("scored_leads.csv") and search_name:
    df = pd.read_csv("scored_leads.csv")
    result = df[df["company"].str.lower().str.contains(search_name.lower())]
    if not result.empty:
        st.markdown("###  Lead Info")
        st.dataframe(result[["company", "email", "linkedin", "website", "score"]].sort_values(by="score", ascending=False), use_container_width=True)

        query = result.iloc[0]['company']

        st.markdown("###  External Information")
        with st.expander(" Complaints"):
            st.markdown(f"[Search Complaints for {query}](https://www.google.com/search?q={query}+complaints)")

        with st.expander(" Images"):
            st.markdown(f"[View Images of {query}](https://www.google.com/search?tbm=isch&q={query}+logo+or+office)")

        with st.expander(" Similar Companies"):
            st.markdown(f"[Find Similar Companies to {query}](https://www.google.com/search?q={query}+similar+companies)")

    else:
        st.info("No matching leads found.")
