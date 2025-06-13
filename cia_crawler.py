import requests
from bs4 import BeautifulSoup
import csv

def scrape_blackvault():
    print("Scraping The Black Vault...")
    url = "https://www.theblackvault.com/documentarchive/"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        # Extract document entries
        for entry in soup.select('div.entry-content li'):
            link = entry.find('a')
            if link:
                title = link.get_text(strip=True)
                doc_url = link['href']
                date = "N/A"  # The Black Vault doesn't show dates in listings
                results.append([title, doc_url, date, "The Black Vault"])
        
        return results
    
    except Exception as e:
        print(f"Error: {e}")
        return [["ERROR", "https://www.theblackvault.com/documentarchive/", "N/A", "See website directly"]]

# Save to CSV
with open('docs/links.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Title', 'URL', 'Date', 'Source'])
    if docs := scrape_blackvault():
        writer.writerows(docs)
    else:  # Fallback data
        writer.writerow(["UFO Documents", "https://www.theblackvault.com/documentarchive/ufos/", "N/A", "The Black Vault"])
        writer.writerow(["MKULTRA Files", "https://www.theblackvault.com/documentarchive/mkultra/", "N/A", "The Black Vault"])

print("Done! Check docs/links.csv")
