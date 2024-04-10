# Fieldnames or column headers in the CSV file
import ccxt
import csv
import time
import random
from datetime import datetime, timedelta
import threading
import pickle

market_list = [
    {
        "name": "mexc",
        "exchange": ccxt.mexc(),
        "doge_symbol": "DOGE/USDT",
        "shib_symbol": "SHIB/USDT"
    },
    {
        "name": "okx",
        "exchange": ccxt.okx(),
        "doge_symbol": "DOGE/USD:DOGE",
        "shib_symbol": "SHIB/USDT"
    },
    {
        "name": "kraken",
        "exchange": ccxt.kraken(),
        "doge_symbol": "DOGE/USD",
        "shib_symbol": "SHIB/USD"
    },
    {
        "name": "gateio",
        "exchange": ccxt.gateio(),
        "doge_symbol": "DOGE/USDT",
        "shib_symbol": "SHIB/USDT"
    },
    {
        "name": "binance",
        "exchange": ccxt.binance(),
        "doge_symbol": "DOGE/USD",
        "shib_symbol": "SHIB/USDT"
    },
    {
        "name": "bingx",
        "exchange": ccxt.bingx(),
        "doge_symbol": "DOGE-USDT",
        "shib_symbol": "SHIB-USDT"
    },
    {
        "name": "bitstamp",
        "exchange": ccxt.bitstamp(),
        "doge_symbol": "dogeusd",
        "shib_symbol": "shibusd"
    },
    {
        "name": "cryptocom",
        "exchange": ccxt.cryptocom(),
        "doge_symbol": "DOGEUSD-PERP",
        "shib_symbol": "SHIBUSD-PERP"
    },
    {
        "name": "gemini",
        "exchange": ccxt.gemini(),
        "doge_symbol": "dogeusd",
        "shib_symbol": "shibusd"
    },
    {
        "name": "lbank",
        "exchange": ccxt.lbank(),
        "doge_symbol": "doge_usdt",
        "shib_symbol": "shib_usdt"
    },
    {
        "name": "bitfinex",
        "exchange": ccxt.bitfinex(),
        "doge_symbol": "DOGE:USD",
        "shib_symbol": "SHIB:USD"
    },
    {
        "name": "kucoin",
        "exchange": ccxt.kucoin(),
        "doge_symbol": "DOGE-USDT",
        "shib_symbol": "SHIB-USDT"
    },
    {
        "name": "htx",
        "exchange": ccxt.htx(),
        "doge_symbol": "DOGE/USDT",
        "shib_symbol": "SHIB/USDT"
    },
    {
        "name": "bitget",
        "exchange": ccxt.bitget(),
        "doge_symbol": "DOGEUSDT",
        "shib_symbol": "SHIBUSDT"
    }
]

def get_market_data(exchange, exchange_symbol: str, save_file: str, time_since: int, time_until: int):

    res = []
    if time_since == None:
        res += exchange.fetch_trades(exchange_symbol, limit=10000)
    else:
        from_ts = time_since
        while True:
            trades =  exchange.fetch_trades(exchange_symbol, since = from_ts, limit=10000)
            # print(trades)
            res += trades
            if trades[-1]['timestamp'] == from_ts or trades[-1]['timestamp'] >= time_until:
                break
            from_ts = trades[-1]['timestamp']

    # Specify the CSV file name
    filename = save_file

    fieldnames = {'timestamp', 'datetime', 'symbol', 'type', 'price',  'amount', 'cost' }

    filtered_data = [{k: v for k, v in row.items() if k in fieldnames} for row in res]

    # Writing to CSV
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames)
        dict_writer.writeheader()
        dict_writer.writerows(filtered_data)


def get_market_data_ohlcv(exchange, exchange_symbol: str, save_file: str, time_since: int):
    
    res = exchange.fetch_ohlcv(exchange_symbol, '1m', since=time_since, limit=720)

    filename = save_file
    header = ['date', 'open', 'high', 'low', 'close', 'volume']

    # Writing to CSV
    with open(filename, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(header)
        writer.writerows(res)


def get_order_books(exchange, exchange_symbol, limit, save_file: str):
    target_time = time.time() + 60*60*5
    with open(save_file, 'wb') as f: 
        while time.time() < target_time:
            try:
                order_book = exchange.fetch_order_book(symbol = exchange_symbol, limit = limit)
                if order_book['timestamp'] == None:
                    order_book['timestamp'] = int(time.time()) * 1000
                # res += order_book
                pickle.dump(order_book, f)
                # print(order_book)
            except Exception as e:
                print(f"An error occurred: {e}")

            time.sleep(1)


if __name__ == "__main__":

    # time_now = int(time.time()) * 1000
    # time_since = time_now - 3600 * 1000 * 42 

    # for market in market_list:
    #     print(f"Fetching data for {market['name']}...")
    #     # Get Doge Data
    #     save_file = f"./static/ohlcvs/doge_data/{market['name']}_doge_transaction.csv"
    #     get_market_data_ohlcv(market["exchange"], market["doge_symbol"], save_file, time_since)
    #     # Get Shib Data
    #     save_file = f"./static/ohlcvs/shib_data/{market['name']}_shib_transaction.csv"
    #     get_market_data_ohlcv(market["exchange"], market["shib_symbol"], save_file, time_since)
    
    
    threads = []
    for market in market_list:
        # if market['name'] == 'bitstamp': # limit argument does not work on bitstamp
        #     continue
        print(f"Fetching data for {market['name']}...")
        # limit = 20 if market["name"] == "kucoin" else 10 # kucoin only accept limit = 20 or 100
        limit = 20
        
        save_file_doge = f"./static/orders/doge_data/{market['name']}_doge_orderbooks.pkl"
        save_file_shib = f"./static/orders/shib_data/{market['name']}_shib_orderbooks.pkl"
        
        t1 = threading.Thread(target=get_order_books, args=(market["exchange"], market["doge_symbol"], limit, save_file_doge))
        t2 = threading.Thread(target=get_order_books, args=(market["exchange"], market["shib_symbol"], limit, save_file_shib))
        t1.start()
        t2.start()
        threads.append(t1)
        threads.append(t2)
    
    for thread in threads:
        thread.join()
    
    print("all threads joined")

    for market in market_list:
        if market['name'] == 'bitstamp': # limit argument does not work on bitstamp
            continue
        
        print(f"printing out {market['name']} doge data.....")
        order_books_doge = []
        count_doge = 0
        with open(f"./static/orders/doge_data/{market['name']}_doge_orderbooks.pkl", "rb") as f:
            try:
                while True:
                    order_book = pickle.load(f)
                    order_books_doge.append(order_book)
                    count_doge += 1
            except EOFError:
                pass  # Reached end of file
        print(order_books_doge[0])
        print(order_books_doge[-1])
        print(count_doge)

        print(f"printing out {market['name']} shib data.....")
        order_books_shib = []
        count_shib = 0
        with open(f"./static/orders/shib_data/{market['name']}_shib_orderbooks.pkl", "rb") as f:
            try:
                while True:
                    order_book = pickle.load(f)
                    order_books_shib.append(order_book)
                    count_shib += 1
            except EOFError:
                pass  # Reached end of file
        print(order_books_shib[0])
        print(order_books_shib[-1])
        print(count_shib)