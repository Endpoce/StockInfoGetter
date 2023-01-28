import csv

# add this file to root directorysystem (fix for reading a saving files error)
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import financial services
import yfinance as yf
from ArticleGetter.GetArticles import get_MW_Articles, get_Paragraphs
from DataVis.ReportCreator import get_symbols, single_ticker_Analysis, report, plots

# Import 
from datetime import datetime
import os.path
import pandas as pd
# import numpy as np
import pandas_datareader as pdr
from yahoo_fin import stock_info as si
from CorrelationTracker import StockCorrelations
from CorrelationTracker import CryptoCorrelations
import requests
from bs4 import BeautifulSoup
import seaborn as sns

# Import mpl, assign bmh style
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.style.use('bmh')

# Set historical window and symbols list
today = datetime.now()
start = '2020-01-01'

# Initalize symbols list for later use
symbols = []

# Get top stock and crypto correlations for user to examine and pursue
def get_corrs():

    # Get top stock correlations?
    StockCorrs = input("Get top Stock Correlations?")

    if StockCorrs == "Y" or StockCorrs == "y" or StockCorrs == "Yes" or StockCorrs == "yes":
 
        print("\nTop Absolute Correlations")
        df = pd.read_csv('Stocks\CorrelationTracker\StockFiles\StockCorrelations.csv')
        print(df.loc[0:10,:])

    # Get top crypto correlations
    CryptoCorrs = input("Get top Crypto Correlations?")

    if CryptoCorrs == "Y" or CryptoCorrs == "y" or CryptoCorrs == "Yes" or CryptoCorrs == "yes":
            print("\nTop Absolute Correlations")
            df = pd.read_csv('Stocks\CorrelationTracker\StockFiles\CryptoCorrelations.csv')
            print(df.loc[0:10,:])
    else:
        pass

def get_single_corr():
    #pull price using iex for each symbol in list defined above
    for ticker in symbols: 
        r = pdr.DataReader(ticker, 'yahoo', start)
        # add a symbol column
        r['Symbol'] = ticker 
        symbols.append(r)

    # concatenate into df
    df = pd.concat(symbols)
    df = df.reset_index()
    df = df[['Date', 'Close', 'Symbol']]
    df.head()

    df_pivot = df.pivot('date','symbol','close').reset_index()
    df_pivot.head()

    corr_df = df_pivot.corr(method='pearson')
    #reset symbol as index (rather than 0-X)
    corr_df.head().reset_index()
    del corr_df.index.name
    corr_df.head(10)

    #take the bottom triangle since it repeats itself
    mask = np.zeros_like(corr_df)
    mask[np.triu_indices_from(mask)] = True
    #generate plot
    sns.heatmap(corr_df, cmap='RdYlGn', vmax=1.0, vmin=-1.0 , mask = mask, linewidths=2.5)
    plt.yticks(rotation=0) 
    plt.xticks(rotation=90) 
    plt.show()

# Get symbols, store in symbols
def get_symbols():

    # Get input
    ticker = input('Ticker Symbol: ').upper()

    # add ticker symbols to symbols list
    if ticker not in symbols:
        symbols.append(ticker)

    # compare against the market?
    global comp
    comp = input('Compare against the market?: ')

    # if yes, add S&p 500 to symbols list
    if comp == 'y' or  comp == 'Y' or comp ==  'yes' or comp ==  'Yes':
        symbols.append('^GSPC')

    # for ticker in symbols, download full data and financials
    for ticker_name in symbols:
        tick = yf.download(ticker_name, start, today)
        tick.to_csv('Stocks\DataVis\Files\StockData\FullData' + str(ticker) + '.csv')

    return symbols

# define function to get ticker info
def get_Ticker_info():

    for symbol in symbols:
        if symbol != "^GSPC":

            qtable = si.get_quote_table(symbol, dict_result=False)
            
            print(qtable)
            print()
            print('-----------------------------------------------')

            url = ("https://www.marketwatch.com/investing/stock/"+symbol.lower()+"?mod=quote_search")

            global soup, site

            reqs = requests.get(url)
            soup = BeautifulSoup(reqs.text, 'lxml')
                
            site = 'Description'

            get_Paragraphs(soup, site, symbol)

            single_ticker_Analysis(symbols)
                
            report(symbols)





            get_MW_Articles(symbol)

            plots()

# Run the program in a loop
t = 0
while t < 5:
    get_corrs()
    get_symbols()
    get_Ticker_info()
    t += 1