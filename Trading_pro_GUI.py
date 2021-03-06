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

### Input data

buy_total = 4000000.0
# tickers = {'TIGER KRX게임K-뉴딜': '364990',
#            'KBSTAR 200철강소재': '285020',
#            'TIGER 200 철강소재': '139240',
#            'KODEX 철강': '117680',
#            'KODEX 2차전지산업': '305720',
#            'KINDEX 미국WideMoat가치주': '309230',
#            'KODEX 게임산업': '300950',
#            'KODEX 배당성장': '211900',
#            'TIGER 우량가치': '227570',
#            'TIGER 2차전지테마': '305540',
#            'KOSPI': 'KOSPI'}
tickers = {'KODEX 2차전지산업': '305720',
           'TIGER 200 헬스케어': '227540',
           'KODEX 바이오': '244580',
           'TIGER 2차전지테마': '305540',
           'KODEX 헬스케어': '266420',
           'TIGER KRX바이오K-뉴딜': '364970',
           'TIGER 헬스케어': '143860',
           'TIGER KRX2차전지K-뉴딜': '364980',
           'TIGER 코스닥150바이오테크': '261070',
           'TIGER 방송통신': '098560',
           'KOSPI': 'KOSPI'}
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

        ### General table
        self.tableWidget_1 = QTableWidget(self)
        self.tableWidget_1.resize(945, 85)
        self.tableWidget_1.setRowCount(2)
        self.tableWidget_1.setColumnCount(9)
        self.tableWidget_1.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_1.verticalHeader().setFixedWidth(20)
        self.tableWidget_1.setHorizontalHeaderLabels(['Ngày mua', 'Tổng tiền', 'KOSPI mua', 'KOSPI hiện tại'])
        self.tableWidget_1.move(10, 10)
        self.tableWidget_1.setItem(0, 0, QTableWidgetItem(str(start_day_show)))
        self.tableWidget_1.setItem(0, 1, QTableWidgetItem(str(buy_total)))
        self.tableWidget_1.setItem(0, 2, QTableWidgetItem(str(self.price[-1][0])))
        self.tableWidget_1.setItem(0, 3, QTableWidgetItem(str(self.price[-1][-1])))
        self.tableWidget_1.setItem(1, 1, QTableWidgetItem('(' + str(self.change_sum) + ')'))
        self.tableWidget_1.setItem(1, 3, QTableWidgetItem('(' + str(self.kospi_change_pct[-1]) + '%)'))

        ### Porfolio table
        self.tableWidget_2 = QTableWidget(self)
        self.tableWidget_2.resize(945, 360)
        self.tableWidget_2.setRowCount(11)
        self.tableWidget_2.setColumnCount(9)
        self.tableWidget_2.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_2.verticalHeader().setFixedWidth(20)
        self.tableWidget_2.setHorizontalHeaderLabels(
            ['Tên', 'Mã', 'Giá mua', 'Số lượng', 'Tổng mua', 'Giá hiện tại', 'Tổng hiện tại', 'Thay đổi (%)',
             'Khối lượng ngày'])
        self.tableWidget_2.move(10, 95)

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

        ### History table
        self.tableWidget_3 = QTableWidget(self)
        self.tableWidget_3.resize(340, 240)
        self.tableWidget_3.setRowCount(14)
        self.tableWidget_3.setColumnCount(3)
        self.tableWidget_3.verticalHeader().setFixedWidth(20)
        self.tableWidget_3.setHorizontalHeaderLabels(['Ngày', 'Danh mục', 'KOSPI'])
        i = 0
        for row in range(1, self.number_of_days):
            self.tableWidget_3.setItem(i, 0, QTableWidgetItem(str(self.day[row])))
            self.tableWidget_3.setItem(i, 1, QTableWidgetItem(str(self.change_pct[row])))
            self.tableWidget_3.setItem(i, 2, QTableWidgetItem(str(self.kospi_change_pct[row])))
            i += 1
        self.tableWidget_3.move(10, 455)
        change_pct = self.change_pct
        kospi_change_pct = self.kospi_change_pct

### Plot data
        m = PlotCanvas(self, width=8, height=4)
        m.move(350, 455)

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
        self.tableWidget_1.setItem(1, 1, QTableWidgetItem('(' + str(self.change_sum) + ')'))
        self.tableWidget_1.setItem(0, 3, QTableWidgetItem(str(self.kospi_current)))
        self.tableWidget_1.setItem(1, 3, QTableWidgetItem('(' + str(self.kospi_change_pct[-1]) + '%)'))
        self.tableWidget_3.setItem(self.number_of_days - 2, 1,
                                   QTableWidgetItem(str(self.change_pct[self.number_of_days - 1])))
        self.tableWidget_3.setItem(self.number_of_days - 2, 2,
                                   QTableWidgetItem(str(self.kospi_change_pct[self.number_of_days - 1])))

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=1, height=2, dpi=60):
        fig = Figure(figsize=(width, height), dpi=dpi)
        # self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    def plot(self):
        # data = [random.random() for i in range(25)]
        # data=MainWindow()
        # data_x=data.date
        # data_y=data.change_pct

        ax = self.figure.add_subplot(111)
        ax.plot(change_pct, 'b-', label='Danh muc')
        ax.plot(kospi_change_pct, 'r-', label='Kospi')
        ax.legend()
        ax.grid()
        ax.set_title('Lịch sử thay đổi')
        ax.set_xlabel('Ngay')
        ax.set_ylabel('Thay doi')
        self.draw()
### Main run
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
