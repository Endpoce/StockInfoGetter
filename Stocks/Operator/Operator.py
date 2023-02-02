import csv

# add this file to root directorysystem (fix for reading a saving files error)
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import financial services
import yfinance as yf
from ArticleGetter.GetArticles import get_MW_Articles, get_Paragraphs
from DataVis.ReportCreator import get_symbols, single_ticker_plot, report, plots
from yahoo_fin import stock_info as si

# Import resources
from datetime import datetime
import os.path
import pandas as pd
import requests
from bs4 import BeautifulSoup


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
    ticker = input('Ticker Symbols: ').upper().split(',')

    # add ticker symbols to symbols list
    if ticker not in symbols:
        symbols.append(ticker)

    return symbols

# Get top stock and crypto correlations for user to examine and pursue
def get_corrs(symbols):
    # compare against the market?
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

    import CorrelationTracker.StockCorrelations as sc

    # Initalize rows list
    rows = []

    # Get correlation
    with open(corrs, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            row = [str(element) for element in row]
            if str(symbols[0]) in ','.join(row):
                rows.append(row)
                print(rows.index(row), row)

    print("-----------------------------------------------")

# define function to get ticker info
def get_Ticker_info(symbols):

    for symbol in symbols:
        if symbol != "^GSPC":


            print('-----------------------------------------------')

            url = f"https://www.marketwatch.com/investing/stock/{symbol.lower()}"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            site = 'Description'
            articles = []
            for article in soup.find_all("a", class_="link"):
                articles.append(article.text)
            


            return articles[:10], soup, site
                



        
        else:
            pass

# define function to get ticker descriptions
def get_descriptions(symbols):
    for symbol in symbols:
        url = f"https://www.marketwatch.com/investing/stock/{symbol[0].lower().strip()}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        site = 'Description'

        get_Paragraphs(soup, site, str(symbol).strip())

# Run the program in a loop
t = 0
while t < 5:

    get_symbols()


    if len(symbols) == 1:
        get_descriptions(symbols)

        report(symbols)

        for symbol in symbols:
            qtable = si.get_quote_table(str(symbol[0]).strip(), dict_result=False)
            print(qtable)
        print('-----------------------------------------------')

        get_single_corr(corrs, symbols)

        single_ticker_plot(symbols)

        get_MW_Articles(symbols[0])

        plots()

    # if more than one symbol, get ticker info for all symbols
    elif len(symbols) > 1:
        get_descriptions(symbols)

        get_corrs(symbols)
        
        report(symbols)

        plots()



    else:
        pass
    


    t += 1