import requests
from bs4 import BeautifulSoup
import csv

def scrape_blackvault():
    print("🚀 Scraping The Black Vault...")
    url = "https://www.theblackvault.com/documentarchive/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        # 1. Get the page with browser-like headers
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Crash if request fails
        
        # 2. Parse with explicit HTML parser
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 3. NEW: More precise selector
        document_section = soup.find('div', class_='entry-content')
        if not document_section:
            raise ValueError("Couldn't find document section!")
        
        # 4. Extract ALL documents
        results = []
        for li in document_section.find_all('li'):
            link = li.find('a')
            if link and link.get('href'):
                title = link.get_text(strip=True)
                doc_url = link['href']
                results.append([title, doc_url, "N/A", "The Black Vault"])
        
        return results

    except Exception as e:
        print(f"⚠️ Error: {e}")
        # Return critical documents even if scraping fails
        return [
            ["UFO Documents", "https://www.theblackvault.com/documentarchive/ufos/", "N/A", "The Black Vault"],
            ["MKULTRA Files", "https://www.theblackvault.com/documentarchive/mkultra/", "N/A", "The Black Vault"],
            ["JFK Assassination", "https://www.theblackvault.com/documentarchive/jfk-assassination/", "N/A", "The Black Vault"]
        ]

# Save to CSV
with open('docs/links.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Title', 'URL', 'Date', 'Source'])
    writer.writerows(scrape_blackvault())

print("✅ Done! Check docs/links.csv")
