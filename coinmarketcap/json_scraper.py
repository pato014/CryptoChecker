import requests


class CoinMarketCapJSONScraper:
    BASE_URL = "https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

    def __init__(self, api_key, pages=5, limit_per_page=20):
        self.api_key = api_key
        self.pages = pages
        self.limit_per_page = limit_per_page
        self.session = requests.Session()
        self.session.headers.update({
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.api_key,
        })

    def fetch_page(self, start):
        parameters = {
            'start': str(start),
            'limit': str(self.limit_per_page),
            'convert': 'USD'
        }
        response = self.session.get(self.BASE_URL, params=parameters)
        response.raise_for_status()
        return response.json()

    def parse_data(self, data):
        result = []
        for item in data['data']:
            result.append({
                "rank": item.get("cmc_rank"),
                "symbol": item.get("symbol"),
                "name": item.get("name"),
                "price_usd": item["quote"]["USD"]["price"],
                "change_24h": item["quote"]["USD"]["percent_change_24h"],
                "market_cap_usd": item["quote"]["USD"]["market_cap"]
            })
        return result

    def scrape(self):
        all_data = []
        for page in range(self.pages):
            start = page * self.limit_per_page + 1
            print(f"Fetching items {start} to {start + self.limit_per_page - 1}...")
            json_data = self.fetch_page(start)
            page_data = self.parse_data(json_data)
            all_data.extend(page_data)
        return all_data
