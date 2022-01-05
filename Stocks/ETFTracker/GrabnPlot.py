import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
import random


#yfinance pandas override
yf.pdr_override()


#list for tickers
ticklist = []

#function for getting multiple tickers
def getInput():
    while True:
        uinput = input('Ticker Symbol:\n').upper()
        ticklist.append(uinput)
        if uinput == 'EXIT':
            break
        else:
            continue

style.use('fivethirtyeight')

fig = plt.figure()

def create_plots():
    xs = []
    ys = []

    for i in range(10):
        x = i
        y = random.randrange(10)

        xs.append(x)
        ys.append(ys)

    return xs, ys

ax1 = fig.add_subplot(111)
ax2 = fig.add_subplot(212)

x,y = create_plots()
ax1.plot(x,y)

x,y = create_plots()
ax2.plot(x,y)


plt.show()
