import requests

def validate_email(email):
    return bool(email) and "@" in email and "." in email.split("@")[-1]

def is_website_alive(url):
    try:
        return requests.get(url, timeout=5).status_code == 200
    except:
        return False

def score_lead(email, linkedin, website):
    score = 0
    score += 0.5 if validate_email(email) else 0
    score += 0.3 if linkedin else 0
    score += 0.2 if is_website_alive(website) else 0
    return round(score, 2)
