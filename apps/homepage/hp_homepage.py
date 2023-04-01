# Settings Menu for the hackP0d
# MIT / mplur.eth 2023
import tkinter as tk 
from config import *
from tools import *
from PIL import ImageTk, Image

class StartFrame(tk.Frame): 
    def __init__(self, parent, controller):  
        tk.Frame.__init__(self, parent) 
        self.green_arrow_image = ImageTk.PhotoImage(flattenAlpha(Image.open('images/pod_arrow_grn.png')))
        self.black_arrow_image = ImageTk.PhotoImage(flattenAlpha(Image.open('images/pod_arrow_blk.png')))
        self.empty_arrow_image = ImageTk.PhotoImage(flattenAlpha(Image.open('images/pod_arrow_empty.png')))
        self.play_image = ImageTk.PhotoImage(flattenAlpha(Image.open('images/pod_play.png')))
        self.pause_image = ImageTk.PhotoImage(flattenAlpha(Image.open('images/pod_pause.png')))
        self.space_image = ImageTk.PhotoImage(flattenAlpha(Image.open('images/pod_space.png')))
        self.wifi_image = ImageTk.PhotoImage(flattenAlpha(Image.open('images/hackpod_wifi.png')))
        self.configure(bg=SPOT_BLACK)
        header_container = tk.Canvas(self, bg=SPOT_BLACK, highlightthickness=0, relief='ridge')
        header_container.grid(sticky='we')
        self.header_label = tk.Label(header_container, text ="hackerz", font = LARGEFONT, background=SPOT_BLACK, foreground=SPOT_GREEN) 
        self.header_label.grid(sticky='we', column=1, row=0, padx=(0, 10))
        self.play_indicator = tk.Label(header_container, image=self.space_image, background=SPOT_BLACK)
        self.play_indicator.grid(sticky='w', column=0, row=0, padx=(70 * SCALE,0))
        self.wifi_indicator = tk.Label(header_container, image=self.space_image, background=SPOT_BLACK)
        self.wifi_indicator.grid(sticky='w', column=2, row=0, padx=(0,90 * SCALE))
        header_container.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        divider = tk.Canvas(self)
        divider.configure(bg=SPOT_GREEN, height=DIVIDER_HEIGHT, bd=0, highlightthickness=0, relief='ridge')
        divider.grid(row = 1, column = 0, sticky ="we", pady=10, padx=(10, 30))
        contentFrame = tk.Canvas(self, bg=SPOT_BLACK, highlightthickness=0, relief='ridge')
        contentFrame.grid(row = 2, column = 0, sticky ="nswe")
        self.grid_rowconfigure(2, weight=1)
        listFrame = tk.Canvas(contentFrame)
        listFrame.configure(bg=SPOT_BLACK, bd=0, highlightthickness=0)
        listFrame.grid(row=0, column=0, sticky="nsew")
        contentFrame.grid_rowconfigure(0, weight=1)
        contentFrame.grid_columnconfigure(0, weight=1)

        # scrollbar 
        self.scrollFrame = tk.Canvas(contentFrame)
        self.scrollFrame.configure(bg=SPOT_BLACK, width=int(50 * SCALE), bd=0, highlightthickness=4, highlightbackground=SPOT_GREEN)
        self.scrollBar = tk.Canvas(self.scrollFrame, bg=SPOT_GREEN, highlightthickness=0, width=int(20 * SCALE))
        self.scrollBar.place(in_=self.scrollFrame, relx=.5,  y=int(10 * SCALE), anchor="n", relwidth=.6, relheight=.9)
        self.scrollFrame.grid(row=0, column=1, sticky="ns", padx=(0, 30), pady=(0, 10))
        
        self.listItems = []
        self.arrows=[]

        for x in range(6):
            item = tk.Label(listFrame, text =" " + str(x), justify=tk.LEFT, anchor="w", font = LARGEFONT, background=SPOT_BLACK, foreground=SPOT_GREEN, padx=(30 * SCALE))
            imgLabel = tk.Label(listFrame, image=self.green_arrow_image, background=SPOT_BLACK)
            imgLabel.image = self.green_arrow_image
            imgLabel.grid(row=x, column=1, sticky="nsw", padx = (0, 30))
            item.grid(row = x, column = 0, sticky="ew",padx = (10, 0))
            self.listItems.append(item)
            self.arrows.append(imgLabel)
        listFrame.grid_columnconfigure(0, weight=1)
        # listFrame.grid_columnconfigure(1, weight=1)
    
    def show_scroll(self, index, total_count):
        scroll_bar_y_rel_size = max(0.9 - (total_count - MENU_PAGE_SIZE) * 0.06, 0.03)
        scroll_bar_y_raw_size = scroll_bar_y_rel_size * self.scrollFrame.winfo_height()
        percentage = index / (total_count - 1)
        offset = ((1 - percentage) * (scroll_bar_y_raw_size + int(20 * SCALE))) - (scroll_bar_y_raw_size + int(10 * SCALE))
        self.scrollBar.place(in_=self.scrollFrame, relx=.5, rely=percentage, y=offset, anchor="n", relwidth=.66, relheight=scroll_bar_y_rel_size)
        self.scrollFrame.grid(row=0, column=1, sticky="ns", padx=(0, 30), pady=(0, 10))

    def hide_scroll(self):
        self.scrollFrame.grid_forget()

    def set_header(self, header, now_playing = None, has_wifi = False):
        truncd_header = header if len(header) < 20 else header[0:17] + "..."
        self.header_label.configure(text=truncd_header)
        wifi_image = self.wifi_image if has_wifi else self.space_image
        self.wifi_indicator.configure(image = wifi_image)
        self.wifi_indicator.image = wifi_image
    
    def set_list_item(self, index, text, line_type = LINE_NORMAL, show_arrow = False):
        bgColor = SPOT_GREEN if line_type == LINE_HIGHLIGHT else SPOT_BLACK
        txtColor = SPOT_BLACK if line_type == LINE_HIGHLIGHT else \
            (SPOT_GREEN if line_type == LINE_NORMAL else SPOT_WHITE)
        truncd_text = text if len(text) < 17 else text[0:15] + "..."
        self.listItems[index].configure(background=bgColor, foreground=txtColor, text=truncd_text)
        arrow = self.arrows[index]
        arrow.grid(row=index, column=1, sticky="nsw", padx = (0, 30))
        arrowImg = self.empty_arrow_image if not show_arrow else \
            (self.black_arrow_image if line_type == LINE_HIGHLIGHT else self.green_arrow_image)
        arrow.configure(background=bgColor, image=arrowImg)
        arrow.image = arrowImg
