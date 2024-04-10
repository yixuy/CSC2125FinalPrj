import requests
import threading
import time
import utils
import csv

doge_fund_lock = threading.Lock()
shib_fund_lock = threading.Lock()
stop_event = threading.Event()

fund_doge = 0
fund_shib = 0

exchange_name_list = ['mexc', 'okx', 'kraken', 'gateio', 'binance', 'bingx', 'cryptocom', 'gemini', 'lbank', 'bitfinex', 'kucoin', 'htx', 'bitget']

real_time_doge_asks = {'mexc': [], 'okx': [], 'kraken': [], 'gateio': [], 'binance': [], 'bingx': [], 'cryptocom': [], 
                           'gemini': [], 'lbank': [], 'bitfinex': [], 'kucoin': [], 'htx': [], 'bitget': []}
real_time_doge_bids = {'mexc': [], 'okx': [], 'kraken': [], 'gateio': [], 'binance': [], 'bingx': [], 'cryptocom': [], 
                           'gemini': [], 'lbank': [], 'bitfinex': [], 'kucoin': [], 'htx': [], 'bitget': []}
real_time_shib_asks = {'mexc': [], 'okx': [], 'kraken': [], 'gateio': [], 'binance': [], 'bingx': [], 'cryptocom': [], 
                           'gemini': [], 'lbank': [], 'bitfinex': [], 'kucoin': [], 'htx': [], 'bitget': []}
real_time_shib_bids = {'mexc': [], 'okx': [], 'kraken': [], 'gateio': [], 'binance': [], 'bingx': [], 'cryptocom': [], 
                           'gemini': [], 'lbank': [], 'bitfinex': [], 'kucoin': [], 'htx': [], 'bitget': []}
future_doge_sell_prices = {'mexc': 0, 'okx': 0, 'kraken': 0, 'gateio': 0, 'binance': 0, 'bingx': 0, 'cryptocom': 0, 
                           'gemini': 0, 'lbank': 0, 'bitfinex': 0, 'kucoin': 0, 'htx': 0, 'bitget': 0}
future_shib_sell_prices = {'mexc': 0, 'okx': 0, 'kraken': 0, 'gateio': 0, 'binance': 0, 'bingx': 0, 'cryptocom': 0, 
                           'gemini': 0, 'lbank': 0, 'bitfinex': 0, 'kucoin': 0, 'htx': 0, 'bitget': 0}
future_doge_bids = {'mexc': [], 'okx': [], 'kraken': [], 'gateio': [], 'binance': [], 'bingx': [], 'cryptocom': [], 
                           'gemini': [], 'lbank': [], 'bitfinex': [], 'kucoin': [], 'htx': [], 'bitget': []}
future_shib_bids = {'mexc': [], 'okx': [], 'kraken': [], 'gateio': [], 'binance': [], 'bingx': [], 'cryptocom': [], 
                           'gemini': [], 'lbank': [], 'bitfinex': [], 'kucoin': [], 'htx': [], 'bitget': []}

doge_volatilities = {}
shib_volatilities = {}

doge_arbitrages = []
shib_arbitrages = []

