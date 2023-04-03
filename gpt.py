import subprocess
import redis
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Initialize Redis connection
redis_conn = redis.Redis(host='localhost', port=6379, db=0)

# Initialize Spotify connection
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-library-read"))

# Main menu function
def menu(items, title):
    while True:
        print("\033[2J")  # Clear screen
        print("\033[1;32;40m", title, "\033[0m\n")  # Header
        for i, item in enumerate(items):
            if i == 0:
                print("\033[1;32;40m>\033[0m", item)
            else:
                print(" ", item)
        keypress = input("\nUse arrow keys to scroll, press enter to select\n")
        if keypress == "\x1b[A":  # Up arrow
            items = items[-1:] + items[:-1]
        elif keypress == "\x1b[B":  # Down arrow
            items = items[1:] + items[:1]
        elif keypress == "\r":  # Enter key
            return items[0]

# Get user's saved albums from Spotify API
albums = sp.current_user_saved_albums(limit=50)["items"]

# Add album names to Redis database
for album in albums:
    redis_conn.lpush("albums", album["album"]["name"])

# Main loop
while True:
    menu_items = ["albums", "artists", "playlists", "settings", "power off"]
    menu_item = menu(menu_items, "iPod Menu")
    if menu_item == "albums":
        album_names = redis_conn.lrange("albums", 0, -1)
        album_choice = menu(album_names, "Albums")
        if album_choice is not None:
            album_tracks = sp.album_tracks(album_choice.decode("utf-8"))
            track_names = [track["name"] for track in album_tracks["items"]]
            track_choice = menu(track_names, album_choice.decode("utf-8"))
            if track_choice is not None:
                track_uri = album_tracks["items"][track_choice]["uri"]
                subprocess.call(["raspotify", "-p", track_uri])
    elif menu_item == "artists":
        pass  # TODO: Implement artist browsing
    elif menu_item == "playlists":
        pass  # TODO: Implement playlist browsing
    elif menu_item == "settings":
        pass  # TODO: Implement settings menu
    elif menu_item == "power off":
        break

print("Goodbye!")
