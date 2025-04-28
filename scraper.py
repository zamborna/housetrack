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
