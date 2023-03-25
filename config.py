from sys import platform

SPOT_GREEN = "#1DB954"
SPOT_BLACK = "#000000"
SPOT_WHITE = "#FFFFFF"
SPOT_RED = "#D30000"

SCALE = 0.2
LARGEFONT =("consolas", int(72 * SCALE))
MED_FONT =("consolas", int(52 * SCALE))
SMALL_FONT =("consolas", int(42 * SCALE))
UDP_IP = "127.0.0.1"
UDP_PORT = 9090

DIMENSIONS = "320x240"
DIVIDER_HEIGHT = 3

MENU_PAGE_SIZE = 6

SCREEN_TIMEOUT_SECONDS = 60

LINE_NORMAL = 0
LINE_HIGHLIGHT = 1
LINE_TITLE = 2

MENU_RENDER_TYPE = 0
ETH_PRICE_RENDER = 3

UP_KEY_CODE = 8255233 if platform == "darwin" else 116 
DOWN_KEY_CODE = 8320768 if platform == "darwin" else 111
LEFT_KEY_CODE = 8124162 if platform == "darwin" else 113
RIGHT_KEY_CODE = 8189699 if platform == "darwin" else 114
PREV_KEY_CODE = 2818092 if platform == "darwin" else 0
NEXT_KEY_CODE = 3080238 if platform == "darwin" else 0
PLAY_KEY_CODE = 3211296 if platform == "darwin" else 0