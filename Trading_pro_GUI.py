import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize, QTimer

import pandas_datareader.data as pdr
import time
import datetime

DURATION_INT=60

### Input data

buy_total=4000000.0/10
tickers={'TIGER KRX게임K-뉴딜':'364990',
         'KBSTAR 200철강소재':'285020',
         'TIGER 200 철강소재':'139240',
         'KODEX 철강':'117680',
         'KODEX 2차전지산업':'305720',
         'KINDEX 미국WideMoat가치주':'309230',
         'KODEX 게임산업':'300950',
         'KODEX 배당성장':'211900',
         'TIGER 우량가치':'227570',
         'TIGER 2차전지테마':'305540'}

### GUI

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(960, 960))
        self.setWindowTitle("Trading Pro")

        # self.nameLabel_name = QLabel(self)
        # self.nameLabel_name.setText(name)
        # self.nameLabel_name.move(20, 20)
        #
        # self.nameLabel_symbol = QLabel(self)
        # self.nameLabel_symbol.setText(symbol)
        # self.nameLabel_symbol.move(80, 20)
        #
        # self.nameLabel_price_buy = QLabel(self)
        # self.nameLabel_price_buy.setText(str(price_buy))
        # self.nameLabel_price_buy.move(140, 20)
        #
        # self.nameLabel_price = QLabel(self)
        # self.nameLabel_price.setText(str(price))
        # self.nameLabel_price.move(200, 20)

        # self.nameLabel_change_pct = QLabel(self)
        # self.nameLabel_change_pct.setText(str(change_pct))
        # self.nameLabel_change_pct.move(260, 20)

### General table
        self.tableWidget_1 = QTableWidget(self)
        self.tableWidget_1.resize(940, 160)
        self.tableWidget_1.setRowCount(4)
        self.tableWidget_1.setColumnCount(9)
        self.tableWidget_1.move(10,10)

### Porfolio table
        self.tableWidget_2 = QTableWidget(self)
        self.tableWidget_2.resize(940, 370)
        self.tableWidget_2.setRowCount(11)
        self.tableWidget_2.setColumnCount(9)
        self.tableWidget_2.setHorizontalHeaderLabels(['Tên', 'Mã', 'Giá mua', 'Số lượng', 'Tổng mua', 'Giá hiện tại', 'Tổng hiện tại', 'Thay đổi (%)', 'Khối lượng ngày'])
        self.tableWidget_2.move(10,170)

### History table
        self.tableWidget_3 = QTableWidget(self)
        self.tableWidget_3.resize(360, 400)
        self.tableWidget_3.setRowCount(14)
        self.tableWidget_3.setColumnCount(3)
        self.tableWidget_3.setHorizontalHeaderLabels(['Ngày', 'Danh mục', 'KOSPI'])
        self.tableWidget_3.move(10, 550)

        self.get_data()

### initiate cell value
        for row in range(10):
            self.fill_name(row)
            self.fill_symbol(row)
            self.fill_buy_price(row)
            self.fill_quantity(row)
            self.fill_buy(row)
            self.fill_price(row)
            self.fill_current(row)
            self.fill_change_pct(row)
            self.fill_volume(row)
        self.fill_buy_sum(10,4)
        self.fill_current_sum(10,6)
        self.fill_change_pct_sum(10,7)
        self.tableWidget_2.setItem(10, 3, QTableWidgetItem('Tổng mua'))
        self.tableWidget_2.setItem(10, 5, QTableWidgetItem('Tổng hiện tại'))


### set window refresh
        self.time_left_int = DURATION_INT
        self.myTimer = QtCore.QTimer(self)
        self.myTimer.timeout.connect(self.timerTimeout)
        self.myTimer.start(20000)
###

    def get_data(self):
        self.ticker = [{}] * len(tickers)
        i = 0
        self.buy_sum=0.0
        self.current_sum=0.0
        for name, symbol in tickers.items():
            df = pdr.DataReader(symbol, 'naver', start='2021-07-27', end=datetime.date.today())
            self.ticker[i] = {'name': name,
                         'symbol': symbol,
                         'buy_price': float(df.iat[0, df.columns.get_loc('Close')]),
                         'price': float(df.iat[-1, df.columns.get_loc('Close')]),
                         'volume': float(df.iat[-1, df.columns.get_loc('Volume')])
                         }
            self.ticker[i]['change_pct']=round((self.ticker[i]['price']-self.ticker[i]['buy_price'])/self.ticker[i]['buy_price']*100,2)
            self.ticker[i]['quantity']=int(round(buy_total/self.ticker[i]['price'],0))
            self.ticker[i]['buy'] = self.ticker[i]['buy_price']*self.ticker[i]['quantity']
            self.ticker[i]['current'] = self.ticker[i]['price'] * self.ticker[i]['quantity']
            self.buy_sum += self.ticker[i]['buy']
            self.current_sum += self.ticker[i]['current']
            i += 1
        self.change_pct_sum=round((self.current_sum-self.buy_sum)/self.buy_sum*100,2)

    def timerTimeout(self):
        self.time_left_int -= 1
        if self.time_left_int == 0:
            self.time_left_int = DURATION_INT

        self.update_gui()

### update cell value

    def update_gui(self):
        self.get_data()
        for row in range(10):
            self.fill_price(row)
            self.fill_current(row)
            self.fill_change_pct(row)
            self.fill_volume(row)
            self.fill_current_sum(10, 6)
            self.fill_change_pct_sum(10, 7)

    def fill_name(self,row):
        self.tableWidget_2.setItem(row,0, QTableWidgetItem(self.ticker[row]['name']))

    def fill_symbol(self, row):
        self.tableWidget_2.setItem(row, 1, QTableWidgetItem(self.ticker[row]['symbol']))

    def fill_buy_price(self, row):
        self.tableWidget_2.setItem(row, 2, QTableWidgetItem(str(self.ticker[row]['buy_price'])))

    def fill_quantity(self, row):
        self.tableWidget_2.setItem(row, 3, QTableWidgetItem(str(self.ticker[row]['quantity'])))

    def fill_buy(self, row):
        self.tableWidget_2.setItem(row, 4, QTableWidgetItem(str(self.ticker[row]['buy'])))

    def fill_price(self, row):
        self.tableWidget_2.setItem(row, 5, QTableWidgetItem(str(self.ticker[row]['price'])))

    def fill_current(self, row):
        self.tableWidget_2.setItem(row, 6, QTableWidgetItem(str(self.ticker[row]['current'])))

    def fill_change_pct(self, row):
        self.tableWidget_2.setItem(row, 7, QTableWidgetItem(str(self.ticker[row]['change_pct'])))

    def fill_volume(self, row):
        self.tableWidget_2.setItem(row, 8, QTableWidgetItem(str(self.ticker[row]['volume'])))

    def fill_buy_sum(self,row,col):
        self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(self.buy_sum)))

    def fill_current_sum(self, row, col):
        self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(self.current_sum)))

    def fill_change_pct_sum(self, row, col):
        self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(self.change_pct_sum)))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_() )