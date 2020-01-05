import pandas_datareader as pdr
import matplotlib.pyplot as plt
import datetime
import pandas as pd

from api_keys import quandl_api_key

start_date = datetime.datetime(2012,1,1)
end_date = datetime.datetime(2019, 1, 1)

def stock_printer(start,end,ticker):
    return pdr.data.DataReader(ticker, 'quandl', start.date(), end.date(), api_key=quandl_api_key)

tesla_stock = stock_printer(start_date, end_date, 'TSLA')
ford_stock = stock_printer(start_date, end_date, 'F')
gm_stock = stock_printer(start_date, end_date, 'GM')

''' Show the plots, using plot function in pandas-datareader '''
fig, axes = plt.subplots(nrows=2,ncols=1)

tesla_stock['Open'].plot(label='Tesla', figsize=(12,8),title='Opening Prices',ax=axes[0])
ford_stock['Open'].plot(label='Ford', ax=axes[0])
gm_stock['Open'].plot(label='GM', ax=axes[0])
plt.ylabel('US dollars')
plt.legend()

tesla_stock['Volume'].plot(label='Tesla', figsize=(
    12, 8), title='Volume Traded', ax=axes[1])
ford_stock['Volume'].plot(label='Ford', ax=axes[1])
gm_stock['Volume'].plot(label='GM', ax=axes[1])
plt.ylabel('Number of stocks')
plt.legend()

plt.tight_layout()
plt.show()



