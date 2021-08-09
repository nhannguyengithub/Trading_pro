import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QGridLayout, \
    QSizePolicy
from PyQt5.QtCore import QSize, QTimer
# import pyqtgraph as pg
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

print(tickers)

start_day = datetime.date(2021, 7, 28)  ### Start day

start_day_show = start_day  ### Show start day

current_time = datetime.datetime.now()
market_open = current_time.replace(hour=9, minute=0, second=0)
market_close = current_time.replace(hour=15, minute=30, second=0)

if current_time < market_open:
    start_day += datetime.timedelta(days=1)


### GUI

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(960, 700))
        self.setWindowTitle("Trading Pro")

        self.get_data()
        global change_pct, kospi_change_pct

        ### Porfolio table
        self.tableWidget_2 = QTableWidget(self)
        self.tableWidget_2.resize(530, 650)
        self.tableWidget_2.setRowCount(11)
        self.tableWidget_2.setColumnCount(5)
        # self.tableWidget_2.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_2.verticalHeader().setFixedWidth(20)
        self.tableWidget_2.setHorizontalHeaderLabels(
            ['Tên', 'Mã', 'Giá hiện tại', 'Thay đổi (%)', 'Khối lượng ngày'])
        self.tableWidget_2.move(10, 10)

        ### initiate cell value
        for row in range(10):
            self.tableWidget_2.setItem(row, 0, QTableWidgetItem(self.ticker[row]['name']))
            self.tableWidget_2.setItem(row, 1, QTableWidgetItem(self.ticker[row]['symbol']))
            self.tableWidget_2.setItem(row, 2, QTableWidgetItem(str(self.ticker[row]['buy_price'])))
            self.tableWidget_2.setItem(row, 3, QTableWidgetItem(str(self.ticker[row]['quantity'])))
            self.tableWidget_2.setItem(row, 4, QTableWidgetItem(str(self.ticker[row]['buy'])))
            self.tableWidget_2.setItem(row, 5, QTableWidgetItem(str(self.ticker[row]['price'])))
            self.tableWidget_2.setItem(row, 6, QTableWidgetItem(str(self.ticker[row]['current'])))
            self.tableWidget_2.setItem(row, 7, QTableWidgetItem(str(self.ticker[row]['change_pct'])))
            self.tableWidget_2.setItem(row, 8, QTableWidgetItem(str(self.ticker[row]['volume'])))
        self.tableWidget_2.setItem(10, 3, QTableWidgetItem('Tổng mua'))
        self.tableWidget_2.setItem(10, 4, QTableWidgetItem(str(self.buy_sum)))
        self.tableWidget_2.setItem(10, 5, QTableWidgetItem('Tổng hiện tại'))
        self.tableWidget_2.setItem(10, 6, QTableWidgetItem(str(self.current_sum)))
        self.tableWidget_2.setItem(10, 7, QTableWidgetItem(str(self.change_pct_sum)))


### Set window refresh
        self.myTimer = QtCore.QTimer(self)
        self.myTimer.timeout.connect(self.timerTimeout)
        self.myTimer.start(20000)

### Get data
    def get_data(self):
        self.ticker = [{} for _ in range(len(tickers))]
        i = 0
        self.buy_sum = 0.0
        self.current_sum = 0.0
        self.price = [[] for _ in range(len(tickers))]
        self.sum = [[] for _ in range(len(tickers))]
        self.total = []
        self.change = []
        self.change_pct = []
        self.kospi_change_pct = []
        self.date = []
        for name, symbol in tickers.items():
            df = pdr.DataReader(symbol, 'naver', start=start_day - datetime.timedelta(days=1),
                                end=datetime.date.today())
            print(df)

            self.day = pd.to_datetime(df.index).strftime('%Y-%m-%d')

            self.ticker[i] = {'name': name,
                              'symbol': symbol
                              }
            self.number_of_days = len(df)
            for j in range(self.number_of_days):
                self.price[i].append(float(df.iat[j, df.columns.get_loc('Close')]))
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

    def timerTimeout(self):
        self.update_gui()

 ### update cell value
    def update_gui(self):
        self.get_data()
        for row in range(10):
            self.tableWidget_2.setItem(row, 5, QTableWidgetItem(str(self.ticker[row]['price'])))
            self.tableWidget_2.setItem(row, 6, QTableWidgetItem(str(self.ticker[row]['current'])))
            self.tableWidget_2.setItem(row, 7, QTableWidgetItem(str(self.ticker[row]['change_pct'])))
            self.tableWidget_2.setItem(row, 8, QTableWidgetItem(str(self.ticker[row]['volume'])))
        self.tableWidget_2.setItem(10, 6, QTableWidgetItem(str(self.current_sum)))
        self.tableWidget_2.setItem(10, 7, QTableWidgetItem(str(self.change_pct_sum)))

### Main run
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
