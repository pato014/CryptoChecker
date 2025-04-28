from html_scraper import CoinMarketCapScraper
from storage import CSVStorage


def main():
    scraper = CoinMarketCapScraper(pages=5)
    data = scraper.scrape()

    storage = CSVStorage(filename="coinmarketcap_data.csv")
    storage.save(data)


if __name__ == "__main__":
    main()
