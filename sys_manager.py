import threading
import requests
import time
import os
import tradingview_ws
from tradingview_ta import TA_Handler, Interval, Exchange
from wifi import Cell, Scheme

has_internet = True
eth_price = {'symbol': 'ETHUSD', 'price': 0, 'prev_price': 0}
prev_price = 0

def callbackFunc(s):
    eth = TA_Handler(
        symbol="ETHUSDT",
        screener="crypto",
        exchange="COINBASE",
        interval=Interval.INTERVAL_4_HOURS
    )
    print(eth.get_analysis().summary)
    reco = eth.get_analysis().summary
    indicators = eth.get_analysis().indicators
    print(reco, type(reco))
    print(indicators['open'])
    print("Tradingview call back")
    global eth_price
    global prev_price
    s["prev_price"] = prev_price
    s["reco"] = reco['RECOMMENDATION']
    s["open"] = indicators['open']
    print(s)
    eth_price = s
    prev_price = s["price"]

def sub_eth_price():
    print("Creating the tradingview thing")

    # Example output: {"RECOMMENDATION": "BUY", "BUY": 8, "NEUTRAL": 6, "SELL": 3}
    pair = "ETHUSD"
    market = "crypto" # 'stock' | 'futures' | 'forex' | 'cfd' | 'crypto' | 'index' | 'economic'
    username = None
    password = None
    trading = tradingview_ws.TradingViewWs(pair, market, username, password)
    # get quote price
    trading.realtime_quote(callbackFunc)

def screen_sleep():
    global screen_on
    screen_on = False
    os.system('xset -display :0 dpms force off')

def screen_wake():
    global screen_on
    screen_on = True
    os.system('xset -display :0 dpms force on')

def check_internet(request):
    global has_internet
    try:
        result = request()
        has_internet = True
    except Exception as _:
        print("no ints")
        result = None
        has_internet = False
    return result

def get_wifi_networks():
    print(Cell.all('wlan0'))

get_price = threading.Thread(target=sub_eth_price, name="GetPrice")
get_price.start()

get_wifi = threading.Thread(target=get_wifi_networks, name="get_wifi")
get_wifi.start()