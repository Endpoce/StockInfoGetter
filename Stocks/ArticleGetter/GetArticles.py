import numpy as np
import pandas as pd
import pandas_datareader as pdr
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import json
import time


def get_Google_articles(symbol):

    url = ("https://www.google.com/finance/quote/" + symbol + ":NASDAQ")

    # r = requests.get(url)
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    site = "Google Finance:"

    t = 0
    with open("Stocks\ArticleGetter\GoogleLinks.txt", 'w') as f:
        while t < 10:
            links = []
            for link in soup.findAll('a'):
                links.append(link.get('href'))

            for link in links:
                if "https:" in str(link):
                    f.writelines(link)
                else:
                    pass
    f.close()

def get_MW_Articles(symbol):

    with open("Stocks\ArticleGetter\Files\\" +symbol+"MWLinks.txt", 'w') as f:
        f.truncate(0)

        url = ("https://www.marketwatch.com/investing/stock/"+symbol.lower()+"?mod=quote_search")

        global soup, site

        # r = requests.get(url)
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'lxml')
        # soup.prettify()

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
    
        

def get_Paragraphs(soup, site):

    with open("Stocks\ArticleGetter\Files\\"+symbol+"Bodies.txt", "w") as f:       
        f.truncate()
        for data in soup.findAll('p'):

            if "company" in str(data):
                f.writelines(site + ":\n\n")
                f.write(str(data.getText()))

                print(str(site) + ":\n\n")
                print(data.getText())
            else:
                pass
            # print(data.getText())
    f.close()

h = 0
while h < 10:

    symbol = input("Ticker: ").upper()

    # ask1 = input("Get Google Articles? (Y/N) : ")

    # if ask1 == "y" or ask1 == "Y" or ask1 =="yes" or ask1 == "Yes":
    #     get_Google_articles(symbol)
    #     get_Paragraphs
    # else:
    #     pass

    ask2 = input("Get MarketWatch Articles? (Y/N) : ")

    if ask2 == "y" or ask2 == "Y" or ask2 =="yes" or ask2 == "Yes":
        get_MW_Articles(symbol)
        get_Paragraphs(soup, site)
    else:
        pass


