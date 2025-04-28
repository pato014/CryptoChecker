import requests
from bs4 import BeautifulSoup
import time


class CoinMarketCapScraper:
    BASE_URL = "https://coinmarketcap.com"

    def __init__(self, pages=5):
        self.pages = pages
        self.session = requests.Session()

    def fetch_page(self, page_number):
        url = f"{self.BASE_URL}/?page={page_number}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.text

    def parse_page(self, html_content):
        soup = BeautifulSoup(html_content, "lxml")
        table = soup.find("table")
        if not table:
            print("Table not found!")
            return []

        tbody = table.find("tbody")
        if not tbody:
            print("Tbody not found!")
            return []

        rows = tbody.find_all("tr")
        data = []

        for row in rows:
            columns = row.find_all("td")
            if len(columns) < 8:
                continue
            try:
                rank = int(columns[1].text.strip())
                name_tag = columns[2].find("p", class_="coin-item-name")
                symbol_tag = columns[2].find("p", class_="coin-item-symbol")

                if not name_tag or not symbol_tag:
                    continue

                name = name_tag.text.strip()
                symbol = symbol_tag.text.strip()
                price = float(columns[3].text.strip().replace("$", "").replace(",", ""))
                change_24h = columns[5].text.strip()
                market_cap = columns[7].text.strip().replace("$", "").replace(",", "")

                data.append({
                    "rank": rank,
                    "symbol": symbol,
                    "name": name,
                    "price_usd": price,
                    "change_24h": change_24h,
                    "market_cap_usd": market_cap
                })
            except (IndexError, AttributeError, ValueError):
                continue
        return data

    def scrape(self):
        all_data = []
        for page in range(1, self.pages + 1):
            print(f"Fetching page {page}...")
            html = self.fetch_page(page)
            page_data = self.parse_page(html)
            all_data.extend(page_data)
            time.sleep(1)
        return all_data
