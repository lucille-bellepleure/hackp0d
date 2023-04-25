import spotipy
from spotipy.oauth2 import SpotifyOAuth
import redis
import pickle

r = redis.Redis(host="localhost", port=6379, db=0)

def cleardb():
    r.flushdb()

# cleardb()

scope = "user-follow-read," \
        "user-library-read," \
        "user-library-modify," \
        "user-modify-playback-state," \
        "user-read-playback-state," \
        "user-read-currently-playing," \
        "app-remote-control," \
        "playlist-read-private," \
        "playlist-read-collaborative," \
        "playlist-modify-public," \
        "playlist-modify-private," \
        "streaming"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

class UserTrack():
    __slots__ = ['title', 'artist', 'album', 'uri']
    def __init__(self, title, artist, album, uri):
        self.title = title
        self.artist = artist
        self.album = album
        self.uri = uri

    def __str__(self):
        return self.title + " - " + self.artist + " - " + self.album

class UserAlbum():
    __slots__ = ['name', 'artist', 'track_count', 'uri']
    def __init__(self, name, artist, track_count, uri):
        self.name = name
        self.artist = artist
        self.uri = uri
        self.track_count = track_count

    def __str__(self):
        return self.name + " - " + self.artist

def parse_album(album):
    artist = album['artists'][0]['name']
    tracks = []
    if 'tracks' not in album :
        return get_album(album['id'])
    for _, track in enumerate(album['tracks']['items']):
        tracks.append(UserTrack(track['name'], artist, album['name'], track['uri']))
    return (UserAlbum(album['name'], artist, len(tracks), album['uri']), tracks)

def get_album_list():
    index = -1
    results = sp.current_user_saved_albums()
    while(results['next']):
        for item in enumerate(results['items']):
            album, tracks = parse_album(item[1]['album'])
            album_id = album.uri.split(":")[-1]
            r.set("album-uri:"+str(album_id), pickle.dumps(album))
            r.set("playlist-tracks:"+str(album_id), pickle.dumps(tracks))
        results = sp.next(results)
 
print("Refreshing Albums", get_album_list())

def getPlaylistTracks(id):
    pickled_pl = r.get("playlist-tracks:"+str(id))
    if (pickled_pl is None):
        return None
    return pickle.loads(pickled_pl)

def getSavedTrack(index):
    pickled_pl = r.get("track:"+str(index))
    return pickle.loads(pickled_pl)

def get_db_albums():
    return list(r.keys("album-uri:*"))

def get_db_album(uri):
    pickled_pl = r.get("album-uri:"+str(uri))
    if (not pickled_pl):
        return None
    return pickle.loads(pickled_pl)

albums = get_db_albums()

print("These are your albums:")

for album in albums:
    album_decode = album.decode('utf-8')
    album_id = album_decode.split(":")[-1]
    print(album_id)
    album_item = get_db_album(album_id)
    print(album_item)

print("example of one album")

print(getPlaylistTracks("78JSLGBEpOP2pGkxRHGzvs"))