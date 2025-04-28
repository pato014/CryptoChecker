import csv


class CSVStorage:
    def __init__(self, filename="coinmarketcap_data.csv"):
        self.filename = filename

    def save(self, data):
        if not data:
            return

        keys = data[0].keys()

        with open(self.filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)

        print(f"Saved {len(data)} records to {self.filename}")
