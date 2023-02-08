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

import streamlit as st

API_KEY = 'S1RT6O9PMYILCVZ4'

# initialize streamlit page
st.set_page_config(layout="wide")

st.title("Stock Info Getter")

st.sidebar.title("Stock Info Getter")
st.sidebar.subheader("Get stock info, news, and more!")

col1, col2 = st.columns(2, gap='small')

# Get symbols, store in symbols, in the sidebar
def get_symbols():

    # Get symbols from user
    ticker = st.sidebar.text_input('Ticker Symbols: ').upper()
    if ticker not in symbols:
        symbols.append(ticker)

# Get top stock and crypto correlations for user to examine and pursue, in the sidebar
def get_corrs(symbols):

    cwd = os.getcwd()

    # for ticker in symbols, download full data and financials
    for ticker_name in symbols:
        import CorrelationTracker.StockCorrelations as sc

        filepath = os.path.join(cwd,'StockCorrelations.csv')

        
        # tick.to_csv(filepath)

    st.sidebar.write("\nTop Absolute Correlations")
    df = pd.read_csv(filepath)
    st.sidebar.write(df.loc[0:10,:])

    st.sidebar.write("\nTop Absolute Correlations")
    df = pd.read_csv(filepath)
    st.sidebar.write(df.loc[0:10,:])

# Get all correlations for a single ticker, on the main page, column 1
def get_single_corr(symbols):

    import CorrelationTracker.StockCorrelations as sc

    corrs = 'E:\Projects\Github\StockInfoGetter\Stocks\StockCorrelations.csv'

    for symbol in symbols:
        file_path = corrs
        data = pd.read_csv(file_path)
        # give the columns a name
        data.columns = ['Ticker1','Ticker2','Correlation']
        filtered_data = data[data['Ticker1'].str.contains(symbol)]
        filtered_data2 = data[data['Ticker2'].str.contains(symbol)]

        filtered_data = filtered_data.append(filtered_data2)
        filtered_data = filtered_data.sort_values(by=['Correlation'], ascending=False)[0:10]


    st.write("Top correlations:")
    st.table(filtered_data)
    st.write("---")

# define function to get ticker info, on the main page, column 2
def get_Ticker_info(symbols):

    for symbol in symbols:
        if symbol != "^GSPC":


            st.write('-----------------------------------------------')

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

# define function to get ticker descriptions, at the top of the main page
def get_descriptions(symbols):

        try:
            for symbol in symbols:
                API_KEY = 'S1RT6O9PMYILCVZ4'
                url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={API_KEY}"
                response = requests.get(url)
                data = response.json()
                description = data["Description"]
                st.write(description)
                st.write('-----------------------------------------------')
        except:
            pass

# define a function to get highest volume and price action stocks, on the main page, column 2
def get_highest_volume(symbols):
    with col2:
        high_price_ticker, high_price, high_volume_ticker, high_volume = report2(symbols)
        st.write(f"Ticker with highest price: {high_price_ticker} ({high_price})")
        st.write(f"Ticker with highest volume: {high_volume_ticker} ({high_volume})")

#### Iterate over csv files and report last and average price and volume for all symbols
def report(symbols):

    try:
        # for each symbol in symbols, download the data and save it to a csv file
        for symbol in symbols:
            if symbol != "^GSPC":
                
                cwd = os.getcwd()

                tick = yf.download(symbol, period='1y', interval='1d')

                filepath = os.path.join(cwd, 'FUllData' + str(symbol) + '.csv')
                tick.to_csv(filepath)

                csvfile = pd.read_csv(filepath)

                last_pri = str(csvfile['Close'].iloc[-1])
                last_vol = str(csvfile['Volume'].iloc[-1])

                avg_pri = str(csvfile['Close'].mean())
                avg_vol = str(csvfile['Volume'].mean())

                # Symbol
                st.write()
                # st.write('---')
                st.write(str(symbol) + ':')

                # Price action
                st.write('\nLast Price:\n\t\t\t' + last_pri)
                st.write('\nAverage (30d) Price:\n\t\t\t' + avg_pri)

                # Volume
                st.write('\nLast Volume:\n\t\t\t' + last_vol)
                st.write('\nAverage (30d) volume:\n\t\t\t' + avg_vol)
            
    except:
        pass
        
# define a function to get the qtable, on the main page, column 2
def get_qtable(symbols):
    # get qtable
    try:
        for symbol in symbols:
            qtable = si.get_quote_table(str(symbol[0]).strip(), dict_result=False)
            st.write(qtable)
        st.write('---')
    except:
        pass


# Run the program
if __name__ == '__main__':

    
    # Set historical window and symbols list
    today = datetime.now()
    start = '2020-01-01'



    
    # Initalize symbols list for later use
    symbols = []

    # get symbols
    get_symbols()

    st.title(symbols)

    st.subheader(get_descriptions(symbols))

    # get correlations on startup
    get_corrs(symbols)

    # if only one symbol, get ticker info for that symbol
    if len(symbols) == 1:

        # get company description


        with col1:
            # get quick report
            report(symbols)
            st.write('---')

            get_qtable(symbols)
        with col2:
            # get correlations for this ticker
            get_single_corr(symbols)

        # display ticker plot
        single_ticker_plot(symbols)

        # get marketwatch articles
        get_MW_Articles(symbols[0])

        # display plots
        # plots()

    # if more than one symbol, get ticker info for all symbols
    elif len(symbols) > 1:
        get_descriptions(symbols)

        report(symbols)

        get_highest_volume(symbols)

        for symbol in symbols:
            qtable = si.get_quote_table(str(symbol).strip(), dict_result=False)
            st.write(qtable)

        plots()



    else:
        pass

    st.run()
    
