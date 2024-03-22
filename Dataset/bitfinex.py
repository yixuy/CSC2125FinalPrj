import ccxt
import csv
import time

exchange_symbol = "DOGE:USD"
exchange = ccxt.bitfinex()

now = int(time.time()) * 1000
since = now - 3600 * 1000 # one hour ago

res = []
res += exchange.fetch_trades(exchange_symbol, since=since, limit=10000) # limit is 500

# Specify the CSV file name
filename = f'doge_data/bitfinex_doge_usdt_transaction.csv'

fieldnames = res[0].keys()
fieldnames = {'timestamp', 'datetime', 'symbol', 'type', 'price',  'amount', 'cost' }

filtered_data = [{k: v for k, v in row.items() if k in fieldnames} for row in res]

# Writing to CSV
with open(filename, 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames)
    dict_writer.writeheader()
    dict_writer.writerows(filtered_data)

