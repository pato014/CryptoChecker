from json_scraper import CoinMarketCapJSONScraper
from storage import CSVStorage

API_KEY = "b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c"

def main():
    scraper = CoinMarketCapJSONScraper(api_key=API_KEY, pages=5, limit_per_page=20)
    data = scraper.scrape()

    storage = CSVStorage(filename="coinmarketcap_data_json.csv")
    storage.save(data)


if __name__ == "__main__":
    main()
