from GetArticles import *

def get_Ticker_info():

    symbols = []

    get_symbols()
    

    
    for symbol in symbols:
        single_ticker_Analysis(symbol)
        report(symbol)
        get_MW_Articles(symbol)
        get_Paragraphs()
        print_Articles()

get_Ticker_info()