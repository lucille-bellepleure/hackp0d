import spotipy
from spotipy.oauth2 import SpotifyOAuth

def get_albums(username, cache_path, client_id, client_secret, redirect_uri):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(username=username, cache_path=cache_path, client_id=client_id,
                                                   client_secret=client_secret, redirect_uri=redirect_uri))

    # Get user's albums
    results = sp.current_user_saved_albums()

    # Extract album info from response
    albums = []
    for item in results['items']:
        album = item['album']
        albums.append({'name': album['name'], 'id': album['id']})

    return albums


def get_album_tracks(username, cache_path, client_id, client_secret, redirect_uri, album_id):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(username=username, cache_path=cache_path, client_id=client_id,
                                                   client_secret=client_secret, redirect_uri=redirect_uri))

    # Get tracks from album
    results = sp.album_tracks(album_id)

    # Extract track info from response
    tracks = []
    for item in results['items']:
        tracks.append({'name': item['name'], 'uri': item['uri']})

    return tracks
