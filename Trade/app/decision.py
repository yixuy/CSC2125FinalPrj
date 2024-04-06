import requests
import threading
import time

real_time_exchange_doge = {'binance': 0, 'gemini': 0, 'kraken': 0, 'lbank': 0}
real_time_exchange_shib = {'binance': 0, 'gemini': 0, 'kraken': 0, 'lbank': 0}
future_exchange_doge = {'binance': 0, 'gemini': 0, 'kraken': 0, 'lbank': 0}
future_exchange_shib = {'binance': 0, 'gemini': 0, 'kraken': 0, 'lbank': 0}


def update_exchange(cointype, exchange, frequency):
    """
    update exchange in the map real_time_exchange_doge\
    based on the exchange, update the new one

    """
    global real_time_exchange_doge,future_exchange_doge

    data= {
        'exchange': exchange,
        'cointype': cointype
    }
    while True:
        try:
            response = requests.post("http://127.0.0.1:5000/getPrice", data=data)
            res_json = response.json()
        except Exception as e:
            print(f"An error occurred: {e}")
        
        if cointype == 'doge':
            real_time_exchange_doge[exchange] = res_json['coin_price']
            # todo: future_exchange_doge[exchange] = 
        elif cointype == 'shib':
            real_time_exchange_shib[exchange] = res_json['coin_price']
            # todo: future_exchange_shib[exchange] = 

        time.sleep(frequency)


def buy_sell():
    while True:
        print("Real-time exchange price (DOGE):", real_time_exchange_doge)
        print("Real-time exchange price (SHIB):", real_time_exchange_shib)
        print("Future exchange price (DOGE):", future_exchange_doge)
        print("Future exchange price (SHIB):", future_exchange_shib)
        
        buy_exchange_doge, buy_price_doge = min(real_time_exchange_doge.items(), key=lambda x: x[1])
        sell_exchange_doge, sell_price_doge = max(future_exchange_doge.items(), key=lambda x: x[1])
        buy_exchange_shib, buy_price_shib = min(real_time_exchange_shib.items(), key=lambda x: x[1])
        sell_exchange_shib, sell_price_shib = max(future_exchange_shib.items(), key=lambda x: x[1])
        if sell_price_doge > buy_price_doge:
            print(f"Buy from {buy_exchange_doge} at ${buy_price_doge} and sell to {sell_exchange_doge}, expect at price {sell_price_doge} ")
            # record
        elif sell_price_shib > buy_price_shib:
            print(f"Buy from {buy_exchange_shib} at ${buy_price_shib} and sell to {sell_exchange_shib}, expect at price {sell_price_shib} ")
            # record
        else:
            print("No arbitrage opportunity available.")
        time.sleep(1)


def simulation():
    initial_fund = 10000
    exchange_threads=[]
    for exchange in ['binance', 'gemini', 'kraken', 'lbank']:
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
    
    # while True:
    #     buy_exchange,sell_exchange,buy_price,sell_price = buy_sell()
    #     #update purchase and balance
    #     with open('example.txt', 'a') as file:
    #         file.write(f"Buy from {buy_exchange} at ${buy_price} and sell to {sell_exchange} ")
    #     time.sleep(frequency) # need to update the frequency


if __name__ == "__main__":
    simulation()
    


