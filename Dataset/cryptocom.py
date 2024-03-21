import ccxt
import csv
import time

# exchange_symbol = "DOGEUSD-PERP"
exchange_symbol = "SHIBUSD-PERP"
exchange = ccxt.cryptocom()

now = int(time.time()) * 1000
since = now - 3600 * 1000 # one hour ago

res = []
res += exchange.fetch_trades(exchange_symbol, since=since, limit=10000) # limit is 500

# Specify the CSV file name
filename = f'shiba_data/cryptocom_shiba_usd_transaction.csv'

fieldnames = res[0].keys()
fieldnames = {'timestamp', 'datetime', 'symbol', 'type', 'price',  'amount', 'cost' }

filtered_data = [{k: v for k, v in row.items() if k in fieldnames} for row in res]

# Writing to CSV
with open(filename, 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames)
    dict_writer.writeheader()
    dict_writer.writerows(filtered_data)



# ========================================== Old API Method =======================================
    
# import requests
# import datetime
# import csv

# def get_trades(url, instrument_name, start_ts, end_ts):
#     params = {
#         "instrument_name": instrument_name,
#         "start_ts": start_ts,
#         "end_ts": end_ts,
#         "count": 150 # max is 150
#     }

#     response = requests.get(url, params=params)
#     if response.status_code == 200:
#         trades_data = response.json()
#         return trades_data
#     else:
#         print(f"Failed to fetch trade data. Status code: {response.status_code}")
#         return None

# url = "https://api.crypto.com/exchange/v1/public/get-trades"
# start_time = datetime.datetime(2024, 3, 16, 14, 0, 0)
# end_time = datetime.datetime(2024, 3, 16, 15, 0, 0)
# instrument_name = "DOGEUSD-PERP"
# start_ts = int(start_time.timestamp())
# end_ts = int(end_time.timestamp())
# trades = get_trades(url, instrument_name, start_ts, end_ts)

# if trades:
#     csv_file = "cryptocom_old.csv"
#     trades_data = trades['result']['data']

#     with open(csv_file, mode='w', newline='') as file:
#         writer = csv.writer(file)

#         writer.writerow(["Trade ID", "Trade Time", "Trade Timestamp (Milliseconds)", "Trade Timestamp (Nanoseconds)", "Quantity", "Price", "Side", "Instrument Name"])

#         for trade in trades_data:
#             timestamp = int(trade['t'])
#             timestamp_str = datetime.datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d %H:%M:%S')
#             writer.writerow([trade['d'], timestamp_str, trade['t'], trade['tn'], trade['q'], trade['p'], trade['s'], trade['i']])

#     print("Data has been written to", csv_file)
