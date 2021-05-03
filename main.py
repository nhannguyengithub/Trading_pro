import pandas_datareader as pdr
import datetime
import matplotlib.pyplot as plt

aapl = pdr.get_data_yahoo('AAPL',
                        start = datetime.datetime(2018,4,1),
                        end = datetime.date.today())
brk_b = pdr.get_data_yahoo('BRK-B',
                           start=datetime.datetime(2018, 4, 1),
                           end=datetime.date.today())

aapl['Close'].plot(grid = True)
brk_b['Close'].plot(grid = True)
plt.show()