
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

with open('tickers.csv', mode='r') as inp:
    reader = reader(inp)
    tickers = {rows[0]:rows[1] for rows in reader}


number_of_tickers=len(tickers)
start_day = datetime.date(2021, 7, 28)  ### Start day

start_day_show = start_day  ### Show start day

current_time = datetime.datetime.now()
market_open = current_time.replace(hour=9, minute=0, second=0)
market_close = current_time.replace(hour=15, minute=30, second=0)

if current_time < market_open:
    start_day += datetime.timedelta(days=1)


### GUI

class Ticker:
    def __init__(self):
        self.ticker = [{} for _ in range(len(tickers))]
        i = 0
        self.buy_sum = 0.0
        self.current_sum = 0.0
        self.price = [[] for _ in range(len(tickers))]
        self.sum = [[] for _ in range(len(tickers))]
        self.total = []
        self.change = [[] for _ in range(len(tickers))]
        self.change_pct = []
        self.kospi_change_pct = []
        self.date = []
        for name, symbol in tickers.items():
            df = pdr.DataReader(symbol, 'naver', start=start_day - datetime.timedelta(days=1),
                                end=datetime.date.today())


            self.day = pd.to_datetime(df.index).strftime('%Y-%m-%d')

            self.ticker[i] = {'name': name,
                              'symbol': symbol
                              }
            self.number_of_days = len(df)
            self.change[i].append(symbol)
            for j in range(self.number_of_days):
                self.price[i].append(float(df.iat[j, df.columns.get_loc('Close')]))
                # self.change[i]['day'+str(j)]=(round((self.price[i][j]-self.price[i][0])/self.price[i][0]*100,2))
                if j!=0:
                    self.change[i].append(round((self.price[i][j]-self.price[i][0])/self.price[i][0]*100,2))
            self.ticker[i]['buy_price'] = self.price[i][0]
            self.ticker[i]['quantity'] = (int(round(buy_total / 10 / self.price[i][0])))
            self.ticker[i]['price'] = self.price[i][-1]
            self.ticker[i]['change_pct'] = round(
                (self.ticker[i]['price'] - self.ticker[i]['buy_price']) / self.ticker[i]['buy_price'] * 100, 2)
            self.ticker[i]['volume'] = float(df.iat[-1, df.columns.get_loc('Volume')])
            for j in range(self.number_of_days):
                self.sum[i].append(self.price[i][j] * self.ticker[i]['quantity'])
            self.ticker[i]['buy'] = self.sum[i][0]
            self.ticker[i]['current'] = self.sum[i][-1]
            if i != (len(tickers) - 1):
                self.buy_sum += self.ticker[i]['buy']
                self.current_sum += self.ticker[i]['current']
            i += 1
        for i in range(self.number_of_days):
            self.date.append(self.day[i])
            total = 0.0
            for j in range(len(tickers) - 1):
                total += self.sum[j][i]
            self.total.append(total)
            self.change_pct.append(round((self.total[i] - self.total[0]) / self.total[0] * 100, 2))
            self.kospi_change_pct.append(round((self.price[-1][i] - self.price[-1][0]) / self.price[-1][0] * 100, 2))
        self.change_pct_sum = round((self.current_sum - self.buy_sum) / self.buy_sum * 100, 2)
        self.change_sum = round((self.current_sum - self.buy_sum), 0)
        self.kospi_buy = self.price[-1][0]
        self.kospi_current = self.price[-1][-1]

        self.change_sorted=sorted(self.change, key=lambda change: change[self.number_of_days-1],reverse=True)
        self.change_sorted=self.change_sorted[:10]

tic=Ticker()
print(number_of_tickers)
for i in range(10):
    print(tic.change_sorted[i])
for i in range(10):
    for j in range(tic.)

# print(tic.change)







