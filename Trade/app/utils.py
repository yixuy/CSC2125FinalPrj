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
    # key1 = 'timestamp'
    # key2 = 'price'
    key1 = 'date'
    key2 = 'open'

    # Read the data from the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    df[key1] = pd.to_datetime(df[key1], unit='ms')

    # Calculate logarithmic returns
    df['returns'] = np.log(df[key2] / df[key2].shift(1))

    # Calculate the time differences in milliseconds
    df['time_diff_ms'] = df[key1].diff().dt.total_seconds() * 1000  # Convert seconds to milliseconds

    # Convert time differences to seconds
    df['time_diff_sec'] = df['time_diff_ms'] / 1000  # Convert milliseconds to seconds

    # Calculate the squared returns weighted by time difference
    df['weighted_squared_returns'] = df['returns'] ** 2 * df['time_diff_sec']

    # Calculate the sum of weighted squared returns
    sum_weighted_squared_returns = df['weighted_squared_returns'].sum()

    # Calculate the total time difference in seconds
    total_time_diff_sec = df['time_diff_sec'].sum()

    # Calculate the volatility per second
    volatility_per_sec = np.sqrt(sum_weighted_squared_returns / total_time_diff_sec)

    return volatility_per_sec


def get_doge_volatilities():
    d = {}
    for market in market_list:
        d[market['name']] = get_volatility(f"../../Dataset/ohlcvs/doge_data/{market['name']}_doge_transaction.csv")
    
    return d


def get_shib_volatilities():
    d = {}
    for market in market_list:
        d[market['name']] = get_volatility(f"../../Dataset/ohlcvs/shib_data/{market['name']}_shib_transaction.csv")
    
    return d


if __name__ == "__main__":
    print(get_estimate_ratio(latency = 2400, sigma = 0.0014224225155174714, confidence_level = 90))
    # for market in market_list:
    #     get_volatility(f"../../Dataset/ohlcvs/doge_data/{market['name']}_doge_transaction.csv")