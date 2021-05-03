import pandas_datareader as pdr
import pandas as pd
import matplotlib.pyplot as plt
import datetime
aapl = pdr.get_data_yahoo('AAPL',
                          start=datetime.datetime(2016,4,1),
#                          end=datetime.datetime(2021,4,30))
                          end=datetime.date.today())
aapl['Close'].plot(grid=True)
plt.show()