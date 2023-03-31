import tkinter as tk 
from sys import platform
import os
from config import *
from tools import *
import sys_manager
import socket
from select import select
import time
from apps.settings.hp_settings import SettingsPage
from apps.settings.subpages.settings_wifi import WifiPage, WifiFrame
from apps.shared.hp_menupage import Rendering, MenuPage
from apps.crypto.hp_crypto import EthPricePage, EthPriceFrame, EthPriceCommand
from apps.homepage.hp_homepage import StartFrame

class tkinterApp(tk.Tk): 
      
    # __init__ function for class tkinterApp  
    def __init__(self, *args, **kwargs):  
        # __init__ function for class Tk 
        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry(DIMENSIONS)
        self.configure(bg=SPOT_BLACK)

        if (platform == 'darwin'):
            self.geometry("320x240")
            SCALE = 0.3
        else:
            self.attributes('-fullscreen', True)
            SCALE = self.winfo_screenheight() / 930

        # creating a container 
        container = tk.Frame(self)   
        container.pack(side = "bottom", fill = "both", expand = True)  
        container.grid_rowconfigure(0, weight = 1) 
        container.grid_columnconfigure(0, weight = 1) 

        # initializing frames to an empty array 
        self.frames = {}   
   
        # iterating through a tuple consisting 
        # of the different page layouts 
        for F in (StartFrame, EthPriceFrame, WifiFrame): 
   
            frame = F(container, self) 
   
            # initializing frame of that object from 
            # startpage, page1, page2 respectively with  
            # for loop 
            self.frames[F] = frame  
   
            frame.grid(row = 0, column = 0, sticky ="nsew") 
   
        # self.show_frame(StartFrame) 

    def show_frame(self, cont): 
        frame = self.frames[cont] 
        frame.tkraise() 

# Scrollwheel stuff
def processInput(app, input, page):
    global wheel_position, last_button, last_interaction
    position = input[2]
    button = input[0]
    button_state = input[1]
    if button == 29 and button_state == 0:
        wheel_position = -1
    elif wheel_position == -1:
        wheel_position = position
    elif position % 2 != 0:
        pass
    elif wheel_position <=1 and position > 44:
        onDownPressed()
        wheel_position = position
    elif wheel_position >=44 and position < 1:
        onUpPressed()
        wheel_position = position
    elif abs(wheel_position - position) > 6:
        wheel_position = -1
    elif wheel_position > position:
        onDownPressed()
        wheel_position = position
    elif wheel_position < position:
        onUpPressed()
        wheel_position = position
    
    if button_state == 0:
        last_button = -1
    elif button == last_button:
        pass
    elif button == 7:
        onSelectPressed()
        last_button = button
    elif button == 11:
        onBackPressed()
        last_button = button
    elif button == 10:
        onPlayPressed()
        last_button = button
    elif button == 8:
        onNextPressed()
        last_button = button
    elif button == 9:
        onPrevPressed()
        last_button = button
    
    now = time.time()
    if (now - last_interaction > SCREEN_TIMEOUT_SECONDS):
        print("waking")
        sys_manager.screen_wake()
    last_interaction = now

def onKeyPress(event):
    c = event.keycode
    if (c == UP_KEY_CODE):
        onUpPressed()
    elif (c == DOWN_KEY_CODE):
        onDownPressed()
    elif (c == RIGHT_KEY_CODE):
        onSelectPressed()
    elif (c == LEFT_KEY_CODE):
        onBackPressed()
    elif (c == NEXT_KEY_CODE):
        onNextPressed()
    elif (c == PREV_KEY_CODE):
        onPrevPressed()
    elif (c == PLAY_KEY_CODE):
        onPlayPressed()
    else:
        print("unrecognized key: ", c)

def onPlayPressed():
    global page, app
    page.nav_play()
    render(app, page.render())
    
def onSelectPressed():
    global page, app
    if (not page.has_sub_page):
        return
    page.render().unsubscribe()
    page = page.nav_select()
    render(app, page.render())

def onBackPressed():
    global page, app
    previous_page = page.nav_back()
    if (previous_page):
        page.render().unsubscribe()
        page = previous_page
        render(app, page.render())
    
def onNextPressed():
    global page, app
    page.nav_next()
    render(app, page.render())

def onPrevPressed():
    global page, app
    page.nav_prev()
    render(app, page.render())

def onUpPressed():
    global page, app
    page.nav_up()
    render(app, page.render())

def onDownPressed():
    global page, app
    page.nav_down()
    render(app, page.render())

class RootPage(MenuPage):
    def __init__(self, previous_page):
        super().__init__("hackP0dR00t", previous_page, has_sub_page=True)
        print("change")
        self.pages = [
            EthPricePage(self, "ETH Price", EthPriceCommand()),
            SettingsPage(self)
        ]
        self.index = 0
        self.page_start = 0
    
    def get_pages(self):
        return self.pages
    
    def total_size(self):
        return len(self.get_pages())

    def page_at(self, index):
        return self.get_pages()[index]

def render_menu(app, menu_render):
    app.show_frame(StartFrame)
    page = app.frames[StartFrame]
    if(menu_render.total_count > MENU_PAGE_SIZE):
        page.show_scroll(menu_render.page_start, menu_render.total_count)
    else:
        page.hide_scroll()
    for (i, line) in enumerate(menu_render.lines):
        page.set_list_item(i, text=line.title, line_type = line.line_type, show_arrow = line.show_arrow) 
    page.set_header(menu_render.header, menu_render.now_playing, menu_render.has_internet)

def update_eth_price(eth_price):
    frame = app.frames[EthPriceFrame]
    frame.update_eth_price(eth_price)

def render_eth_price(app, eth_price_render):
    app.show_frame(EthPriceFrame)
    eth_price_render.subscribe(app, update_eth_price)

def update_wifi():
    frame = app.frames[WifiPage]
    frame.update_wifi()

def render_wifi(app, wifi_render):
    app.show_frame(WifiFrame)
    wifi_render.subscribe(app, update_wifi)

def render(app, render):
    if (render.type == MENU_RENDER_TYPE):
        render_menu(app, render)
    elif (render.type == ETH_PRICE_RENDER):
        render_eth_price(app, render)
    elif (render.type == WIFI_RENDER):
        render_wifi(app, render)

# Driver Code 
app = tkinterApp() 
app.overrideredirect(False)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
sock.setblocking(0)
socket_list = [sock]
loop_count = 0

page = RootPage(None)

def app_main_loop():
    global app, page, loop_count, last_interaction, screen_on

    try:
        read_sockets = select(socket_list, [], [], 0)[0]
        for socket in read_sockets:
            data = socket.recv(128)
            processInput(app, data, page)
        loop_count += 1
        if (loop_count >= 300):
            # print('start render')
          render(app, page.render())
            # loop_count = 0
    except:
        pass
    finally:
        app.after(2, app_main_loop)

app.bind('<KeyPress>', onKeyPress)
app.after(5, app_main_loop)
app.mainloop()