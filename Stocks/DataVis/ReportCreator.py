#### import dependencies
from re import S
import pandas as pd
from pandas.plotting import scatter_matrix
import numpy as np
from requests.api import get
import yfinance as yf
from datetime import datetime
import matplotlib.pyplot as plt
import collections
import pandas_datareader

#### YF pandas override
yf.pdr_override()
t = 0
while t < 10:
    #### Grab todays date and starting date
    today = datetime.now()
    start = '2020-01-01'

    #### price and volume dictionaries for later use
    price_actions = {}
    avgvolumes = {}
    symbols = []

    #### Do you want top market correlations?
    def top_correlations():
        
        yes_or_no = input('Do you want top market correlations?')

        if yes_or_no == 'y' or yes_or_no ==  "Y" or yes_or_no ==  'yes' or yes_or_no ==  'Yes':

            from FindCorrelations import dataset, stocks_returns, get_redundant_pairs, get_top_abs_correlations
            df = pd.read_csv('Stocks\DataVis\Files\Correlations\FoundCorrs.csv')
            print(df.loc[0:10,:])

        else:

            pass

    # run function for asking if they want/getting the top market correlations
    # good for getting hot stocks correlated with the market
    top_correlations()

    #### get list of tickers to be analyzed
    def get_symbols():
        
        # Grab up to 10 tickers
        j = 0
        while j < 10: 

            # Get input
            uinput = input('Ticker Symbol: ').upper()

            # If ticker symbol = QUIT, quit
            if uinput == 'QUIT':
                break

            # add ticker symbols to symbols list
            symbols.append(uinput)

            # Iterate
            j = j+1
        
        # compare against the market?
        global comp
        comp = input('Compare against the market?: ')

        # if yes, add S&p 500 to symbols list
        if comp == 'y' or  comp == 'Y' or comp ==  'yes' or comp ==  'Yes':
            symbols.append('^GSPC')

        # Place symbols in dataframe for easier use
        symboldf = pd.DataFrame(symbols)
        symboldf.to_csv('Stocks\DataVis\Files\Tickers\Symbols.csv')
        
        # for each symbol in symbols, download the data and save it to a csv file
        for symbol in symbols:

            tick = yf.download(symbol, period='1y', interval='1d')
            tick.to_csv('Stocks\DataVis\Files\StockData\\' + str(symbol) + '.csv')

    # get symbols to be analyzed
    # can use top correlations to get hot stocks correlated with the market
    get_symbols()

    #### if you have a single ticker, proceed here to single analysis
    if len(symbols) == 1:

        def single_ticker_Analysis(symbols):
            
            i = 0
            for symbol in symbols:
                # var for ticker csv file
                TICKER = pd.read_csv('Stocks\DataVis\Files\StockData\\' + str(symbol) + ".csv", skipfooter=3, engine='python')

                #SMA 30 day stored in a pandas dataframe
                smaThirty = pd.DataFrame()
                smaThirty['Adj Close'] = TICKER['Adj Close'].rolling(window=30).mean()
                price_actions[symbol] = TICKER['Adj Close'].mean()

                # SMA 100 day stored in a pandas dataframe
                smaHundred = pd.DataFrame()
                smaHundred['Adj Close'] = TICKER['Adj Close'].rolling(window=100).mean()

                # volme stored in a pandas dataframe
                volume = pd.DataFrame()
                volume['Volume'] = TICKER['Volume'].rolling(window=30).mean()
                # volume['Volume'] = TICKER['Volume']

                avgvolumes[symbol] = TICKER['Volume'].mean()

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
                plt.figure()
                plt.style.use('fivethirtyeight')
                plt.plot(TICKER['Adj Close'], label = symbol, alpha=0.35)
                plt.plot(smaThirty['Adj Close'], label='SMA30',alpha=0.35)
                plt.plot(smaHundred['Adj Close'], label='SMA100',alpha=0.35)
                plt.legend(loc=0)
                plt.scatter(data.index, data['Buy_Signal_Price'], label='BUY', marker='^', color='green' )
                plt.scatter(data.index, data['Sell_Signal_Price'], label='SELL', marker='v', color='red' )
                plt.title(symbol + ' Adj. Close Price History')
                plt.xlabel('SMA 30 vs. 100 day')
                plt.ylabel('Adj. Close Price')

                i += 1
        
        #### Report (Display information)
        ## Correlation Matrices
        if comp == 'y' or  comp == 'Y' or comp ==  'yes' or comp ==  'Yes':


            # Price Matrix
            stock_data = yf.download(symbols, start)['Close']
            returns = pd.DataFrame()
            for stock in stock_data:
                if stock not in returns:
                    returns[stock] = np.log(stock_data[stock]).diff()
            returns = returns[1:]        
            returns.describe()
            returns.corr()
            for symbol in symbols:
                returns.to_csv('Stocks\DataVis\Files\Correlations\\'+symbol+'PriceCorrelation.csv')
            # plt.title('Price Correlations')
            scatter_matrix(returns, figsize=(10,8), alpha=0.3)

            # Volume Matrix
            vol_data = yf.download(symbols, start)['Volume']
            volreturns = pd.DataFrame()
            for stock in vol_data:
                if stock not in volreturns:
                    volreturns[stock] = np.log(vol_data[stock]).diff()
            volreturns = volreturns[1:]        
            volreturns.describe()
            volreturns.corr()
            for symbol in symbols:
                returns.to_csv('Stocks\DataVis\Files\Correlations\\'+symbol+'VolumeCorrelation.csv')
            # plt.title('Volume Correlations')
            scatter_matrix(volreturns, figsize=(10,8), alpha=0.3)



        ### Report (Display information)
        else:
            pass

        single_ticker_Analysis(symbols)

    #### if have more the one ticker, proceed to batch analysis
    if len(symbols) != 1:

        def batch_ticker_analysis(symbols):

            i = 0
            for symbol in symbols:
                # download YF data and store in tick.csv
                tick = yf.download(symbol, start=start, end=today)
                tick.to_csv('Stocks\DataVis\Files\StockData\FullData' + str(symbol) + ".csv")
                TICKER = pd.read_csv('Stocks\DataVis\Files\StockData\FullData' + str(symbol) + ".csv", skipfooter=3, engine='python')


                #SMA 30 day stored in a pandas dataframe
                smaThirty = pd.DataFrame()
                smaThirty['Adj Close'] = TICKER['Adj Close'].rolling(window=30).mean()
                price_actions[symbol] = TICKER['Adj Close'].mean()

                # SMA 100 day stored in a pandas dataframe
                smaHundred = pd.DataFrame()
                smaHundred['Adj Close'] = TICKER['Adj Close'].rolling(window=100).mean()

                # volme stored in a pandas dataframe
                volume = pd.DataFrame()
                volume['Volume'] = TICKER['Volume'].rolling(window=30).mean()
                # volume['Volume'] = TICKER['Volume']

                avgvolumes[symbol] = TICKER['Volume'].mean()

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
                plt.figure()
                plt.style.use('fivethirtyeight')
                plt.plot(TICKER['Adj Close'], label = symbol, alpha=0.35)
                plt.plot(smaThirty['Adj Close'], label='SMA30',alpha=0.35)
                plt.plot(smaHundred['Adj Close'], label='SMA100',alpha=0.35)
                plt.legend(loc=0)
                plt.scatter(data.index, data['Buy_Signal_Price'], label='BUY', marker='^', color='green' )
                plt.scatter(data.index, data['Sell_Signal_Price'], label='SELL', marker='v', color='red' )
                plt.title(symbol + ' Adj. Close Price History')
                plt.xlabel('SMA 30 vs. 100 day')
                plt.ylabel('Adj. Close Price')

                i += 1
                
        # Report (Display information)
        # Correlation Matrices
        # Price Matrix
        stock_data = yf.download(symbols, start)['Close']
        returns = pd.DataFrame()
        for stock in stock_data:
            if stock not in returns:
                returns[stock] = np.log(stock_data[stock]).diff()
        returns = returns[1:]        
        returns.describe()
        returns.corr()
        for symbol in symbols:
            returns.to_csv('Stocks\DataVis\Files\Correlations\\'+symbol+ 'PriceCorrelations.csv')
        plt.title('Price Correlations')
        scatter_matrix(returns, figsize=(10,8), alpha=0.3)

        # Volume Matrix
        vol_data = yf.download(symbols, start)['Volume']
        volreturns = pd.DataFrame()
        for stock in vol_data:
            if stock not in volreturns:
                volreturns[stock] = np.log(vol_data[stock]).diff()
        volreturns = volreturns[1:]        
        volreturns.describe()
        volreturns.corr()
        plt.title('Volume Correlations')
        for symbol in symbols:
            returns.to_csv('Stocks\DataVis\Files\Correlations\\'+symbol+ 'VolumeCorrelations.csv')
        scatter_matrix(volreturns, figsize=(10,8), alpha=0.3)


        ### Report (Display information)

        # Correlation Matrices
        # Price Matrix
        stock_data = yf.download(symbols, start)['Close']
        returns = pd.DataFrame()
        for stock in stock_data:
            if stock not in returns:
                returns[stock] = np.log(stock_data[stock]).diff()
        returns = returns[1:]        
        returns.describe()
        returns.corr()
        returns.to_csv('Stocks\DataVis\Files\Tickers\\StockData.csv')
        plt.title('Price Correlations')
        scatter_matrix(returns, figsize=(10,8), alpha=0.3)

        # Volume Matrix
        vol_data = yf.download(symbols, start)['Volume']
        volreturns = pd.DataFrame()
        for stock in vol_data:
            if stock not in volreturns:
                volreturns[stock] = np.log(vol_data[stock]).diff()
        volreturns = volreturns[1:]        
        volreturns.describe()
        volreturns.corr()
        plt.title('Volume Correlations')
        scatter_matrix(volreturns, figsize=(10,8), alpha=0.3)
        batch_ticker_analysis(symbols)

    else:
        pass

    #### Iterate over csv files and report last and average price and volume for all symbols
    def report():

        k=0
        for symbol in symbols:
            csvfile = pd.read_csv('Stocks\DataVis\Files\StockData\\'+symbol+'.csv')
            pricefile = pd.read_csv( 'Stocks\DataVis\Files\Correlations\\' + symbol +'PriceCorrelations.csv')
            volumefile = pd.read_csv( 'Stocks\DataVis\Files\Correlations\\' + symbol +'VolumeCorrelations.csv')

            last_pri = str(csvfile['Close'].iloc[-1])
            last_vol = str(csvfile['Volume'].iloc[-1])

            avg_pri = str(csvfile['Close'].mean())
            avg_vol = str(csvfile['Volume'].mean())
            
            avg_pri_corr = pricefile['^GSPC'].mean()
            avg_vol_corr = volumefile['^GSPC'].mean()

            # Symbol
            print()
            print('------------------------------------------')
            print(str(symbol) + ':')

            # Price action
            print('\nLast Price:\n\t\t\t' + last_pri)
            print('\nAverage (30d) Price:\n\t\t\t' + avg_pri)
            print('\nAverage Price correlation:\n\t\t\t' + str(avg_pri_corr))

            # Volume
            print('\nLast Volume:\n\t\t\t' + last_vol)
            print('\nAverage (30d) volume:\n\t\t\t' + avg_vol)
            print('\nAverage Volume correlation:\n\t\t\t' + str(avg_vol_corr))
            
            k += 1

        # Sort dictionaries
        sorted_volumes = sorted(avgvolumes.items(), key=lambda x:x[1])
        sortvol = dict(sorted_volumes)
        sorted_prices = sorted(price_actions.items(), key=lambda x:x[1])
        sortpri = dict(sorted_prices)

        max_price = max(sortpri, key=sortpri.get)
        max_vol = max(sortvol,key=sortvol.get)



        # report highest price and highest volume
        print('------------------------------------------')
        print('\nHighest price action:\n\t\t\t' + str(max_price))
        print('\nMost Volume:\n\t\t\t' + str(max_vol))
        print('------------------------------------------')
            
    #### Show and save Plots
    def plots():
        # plt.savefig('Stocks\DataVis\Files\Graphs\\'+str(symbol) + 'Graphs.png')
        plt.show()



    #### run functions
    # get_symbols()
    report()
    plots()

    # Iterate
    t += 1
