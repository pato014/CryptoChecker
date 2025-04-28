import requests
import time
import threading
import queue
import signal
from datetime import datetime
from collections import deque


""" 
    Fetch prices from API
"""
class PriceFetcher:
    def __init__(self, url, params, output_queue, shutdown_event):
        self.url = url
        self.params = params
        self.output_queue = output_queue
        self.shutdown_event = shutdown_event
        self.max_failures = 5

    def fetch_price(self):
        response = requests.get(self.url, params=self.params, timeout=5)
        response.raise_for_status()
        data = response.json()
        price = data["bitcoin"]["usd"]
        timestamp = data["bitcoin"]["last_updated_at"]
        readable_time = datetime.utcfromtimestamp(timestamp).isoformat()
        return readable_time, price

    def run(self):
        failure_count = 0
        backoff = 1

        while not self.shutdown_event.is_set():
            try:
                timestamp, price = self.fetch_price()
                self.output_queue.put((timestamp, price))
                failure_count = 0
                backoff = 1
                time.sleep(1)

            except Exception as e:
                failure_count += 1
                print(f"[Fetcher] Error: {e}. Retrying in {backoff} seconds...")
                time.sleep(backoff)
                backoff = min(backoff * 2, 60)

                if failure_count >= self.max_failures:
                    print("[Fetcher] 5 consecutive failures encountered. Continuing...")


"""
    Calculate SMA, fromat output for printing
"""
class PricePrinter:
    def __init__(self, input_queue, shutdown_event):
        self.input_queue = input_queue
        self.shutdown_event = shutdown_event
        self.prices = deque(maxlen=10)

    def calculate_sma(self):
        if not self.prices:
            return 0
        return sum(self.prices) / len(self.prices)

    def run(self):
        while not self.shutdown_event.is_set():
            try:
                timestamp, price = self.input_queue.get(timeout=1)
                self.prices.append(price)
                sma = self.calculate_sma()
                print(f"[{timestamp}] BTC → USD: ${price:,.2f} | SMA(10): ${sma:,.2f}")
            except queue.Empty:
                continue


"""
    Main function for running the crawler
"""
class CryptoCrawler:
    URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_last_updated_at=true"

    def __init__(self):
        self.shutdown_event = threading.Event()
        self.price_queue = queue.Queue()
        self.params = {
            "ids": "bitcoin",
            "vs_currencies": "usd",
            "include_last_updated_at": "true"
        }

    def signal_handler(self, sig, frame):
        print("\nShutting down...")
        self.shutdown_event.set()

    def run(self):
        signal.signal(signal.SIGINT, self.signal_handler)

        fetcher = PriceFetcher(
            url=self.URL,
            params=self.params,
            output_queue=self.price_queue,
            shutdown_event=self.shutdown_event
        )

        printer = PricePrinter(
            input_queue=self.price_queue,
            shutdown_event=self.shutdown_event
        )

        fetcher_thread = threading.Thread(target=fetcher.run, daemon=True)
        fetcher_thread.start()

        try:
            printer.run()
        finally:
            fetcher_thread.join()
            print("Exited cleanly.")


def main():
    crawler = CryptoCrawler()
    crawler.run()


if __name__ == "__main__":
    main()
