'''
Write multithreaded listener for price
'''
import time


def get_variance(exchange_name):
    '''
    Return variance for exchange exchange_name
    '''
    return 0.005
    

if __name__ == "__main__":

    virtual_beginning_time = 0 # set to a timestamp
    actual_beginning_time = time.time()


    # Set expected latency in second
    expected_latency = 0.5

    while time.time() - actual_beginning_time < 5 * 60 * 60: # set to 5hrs of simulation time
        '''
        We want multiple threads listening to all exchanges
        By listening it means sending request (timestamp, cointype, exchange_name) to simulator 
        '''

        # Assume p1 is price of doge on ex1, p2 is price of doge on ex2. Then:

        # if p1 and p2 satisfies our model, then make transaction
        pass