def update_exchange(cointype, exchange, frequency):
    """
    update exchange in the map real_time_exchange_doge\
    based on the exchange, update the new one

    """
    global real_time_doge_asks, real_time_doge_bids, real_time_shib_asks, real_time_shib_bids
    global future_doge_sell_prices, future_shib_sell_prices, future_doge_bids, future_shib_bids

    if cointype == 'doge':  
        future_timestamp = 2400000
    elif cointype == 'shib':
        future_timestamp = 840000
    else:
        return
    
    data_current = {
        'exchange': exchange,
        'cointype': cointype
    }
    data_future = {
        'exchange': exchange,
        'cointype': cointype,
        'timestamp': future_timestamp
    }

    while not stop_event.is_set():
        try:
            response_current = requests.post("http://127.0.0.1:5000/getPrice", data=data_current)
            res_current_json = response_current.json()
        except Exception as e:
            print(f"An error occurred: {e}")
        try:
            response_future = requests.post("http://127.0.0.1:5000/getPrice", data=data_future)
            res_future_json = response_future.json()
        except Exception as e:
            print(f"An error occurred: {e}")
        
        if res_future_json['message'] == 'timestamp too large':
            print("data_future reaches the end of market data, stopping....")
            stop_event.set()
            break

        if cointype == 'doge':
            real_time_doge_asks[exchange] = res_current_json['order_book']['asks']
            real_time_doge_bids[exchange] = res_current_json['order_book']['bids']
            max_bid_price = res_current_json['order_book']['bids'][0][0]
            # min_ask_price = res_current_json['order_book']['asks'][0][0]
            future_doge_sell_prices[exchange] = max_bid_price * utils.get_estimate_ratio(latency=2400, sigma=doge_volatilities[exchange], confidence_level=55)
            future_doge_bids[exchange] = res_future_json['order_book']['bids']
        elif cointype == 'shib':
            real_time_shib_asks[exchange] = res_current_json['order_book']['asks']
            real_time_shib_bids[exchange] = res_current_json['order_book']['bids']
            max_bid_price = res_current_json['order_book']['bids'][0][0]
            # min_ask_price = res_current_json['order_book']['asks'][0][0]
            future_shib_sell_prices[exchange] = max_bid_price * utils.get_estimate_ratio(latency=840, sigma=shib_volatilities[exchange], confidence_level=55)
            future_shib_bids[exchange] = res_future_json['order_book']['bids']

        time.sleep(frequency)


