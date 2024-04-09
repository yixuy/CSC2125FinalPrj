'''
Write main function for market simulator

We want server to have one functionality
When server received request (cointype, exchange, timestamp), 
respond with (order_book)
'''

from app import marketsim
from flask import jsonify, request
import os
import csv
import time
import sys
import pickle

current_dir = os.path.dirname(os.path.abspath(__file__))

# exchange_name_list = ["mexc", "okx", "kraken", "gateio", "binance", "bingx", "bitstamp", "cryptocom", "gemini", "lbank", "bitfinex", "kucoin", "htx", "bitget"]
exchange_name_list = ["mexc", "okx", "kraken", "gateio", "binance", "bingx", "cryptocom", "gemini", "lbank", "bitfinex", "kucoin", "htx", "bitget"]

def getMarket():
    market = {}
    for cointype in ["doge", "shib"]:
        coin_market = {}
        for exchange in exchange_name_list:
            if sys.platform.startswith('win'):
                # For Windows
                pickle_file_path = os.path.join(current_dir, r"static\orders\{}_data\{}_{}_orderbooks.pkl".format(cointype, exchange, cointype))
            else:
                pickle_file_path = os.path.join(current_dir, r"static/orders/{}_data/{}_{}_orderbooks.pkl".format(cointype, exchange, cointype))
            print(f"retrieving {exchange} {cointype} data into memory...")
            order_books = []
            with open(pickle_file_path, "rb") as f:
                try:
                    while True:
                        order_book = pickle.load(f)
                        order_books.append(order_book)
                except EOFError:
                    pass  # Reached end of file
            coin_market[exchange] = order_books
        market[cointype] = coin_market
    return market

def getMarketStartTime(market):
    return market['shib']['bitget'][0]['timestamp']


market = getMarket()
market_start_timestamp = getMarketStartTime(market)
print("market start timestamp: ", market_start_timestamp)
real_start_timestamp = round(time.time() * 1000)
print("real start timestamp: ", real_start_timestamp)

@marketsim.route('/',methods=['GET'])
def main():
    return 'Hello, World'

@marketsim.route('/getPrice',methods=['POST'])
def getPrice():
    if 'exchange' not in request.form:
        return "Need an exchange market"
    if 'cointype' not in request.form:
        return "Need a cointype"
    exchange = request.form.get('exchange')
    cointype = request.form.get('cointype')
    
    real_current_timestamp = round(time.time() * 1000)
    print("real current timestamp: ", real_current_timestamp)
    elapsed_time = real_current_timestamp - real_start_timestamp
    if 'timestamp' not in request.form:
        market_target_timestamp = market_start_timestamp + elapsed_time
        print("market target timestamp: ", market_target_timestamp)
    else:
        market_current_time = market_start_timestamp + elapsed_time
        market_target_timestamp = int(request.form.get('timestamp')) + market_current_time
        print("market current timestamp: {}, market target timestamp: {}".format(market_current_time, market_target_timestamp))
    
    start_time_micro = time.time_ns() // 1000

    order_books = market[cointype][exchange]
    res_order_book = {}
    
    if market_target_timestamp < order_books[0]['timestamp']:
        print("Cannot find order book that matches the timestamp, timestamp too small")
        response = jsonify(success='False', message='timestamp too small', order_book={})
        return response
    if market_target_timestamp > order_books[-1]['timestamp']:
        print("Cannot find order book that matches the timestamp, timestamp too large")
        response = jsonify(success='False', message='timestamp too large', order_book={})
        return response
    
    for order_book in order_books:
        timestamp = int(order_book['timestamp'])
        if timestamp > market_target_timestamp:
            break
        res_order_book = order_book
    
    end_time_micro = time.time_ns() // 1000

    # Calculate the elapsed time
    time_to_retrieve_price = end_time_micro - start_time_micro
    print("time to retrieve price:", time_to_retrieve_price, "microseconds")

    if res_order_book == {}:
        print("Cannot find order book that matches the timestamp")
        response = jsonify(success='False', message='No match timestamp', order_book=res_order_book)
        return response
    else:
        print("Order book at timestamp {}: ".format(market_target_timestamp))
        print(res_order_book)
        response = jsonify(success='True', message='Congrats', order_book=res_order_book)
        return response