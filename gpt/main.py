import os
from dotenv import load_dotenv

from api import get_albums, get_album_tracks
from gui import Menu

load_dotenv()  # Load environment variables from .env file

if __name__ == '__main__':
    menu = Menu()
    menu.add_item('settings')
    menu.add_item('wallet')
    menu.add_item('music')
    menu.add_item('phone')
    menu.add_item('about')

    # Get Spotify albums
    albums = get_albums(os.getenv('SPOTIPY_USERNAME'), os.getenv('SPOTIPY_CACHE_PATH'), os.getenv('SPOTIPY_CLIENT_ID'),
                        os.getenv('SPOTIPY_CLIENT_SECRET'), os.getenv('SPOTIPY_REDIRECT_URI'))

    # Add albums as sub-menu of music
    music_submenu = Menu()
    for album in albums:
        music_submenu.add_item(album['name'], album['id'])

    menu.add_submenu('music', music_submenu)

    # Run menu
    menu.run()
