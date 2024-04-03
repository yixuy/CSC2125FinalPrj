from app import marketsim
from flask import jsonify, request
import os
import csv
import time

current_dir = os.path.dirname(os.path.abspath(__file__))

@marketsim.route('/',methods=['GET'])
def main():
    return 'Hello, World'

@marketsim.route('/getPrice',methods=['POST'])
def getPrice():
    exchange = request.form.get('exchange')
    cryptocurrency = request.form.get('cryptocurrency')
    csv_file_path = os.path.join(current_dir, r'static\{}_data\{}_{}_transaction.csv'.format(cryptocurrency, exchange, cryptocurrency))
    print("csv path: ", csv_file_path)
    
    target_timestamp = 1712135713355
    start_time = time.time_ns()

    with open(csv_file_path, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            timestamp = int(row['timestamp'])
            if timestamp == target_timestamp:
                price = float(row['price'])
                print("Price at timestamp {}: {}".format(target_timestamp, price))
                break
        else:
            print("Timestamp {} not found in the CSV file.".format(target_timestamp))

    end_time = time.time_ns()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    print("Elapsed time:", elapsed_time, "nanoseconds")

    response = jsonify(success='True', price=price)
    return response