import numpy as np
import warnings
from pandas_datareader import data as pdr
import yfinance as yf
import datetime as dt
from yahoo_fin import stock_info as si
import pandas as pd
from csv import *
import time


pd.set_option('display.max_rows', None)
warnings.filterwarnings("ignore")
yf.pdr_override()

num_of_years = 1
start = dt.date.today() - dt.timedelta(days = int(365.25*num_of_years))
end = dt.date.today()


tickers = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'BNB-USD', 'ADA-USD']

dataset = pdr.get_data_yahoo(tickers, start, end)['Adj Close']

stocks_returns = np.log(dataset/dataset.shift(1))

# print('\nCorrelation Matrix')
corr_matrix = stocks_returns.corr()
# print (corr_matrix)

def get_redundant_pairs(df):
    pairs_to_drop = set()
    cols = df.columns
    for i in range(0, df.shape[1]):
        for j in range(0, i+1):
            pairs_to_drop.add((cols[i], cols[j]))
    return pairs_to_drop

def get_top_abs_correlations(df):
    au_corr = df.corr().abs().unstack()
    labels_to_drop = get_redundant_pairs(df)
    au_corr = au_corr.drop(labels=labels_to_drop).sort_values(ascending=False)
    FindCorrelations = au_corr.to_csv('Stocks\CorrelationTracker\StockFiles\CryptoCorrelations.csv')

    return au_corr

get_top_abs_correlations(stocks_returns)


print("\nTop Absolute Correlations")
df = pd.read_csv('Stocks\CorrelationTracker\StockFiles\CryptoCorrelations.csv')
print(df.loc[0:10,:])

