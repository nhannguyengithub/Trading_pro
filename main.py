import pandas_datareader as pdr
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get(tickers, startday, endday):
    def data(ticker):
        return pdr.get_data_yahoo(ticker,start=startday,end=endday)
    datas=map(data,tickers)
    return pd.concat(datas,keys=tickers, names=['Ticker', 'Date'])

tickers=['AAPL','MSFT','IBM','GOOG']
all_data=get(tickers,datetime.datetime(2018,4,1),datetime.date.today())
daily_close_px=all_data[['Adj Close']].reset_index().pivot('Date', 'Ticker', 'Adj Close')
daily_pct_change_px=daily_close_px.pct_change()
#daily_pct_change_px.hist(bins=50, sharex=True, figsize=(12,8))
#plt.show()
aapl = pdr.get_data_yahoo('AAPL',
                        start = datetime.datetime(2018,4,1),
                        end = datetime.date.today())
#brk_b = pdr.get_data_yahoo('BRK-B',
#                           start=datetime.datetime(2018, 4, 1),
#                           end=datetime.date.today())

#aapl['Close'].plot(grid = True)
#brk_b['Close'].plot(grid = True)
#plt.show()
#aapl.to_csv('aapl_data')
#pd=pd.read_csv('aapl_data',header=0, index_col='Date', parse_dates=True)

daily_close=aapl[['Adj Close']]
daily_pct_change=daily_close.pct_change()
daily_pct_change.fillna(0,inplace=True)
#print(daily_pct_change)

daily_log_returns=np.log(daily_pct_change+1)
#print(daily_log_returns)

monthly=daily_close.resample('BM').apply(lambda x:x[-1])
monthly_pct_change=monthly.pct_change()
#print(aapl)
#print(monthly_pct_change)

#aapl.asfreq("M", method="bfill")
#daily_pct_change.hist(bins=100)
#plt.show()
#print(daily_pct_change.describe())

cum_daily_returns=(1+daily_pct_change).cumprod()
#print(cum_daily_returns)

#cum_daily_returns.plot()
cum_monthly_returns=cum_daily_returns.resample('BM').apply(lambda x:x[-1])
cum_quarter_returns=cum_monthly_returns.resample('4M').mean()
#cum_quarter_returns.plot()
#plt.show()

#pd.plotting.scatter_matrix(daily_pct_change_px, diagonal='kde', alpha=0.1, figsize=(12,12))
#plt.show()

adj_close_px=aapl['Adj Close']
aapl['42']=adj_close_px.rolling(window=40).mean()
aapl['252']=adj_close_px.rolling(window=252).mean()
#aapl[['Adj Close', '42', '252']].plot()
min_periods=75
vol=daily_pct_change.rolling(min_periods).std()*np.sqrt(min_periods)
vol.plot(figsize=(10,8))
plt.show()