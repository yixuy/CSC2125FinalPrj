import time
import csv
import requests
from datetime import datetime

exchange_symbol = 'DOGEUSDT'  # Dogecoin to Tether pair, adjust the pair according to your needs
limit = 1000  # Adjust based on how many trades you want to fetch (check the API's limit)
url = f'https://api.deepcoin.com/deepcoin/market/tickers/?instType=SWAP&uly=DOGE-USDT'
# url = f'https://api.deepcoin.com/deepcoin/market/candles/instId="BTC-USDT"'
def convert_timestamp(item):
    item = datetime.utcfromtimestamp(float(item) / 1000).strftime('%Y-%m-%d %H:%M:%S')
    return item

end = time.time() + 1*5
res = []
while time.time() < end:
    response = requests.get(url)
    trades = response.json()['data']
    print(trades)
    res.append({'datetime': convert_timestamp(trades[0]['ts']), 'price': trades[0]['last']})

fieldnames = {'datetime', 'price'}
filename = f'data/deep_coin_{exchange_symbol}_transaction.csv'

# Writing to CSV
with open(filename, 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames)
    dict_writer.writeheader()
    dict_writer.writerows(res)