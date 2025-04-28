# Crypto Crawler Challenge


## Setup Instructions

1. Clone the repository.
2. Install all required Python packages:

```bash
  make install
```

# Run specific scrapers:

Run Coingecko Crypto Crawler:
```bash
    make run target=coingecko
```

Run CoinMarketCap HTML Scraper:
```bash
    make run target=coinmarketcap_html
```

Run CoinMarketCap JSON Scraper:
```bash
    make run target=coinmarketcap_json
```

# Check result in "coinmarketcap_data_json.csv" or "coinmarketcap_data.csv" files

Requirements

    Python 3.9+

    pip (Python package manager)

Features
Phase 1 – Price Pulse (Coingecko)

    Polls Bitcoin's USD price every 1 second.

    Prints price and Simple Moving Average (SMA) of the last 10 values.

    Handles API failures with exponential backoff and retry logic.

    Graceful shutdown on Ctrl+C (SIGINT).

Phase 2 – CoinMarketCap Watchlist

    HTML Scraper:

        Scrapes pages 1–5 from CoinMarketCap.

        Extracts Rank, Name, Symbol, Price, 24h % Change, Market Cap.

        Stores results into a SQLite database (coinmarketcap.db).

    JSON Scraper:

        Uses internal CoinMarketCap JSON API.

        Fetches and parses listing data faster and more reliably.

        Stores results into the same database schema.

Performance Metrics

See detailed comparison between HTML and JSON scrapers in coinmarketcap/metrics.txt.
Notes

    Sandbox API Usage: CoinMarketCap Sandbox API was used for development purposes, which may limit the number of available coins.

    Bot Detection: HTML scraping includes basic precautions (politeness delays) to avoid triggering anti-bot mechanisms.

Bonus Features

    Multi-threading used in Coingecko Crawler for non-blocking data fetching.

    Exponential backoff implemented for resilience against API issues.

    Automatic installation and easy application control via Makefile.

Future Improvements

    Add Docker support for containerized deployments.

    Introduce argument parsing (argparse) for more flexible CLI controls.

    Implement retries for scraping failures automatically.

