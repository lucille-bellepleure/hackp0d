# Wifi discovery and setting the wifi network
from wifi import Cell, Scheme
from apps.shared.hp_menupage import MenuPage

class WifiPage(MenuPage):
    def __init__(self, previous_page):
        super().__init__("Wifi", previous_page, has_sub_page=True)
        print("change")
        self.pages = [
           # WifiPage(self, "Wifi")
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
