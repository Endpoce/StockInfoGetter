import csv
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import yfinance as yf
from ArticleGetter.GetArticles import get_MW_Articles, get_Paragraphs, print_Articles
from DataVis.ReportCreator import top_correlations, get_symbols, single_ticker_Analysis, report, compare_Against_Market
from datetime import datetime
import os.path
import pandas as pd

top_correlations()

symbols = []

def get_symbols():
    
    # Grab up to 10 tickers

    # Get input
    uinput = input('Ticker Symbol: ').upper()

    # add ticker symbols to symbols list
    symbols.append(uinput)

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
    
    return symbols


def get_Ticker_info():

    #### Grab todays date and starting datey
    today = datetime.now()
    start = '2020-01-01'

    get_symbols()

    # for symbol in symbols:
    #     print("\n"+symbol+"\n")

    for symbol in symbols:

        single_ticker_Analysis(symbol)
        report(symbol)
        get_MW_Articles(symbol)

        with open("Stocks\ArticleGetter\Files\\"+ str(symbol) +"Bodies.txt") as f:
            print(f.read())

t = 0
while t < 5:
    get_Ticker_info()
    t+=1