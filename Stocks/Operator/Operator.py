import csv

# add this file to root directorysystem (fix for reading a saving files error)
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import financial services
import yfinance as yf
from ArticleGetter.GetArticles import get_MW_Articles, get_Paragraphs
from DataVis.ReportCreator import get_symbols, single_ticker_plot, report, plots, report2
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

# Get symbols, store in symbols
def get_symbols():

    # define a loop to get symbols
    while True:

        # Get input
        ticker = input('Ticker Symbols: ').upper()
        if ticker == 'DONE':
            break
        else:
            pass

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
            API_KEY = 'S1RT6O9PMYILCVZ4'
            url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={API_KEY}"
            response = requests.get(url)
            data = response.json()
            description = data["Description"]
            print(description)
            print('-----------------------------------------------')

# define a function to get highest volume and price action stocks
def get_highest_volume(symbols):
    high_price_ticker, high_price, high_volume_ticker, high_volume = report2(symbols)
    print(f"Ticker with highest price: {high_price_ticker} ({high_price})")
    print(f"Ticker with highest volume: {high_volume_ticker} ({high_volume})")

# Run the program in a loop
t = 0
while t < 5:

    # Set historical window and symbols list
    today = datetime.now()
    start = '2020-01-01'

    corrs = 'E:\Projects\Github\StockInfoGetter\Stocks\CorrelationTracker\StockFIles\StockCorrelations.csv'

    # Initalize symbols list for later use
    symbols = []

    # Run the program
    if __name__ == '__main__':
        
        # get correlations on startup
        get_corrs(symbols)

        # get symbols
        get_symbols()

        # if only one symbol, get ticker info for that symbol
        if len(symbols) == 1:

            # get company description
            get_descriptions(symbols)

            # get quick report
            report(symbols)

            # get qtable
            for symbol in symbols:
                qtable = si.get_quote_table(str(symbol[0]).strip(), dict_result=False)
                print(qtable)
            print('-----------------------------------------------')

            # get correlations for this ticker
            get_single_corr(corrs, symbols)

            # get ticker info
            single_ticker_plot(symbols)

            # get marketwatch articles
            get_MW_Articles(symbols[0])

            # display plots
            plots()

        # if more than one symbol, get ticker info for all symbols
        elif len(symbols) > 1:
            get_descriptions(symbols)

            report(symbols)

            get_highest_volume(symbols)
            
            for symbol in symbols:
                qtable = si.get_quote_table(str(symbol).strip(), dict_result=False)
                print(qtable)

            plots()



        else:
            pass
        


        t += 1