import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.title(" Company Scraper")

if st.button("Scrape YC Startups"):
    url = "https://en.wikipedia.org/wiki/List_of_Y_Combinator_startups"
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    companies = []
    for ul in soup.select("div.mw-parser-output > ul"):
        for li in ul.find_all("li"):
            name = li.get_text().split("–")[0].strip()
            if name and len(name) < 60:
                companies.append(name)

    df = pd.DataFrame(sorted(set(companies)), columns=["company"])
    df.to_csv("sample_leads.csv", index=False)
    
    st.success(f" Scraped {len(df)} companies to sample_leads.csv")
    st.dataframe(df.head(10))
