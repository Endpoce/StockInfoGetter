"""
This is a program for automatically buying/selling stocks using th alpaca_trade_api and my own personal paper
trading account with Alpaca. They are commission free, and the paper trading api is also free. So use it to
learn as much as possible.

PseudoCode:

x-import resources
x-create while loop for reoccuring input
    x-Get user input for ticker symbols
    x-Quits properly
x-plot ticker symbol

x-implement portfolio management system
    x-determine portfolio sizes
    x-determine positions
    x-determine how many stocks can be bought/sold
    x-determine gains/losses for the day

x-initialize class for Strategy implementation
    x-set the parameters for the class
        x-'login' using credentials
    x-check for last price
    x-check for account positions
    x-can only sell if position > 0
    x-initialize backtest

    -continuously monitor ticker symbols
        -continuously trade based on crossovers
            -can only sell stock at a profit
            -must follow the pattern day trading rule
            -can only spend 2.5% of portfolio per trade

   
-print 'report' on ticker symbol
    -get rid of footers

-port to github

-redo config file

-error handling

"""


#import resources
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import timedelta
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import style
import requests
import json
import alpaca_trade_api as trade_api
from ConfigFile import *
import pprint

# YF pandas override
yf.pdr_override()

# Grab todays date
today = datetime.now()

#The date that you want to start getting data from
start = '2016-01-01'

#api for api calls
api = trade_api.REST(
    'PKFSKIR6TQQQOH8W14Y7',
    'pbvGN91GWOLjTyfaaW7QHGkAJ9dPl3nvj7B4yLaN',
    'https://paper-api.alpaca.markets'
)

#get account info
account = api.get_account()

#initialize uinput
uinput = ""


