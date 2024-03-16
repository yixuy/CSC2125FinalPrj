import ccxt
import requests
import json
import csv
import time
import pyxt

# exchange platform
print(ccxt.exchanges)
# choose exchange platform
exchange_symbol = "doge_usdt"
exchange = ccxt.lbank()
btc_usdt = exchange.fetch_trades(exchange_symbol)

t_end = time.time() + 1*1
res = []
while time.time() < t_end:
    res += exchange.fetch_trades(exchange_symbol)

# Specify the CSV file name
filename = f'data/{exchange_symbol}_transaction.csv'
# Fieldnames or column headers in the CSV file


fieldnames = res[0].keys()
print(fieldnames)
fieldnames = {'timestamp', 'datetime', 'symbol', 'type', 'price',  'amount', 'cost' }
# columns_to_exclude = {'datetime', 'price'}
filtered_data = [{k: v for k, v in row.items() if k in fieldnames} for row in res]

# Writing to CSV
with open(filename, 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames)
    dict_writer.writeheader()
    dict_writer.writerows(filtered_data)