def buy_sell():
    time.sleep(2)
    global real_time_doge_asks, real_time_shib_asks
    global fund_doge, fund_shib
    global doge_arbitrages, shib_arbitrages
    
    real_time_doge_low_asks = {}
    real_time_shib_low_asks = {}

    print("Initial DOGE fund:", fund_doge)
    print("Initial SHIB fund:", fund_shib)

    while not stop_event.is_set():
        buy_exchange_doge = None
        buy_price_doge = float('inf')
        # print("real_time_doge_asks: ", real_time_doge_asks)
        for exchange, asks in real_time_doge_asks.items():
            min_ask_price = min(asks, key=lambda x: x[0])[0]
            real_time_doge_low_asks[exchange] = min_ask_price ####
            if min_ask_price < buy_price_doge:
                buy_price_doge = min_ask_price
                buy_exchange_doge = exchange
        real_time_doge_buys = real_time_doge_asks[buy_exchange_doge]
        

        buy_exchange_shib = None
        buy_price_shib = float('inf')
        for exchange, asks in real_time_shib_asks.items():
            min_ask_price = min(asks, key=lambda x: x[0])[0]
            real_time_shib_low_asks[exchange] = min_ask_price ####
            if min_ask_price < buy_price_shib:
                buy_price_shib = min_ask_price
                buy_exchange_shib = exchange
        real_time_shib_buys = real_time_shib_asks[buy_exchange_shib]

        sell_exchange_doge, expect_sell_price_doge = max(future_doge_sell_prices.items(), key=lambda x: x[1])
        sell_exchange_shib, expect_sell_price_shib = max(future_shib_sell_prices.items(), key=lambda x: x[1])
        future_doge_sells = future_doge_bids[sell_exchange_doge]
        future_shib_sells = future_shib_bids[sell_exchange_shib]

        print("Real-time buy prices (DOGE):", real_time_doge_low_asks)
        print("Future expected sell prices (DOGE):", future_doge_sell_prices)
        print("Real-time buy prices (SHIB):", real_time_shib_low_asks)
        print("Future expected sell prices (SHIB):", future_shib_sell_prices)
        
        if expect_sell_price_doge > buy_price_doge:
            print(f"Buying DOGE from {buy_exchange_doge} at price starting of ${buy_price_doge} and selling to {sell_exchange_doge},")
            print(f"Expecting at sell price of {expect_sell_price_doge} ")
            with doge_fund_lock:
                bought_amount = 0
                fund_doge_before_trade = fund_doge
                for ask in real_time_doge_buys[:10]:
                    if ask[0] >= expect_sell_price_doge:
                        break
                    if ask[0] * ask[1] > fund_doge:
                        bought_amount += fund_doge / ask[0]
                        fund_doge -= ask[0] * bought_amount
                        break
                    bought_amount += ask[1]
                    fund_doge -= ask[0] * ask[1]
                volume = bought_amount
                for bid in future_doge_sells:
                    if bid[1] > bought_amount:
                        fund_doge += bid[0] * bought_amount
                        bought_amount = 0
                        break
                    fund_doge += bid[0] * bid[1]
                    bought_amount -= bid[1]
                profit = fund_doge - fund_doge_before_trade
                arbitrage = [buy_exchange_doge, sell_exchange_doge, volume, profit, time.time() - start_time]
                doge_arbitrages.append(arbitrage)
                    
        elif expect_sell_price_shib > buy_price_shib:
            print(f"Buying SHIB from {buy_exchange_shib} at price strating of ${buy_price_shib} and selling to {sell_exchange_shib},")
            print(f"Expecting at sell price of {expect_sell_price_shib} ")
            with shib_fund_lock:
                bought_amount = 0
                fund_shib_before_trade = fund_shib
                for ask in real_time_shib_buys[:10]:
                    if ask[0] > expect_sell_price_shib:
                        break
                    if ask[0] * ask[1] > fund_shib:
                        bought_amount += fund_shib / ask[0]
                        fund_shib -= ask[0] * bought_amount
                        break
                    bought_amount += ask[1]
                    fund_shib -= ask[0] * ask[1]
                volume = bought_amount
                for bid in future_shib_sells:
                    if bid[1] > bought_amount:
                        fund_shib += bid[0] * bought_amount
                        bought_amount = 0
                        break
                    fund_shib += bid[0] * bid[1]
                    bought_amount -= bid[1]
                profit = fund_shib - fund_shib_before_trade
                arbitrage = [buy_exchange_shib, sell_exchange_shib, volume, profit, time.time() - start_time]
                shib_arbitrages.append(arbitrage)

        else:
            print("No arbitrage opportunity available.")
        
        print("Remaining DOGE fund:", fund_doge)
        print("Remaining SHIB fund:", fund_shib)
        time.sleep(1)


def simulation(initial_fund):
    global fund_doge, fund_shib
    fund_doge = float(initial_fund / 2)
    fund_shib = float(initial_fund / 2)

    exchange_threads=[]
    for exchange in exchange_name_list:
        t1 = threading.Thread(target=update_exchange, args=('doge', exchange, 1))
        t2 = threading.Thread(target=update_exchange, args=('shib', exchange, 1))
        t1.start()
        t2.start()
        exchange_threads.append(t1)
        exchange_threads.append(t2)

    buy_sell_thread = threading.Thread(target=buy_sell)
    buy_sell_thread.start()
    
    for thread in exchange_threads:
        thread.join()
    buy_sell_thread.join()

    header = ['buy_exchange', 'sell_exchange', 'volume', 'profit', 'time']
    save_file_doge = f"../records/arbitrage_doge_records.csv"
    with open(save_file_doge, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(header)
        writer.writerows(doge_arbitrages)
    save_file_shib = f"../records/arbitrage_shib_records.csv"
    with open(save_file_shib, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(header)
        writer.writerows(shib_arbitrages)


if __name__ == "__main__":
    # Prepare volatilities
    doge_volatilities = utils.get_doge_volatilities()
    shib_volatilities = utils.get_shib_volatilities()
    start_time = time.time()
    simulation(20000)
    