while uinput != "QUIT":

    #get user input for ticker symbol
    uinput = input('Ticker Symbol: ').upper()

    # get buy_quantity
    buy_quantity = input("How much to buy/sell?: ")

    # get last week of price data
    delta = timedelta(days = 7)
    lastPrice = yf.download(uinput, start=(today - delta), interval='1m', end=today)

    # get account info
    BASE_URL = "https://paper-api.alpaca.markets"
    ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
    ORDERS_URL = "{}/v2/orders".format(BASE_URL)
    HEADERS = {"APCA-API-KEY-ID": "PKFSKIR6TQQQOH8W14Y7", "APCA-API-SECRET-KEY": "pbvGN91GWOLjTyfaaW7QHGkAJ9dPl3nvj7B4yLaN"}

    # get account data
    def get_account_data():
        r = requests.get(ACCOUNT_URL, headers=HEADERS)
        print(json.loads(r.content))
        return json.loads(r.content)

    get_account_data()

    # download YF data and store in tick.csv
    tick = yf.download(uinput, start=start, end=today)
    tick.to_csv(r"tick.csv")
    TICKER = pd.read_csv(r'tick.csv')

    # SMA 30 day stored in a pandas dataframe
    smaThirty = pd.DataFrame()
    smaThirty['Adj Close'] = TICKER['Adj Close'].rolling(window=30).mean()

    # SMA 100 day stored in a pandas dataframe
    smaHundred = pd.DataFrame()
    smaHundred['Adj Close'] = TICKER['Adj Close'].rolling(window=100).mean()

    # volme stored in a pandas dataframe
    volume = pd.DataFrame()
    volume['Volume'] = TICKER['Volume'].rolling(window=1000).mean()

    # create a new data frame to store all the data in 1 dataframe : dataframe of dataframes
    data = pd.DataFrame()
    data[str(TICKER)] = TICKER['Adj Close']
    data['smaThirty'] = smaThirty['Adj Close']
    data['smaHundred'] = smaHundred['Adj Close']
    data['Volume'] = volume['Volume']

    #class for API call to Buy/Sell the target amount of stocks
    class Strategy(object):
        def __init__(self):
            self.key = "PKFSKIR6TQQQOH8W14Y7"
            self.secret = "pbvGN91GWOLjTyfaaW7QHGkAJ9dPl3nvj7B4yLaN"
            self.alpaca_endpoint = 'https://paper-api.alpaca.markets'
            self.api = trade_api.REST(self.key, self.secret, self.alpaca_endpoint)
            self.symbol = uinput
            self.current_order = None
            self.last_price = lastPrice[-1:]

            try:
                self.position = int(self.api.get_position(self.symbol).qty)
            except Exception as exception:
                if exception.__str__() == 'position does not exist':
                    self.position = 0
        
        def get_Positions(self):
            my_positions = self.api.list_positions()
            my_positions_df = pd.DataFrame([position._raw for position in my_positions])
            my_positions_df.set_index('symbol', 'qty')

            if uinput in my_positions_df:
                qty = float(my_positions_df.at[uinput, 'qty'])
            else:
                qty = 0

            with open("Positions.txt", "w") as f:

                f.write("P/L OTD: " + str(float(account.equity)-float(account.last_equity))+ "\n")
                f.write("Equity: " + account.equity + "\n")
                f.write("Buying Power: " + account.buying_power + "\n")

                f.write(str(my_positions_df['symbol']+ " " +  my_positions_df['qty']))

        def BackTest(self):

            df=yf.download(uinput,start,today)

            emasUsed=[3,5,8,10,12,15,30,35,40,45,50,60,100]

            for x in emasUsed:
                ema=x
                df["Ema_"+str(ema)]=round(df.iloc[:,4].ewm(span=ema, adjust=False).mean(),2)

            df=df.iloc[60:]

            pos=0
            num=0
            percentchange=[]

            for i in df.index:
                cmin=min(df["Ema_3"][i],df["Ema_5"][i],df["Ema_8"][i],df["Ema_10"][i],df["Ema_12"][i],df["Ema_15"][i],)
                cmax=max(df["Ema_30"][i],df["Ema_35"][i],df["Ema_40"][i],df["Ema_45"][i],df["Ema_50"][i],df["Ema_60"][i], df["Ema_100"][i])

                close=df["Adj Close"][i]
                
                if(cmin>cmax):
                    #print("Red White Blue")
                    if(pos==0):
                        bp=close
                        pos=1
                        print("Buying now at "+str(bp))


                elif(cmin<cmax):
                    #print("Blue White Red")
                    if(pos==1):
                        pos=0
                        sp=close
                        print("Selling now at "+str(sp))
                        pc=(sp/bp-1)*100
                        percentchange.append(pc)
                if(num==df["Adj Close"].count()-1 and pos==1):
                    pos=0
                    sp=close
                    print("Selling now at "+str(sp))
                    pc=(sp/bp-1)*100
                    percentchange.append(pc)

                num+=1

            #print(percentchange)

            gains = 0
            ng = 0
            losses = 0
            nl =0
            totalR = 0

            for i in percentchange:
                if(i>0):
                    gains+=i
                    ng+=1
                else:
                    losses+=i
                    nl+=1
                totalR=totalR*((i/100)+1)

            totalR=round((totalR-1)*100,2)

            if(ng>0):
                avgGain=gains/ng
                maxR=str(max(percentchange))
            else:
                avgGain=0
                maxR="undefined"

            if(nl>0):
                avgLoss=losses/nl
                maxL=str(min(percentchange))
                ratio=str(-avgGain/avgLoss)
            else:
                avgLoss=0
                maxL="undefined"
                ratio="inf"

            if(ng>0 or nl>0):
                battingAvg=ng/(ng+nl)
            else:
                battingAvg=0

            print()
            print("Results for "+ uinput +" going back to "+str(data.index[0])+", Sample size: "+str(ng+nl)+" trades"+"\n")
            print("EMAs used: 30, 100 day"+"\n")
            print("Batting Avg: "+ str(battingAvg)+"\n")
            print("Gain/loss ratio: "+ ratio+"\n")
            print("Average Gain: "+ str(avgGain)+"\n")
            print("Average Loss: "+ str(avgLoss)+"\n")
            print("Max Return: "+ maxR+"\n")
            print("Max Loss: "+ maxL+"\n")
            print("Total return over "+str(ng+nl)+ " trades: "+ str(totalR)+"%" +"\n")
            #print("Example return Simulating "+str(n)+ " trades: "+ str(nReturn)+"%" )
            print()

            with open("BackTestData.txt", 'w') as a:
                a.write("Results for "+ uinput +" going back to "+str(data.index[0])+", Sample size: "+str(ng+nl)+" trades"+"\n")
                a.write("EMAs used: 30, 100 day"+"\n")
                a.write("Batting Avg: "+ str(battingAvg)+"\n")
                a.write("Gain/loss ratio: "+ ratio+"\n")
                a.write("Average Gain: "+ str(avgGain)+"\n")
                a.write("Average Loss: "+ str(avgLoss)+"\n")
                a.write("Max Return: "+ maxR+"\n")
                a.write("Max Loss: "+ maxL+"\n")
                a.write("Total return over "+str(ng+nl)+ " trades: "+ str(totalR)+"%" +"\n")
                
        def submit_order(self,target):
            if self.current_order is not None:
                self.api.cancel_order(self.current_order.id)

        # SMA CROSSOVER STRATEGY
        def buy_sell(self, data, buy_quantity):
            sigPriceBuy = []
            sigPriceSell = []
            flag = -1

            # if sma30 > sma100 BUY, if sma30<sma100 SELL
            for i in range(len(data)):
                if data['smaThirty'][i] > data['smaHundred'][i]:

                    if flag != 1:
                        sigPriceBuy.append(data[str(TICKER)][i])
                        sigPriceSell.append(np.nan)

                        if self.position<0 or self.position == 0:
                            try:
                                # buy_quantity = abs(self.position), buy_quantity
                                print(f"Buying {buy_quantity} shares")
                                self.api.submit_order(symbol=uinput, qty = buy_quantity, side='buy', type='market', time_in_force='day')
                                flag = 1

                            except BaseException:
                                print("Insufficient quantity available for order.")
                                break
                    else:
                        sigPriceBuy.append(np.nan)
                        sigPriceSell.append(np.nan)

                elif data['smaThirty'][i] < data['smaHundred'][i]:

                    if flag != 0:
                        sigPriceBuy.append(np.nan)
                        sigPriceSell.append(data[str(TICKER)][i])
                        sell_quantity = buy_quantity

                        if self.position> 0 :
                            try:
                                # sell_quantity = abs(self.position), sell_quantity
                                print(f"selling {sell_quantity} shares")
                                self.api.submit_order(symbol=uinput,qty= sell_quantity,side='sell',type='market',time_in_force='day')
                                flag = 0
                            except BaseException as e:
                                print("Insufficient quantity available for order.")
                                break
                                

                    else:
                        sigPriceBuy.append(np.nan)
                        sigPriceSell.append(np.nan)
                else:
                    sigPriceBuy.append(np.nan)
                    sigPriceSell.append(np.nan)
            return(sigPriceBuy, sigPriceSell)

    #Print out report
    print(f"\nLast Close: " + "\t" + str(TICKER['Adj Close'][-1:]) + "\n")
    print(f"Last volume:" + "\t"+ str(TICKER["Volume"][-1:]) + "\n")
    # print(Strategy.position)

    #if smaThirty > smaHundred, its in a buy position
    if data['smaThirty'][-1:].item() > data['smaHundred'][-1:].item():
        print("Ticker is in a Buy Position")

    #if smaThirty < smaHundred, its in a sell postion
    elif data['smaThirty'][-1:].item() < data['smaHundred'][-1:].item():
        print("Ticker is in a Sell Position")

        # a function to signal when to buy and sell the stock
    def buy_sell_data(data):
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
    buy_sell_data = buy_sell_data(data)
    data['Buy_Signal_Price'] = buy_sell_data[0]
    data['Sell_Signal_Price'] = buy_sell_data[1]

    #visualize the data and the strategy to buy and sell the stock
    # TODO reformat for multiple graphs

    if __name__ == '__main__':
        t = Strategy()
        t.BackTest()
        t.submit_order(buy_quantity)
        t.buy_sell(data,buy_quantity)
        t.get_Positions()
        
        plot1 = plt.figure(figsize=(12.6, 4.6))
        plt.style.use('fivethirtyeight')
        plt.plot(TICKER['Adj Close'], label = uinput, alpha=0.35)
        plt.plot(smaThirty['Adj Close'], label='SMA30',alpha=0.35)
        plt.plot(smaHundred['Adj Close'], label='SMA100',alpha=0.35)
        plt.legend(loc=0)
        plt.scatter(data.index, data['Buy_Signal_Price'], label='BUY', marker='^', color='green' )
        plt.scatter(data.index, data['Sell_Signal_Price'], label='SELL', marker='v', color='red' )
        plt.title(uinput + " Adj. Close Price History for "+ str(start) + " to " + str(today))
        plt.xlabel('SMA 30 vs. 100 day')
        plt.ylabel('Adj. Close Price')
        plt.show()
