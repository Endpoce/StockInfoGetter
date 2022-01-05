import ibapi
from ibapi.client import EClient
from ibapi.wrapper import EWrapper

from ibapi.contract import Contract
from ibapi.order import *
import threading
import time

#vars

#class for IB connection
class IBApi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def realtimeBar(self, reqId, time, open_, high, low, close, volume, wap, count):
        super().realtimeBar(reqId, time, open_, high, low, close, volume, wap, count)
        try:
            bot.on_Bar_Update(reqId, time, open_, high, low, close, volume, wap, count)
        except Exception as e:
            print(e)
        
    def error(self, id, erroCode, erroMsg):
        print(erroCode)
        print(erroMsg)

    


#Bot logic
class Bot():

    ib = None
    
    def __init__(self):
        ib = IBApi()
        ib.connect("127.0.0.1", 7497,1)
        ib.run()
        ib_thread = threading.Thread(target=self.run_loop, daemon=True)
        ib_thread.start()
        time.sleep(3)
        symbol = input("Enter symbold you want to trade : ")
        #create contract object / must have
        contract = Contract()
        contract.symbol = symbol.upper()
        contract.secType = "STk"
        contract.exchange = "SMART"
        contract.currency = "USD"
        # request market data
        self.ib.reqRealTimeBars(0, contract, 5, "TRADES", 1, [])

    def run_loop(self):
        self.ib.run()
    
    def on_Bar_Update(self, reqId, time, open_, high, low, close, volume, wap, count):
        print(reqId)


#start bot
bot = Bot()
