'''
Write main function for market simulator

We want server to have one functionality
When server received request (timestamp, cointype, exchange), 
respond with (coin_price)
'''

from app import marketsim
from flask import jsonify, request
import os
import csv
import time
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))

def getMarketStartTime():
    if sys.platform.startswith('win'):
        # For Windows
        lbank_shib_path = os.path.join(current_dir, r'static\shib_data\lbank_shib_transaction.csv')
    else:
       lbank_shib_path = os.path.join(current_dir, r'static/shib_data/lbank_shib_transaction.csv')
    
    with open(lbank_shib_path, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            timestamp = int(row['timestamp'])
            if timestamp > 0:
                return timestamp

market_start_timestamp = getMarketStartTime()
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
    
    
    if sys.platform.startswith('win'):
        # For Windows
        print("win")
        csv_file_path = os.path.join(current_dir, r'static\{}_data\{}_{}_transaction.csv'.format(cointype, exchange, cointype))
        os.path.join(current_dir, r'static\{}_data\{}_{}_transaction.csv'.format(cointype, exchange, cointype))
    else:
        # For macOS
        print("mos")
        csv_file_path = os.path.join(current_dir, r'static/{}_data/{}_{}_transaction.csv'.format(cointype, exchange, cointype))
        os.path.join(current_dir, r'static/{}_data/{}_{}_transaction.csv'.format(cointype, exchange, cointype))

    
    
    print("csv path: ", csv_file_path)
    
    real_current_timestamp = round(time.time() * 1000)
    print("real current timestamp: ", real_current_timestamp)
    elapsed_time = real_current_timestamp - real_start_timestamp
    market_target_timestamp = market_start_timestamp + elapsed_time
    print("market target timestamp: ", market_target_timestamp)
    
    # start_time = time.time() * 1000
    start_time_micro = time.time_ns() // 1000

    with open(csv_file_path, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            timestamp = int(row['timestamp'])
            if timestamp >= market_target_timestamp:
                coin_price = float(row['price'])
                print("Price at timestamp {}: {}".format(market_target_timestamp, coin_price))
                break
        else:
            print("Timestamp {} not found in the CSV file.".format(market_target_timestamp))

    # end_time = time.time() * 1000
    end_time_micro = time.time_ns() // 1000

    # Calculate the elapsed time
    time_to_retrieve_price = end_time_micro - start_time_micro
    print("time to retrieve price:", time_to_retrieve_price, "microseconds")

    response = jsonify(success='True', coin_price=coin_price)
    return response