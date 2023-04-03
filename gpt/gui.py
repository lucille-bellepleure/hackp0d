import tkinter as tk
from tkinter import font
import subprocess
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

class Menu:
    def __init__(self):
        self.root = tk.Tk()
        self.root.configure(bg='black')
        self.root.attributes('-fullscreen', True)
        self.root.bind('<Escape>', lambda e: self.root.quit())

        self.menu_frame = tk.Frame(self.root, bg='black', bd=0)
        self.menu_frame.pack(side='left', fill='both', expand=True)

        self.current_submenu = None
        self.select_callback = None

        self.menu_items = []

        self.selected_item = tk.StringVar()
        self.selected_item.set('')
        self.selected_index = -1

        self.font_family = 'Courier New'
        self.font_size = 18
        self.highlight_bg = 'green'
        self.highlight_fg = 'black'
        self.default_fg = 'green'
        self.default_bg = 'black'
        self.header_text = 'iPod Menu'

        self.load_font()

    def load_font(self):
        self.font = font.Font(family=self.font_family, size=self.font_size)

    def add_item(self, label, value=None):
        item =
