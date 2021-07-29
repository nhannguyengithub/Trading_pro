import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize, QTimer

import pandas_datareader.data as pdr
import time
import datetime

### get data

tickers={'삼성전자':'005930'}

for name,symbol in tickers.items():

    df = pdr.DataReader(symbol, 'naver', start='2021-07-13', end=datetime.date.today())
    price_buy=float(df.iat[0, df.columns.get_loc('Close')])
    price=float(df.iat[-1, df.columns.get_loc('Close')])
    change_pct=(price-price_buy)/price_buy*100
    volume=df.iat[-1, df.columns.get_loc('Volume')]
    print(name,symbol,price_buy,price,round(change_pct,2),'%',volume)


###

### GUI

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(960, 540))
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
        i=1

        self.tableWidget = QTableWidget(self)
        self.tableWidget.resize(820, 290)
        self.tableWidget.setRowCount(4)
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setItem(0,0, QTableWidgetItem(name))
        self.tableWidget.setItem(0,1, QTableWidgetItem(symbol))
        self.tableWidget.setItem(0,2, QTableWidgetItem(str(price)))
        self.tableWidget.setItem(0, 3, QTableWidgetItem(str(volume)))
        self.tableWidget.setItem(1,1, QTableWidgetItem("Cell (3,1)"))
        self.tableWidget.setItem(2,0, QTableWidgetItem("Cell (3,1)"))
        self.tableWidget.setItem(2,1, QTableWidgetItem("Cell (3,2)"))
        self.tableWidget.setItem(3,0, QTableWidgetItem("Cell (4,1)"))
        self.tableWidget.setItem(3,1, QTableWidgetItem("Cell (4,2)"))
        self.tableWidget.move(20, 50)

        # make QTimer
        self.qTimer = QTimer()
        # set interval to 1 s
        self.qTimer.setInterval(1000)  # 1000 ms = 1 s
        # connect timeout signal to signal handler
#        self.qTimer.timeout.connect(float(volume))
        # start timer
        self.qTimer.start()





        # self.line = QLineEdit(self)

        # self.line.move(80, 20)
        # self.line.resize(200, 32)



    #     pybutton = QPushButton('OK', self)
    #     pybutton.clicked.connect(self.clickMethod)
    #     pybutton.resize(200,32)
    #     pybutton.move(80, 60)
    #
    # def clickMethod(self):
    #     print('Your name: ' + self.line.text())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_() )