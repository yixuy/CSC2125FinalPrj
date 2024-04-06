import requests
import threading
import time

real_time_exchange_doge={} # {''binance':3.111';'karen':3.0024}
future_exchange_doge={}


def update_exchange(cointype='doge',exchange, frequency):
    """
    update exchange in the map real_time_exchange_doge\
    based on the exchange, update the new one

    """
    global real_time_exchange_doge,future_exchange_doge

    data= {
        'exchange':exchange,
        'cointype': cointype
    }
    while True:
        try:
            response = requests.post("http://127.0.0.1:5000/getPrice",data=data)
             # unable to import from the Dataset/app/model.py
            # update the real_time and future_exchange
        except Exception as e:
            print(f"An error occurred: {e}")
        time.sleep(frequency)
    



def buy_sell():
    global real_time_exchange_doge,future_exchange_doge
    buy_exchange, buy_price = min(real_time_exchange_doge.items(), key=lambda x: x[1])
    sell_exchange, sell_price = max(future_exchange_doge.items(), key=lambda x: x[1])
    if sell_price > buy_price:
        print(f"Buy from {buy_exchange} at ${buy_price} and sell to {sell_exchange} ")
        return buy_exchange,sell_exchange,buy_price,sell_price
    else:
        print("No arbitrage opportunity available.")
        return "",""


def simulation():
    initial_fund = 10000
    threads=[]
    for exchange in ['']:
        t = threading.Thread(target = update_exchange,args=())# need to be fixed
        t.start()
        threads.append(t)
    
    while True:
        buy_exchange,sell_exchange,buy_price,sell_price = buy_sell()
        #update purchase and balance
        with open('example.txt', 'a') as file:
            file.write(f"Buy from {buy_exchange} at ${buy_price} and sell to {sell_exchange} ")
        time.sleep(frequency) # need to update the frequency
















