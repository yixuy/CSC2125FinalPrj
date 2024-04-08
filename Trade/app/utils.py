import pandas as pd
import numpy as np
import ccxt
from scipy import stats 

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


def get_estimate_ratio(latency: float, sigma: float, confidence_level:int = 99, risk_free_rate: float = 0):
    '''
    Return the lowest estimate ratio given a confidence_interval 
    latency: estimated time interval, in second
    sigma: standard deviation, per second
    confidence_level: the confidence_level we want, in percentage
    risk_free_rate: risk free rate (per second), set to 0 by default
    '''
    z = - stats.norm.ppf(confidence_level / 100)

    t = latency
    r = risk_free_rate
    
    return np.exp((r - 0.5 * sigma ** 2) * t + sigma * t ** 0.5 * z)


def get_volatility(csv_file):

    # Read the data from the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    adj_price = []
    l = len(df['timestamp'])
    beg = (df['timestamp'][0] // 1000 + 1) * 1000
    end = (df['timestamp'][l - 1] // 1000) * 1000

    i = 0
    for t in range(beg, end + 1, 1000):
        while df['timestamp'][i] < t:
            i += 1
        if df['timestamp'][i] == t:
            adj_price.append(df['price'][i])
        else:
            interv = df['timestamp'][i] - df['timestamp'][i - 1]
            adj_price.append(df['price'][i - 1] * (t - df['timestamp'][i - 1]) / interv + df['price'][i] * (df['timestamp'][i] - t)/ interv)
    
    adj_price = np.array(adj_price)

    returns = adj_price[1:] / adj_price[:-1] - 1

    volatility = np.std(returns)

    return volatility


def get_doge_volatilities():
    d = {}
    for market in market_list:
        d[market['name']] = get_volatility(f"../../Dataset/doge_data/{market['name']}_doge_transaction.csv")
    
    return d


def get_shib_volatilities():
    d = {}
    for market in market_list:
        d[market['name']] = get_volatility(f"../../Dataset/shib_data/{market['name']}_shib_transaction.csv")
    
    return d


if __name__ == "__main__":
    print(get_estimate_ratio(latency = 2400, sigma = 0.0003022265544126979, confidence_level = 80))
    # for market in market_list:
    #     get_volatility(f"../../Dataset/doge_data/{market['name']}_doge_transaction.csv")