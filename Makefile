.PHONY: install run clean

install:
	pip install -r requirements.txt

run: ## Usage: make run target=coingecko|coinmarketcap_html|coinmarketcap_json
ifeq ($(target),coingecko)
	python3 coingecko/crypto_crawler.py
else ifeq ($(target),coinmarketcap_html)
	python3 coinmarketcap/run_coinmarketcap_html_scraper.py
else ifeq ($(target),coinmarketcap_json)
	python3 coinmarketcap/run_coinmarketcap_json_scraper.py
else
	@echo "Usage: make run target=[coingecko|coinmarketcap_html|coinmarketcap_json]"
endif

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
