import csv
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import yfinance as yf
from ArticleGetter.GetArticles import get_MW_Articles, get_Google_articles,get_Paragraphs, print_Articles
from DataVis.ReportCreator import get_symbols, single_ticker_Analysis, report, batch_ticker_analysis, compare_Against_Market, plots
from datetime import datetime
import os.path
import pandas as pd

def get_corrs():
    StockCorrs = input("Get top Stock Correlations?")

    if StockCorrs == "Y" or StockCorrs == "y" or StockCorrs == "Yes" or StockCorrs == "yes":
        from CorrelationTracker import StockCorrelations

    CryptoCorrs = input("Get top Crypto Correlations?")

    if CryptoCorrs == "Y" or StockCorrs == "y" or StockCorrs == "Yes" or StockCorrs == "yes":
        from CorrelationTracker import CryptoCorrelations

def get_symbols():
    #### Grab todays date and starting date
    today = datetime.now()
    start = '2020-01-01'

    global symbols
    symbols = []

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

    for ticker_name in symbols:
        tick = yf.download(str(ticker_name), start)
        tick.to_csv('Stocks\DataVis\Files\StockData\FullData' + str(ticker) + '.csv')

    return ticker, symbols

def get_Ticker_info():

    get_corrs()

    get_symbols()

    for symbol in symbols:
        if symbol != "^GSPC":

            single_ticker_Analysis(symbols)
                
            report(symbol, symbols)
            get_Google_articles(symbol)
            get_MW_Articles(symbol)

            with open("Stocks\ArticleGetter\Files\\"+ str(symbol) +"Bodies.txt") as f:
                print(f.read())
                print()


t = 0
while t < 5:
    get_Ticker_info()
    plots()
    t+=1