import numpy as np
import pandas as pd
import pandas_datareader as pdr
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import json

symbol = input("Ticker: ").upper()

url = ("https://www.google.com/finance/quote/" + symbol + ":NASDAQ")

# r = requests.get(url)
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'html.parser')


links = []
for link in soup.findAll('a'):
    links.append(link.get('href'))

for link in links:
    if "https:" in str(link):
        print(link)
        print()
    else:
        pass

url = ("https://www.marketwatch.com/investing/stock/"+symbol.lower()+"?mod=quote_search")

# r = requests.get(url)
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'lxml')


links = []
for link in soup.findAll('a'):
    links.append(link.get('href'))

for link in links:
    if "https:" in str(link):
        print(link)
        print()
    else:
        pass