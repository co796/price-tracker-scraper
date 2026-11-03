import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def scrape_prices(url, item_selector, price_selector):
    """
    Simple price scraper.
    url: target web page URL
    item_selector: CSS class for the item name
    price_selector: CSS class for the price
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        items = soup.select(item_selector)
        prices = soup.select(price_selector)
        
        results = []
        for item, price in zip(items, prices):
            results.append({
                'Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'Item': item.get_text(strip=True),
                'Price': price.get_text(strip=True)
            })
            
        return results
    except Exception as e:
        print(f"Error scraping: {e}")
        return []

def save_to_csv(data, filename="prices.csv"):
    if not data:
        print("No data to save.")
        return
        
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    print(f"Successfully saved {len(data)} items to {filename}")

if __name__ == "__main__":
    # Example usage (update selectors for your target site)
    target_url = "https://books.toscrape.com/" 
    item_class = ".product_pod h3 a"
    price_class = ".product_pod .price_color"
    
    print(f"Scraping {target_url}...")
    scraped_data = scrape_prices(target_url, item_class, price_class)
    save_to_csv(scraped_data)
