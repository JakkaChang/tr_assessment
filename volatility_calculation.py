import pandas as pd
import numpy as np

def longTermVol(current_index, n_days, df):
    n_days = min(int(np.floor(current_index/1440)), n_days) #Necessary so next line doesn't look for negative index
    recent = df['close'][current_index - (n_days * 1440):current_index:1440].values
    returns = np.diff(np.log(recent))
    volatility = np.std(returns)
    return volatility*np.sqrt(1/24) #Adjust daily volatility to hourly

def shortTermVol(current_index, t_1, df):
    t_1 = min(t_1, current_index) #Necessary so next line doesn't look for negative index
    recent = df['close'][current_index - t_1:current_index].values
    returns = np.diff(np.log(recent))
    volatility = np.std(returns)
    return volatility*np.sqrt(60) #Adjust minute-based volatility to hourly
