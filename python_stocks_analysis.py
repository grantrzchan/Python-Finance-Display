import pandas_datareader as pdr
import matplotlib.pyplot as plt
import datetime
import pandas as pd

from api_keys import quandl_api_key
from pandas.plotting import scatter_matrix
from mpl_finance import candlestick_ohlc
#set minor ticks on other days, major on Mondays
from matplotlib.dates import DateFormatter,date2num, WeekdayLocator, DayLocator, MONDAY

start_date = datetime.datetime(2012, 1, 1)
end_date = datetime.datetime(2018, 3, 1)

def stock_printer(start,end,ticker):
    return pdr.data.DataReader(ticker, 'quandl', start.date(), end.date(), api_key=quandl_api_key)

def total_traded(df):
    return df[['Open', 'Close']].mean(axis=1)*df['Volume']

def moving_average(df, days):
    return df['Open'].rolling(days).mean()

tesla_stock = stock_printer(start_date, end_date, 'TSLA')
# print(tesla_stock)
tesla_stock['Total Traded'] = total_traded(tesla_stock)
tesla_stock['MA50'] = moving_average(tesla_stock, 50)
tesla_stock['MA200'] = moving_average(tesla_stock, 100)
tesla_reset = tesla_stock.loc['2018-01'].reset_index()
# print(tesla_reset.info())
tesla_reset['date_ax'] = tesla_reset['Date'].apply(lambda date: date2num(date)) #create numerical date column
tesla_values = [tuple(vals) for vals in tesla_reset[[
    'date_ax', 'Open', 'High', 'Low', 'Close']].values]
# print(tesla_values)

ford_stock = stock_printer(start_date, end_date, 'F')
ford_stock['Total Traded'] = total_traded(ford_stock)

gm_stock = stock_printer(start_date, end_date, 'GM')
gm_stock['Total Traded'] = total_traded(gm_stock)

''' Print out the maxima in the stock prices'''
tesla_max, ford_max, gm_max = map(lambda x: x.idxmax(), [tesla_stock['Total Traded'], ford_stock['Total Traded'], gm_stock['Total Traded']])
print('\n', tesla_max, ford_max, gm_max)

'''scatter plot'''
car_companies = pd.concat([tesla_stock['Open'], ford_stock['Open'], gm_stock['Open']], axis=1)
car_companies.columns = ['Tesla Open', 'Ford Open', 'GM Open']

''' Show the plots, using plot function in pandas-datareader '''
fig, axes = plt.subplots(nrows=2,ncols=2)
fig.subplots_adjust(bottom=0.2)
plt1 = tesla_stock[['Open', 'MA50', 'MA200']].plot(figsize=(12, 8), title='Opening Prices', ax=axes[0, 0])
ford_stock['Open'].plot(ax=axes[0,0])
gm_stock['Open'].plot(ax=axes[0,0])
plt1.set_ylabel('US Dollars')
plt1.legend(('Tesla', 'Tesla MA50', 'Tesla MA100','Ford','GM'))

plt2 = tesla_stock['Volume'].plot(label='Tesla', figsize=(
    12, 8), title='Volume Traded', ax=axes[0,1])
ford_stock['Volume'].plot(label='Ford', ax=axes[0,1])
gm_stock['Volume'].plot(label='GM', ax=axes[0,1])
plt2.set_ylabel('Number of stocks')
plt2.legend()


plt3 = tesla_stock['Total Traded'].plot(label='Tesla', figsize=(
    12, 8), title='Total Traded', ax=axes[1, 0])
ford_stock['Total Traded'].plot(label='Ford', ax=axes[1, 0])
gm_stock['Total Traded'].plot(label='GM', ax=axes[1, 0])
plt3.set_ylabel('US Dollars')
plt3.legend()

mondays = WeekdayLocator(MONDAY) # major ticks on Monday
alldays = DayLocator() # minor ticks on every other day beside Mondays
week_formatter = DateFormatter('%b %d') # format e.g., Jan 12
day_formatter = DateFormatter('%b %d') # e.g., 12

'''Set candle chart as plot #4'''
plt4_axes = axes[1, 1]
plt4_axes.xaxis.set_major_locator(mondays)
plt4_axes.xaxis.set_minor_locator(alldays)
plt4_axes.xaxis.set_major_formatter(week_formatter)
plt4_axes.set_xlabel('Date')
plt4_axes.set_ylabel('US Dollars/share')
candlestick_ohlc(plt4_axes,tesla_values,width=0.6,colorup='g',colordown='r')

plt.tight_layout()

plt5 = scatter_matrix(car_companies, figsize=(8,8), alpha=0.2, hist_kwds={'bins': 50}) #use alpha to adjust data point transparency

plt.show()


