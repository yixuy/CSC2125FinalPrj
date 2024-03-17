import requests
import datetime
import csv

def get_trades(url, instrument_name, start_ts, end_ts):
    params = {
        "instrument_name": instrument_name,
        "start_ts": start_ts,
        "end_ts": end_ts,
        "count": 150 # max is 150
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        trades_data = response.json()
        return trades_data
    else:
        print(f"Failed to fetch trade data. Status code: {response.status_code}")
        return None

url = "https://api.crypto.com/exchange/v1/public/get-trades"
start_time = datetime.datetime(2024, 3, 16, 14, 0, 0)
end_time = datetime.datetime(2024, 3, 16, 15, 0, 0)
instrument_name = "DOGEUSD-PERP"
start_ts = int(start_time.timestamp())
end_ts = int(end_time.timestamp())
trades = get_trades(url, instrument_name, start_ts, end_ts)

if trades:
    csv_file = "crypto.csv"
    trades_data = trades['result']['data']

    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(["Trade ID", "Trade Time", "Trade Timestamp (Milliseconds)", "Trade Timestamp (Nanoseconds)", "Quantity", "Price", "Side", "Instrument Name"])

        for trade in trades_data:
            timestamp = int(trade['t'])
            timestamp_str = datetime.datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([trade['d'], timestamp_str, trade['t'], trade['tn'], trade['q'], trade['p'], trade['s'], trade['i']])

    print("Data has been written to", csv_file)
