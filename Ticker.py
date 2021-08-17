
import pandas as pd
import pandas_datareader.data as pdr
import time
import datetime
import random
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from csv import  reader

### Input data

buy_total = 4000000.0
tickers={}

with open('tickers.csv', mode='r',encoding = 'CP949') as inp:
    reader = reader(inp)
    tickers = {rows[0]:rows[1] for rows in reader}

number_of_tickers=len(tickers)
start_day = datetime.date(2021, 7, 28)  ### Start day

current_time = datetime.datetime.now()
market_open = current_time.replace(hour=9, minute=0, second=0)
market_close = current_time.replace(hour=15, minute=30, second=0)

if (current_time < market_open) or datetime.date.today().weekday()==6:
    start_day += datetime.timedelta(days=1)


### GUI

class Ticker:
    def __init__(self):
        self.ticker = {}
        i = 0
        self.buy_sum = 0.0

        self.current_sum = 0.0
        self.price = [[] for _ in range(len(tickers))]
        self.sum = [[] for _ in range(len(tickers))]
        self.total = []
        self.change = [[] for _ in range(len(tickers))]
        self.total_change_pct = [[] for _ in range(len(tickers))]
        self.change_pct = []
        self.kospi_change_pct = []
        self.date = []
        self.kospi_price=[]
    def get_data(self):
        i=0
        for name, symbol in tickers.items():
            df = pdr.DataReader(symbol, 'naver', start=start_day - datetime.timedelta(days=1),
                                end=datetime.date.today())


            self.day = pd.to_datetime(df.index).strftime('%Y-%m-%d')

            self.ticker[symbol] = {'name': name,
                              'symbol': symbol
                              }
            self.number_of_days = len(df)
            self.change[i].append(symbol)
            self.ticker[symbol]['price1']=[[] for _ in range(self.number_of_days)]
            self.ticker[symbol]['change1'] = [[] for _ in range(self.number_of_days)]
            for j in range(self.number_of_days):
                self.ticker[symbol]['price1'][j] = float(df.iat[j, df.columns.get_loc('Close')])
                # self.price[i].append(float(df.iat[j, df.columns.get_loc('Close')]))
                # self.change[i].append(round((self.price[i][j]-self.price[i][0])/self.price[i][0]*100,2))
                self.change[i].append(round(
                    (self.ticker[symbol]['price1'][j] - self.ticker[symbol]['price1'][0]) / self.ticker[symbol]['price1'][0] * 100, 2))
            self.ticker[symbol]['buy_price'] = self.ticker[symbol]['price1'][0]
            self.ticker[symbol]['quantity'] = (int(round(buy_total / 10 / self.ticker[symbol]['buy_price'])))
            self.ticker[symbol]['price'] = self.ticker[symbol]['price1'][-1]
            self.ticker[symbol]['change_pct'] = round(
                (self.ticker[symbol]['price'] - self.ticker[symbol]['buy_price']) / self.ticker[symbol]['buy_price'] * 100, 2)
            self.ticker[symbol]['volume'] = float(df.iat[-1, df.columns.get_loc('Volume')])
            self.ticker[symbol]['sum1']=[[] for _ in range(self.number_of_days)]
            for j in range(self.number_of_days):
                self.ticker[symbol]['sum1'][j]=self.ticker[symbol]['price1'][j]*self.ticker[symbol]['quantity']
            self.ticker[symbol]['buy'] = self.ticker[symbol]['sum1'][0]
            self.ticker[symbol]['current'] = self.ticker[symbol]['sum1'][-1]
            i += 1

        self.change_sorted=sorted(self.change, key=lambda change: change[-1],reverse=True)

        self.change_sorted=self.change_sorted[:10]
        for i in range(10):
            self.buy_sum+=self.ticker[self.change_sorted[i][0]]['buy']
            self.current_sum+=self.ticker[self.change_sorted[i][0]]['current']
        self.sum1 = [0.0 for i in range(self.number_of_days)]
        self.pct1 = [0.0 for i in range(self.number_of_days)]
        for j in range(self.number_of_days):
            for i in range(10):
                self.sum1[j]+=self.ticker[self.change_sorted[i][0]]['sum1'][j]
            self.pct1[j]=round((self.sum1[j] - self.sum1[0]) / self.sum1[0] * 100, 2)
        self.change_pct_sum = round((self.current_sum - self.buy_sum) / self.buy_sum * 100, 2)
        self.change_sum = round((self.current_sum - self.buy_sum), 0)
        kospi= pdr.DataReader('KOSPI', 'naver', start=start_day - datetime.timedelta(days=1),
                                end=datetime.date.today())
        for j in range(self.number_of_days):
            self.kospi_price.append(float(kospi.iat[j, kospi.columns.get_loc('Close')]))
            self.kospi_change_pct.append(round((self.kospi_price[j]-self.kospi_price[0])/self.kospi_price[0]*100,2))
        self.kospi_buy=self.kospi_price[0]
        self.kospi_current=self.kospi_price[-1]



# tic=Ticker()
# tic.get_data()
# for i in range(10):
#     print(tic.ticker[tic.change_sorted[i][0]])
# print(tic.change)







