import numpy as np
import pandas as pd
import pandas_datareader as pdr
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import json
import time

symbols = []

def get_symbols():
    
    # Grab up to 10 tickers
    j = 0
    while j < 10: 

        # Get input
        uinput = input('Ticker Symbol: ').upper()

        # If ticker symbol = QUIT, quit
        if uinput == 'QUIT' or uinput == "":
            break

        # add ticker symbols to symbols list
        symbols.append(uinput)

        # Iterate
        j = j+1

def get_Google_articles(symbol):

    with open("Stocks\ArticleGetter\Files\\" +symbol+"MWLinks.txt", 'r+') as f:
        f.truncate(0)

        url = ("https://www.google.com/finance/quote/"+symbol+":NYSE")

        global soup, site

        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')

        site = "Google Finance:"

        links = []
        for link in soup.findAll('a'):
            links.append(link.get('href'))

        f.writelines("MarketWatch Links:\n\n")

        for link in links:
            if "https:" in str(link):
                f.write(link)
            else:
                pass
    f.close()

def get_MW_Articles(symbol):

    with open("Stocks\ArticleGetter\Files\\" +symbol+"MWLinks.txt", 'w') as f:
        f.truncate(0)

        url = ("https://www.marketwatch.com/investing/stock/"+symbol.lower()+"?mod=quote_search")

        global soup, site

        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'lxml')
        
        site = "MarketWatch"

        links = []
        for link in soup.findAll('a'):
            links.append(link.get('href'))

        f.writelines("MarketWatch Links:\n\n")

        for link in links:
            if "https:" in str(link):
                f.write(link)
            else:
                pass
    f.close()
    return soup, site

def get_Paragraphs(soup, site, symbol):

    with open("Stocks\ArticleGetter\Files\\"+symbol+"Bodies.txt", "") as f:       
        f.truncate()
        for data in soup.findAll('p'):
            try:
                if "company" in str(data):
                    f.writelines("\n" + site + ":\n\n")
                    f.write(str(data.getText()))

                    print(str(site) + ":\n\n")
                    print(data.getText())
                    print()
                else:
                    pass
            except Exception as e:
                pass

            # print(data.getText())
    f.close()

def print_Articles(symbols):

        ask1 = input("Get Google Articles? (Y/N) : ")

        if ask1 == "y" or ask1 == "Y" or ask1 =="yes" or ask1 == "Yes":
            get_Google_articles(symbol)
            get_Paragraphs
        else:
            pass

        ask2 = input("Get MarketWatch Articles? (Y/N) : ")

        for symbol in symbols:
            if ask2 == "y" or ask2 == "Y" or ask2 =="yes" or ask2 == "Yes":
                get_MW_Articles(symbol)
                get_Paragraphs(soup, site, symbol)
            else:
                pass


