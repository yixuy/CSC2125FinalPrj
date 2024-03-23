# Fieldnames or column headers in the CSV file
import ccxt
import csv
import time

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

def get_market_data(exchange, exchange_symbol: str, save_file: str, time_since: int):

    res = []
    if time_since == None:
        res += exchange.fetch_trades(exchange_symbol, limit=10000)
    else:
        res += exchange.fetch_trades(exchange_symbol, since = time_since, limit=10000)

    # Specify the CSV file name
    filename = save_file

    fieldnames = {'timestamp', 'datetime', 'symbol', 'type', 'price',  'amount', 'cost' }

    filtered_data = [{k: v for k, v in row.items() if k in fieldnames} for row in res]

    # Writing to CSV
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames)
        dict_writer.writeheader()
        dict_writer.writerows(filtered_data)

if __name__ == "__main__":

    default_time_until = int(time.time()) * 1000
    default_time_since = default_time_until - 3600 * 1000 # 1hr data by default

    for market in market_list:
        time_since = None if market["name"] == "mexc" else default_time_since
        time_until = None if market["name"] == "mexc" else default_time_until
        print(f"Fetching data for {market['name']}...")
        # Get Doge Data
        save_file = f"./doge_data/{market['name']}_doge_transaction.csv"
        get_market_data(market["exchange"], market["doge_symbol"], save_file, time_since)
        # Get Shib Data
        save_file = f"./shib_data/{market['name']}_shib_transaction.csv"
        get_market_data(market["exchange"], market["shib_symbol"], save_file, time_since)
        
