import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Replace these with your own values
SPOTIPY_CLIENT_ID = ''
SPOTIPY_CLIENT_SECRET = ''
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'

# Set the necessary scope for playback control
scope = 'user-modify-playback-state,user-read-playback-state,streaming'

last_device = ''

def create_spotify():
    auth_manager = SpotifyOAuth(
        scope=scope,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET)

    spotify = spotipy.Spotify(auth_manager=auth_manager)

    return auth_manager, spotify

def refresh_spotify(auth_manager, spotify):
    token_info = auth_manager.cache_handler.get_cached_token()
    if auth_manager.is_token_expired(token_info):
        auth_manager, spotify = create_spotify()
    return auth_manager, spotify


auth_manager, spotify = create_spotify()

print(spotify.devices())

def get_current_device_id():
    global last_device
    devices = spotify.devices()
    for device in devices.get('devices', []):
        if device.get('is_active', False):
            last_device = device.get('id', None)
            return device.get('id', None)

    return last_device

print(get_current_device_id())

device_id = get_current_device_id()

def play():
    global auth_manager
    global spotify
    auth_manager, spotify = refresh_spotify(auth_manager, spotify)
    spotify.start_playback(device_id)

def pause():
    global auth_manager
    global spotify
    auth_manager, spotify = refresh_spotify(auth_manager, spotify)
    spotify.pause_playback(device_id)

def next_track():
    global auth_manager
    global spotify
    auth_manager, spotify = refresh_spotify(auth_manager, spotify)
    spotify.next_track(device_id)

def previous_track():
    global auth_manager
    global spotify
    auth_manager, spotify = refresh_spotify(auth_manager, spotify)
    spotify.start_playback(device_id)

def search_play(list):
    global auth_manager
    global spotify
    auth_manager, spotify = refresh_spotify(auth_manager, spotify)

    song = list[0]
    artist = list[1]

    if artist == None:
        searchResults = spotify.search(q=f"{song}", type="track", limit=1)

    else:
        searchResults = spotify.search(q=f"{song} {artist}", type="track", limit=1)

    print(searchResults)


    if searchResults['tracks']['items']:
        track_uri = searchResults['tracks']['items'][0]['uri']


        spotify.add_to_queue(uri=track_uri)
        spotify.next_track(device_id)
        print("good")
        return
    print("bad")




