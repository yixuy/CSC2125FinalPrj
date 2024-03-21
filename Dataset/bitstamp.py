import ccxt
import csv
import time

# exchange_symbol = "dogeusd"
exchange_symbol = "shibusd"
exchange = ccxt.bitstamp()

now = int(time.time()) * 1000
since = now - 3600 * 1000 # one hour ago

res = []
res += exchange.fetch_trades(exchange_symbol, since=since, limit=10000) # limit is 500

# Specify the CSV file name
filename = f'shiba_data/bitstamp_shiba_usd_transaction.csv'

fieldnames = res[0].keys()
fieldnames = {'timestamp', 'datetime', 'symbol', 'type', 'price',  'amount', 'cost' }

filtered_data = [{k: v for k, v in row.items() if k in fieldnames} for row in res]

# Writing to CSV
with open(filename, 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames)
    dict_writer.writeheader()
    dict_writer.writerows(filtered_data)



# ========================================== Old API Method =======================================

# import csv
# import requests

# url = "https://www.bitstamp.net/api/v2/transactions/{market_symbol}/"

# market_symbol = "dogeusd"
# time_interval = "hour"  # "minute", "hour" or "day"

# params = {"time": time_interval}

# response = requests.get(url.format(market_symbol=market_symbol), params=params)

# if response.status_code == 200:
#     transactions = response.json()
#     csv_file = "bitstamp_old.csv"
#     fieldnames = ["Amount", "Date", "Price", "TID", "Type"]
    
#     with open(csv_file, mode="w", newline="") as file:
#         writer = csv.DictWriter(file, fieldnames=fieldnames)
        
#         # Write header
#         writer.writeheader()
        
#         for transaction in transactions:
#             print("Amount:", transaction["amount"])
#             print("Date:", transaction["date"])
#             print("Price:", transaction["price"])
#             print("TID:", transaction["tid"])
#             print("Type:", transaction["type"])
#             print()  # Empty line for separation

#             writer.writerow({
#                 "Amount": transaction["amount"],
#                 "Date": transaction["date"],
#                 "Price": transaction["price"],
#                 "TID": transaction["tid"],
#                 "Type": transaction["type"]
#             })
    
#     print("Transaction data has been written to", csv_file)
# else:
#     print("Failed to fetch transaction data. Status code:", response.status_code)
