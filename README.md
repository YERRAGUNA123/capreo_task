#  Smart Lead Quality Scorer – Caprae AI Challenge

This tool helps Caprae Capital score and filter B2B leads based on contact quality and web presence.

## Features
- Input: CSV with company names or emails
- Finds:
  - Email (regex or scraping)
  - LinkedIn URL (via Google search)
  - Website (via Google search)
- Scores leads based on presence & validity
- Export enriched + scored CSV

## Scoring
| Field      | Weight | Criteria              |
|------------|--------|-----------------------|
| Email      | 0.5    | Valid format/scraped  |
| LinkedIn   | 0.3    | Found via search      |
| Website    | 0.2    | HTTP 200 check        |

## How to Run
```bash
pip install -r requirements.txt
streamlit run app.py
```


## Author
Yerra Guna Shekhar
