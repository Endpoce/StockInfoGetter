import csv

# add this file to root directorysystem (fix for reading a saving files error)
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import financial services
import yfinance as yf
from ArticleGetter.GetArticles import get_MW_Articles, get_Paragraphs
from DataVis.ReportCreator import get_symbols, single_ticker_plot, report, plots

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

corrs = 'E:\Projects\Github\StockInfoGetter\Stocks\CorrelationTracker\StockFIles\StockCorrelations.csv'

# Initalize symbols list for later use
symbols = []

# Get symbols, store in symbols
def get_symbols():

    # Get input
    ticker = input('Ticker Symbols: ').upper()

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

# Get all correlations for a single ticker
def get_single_corr(corrs, symbols):

    # Get correlation
<<<<<<< HEAD
    with open(corrs, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            row = [str(element) for element in row]
            if str(symbols[0]) in ','.join(row):
                print(row)
=======
    corr = input("Get correlations?")

    # if yes, get correlation
    if corr == "Y" or corr == "y" or corr == "Yes" or corr == "yes":
        correlations = pd.read_csv("Stocks\CorrelationTracker\StockFIles\StockCorrelations.csv", delimiter=',')
        # print(correlations.loc[0:10,:])

        correlations.columns = ['ticker1', 'ticker2', 'correlation']

        df = pd.DataFrame(correlations)

        df = df.loc[df[] == symbols[0]]

        # give columns meaningful names

        correlations.sort_values(by=['correlation'], ascending=False, inplace=True)
                
    else:
        pass

>>>>>>> a917c47062fcc2493f3eeb7a751f18f048ad6894

    print("-----------------------------------------------")

# define function to get ticker info
def get_Ticker_info(symbols):

    for symbol in symbols:
        if symbol != "^GSPC":


            print('-----------------------------------------------')

            url = ("https://www.marketwatch.com/investing/stock/"+str(symbol).strip().lower()+"?mod=quote_search")

            global soup, site

            reqs = requests.get(url)
            soup = BeautifulSoup(reqs.text, 'lxml')
                
            site = 'Description'

            get_Paragraphs(soup, site, str(symbol).strip())

            report(symbols)

            qtable = si.get_quote_table(str(symbol).strip(), dict_result=False)
            print(qtable)

            get_single_corr(corrs, symbols)

            single_ticker_plot(symbols)

            get_MW_Articles(symbol)

            plots()
        
        else:
            pass

# Run the program in a loop
t = 0
while t < 5:

    get_symbols()


    if len(symbols) == 1:
        get_Ticker_info(symbols)


    elif len(symbols) > 1:
        get_corrs(symbols)
        get_Ticker_info(symbols)

    else:
        pass
    


    t += 1