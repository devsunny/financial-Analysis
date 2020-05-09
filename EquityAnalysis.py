import numpy as np
import pandas as pd
import pandas_datareader as pdr
import pandas_datareader.data as web
import matplotlib as plot
import datetime
import os
from dateutil.relativedelta import relativedelta

def fetch_historical_data(symbol, start_date=None, end_date=None):
    symbol = "TECL"
    datestring = datetime.datetime.now().strftime("%Y-%m-%d")
    if end_date is None:
        end = datetime.datetime.now()
    else:
        end = end_date
    
    if start_date is None:
        start = end - relativedelta(years=1)
    else:
        start = start_date
    
    file_name = symbol + "-" + datestring + ".dat"
    historicaldata = None
    if not os.path.exists(file_name):
        historicaldata = web.get_data_yahoo(symbol, start,  end)
        csv = historicaldata.to_csv()
    else:
        historicaldata = pd.read_csv(file_name)
    return historicaldata
    
def analyze_moving_trend(symbol, window=20, cross_window=60,  start_date=None, end_date=None):
    hist_data = fetch_historical_data(symbol, start_date, end_date)
    mean_window_colname = "Mean_{}_Days".format(window)
    mean_xwindow_colname = "Mean_{}_Days".format(cross_window)
    hist_data[mean_window_colname] = hist_data.iloc[:,5].rolling(window).mean()
    hist_data[mean_xwindow_colname] = hist_data.iloc[:,5].rolling(cross_window).mean()
    hist_data['stddev'] = hist_data.iloc[:,5].rolling(window).std(ddof=0)
    hist_data['Upper_Band'] = hist_data[mean_window_colname] + hist_data["stddev"]*2
    hist_data['Lower_Band'] = hist_data[mean_window_colname] - hist_data["stddev"]*2
    return hist_data[['High','Low','Open','Close','Volume','Adj Close', mean_window_colname, mean_xwindow_colname, 'Upper_Band', 'Lower_Band']]
