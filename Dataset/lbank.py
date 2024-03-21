import ccxt
import csv

# Fieldnames or column headers in the CSV file
field_names = {'timestamp', 'datetime', 'symbol', 'type', 'price',  'amount', 'cost' }

def get_data(platform_name, exchange_symbol):
    exchange = ''
    if platform_name == 'lbank':
        exchange = ccxt.lbank()
    res = exchange.fetch_trades(exchange_symbol)
    return [{k: v for k, v in row.items() if k in field_names} for row in res]

# Specify the CSV file name
def exchange_save_csv(platform_name, exchange_symbol):
    filename = f'doge_data/{platform_name}_{exchange_symbol}_transaction.csv' if exchange_symbol == 'doge_usdt'                                        else f'shiba_data/{platform_name}_{exchange_symbol}_transaction.csv'
    # Writing to CSV
    filtered_data = get_data(platform_name, exchange_symbol)
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, field_names)
        dict_writer.writeheader()
        dict_writer.writerows(filtered_data)

exchange_save_csv("lbank", "doge_usdt")
exchange_save_csv("lbank", "shib_usdt")







