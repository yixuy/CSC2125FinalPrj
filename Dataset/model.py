import numpy as np
from scipy import stats 

def get_estimate_ratio(latency: float, sigma: float, confidence_level:int = 80, risk_free_rate: float = 0):
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