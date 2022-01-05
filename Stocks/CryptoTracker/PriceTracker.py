import requests
from datetime import datetime
import time
from requests.api import get

from requests.models import Response

# 'https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,JPY,EUR'
# you can add international currencies by appending them to the url ^^^^^
URL = 'https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD'

def get_price(coin, currency):
    try:
        response = requests.get(URL.format(coin,currency)).json()
        return response

    except:
        return False



curr = str(input("Currency: ").upper())

curr_file = open("F:\Projects\Quantv2\Stocks\CryptoTracker\\" + curr + ".txt", "w")


i = 0
while i < 10:
    date_time = datetime.now()
    date_time = date_time.strftime("%d/%m/%Y %H:%M:%S")

    current_price = get_price(curr, "USD")
    if current_price:
        price_info = str(date_time)+ "$"+ str(current_price)
        curr_file.write(price_info)
        print(price_info)
        time.sleep(5)
    i + 1
