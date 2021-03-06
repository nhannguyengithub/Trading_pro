import pandas_datareader.data as pdr
import time
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from pandas import tseries
import yfinance as yf
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


#


# import investpy
#
# # search_result = investpy.search_quotes(text='samsung', products=['stocks'],
# #                                        countries=['south korea'], n_results=1)
# # print(search_result)
#
# df = investpy.get_stock_historical_data(stock='005930',
#                                         country='south korea',
#                                         from_date='22/07/2021',
#                                         to_date='26/07/2021')
# print(df.head())
# tickers={'TIGER KRX게임K-뉴딜':'364990',
#         'KINDEX 미국WideMoat가치주':'309230',
#         'TIGER 2차전지테마':'305540',
#         'KODEX 2차전지산업':'305720',
#         'TIGER KRX BBIG K-뉴딜':'364960',
#         'TIGER KRX2차전지K-뉴딜':'364980',
#         'KODEX 게임산업':'300950',
#         'TIGER KRX인터넷K-뉴딜':'365000',
#         'KODEX 미디어&엔터테인먼트':'266360',
#         'TIGER 미디어컨텐츠':'228810'}

tickers={'삼성전자':'005930'}

for name,symbol in tickers.items():

    df = pdr.DataReader(symbol, 'naver', start='2021-07-13', end=datetime.date.today())
    price_buy=float(df.iat[0, df.columns.get_loc('Close')])
    price=float(df.iat[-1, df.columns.get_loc('Close')])
    change_pct=(price-price_buy)/price_buy*100
    volume=df.iat[-1, df.columns.get_loc('Volume')]
    print(name,symbol,price_buy,price,round(change_pct,2),'%',volume)

    # data = yf.download(tickers='016880.KS', start='2021-07-27')
    # print(data['Close'], data['Volume'])
 #   time.sleep(5)





# def get(tickers, startday, endday):
#     def data(ticker):
#         return pdr.get_data_yahoo(ticker,start=startday,end=endday)
#     datas=map(data,tickers)
#     return pd.concat(datas,keys=tickers, names=['Ticker', 'Date'])
# tickers=[]
# with open('tickers.csv','r') as csvfile:
#     for line in csvfile.readlines():
#         line=line.strip()
#         line+='.KS'
#         tickers.append(line)
# print(tickers)
#
# naver=pdr.get_data_naver

#aapl['Close'].plot(grid = True)
#brk_b['Close'].plot(grid = True)
#plt.show()
#aapl.to_csv('aapl_data')
#pd=pd.read_csv('aapl_data',header=0, index_col='Date', parse_dates=True)
#print(a117680)

