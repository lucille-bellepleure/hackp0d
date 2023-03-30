# Settings Menu for the hackP0d
# MIT / mplur.eth 2023
import tkinter as tk 
from config import *
from tools import *
import sys_manager
from apps.shared.hp_menupage import Rendering

class EthPriceFrame(tk.Frame): 
    def __init__(self, parent, controller):  
        tk.Frame.__init__(self, parent) 
        self.prevprice = 0
        self.inflated = False
        self.active = False
        self.update_time = False
        self.configure(bg=SPOT_BLACK)
        self.header_label = tk.Label(self, text ="ETHUSDT", font = LARGEFONT, background=SPOT_BLACK, foreground=SPOT_GREEN) 
        self.header_label.grid(sticky='we', padx=(0, 10))
        self.grid_columnconfigure(0, weight=1)
        divider = tk.Canvas(self)
        divider.configure(bg=SPOT_GREEN, height=DIVIDER_HEIGHT, bd=0, highlightthickness=0, relief='ridge')
        divider.grid(row = 1, column = 0, sticky ="we", pady=10, padx=(10, 30))
        contentFrame = tk.Canvas(self, bg=SPOT_BLACK, highlightthickness=0, relief='ridge')
        contentFrame.grid(row = 2, column = 0, sticky ="nswe")
        contentFrame.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.price_price = tk.Label(contentFrame, text="0", font = LARGEFONT, background=SPOT_GREEN, foreground=SPOT_BLACK)
        self.price_price.grid(row=1, column=0,sticky ="we", padx=(30, 50))
        self.open_label = tk.Label(contentFrame, text="open", font = MED_FONT, background=SPOT_BLACK, foreground=SPOT_GREEN)
        self.open_label.grid(row=2, column=0,sticky ="we", padx=(30, 50))
        self.price_reco = tk.Label(contentFrame, text ="reco", font = LARGEFONT, background=SPOT_BLACK, foreground=SPOT_GREEN) 
        self.price_reco.grid(row=3, column=0,sticky ="we", padx=(10, 30))
        
    def update_eth_price(self, eth_price):
        ethprice = eth_price['price']
        prev_price = eth_price['prev_price']
        open_price = eth_price['open']
        # ethchange = eth_price['percent_change_1h']
        # ethvolume = eth_price['volume_24h']
        ethprice_formatted = "{:.2f}".format(ethprice)
        if open_price >= ethprice:
            bgcolor = SPOT_RED
        else: 
            bgcolor = SPOT_GREEN

        self.price_reco.configure(text=eth_price["reco"])
        self.price_price.configure(text=ethprice_formatted, background=bgcolor)
        self.open_label.configure(text=('OPEN: ' + str(open_price)))
        return

class EthPriceRendering(Rendering):
    def __init__(self):
        super().__init__(ETH_PRICE_RENDER)
        self.callback = None
        self.after_id = None

    def subscribe(self, app, callback):
        if callback == self.callback:
            return
        new_callback = self.callback is None
        self.callback = callback
        self.app = app
        if new_callback:
            self.refresh()

    def refresh(self):
        if not self.callback:
            return
        if self.after_id:
            self.app.after_cancel(self.after_id)
        self.callback(sys_manager.eth_price)
        self.after_id = self.app.after(500, lambda: self.refresh())

    def unsubscribe(self):
        super().unsubscribe()
        self.callback = None
        self.app = None

class EthPriceCommand():
    def __init__(self, runnable = lambda:()):
        self.has_run = False
        self.runnable = runnable
    
    def run(self):
        self.has_run = True
        self.runnable()

class EthPricePage():
    def __init__(self, previous_page, header, command):
        self.has_sub_page = True
        self.previous_page = previous_page
        self.command = command
        self.header = header
        self.live_render = EthPriceRendering()
        self.is_title = False

    def nav_back(self):
        return self.previous_page

    def render(self):
        if (not self.command.has_run):
            self.command.run()
        return self.live_render
