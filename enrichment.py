import requests
from bs4 import BeautifulSoup
import re
from googlesearch import search

HEADERS = {"User-Agent": "Mozilla/5.0"}

def find_website(company_name):
    query = f"{company_name} official site"
    for result in search(query, num_results=5):
        if company_name.lower() in result.lower():
            return result
    return ""

def find_linkedin(company_name):
    query = f"{company_name} LinkedIn"
    for result in search(query, num_results=5):
        if "linkedin.com/company" in result or "linkedin.com/in" in result:
            return result
    return ""

def extract_email_from_website(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")
        text = soup.get_text()
        emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
        return emails[0] if emails else ""
    except:
        return ""

def enrich_company(name):
    website = find_website(name)
    linkedin = find_linkedin(name)
    email = extract_email_from_website(website) if website else ""
    return {"website": website, "linkedin": linkedin, "email": email}
