import csv
import requests

url = "https://www.bitstamp.net/api/v2/transactions/{market_symbol}/"

market_symbol = "dogeusd"
time_interval = "hour"  # "minute", "hour" or "day"

params = {"time": time_interval}

response = requests.get(url.format(market_symbol=market_symbol), params=params)

if response.status_code == 200:
    transactions = response.json()
    csv_file = "bitstamp.csv"
    fieldnames = ["Amount", "Date", "Price", "TID", "Type"]
    
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Write header
        writer.writeheader()
        
        for transaction in transactions:
            print("Amount:", transaction["amount"])
            print("Date:", transaction["date"])
            print("Price:", transaction["price"])
            print("TID:", transaction["tid"])
            print("Type:", transaction["type"])
            print()  # Empty line for separation

            writer.writerow({
                "Amount": transaction["amount"],
                "Date": transaction["date"],
                "Price": transaction["price"],
                "TID": transaction["tid"],
                "Type": transaction["type"]
            })
    
    print("Transaction data has been written to", csv_file)
else:
    print("Failed to fetch transaction data. Status code:", response.status_code)
