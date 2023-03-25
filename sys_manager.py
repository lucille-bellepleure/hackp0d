import threading
import requests
import time
import os

has_internet = True
prev_price = 0

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

def get_eth_price(data = None):
    global prev_price
    global eth_price
    res = requests.get(
        f"https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest?CMC_PRO_API_KEY=10bc11b8-4a12-43fe-8000-8503b984243f&symbol=ETH"
    )
    if res.status_code == 200:
        res = res.json()
        token = res['data']['ETH'][0]['quote']['USD']
        change = token['percent_change_1h']
        price = token['price']
        token['prev_price'] = prev_price
        assert len(res) != 0, "Nothing Found."
    else:
        print("Network Error!")
        exit(1)

    if (not token):
        return None
    else:
        prev_price = price
        print("token: ", token)
        eth_price = token
        has_internet = True
        return token

def bg_crypto_loop():
    global sleep_time
    while True:
        # refresh_now_playing()
        get_eth_price()
        time.sleep(sleep_time)
        sleep_time = min(12, sleep_time * 20)

sleep_time = 0.3
thread = threading.Thread(target=bg_crypto_loop, args=())
thread.daemon = True                            # Daemonize thread
thread.start()

def run_async(fun):
    threading.Thread(target=fun, args=()).start()