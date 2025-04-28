import requests
from bs4 import BeautifulSoup
import json
from fake_useragent import UserAgent

# URL example: willhaben search for houses
SEARCH_URL = 'https://www.willhaben.at/iad/immobilien/haus-kaufen'

# Prepare headers to look like a normal browser
ua = UserAgent()
headers = {
    'User-Agent': ua.random
}

# Scrape function
def scrape_willhaben():
    houses = []

    # Send request
    response = requests.get(SEARCH_URL, headers=headers)
    if response.status_code != 200:
        print(f"Failed to load page: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find house listings
    listings = soup.find_all('div', class_='search-result-entry')  # Corrected class name
    print(f"Found {len(listings)} listings.")

    for listing in listings:
        try:
            title_tag = listing.find('a', class_='header__title')
            title = title_tag.text.strip() if title_tag else 'No Title'

            url = 'https://www.willhaben.at' + title_tag['href'] if title_tag else '#'

            price_tag = listing.find('div', class_='search-result-entry__price')
            price = price_tag.text.strip() if price_tag else '0'
            price = int(''.join(filter(str.isdigit, price)))  # Keep only numbers

            location_tag = listing.find('div', class_='search-result-entry__location')
            location = location_tag.text.strip() if location_tag else 'Unknown'

            img_tag = listing.find('img')
            image = img_tag['src'] if img_tag else ''

            id = url.split('-')[-1]  # Take ID from URL, usually at the end

            house = {
                'id': id,
                'title': title,
                'price': price,
                'location': location,
                'size': 0,  # We can extend later
                'url': url,
                'image': image
            }

            houses.append(house)

        except Exception as e:
            print(f"Error parsing listing: {e}")

    # Save results to JSON
    with open('houses.json', 'w', encoding='utf-8') as f:
        json.dump(houses, f, ensure_ascii=False, indent=4)

    print(f"Saved {len(houses)} houses to houses.json.")

if __name__ == "__main__":
    scrape_willhaben()
