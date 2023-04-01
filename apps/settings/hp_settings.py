# Settings Menu for the hackP0d
# MIT / mplur.eth 2023
from apps.shared.hp_menupage import MenuPage
from apps.settings.subpages.settings_wifi import WifiPage

class SettingsPage(MenuPage):
    def __init__(self, previous_page):
        super().__init__("Settings", previous_page, has_sub_page=True)
        self.pages = [
            WifiPage(self, "Wi-Fi", WifiCommand())
           # EthPricePage(self, "ETH Price", EthPriceCommand()),
        ]
        self.index = 0
        self.page_start = 0
    
    def get_pages(self):
        # if (not spotify_manager.DATASTORE.now_playing):
        #    return self.pages[0:-1]
        return self.pages
    
    def total_size(self):
        return len(self.get_pages())

    def page_at(self, index):
        return self.get_pages()[index]

class WifiCommand():
    def __init__(self, runnable = lambda:()):
        self.has_run = False
        self.runnable = runnable
    
    def run(self):
        self.has_run = True
        self.runnable()
