import pandas_datareader as pdr
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
print(cum_daily_returns)
cum_daily_returns.plot()
plt.show()