import requests
from bs4 import BeautifulSoup
import csv

# Scrape CIA FOIA (working as of June 2024)
def scrape_cia():
    url = "https://www.cia.gov/readingroom/search/site"
    params = {
        "search_api_fulltext": "",
        "sort_by": "field_foia_date_released",
        "sort_order": "DESC"
    }
    headers = {"User-Agent": "Mozilla/5.0"}  # Pretend to be a browser
    response = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    links = []
    for result in soup.select('.search-result'):
        title = result.select_one('h3').text.strip()
        link = "https://www.cia.gov" + result.select_one('a')['href']
        date = result.select_one('.search-result__date').text.strip()
        links.append([title, link, date, "CIA FOIA"])
    return links

# Save to CSV
with open('docs/links.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Title', 'URL', 'Date', 'Source'])
    writer.writerows(scrape_cia())

print("Done! Check docs/links.csv")
