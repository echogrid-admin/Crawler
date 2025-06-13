import requests
from bs4 import BeautifulSoup
import csv

# Configure browser-like headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}

def scrape_cia_foia():
    print("Scraping CIA FOIA...")
    url = "https://www.cia.gov/readingroom/collection/crest-25-year-program-archive"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        # Updated selector for CIA's current layout
        for item in soup.select('div.item-list ul li'):
            link = item.find('a')
            if link:
                title = link.get_text(strip=True)
                href = "https://www.cia.gov" + link['href']
                date = item.find('span', class_='date').get_text(strip=True) if item.find('span', class_='date') else "N/A"
                results.append([title, href, date, "CIA FOIA"])
        return results
    except Exception as e:
        print(f"Error: {e}")
        return []

# Save to CSV
with open('docs/links.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Title', 'URL', 'Date', 'Source'])
    writer.writerows(scrape_cia_foia())

print("Scraping complete. Check docs/links.csv")
