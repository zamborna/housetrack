import requests
from bs4 import BeautifulSoup
import json
from fake_useragent import UserAgent
import time

# Base search URL
BASE_URL = 'https://www.willhaben.at/iad/immobilien/haus-kaufen'
ua = UserAgent()

headers = {
    'User-Agent': ua.random
}

# Scrape one page
def scrape_page(page_num):
    url = f"{BASE_URL}?page={page_num}"
    print(f"Scraping page {page_num}...")

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to load page {page_num}: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    listings = soup.find_all('div', class_='search-result-entry')
    houses = []

    for listing in listings:
        try:
            title_tag = listing.find('a', class_='header__title')
            title = title_tag.text.strip() if title_tag else 'No Title'

            url = 'https://www.willhaben.at' + title_tag['href'] if title_tag else '#'

            price_tag = listing.find('div', class_='search-result-entry__price')
            price = price_tag.text.strip() if price_tag else '0'
            price = int(''.join(filter(str.isdigit, price)))

            location_tag = listing.find('div', class_='search-result-entry__location')
            location = location_tag.text.strip() if location_tag else 'Unknown'

            img_tag = listing.find('img')
            image = img_tag['src'] if img_tag else ''

            id = url.split('-')[-1]

            house = {
                'id': id,
                'title': title,
                'price': price,
                'location': location,
                'size': 0,  # Placeholder for size
                'url': url,
                'image': image
            }

            houses.append(house)

        except Exception as e:
            print(f"Error parsing listing: {e}")

    return houses

# Scrape multiple pages
def scrape_willhaben(max_pages=5):
    all_houses = []

    for page in range(1, max_pages + 1):
        houses = scrape_page(page)

        if not houses:
            print("No more houses found, stopping.")
            break

        all_houses.extend(houses)

        # Respectful delay between page loads
        time.sleep(1)

    # Save results
    with open('houses.json', 'w', encoding='utf-8') as f:
        json.dump(all_houses, f, ensure_ascii=False, indent=4)

    print(f"Saved {len(all_houses)} houses to houses.json.")

if __name__ == "__main__":
    scrape_willhaben(max_pages=10)  # 👈 Adjust how many pages you want
