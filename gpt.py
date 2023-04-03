import tkinter as tk
import redis
import spotipy
import spotipy.util as util
import subprocess

# Set up redis client
r = redis.Redis(host='localhost', port=6379, db=0)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="user-library-read",
    client_id=os.environ.get('SPOTIPY_CLIENT_ID'),
    client_secret=os.environ.get('SPOTIPY_CLIENT_SECRET'),
    redirect_uri=os.environ.get('SPOTIPY_REDIRECT_URI'),
    cache_path=".cache",
))

# Set up raspotify subprocess
raspotify_process = subprocess.Popen(["sudo", "systemctl", "start", "raspotify"])

# Define function to get user's albums and store them in redis
def get_albums():
    results = sp.current_user_saved_albums()
    albums = results['items']
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    for album in albums:
        r.hset('albums', album['id'], album['name'])

# Define function to get tracks for an album and return them as a list
def get_tracks(album_id):
    results = sp.album_tracks(album_id)
    tracks = []
    for track in results['items']:
        tracks.append(track['name'])
    return tracks

# Define function to play a track on raspotify
def play_track(track_uri):
    subprocess.run(["sudo", "raspotify", "--uri", track_uri])

# Set up tkinter window
root = tk.Tk()
root.geometry("320x240")
root.configure(background='black')

# Set up font
font = ("Courier", 12)

# Define function to update menu
def update_menu(menu_title, menu_items):
    # Clear current menu
    for widget in root.winfo_children():
        widget.destroy()

    # Add title
    title_label = tk.Label(root, text=menu_title, fg="green", bg="black", font=font)
    title_label.pack(side="top")

    # Add menu items
    for item in menu_items:
        item_label = tk.Label(root, text=item, fg="green", bg="black", font=font)
        item_label.pack(side="top")

    # Add wifi icon
    wifi_icon = tk.Label(root, text="WIFI_ICON", fg="green", bg="black", font=font)
    wifi_icon.pack(side="right")

    # Refresh window
    root.update()

# Define function to handle menu selection
def handle_selection(selection):
    if selection == "settings":
        update_menu("SETTINGS", ["Option 1", "Option 2", "Option 3"])
    elif selection == "wallet":
        update_menu("WALLET", ["Balance: $100", "Deposit", "Withdraw"])
    elif selection == "music":
        update_menu("ALBUMS", list(r.hvals('albums')))
    elif selection == "phone":
        update_menu("PHONE", ["Dial", "Contacts", "Call History"])
    elif selection == "about":
        update_menu("ABOUT", ["Version 1.0", "Created by Me"])
    elif selection in r.hvals('albums'):
        album_id = r.hget('albums', selection)
        update_menu(selection.upper(), get_tracks(album_id))
    else:
        play_track(selection)

# Set up initial menu
menu_title = "MAIN MENU"
menu_items = ["SETTINGS", "WALLET", "MUSIC", "PHONE", "ABOUT"]
update_menu
