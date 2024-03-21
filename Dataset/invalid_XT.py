from pyxt.perp import Perp
from pyxt.spot import Spot
import csv
import time
from datetime import datetime

xt = Perp(host="https://fapi.xt.com", access_key='', secret_key='')
api_key = "xxxxx"
secret_key = "xxxxx"
xt = Spot(host="https://sapi.xt.com", access_key=api_key, secret_key=secret_key)
exchange_symbol = 'doge_usdt'

# print(xt.get_tickers(symbol='doge_usdt'))
# print(xt.get_tickers_book(symbol='btc_usdt'))
t_end = time.time() + 1 * 1
res = []
fieldnames = {'timestamp', 'symbol', 'price'}

rename_map = {
    't': 'timestamp',
    's': 'symbol',
    'p': 'price'
    # Add more mappings as necessary
}
def rename_keys(data, rename_map):
    new_data = []
    for row in data:
        new_row = {rename_map.get(key, key): value for key, value in row.items()}
        # new_row = convert_timestamp(new_row)
        new_data.append(new_row)
    return new_data

def convert_timestamp(item):
    item['timestamp'] = datetime.utcfromtimestamp(float(item['timestamp']) / 1000).strftime('%Y-%m-%d %H:%M:%S')
    return item

while time.time() < t_end:
    res += xt.get_tickers(symbol=exchange_symbol)

res = rename_keys(res, rename_map)
converted_data = [convert_timestamp(item) for item in res]

filename = f'data/XT_{exchange_symbol}_transaction.csv'
with open(filename, 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames)
    dict_writer.writeheader()
    dict_writer.writerows(res)

# ap: Ask Price
# bp: Bid Price
# aq: Ask Quantity
# bq: Bid Quantity
