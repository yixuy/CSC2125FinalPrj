
import ccxt

exchange_platform_1 = ccxt.binance({
    'apiKey': 'API_KEY_1',
    'secret': 'SECRET_1',
})

exchange_platform_2 = ccxt.kraken({
    'apiKey': 'API_KEY_1',
    'secret': 'SECRET_1',
})

ticker1 = exchange_platform_1.fetch_ticker('DOGE/USDT')
ticker2 = exchange_platform_2.fetch_ticker('DOGE/USDT')
print(ticker1['last'], ticker2['last'])


sell_order = exchange_platform_1.create_order('DOGE/USDT', 'market', 'sell', amount=0.01)
buy_order = exchange_platform_2.create_order('DOGE/USDT', 'market', 'buy', amount=0.01)
