import os
import redis
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import subprocess

# Initialize Redis client
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Spotify API credentials
SPOTIPY_CLIENT_ID = os.environ['SPOTIPY_CLIENT_ID']
SPOTIPY_CLIENT_SECRET = os.environ['SPOTIPY_CLIENT_SECRET']
SPOTIPY_REDIRECT_URI = os.environ['SPOTIPY_REDIRECT_URI']

# Initialize Spotipy client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI))

# Define album list function
def get_album_list():
    # Check Redis cache for saved albums
    if redis_client.exists('spotify_albums'):
        album_list = redis_client.lrange('spotify_albums', 0, -1)
        album_list = [album.decode('utf-8') for album in album_list]
    else:
        # If no saved albums, query Spotify API and save results to Redis
        results = sp.current_user_saved_albums()
        album_list = [item['album']['name'] for item in results['items']]
        redis_client.rpush('spotify_albums', *album_list)

    return album_list

# Define track list function
def get_track_list(album_name):
    # Check Redis cache for saved tracks
    if redis_client.exists(f'spotify_tracks:{album_name}'):
        track_list = redis_client.lrange(f'spotify_tracks:{album_name}', 0, -1)
        track_list = [track.decode('utf-8') for track in track_list]
    else:
        # If no saved tracks, query Spotify API and save results to Redis
        results = sp.search(q=f'album:{album_name}', type='track', limit=50)
        track_list = [item['name'] for item in results['tracks']['items']]
        redis_client.rpush(f'spotify_tracks:{album_name}', *track_list)

    return track_list

# Define function to play a track on raspotify
def play_track(track_name):
    cmd = f'raspotify play -t "{track_name}"'
    subprocess.run(cmd, shell=True)


# Define menu items
menu_items = [
    "Now Playing",
    "Albums",
    "Quit"
]

# Define menu header
menu_header = "Spotify"

# Define wifi icon
wifi_icon = "  WIFI ICON HERE"

# Define font
font = "Computer_Terminal.ttf"

# Initialize menu selection
menu_selection = 0

# Run menu loop
while True:
    # Clear the screen
    os.system('clear')

    # Print the menu header
    print(menu_header + wifi_icon)

    # Print the menu items
    for i, item in enumerate(menu_items):
        if i == menu_selection:
            print(f"\033[32m{item}\033[0m")
        else:
            print(item)

    # Wait for user input
    keypress = input()

    # Process user input
    if keypress == "up":
        menu_selection -= 1
        if menu_selection < 0:
            menu_selection = len(menu_items) - 1
    elif keypress == "down":
        menu_selection += 1
        if menu_selection == len(menu_items):
            menu_selection = 0
    elif keypress == "select":
        if menu_items[menu_selection] == "