# daily_close=aapl[['Adj Close']]
# daily_pct_change=daily_close.pct_change()
# daily_pct_change.fillna(0,inplace=True)
# #print(daily_pct_change)
#
# daily_log_returns=np.log(daily_pct_change+1)
# #print(daily_log_returns)
#
# monthly=daily_close.resample('BM').apply(lambda x:x[-1])
# monthly_pct_change=monthly.pct_change()
# #print(aapl)
# #print(monthly_pct_change)
#
# #aapl.asfreq("M", method="bfill")
# #daily_pct_change.hist(bins=100)
# #plt.show()
# #print(daily_pct_change.describe())
#
# cum_daily_returns=(1+daily_pct_change).cumprod()
# #print(cum_daily_returns)
#
# #cum_daily_returns.plot()
# cum_monthly_returns=cum_daily_returns.resample('BM').apply(lambda x:x[-1])
# cum_quarter_returns=cum_monthly_returns.resample('4M').mean()
# #cum_quarter_returns.plot()
# #plt.show()
#
# #pd.plotting.scatter_matrix(daily_pct_change_px, diagonal='kde', alpha=0.1, figsize=(12,12))
# #plt.show()
#
# adj_close_px=aapl['Adj Close']
# aapl['42']=adj_close_px.rolling(window=40).mean()
# aapl['252']=adj_close_px.rolling(window=252).mean()
# #aapl[['Adj Close', '42', '252']].plot()
# min_periods=75
# vol=daily_pct_change_px.rolling(min_periods).std()*np.sqrt(min_periods)
# #vol.plot(figsize=(10,8))
# #plt.show()
#
# # Isolate the adjusted closing price
# all_adj_close=all_data[['Adj Close']]
# all_returns=np.log(all_adj_close/all_adj_close.shift(1))
#
# # Isolate the AAPL returns
# aapl_returns=all_returns.iloc[all_returns.index.get_level_values('Ticker')=="AAPL"]
# aapl_returns.index=aapl_returns.index.droplevel('Ticker')
#
# # Isolate the MSFT returns
# msft_returns=all_returns.iloc[all_returns.index.get_level_values('Ticker')=="MSFT"]
# msft_returns.index=msft_returns.index.droplevel('Ticker')
#
# # Build up a new DataFrame with AAPL and MSFT returns
# return_data=pd.concat([aapl_returns,msft_returns],axis=1)[1:]
# return_data.columns=['AAPL','MSFT']
#
# X = sm.add_constant(return_data['AAPL'])
#
# model=sm.OLS(return_data['MSFT'],X).fit()
#
# #print(model.summary())
#
# #plt.plot(return_data['AAPL'],return_data['MSFT'],'r.')
# #ax=plt.axis()
# #x=np.linspace(ax[0],ax[1]+0.01)
# #plt.plot(x,model.params[0]+model.params[1]*x,'b',lw=2)
# #plt.grid(True)
# #plt.axis('tight')
# #plt.xlabel('Apple Returns')
# #plt.ylabel('Microsoft Returns')
# #return_data['MSFT'].rolling(window=252).corr(return_data['AAPL']).plot()
# #plt.show()
#
# ######
#
# short_window=40
# long_window=100
#
# signals=pd.DataFrame(index=aapl.index)
# signals['signal']=0.0
#
# signals['short_mavg']=aapl['Close'].rolling(window=short_window,min_periods=1,center=False).mean()
# signals['long_mavg']=aapl['Close'].rolling(window=long_window,min_periods=1,center=False).mean()
#
# signals['signal'][short_window:]=np.where(signals['short_mavg'][short_window:]>
#                                           signals['long_mavg'][short_window:],1.0,0.0)
# signals['positions']=signals['signal'].diff()
#
# signals['positions'].plot()
# signals['signal'].plot()
# plt.show()
#
# #fig=plt.figure()
# #ax1=fig.add_subplot(111, ylabel="Price in $")
# #aapl['Close'].plot(ax=ax1, color='r', lw=2.)
# #signals[['short_mavg','long_mavg']].plot(ax=ax1, lw=2.)
# #ax1.plot(signals.loc[signals.positions==1.0].index, signals.short_mavg[signals.positions==1.0],
# #         '^', markersize=10, color='m')
# #ax1.plot(signals.loc[signals.positions==-1.0].index, signals.short_mavg[signals.positions==-1.0],
# #         'v',markersize=10, color='k')
# #plt.show()
#
# inintial_capital=float(100000.0)
# positions=pd.DataFrame(index=signals.index).fillna(0.0)
# positions['AAPL']=100*signals['signal']
# portfolio=positions.multiply(aapl['Adj Close'],axis=0)
# pos_diff=positions.diff()
# portfolio['holdings']=(positions.multiply(aapl['Adj Close'],axis=0)).sum(axis=1)
# portfolio['cash']=inintial_capital-(pos_diff.multiply(aapl['Adj Close'],axis=0)).sum(axis=1).cumsum()
# portfolio['total']=portfolio['cash']+portfolio['holdings']
# portfolio['returns']=portfolio['total'].pct_change()
# #print(portfolio.head())
#
# #fig=plt.figure()
# #ax1=fig.add_subplot(111, ylabel="portfolio value in $")
# #portfolio['total'].plot(ax=ax1, color='r', lw=2.)
# #signals[['short_mavg','long_mavg']].plot(ax=ax1, lw=2.)
# #ax1.plot(portfolio.loc[signals.positions==1.0].index, portfolio.total[signals.positions==1.0],
# #         '^', markersize=10, color='m')
# #ax1.plot(portfolio.loc[signals.positions==-1.0].index, portfolio.total[signals.positions==-1.0],
# #         'v',markersize=10, color='k')
# #plt.show()
#
# # Print the Sharpe ratio
# returns=portfolio['returns']
# sharpe_ratio=np.sqrt(252)*(returns.mean()/returns.std())
# #print(sharpe_ratio)
#
# # Calculate the max drawdown
# window=252
# rolling_max=aapl['Adj Close'].rolling(window, min_periods=1).max()
# daily_drawdown=aapl['Adj Close']/rolling_max-1.0
# max_daily_drawdown=daily_drawdown.rolling(window, min_periods=1).min()
# #daily_drawdown.plot()
# #max_daily_drawdown.plot()
# #plt.show()
#
# # Calculate the CAGR
# days=(aapl.index[-1]-aapl.index[0]).days
# cagr=((((aapl['Adj Close'][-1])/aapl['Adj Close'][1]))**(365.0/days))-1
# print(cagr)