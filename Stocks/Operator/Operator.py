import csv

# add this file to root directorysystem (fix for reading a saving files error)
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import financial services
import yfinance as yf
from ArticleGetter.GetArticles import get_MW_Articles, get_Paragraphs
from DataVis.ReportCreator import get_symbols, single_ticker_Analysis, report, plots

# Import resources
from datetime import datetime
import os.path
import pandas as pd
import numpy as np
import pandas_datareader as pdr
from yahoo_fin import stock_info as si
# from CorrelationTracker import StockCorrelations
# from CorrelationTracker import CryptoCorrelations
import requests
from bs4 import BeautifulSoup
import seaborn as sns
import warnings

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

# Get symbols, store in symbols
def get_symbols():

    # Get input
    ticker = input('Ticker Symbols: ').upper().split(',')

    # add ticker symbols to symbols list
    if ticker not in symbols:
        symbols.append(ticker)

    

    return symbols

# Get top stock and crypto correlations for user to examine and pursue
def get_corrs(symbols):
    # compare against the market?
    global comp
    comp = input('Compare against the market?: ')

    # if yes, add S&p 500 to symbols list
    if comp == 'y' or  comp == 'Y' or comp ==  'yes' or comp ==  'Yes':
        symbols.append('^GSPC')

    # for ticker in symbols, download full data and financials
    for ticker_name in symbols:
        tick = yf.download(ticker_name, start, today)
        tick.to_csv('Stocks\DataVis\Files\StockData\FullData' + str(ticker_name) + '.csv')

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

# Get single correlation
def get_single_corr(symbols):

    # load the CSV file containing all of the stock correlations
    correlations = pd.read_csv("Stocks\CorrelationTracker\StockFIles\StockCorrelations.csv")

    # give the columns meaningful names
    correlations.columns = ['ticker1', 'ticker2', 'correlation']

    # filter the data to include only the correlations for the target stock
    correlations = correlations[(correlations['ticker1'] == symbols) | (correlations['ticker2'] == symbols)].reset_index(drop=True) 
    
    # sort the results in descending order and keep only the top 10
    correlations = correlations.sort_values('correlation', ascending=False).head(10)
    
    print("\nTop Absolute Correlations: ")
    print(correlations)

    print("-----------------------------------------------")

    return correlations

    # # Get correlation
    # corr = input("Get correlation?")

    # if corr == "Y" or corr == "y" or corr == "Yes" or corr == "yes":
    #     ticker1 = input("compare Correlation to (seperated by ,): ").split(', ')

    #     # Get correlation
    #     symbols_data = yf.download(symbols[0], start, today)
        
    #     for ticker in ticker1:
    #         ticker1_data = yf.download(ticker1, start, today)

    #         # Get correlation
    #         corr = symbols_data['Adj Close'].corr(ticker1_data['Adj Close'])
    #         print(ticker +" Correlation: ")
    #         print(corr)

# define function to get ticker info
def get_Ticker_info(symbols):

    for symbol in symbols:
        if symbol != "^GSPC":

            qtable = si.get_quote_table(str(symbol).strip(), dict_result=False)
            
            print(qtable)
            print()
            print('-----------------------------------------------')

            url = ("https://www.marketwatch.com/investing/stock/"+str(symbol).strip().lower()+"?mod=quote_search")

            global soup, site

            reqs = requests.get(url)
            soup = BeautifulSoup(reqs.text, 'lxml')
                
            site = 'Description'

            get_Paragraphs(soup, site, str(symbol).strip())

            single_ticker_Analysis(symbols)
                
            report(symbols)

            get_MW_Articles(symbol)

            plots()
        
        else:
            pass

# Run the program in a loop
t = 0
while t < 5:

    get_symbols()

    if len(symbols) == 1:
        get_single_corr(symbols)
    elif len(symbols) > 1:
        get_corrs(symbols)
    else:
        pass
    
    get_Ticker_info(symbols)

    t += 1