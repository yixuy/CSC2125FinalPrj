import ccxt
import csv
import time

exchange_symbol = 'DOGE-USDT'
exchange = ccxt.bingx()

now = int(time.time()) * 1000
since = now - 3600 * 1000 # one hour ago

res = []
res += exchange.fetch_trades(exchange_symbol, since=since, limit=10000) # limit is 100

# Specify the CSV file name
filename = f'data/bingx.csv'

fieldnames = res[0].keys()
fieldnames = {'timestamp', 'datetime', 'symbol', 'type', 'price',  'amount', 'cost' }

filtered_data = [{k: v for k, v in row.items() if k in fieldnames} for row in res]

# Writing to CSV
with open(filename, 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames)
    dict_writer.writeheader()
    dict_writer.writerows(filtered_data)

