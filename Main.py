"""
This is a program for automatically buying/selling stocks using th alpaca_trade_api and my own personal paper
trading account with Alpaca. They are commission free, and the paper trading api is also free. So use it to
learn as much as possible.

PseudoCode:
x-import resources
x-Get user input for ticker symbols
x-plot ticker symbol

-implement portfolio management system
    -determine portfolio sizes
    -determine positions
    -determine how many stocks can be bought/sold
    -use while loop to continue buying/selling at last price

-initialize class for Strategy implementation
    -set the parameters for the class
        -'login' using credentials
    -check for last price
    -check for account positions
    -can only sell stock at a profit
    -can only spend 2.5% of portfolio per trade
    -must follow the pattern day trading rule
    
   
-print 'report' on ticker symbol
    -get rid of footers
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import style
import requests
import json
from Config import *
import alpaca_trade_api as trade_api

# YF pandas override
yf.pdr_override()

# Grab todays date
today = datetime.now()

#The date that you want to start getting data from
start = '2020-01-01'


uinput = ""

while uinput != "QUIT":
    #get user input for ticker symbol
    uinput = input('Ticker Symbol: ').upper()

    # get buy_quantity
    buy_quantity = input("How much to buy/sell?: ")

    #get last price
    lastPrice = yf.download(uinput, start='2021-04-15', interval='1m', end=today)

    # get account balance
    BASE_URL = "https://paper-api.alpaca.markets"
    ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
    ORDERS_URL = "{}/v2/orders".format(BASE_URL)
    HEADERS = {"APCA-API-KEY-ID": "PKICKKBU3W6RBMO4HKUR", "APCA-API-SECRET-KEY": "irrgZH94o7xe00aMq8RyEJmzLAGcP7k4UX05Oovi"}

    def get_account_data():
        r = requests.get(ACCOUNT_URL, headers=HEADERS)
        print(json.loads(r.content))
        return json.loads(r.content)

    get_account_data()

    # download YF data and store in tick.csv
    tick = yf.download(uinput, start=start, end=today)
    tick.to_csv(r"tick.csv")
    TICKER = pd.read_csv(r'tick.csv')

    #SMA 30 day stored in a pandas dataframe
    smaThirty = pd.DataFrame()
    smaThirty['Adj Close'] = TICKER['Adj Close'].rolling(window=30).mean()

    # SMA 100 day stored in a pandas dataframe
    smaHundred = pd.DataFrame()
    smaHundred['Adj Close'] = TICKER['Adj Close'].rolling(window=100).mean()

    # volme stored in a pandas dataframe
    volume = pd.DataFrame()
    volume['Volume'] = TICKER['Volume'].rolling(window=1000).mean()

    # create a new data frame to store all the data in 1 dataframe
    data = pd.DataFrame()
    data[str(TICKER)] = TICKER['Adj Close']
    data['smaThirty'] = smaThirty['Adj Close']
    data['smaHundred'] = smaHundred['Adj Close']
    data['Volume'] = volume['Volume']

    # a function to signal when to buy and sell the stock
    def buy_sell(data):
        sigPriceBuy = []
        sigPriceSell = []
        flag = -1

        # if sma30 > sma100 BUY, if sma100>sma30 SELL
        for i in range(len(data)):
            if data['smaThirty'][i] > data['smaHundred'][i]:
                if flag != 1:
                    sigPriceBuy.append(data[str(TICKER)][i])
                    sigPriceSell.append(np.nan)
                    flag = 1
                else:
                    sigPriceBuy.append(np.nan)
                    sigPriceSell.append(np.nan)

            elif data['smaThirty'][i] < data['smaHundred'][i]:
                if flag != 0:
                    sigPriceBuy.append(np.nan)
                    sigPriceSell.append(data[str(TICKER)][i])
                    flag = 0
                else:
                    sigPriceBuy.append(np.nan)
                    sigPriceSell.append(np.nan)
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        return(sigPriceBuy, sigPriceSell)

    #store the buy and sell data into a var
    buy_sell = buy_sell(data)
    data['Buy_Signal_Price'] = buy_sell[0]
    data['Sell_Signal_Price'] = buy_sell[1]

    #visualize the data and the strategy to buy and sell the stock
    # TODO reformat for multiple graphs

    plot1 = plt.figure(figsize=(12.6, 4.6))
    plt.style.use('fivethirtyeight')
    plt.plot(TICKER['Adj Close'], label = uinput, alpha=0.35)
    plt.plot(smaThirty['Adj Close'], label='SMA30',alpha=0.35)
    plt.plot(smaHundred['Adj Close'], label='SMA100',alpha=0.35)
    plt.legend(loc=0)
    plt.scatter(data.index, data['Buy_Signal_Price'], label='BUY', marker='^', color='green' )
    plt.scatter(data.index, data['Sell_Signal_Price'], label='SELL', marker='v', color='red' )
    plt.title(uinput + ' Adj. Close Price History')
    plt.xlabel('SMA 30 vs. 100 day')
    plt.ylabel('Adj. Close Price')
    plt.show()

    #class for API call to Buy/Sell the target amount of stocks
    class Strategy(object):
        def __init__(self):
            self.key = "PKICKKBU3W6RBMO4HKUR"
            self.secret = "irrgZH94o7xe00aMq8RyEJmzLAGcP7k4UX05Oovi"
            self.alpaca_endpoint = 'https://paper-api.alpaca.markets'
            self.api = trade_api.REST(self.key, self.secret, self.alpaca_endpoint)
            self.symbol = uinput
            self.current_order = None
            self.last_price = lastPrice

            try:
                self.position = int(self.api.get_position(self.symbol).qty)
            except:
                self.position = 0
        
        def submit_order(self,target):
            if self.current_order is not None:
                self.api.cancel_order(self.current_order.id)

        # SMA CROSSOVER STRATEGY
        def buy_sell(self, data, target):
            sigPriceBuy = []
            sigPriceSell = []
            flag = -1

            # if sma30 > sma100 BUY, if sma100>sma30 SELL
            for i in range(len(data)):
                if data['smaThirty'][i] > data['smaHundred'][i]:

                    if flag != 1:
                        sigPriceBuy.append(data[str(TICKER)][i])
                        sigPriceSell.append(np.nan)

                    if self.position<0 or self.position == 0:
                        buy_quantity = min(abs(self.position), buy_quantity)
                        print(f"Buying {buy_quantity} shares")
                        self.current_order = self.api.submit_order(self.symbol, buy_quantity, 'buy', 'limit', 'day', data['smaThirty'][i])
                        flag = 1

                    else:
                        sigPriceBuy.append(np.nan)
                        sigPriceSell.append(np.nan)

                elif data['smaThirty'][i] < data['smaHundred'][i]:

                    if flag != 0:
                        sigPriceBuy.append(np.nan)
                        sigPriceSell.append(data[str(TICKER)][i])
                        sell_quantity = buy_quantity

                    if self.position> 0 :
                        sell_quantity = min(abs(self.position), sell_quantity)
                        print(f"selling {sell_quantity} shares")
                        self.current_order = self.api.submit_order(self.symbol, sell_quantity,'sell','limit','day', data['smaThirty'][i])
                        flag = 0

                    else:
                        sigPriceBuy.append(np.nan)
                        sigPriceSell.append(np.nan)
                else:
                    sigPriceBuy.append(np.nan)
                    sigPriceSell.append(np.nan)
            return(sigPriceBuy, sigPriceSell)

    #Print out report
    print(f"\nLast Close: " + "\t" + str(TICKER['Adj Close'][-1:]) + "\n")
    print(f"Last price: " + str(lastPrice[-1:]) + "\n")
    print(f"Last volume:" + "\t"+ str(TICKER["Volume"][-1:]) + "\n")
    # print(Strategy.position)

    #if smaThirty > smaHundred, its in a buy position
    if data['smaThirty'][-1:].item() > data['smaHundred'][-1:].item():
        print("Ticker is in a Buy Position")

    #if smaThirty < smaHundred, its in a sell postion
    elif data['smaThirty'][-1:].item() < data['smaHundred'][-1:].item():
        print("Ticker is in a Sell Position")


    if __name__ == '__main__':
        t = Strategy()
        t.submit_order(buy_quantity)
