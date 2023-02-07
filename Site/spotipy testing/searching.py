import spotipy
from spotipy.oauth2 import SpotifyOAuth


scope = 'user-top-read user-library-modify'
client_id = 'bd9c275a853c493ba51fdafefcb08578'
client_secret = 'ddf20a988de843b296a31d2e20e59d9d'
redirect_uri = 'http://localhost:8888/callback'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret,  redirect_uri=redirect_uri, scope=scope))



def get_artist():
    artist_in = input('Search for an artist: ')

    artist = sp.search(artist_in, type='artist', limit=1)  
    artist = artist['artists']['items'][0]
    id = artist['id']
    name = artist['name']
    images = artist['images']

    return id, name, images

def get_song():
    song_in = input('Search for a song: ')
    song = sp.search(song_in, type='track', limit=1, market='GB')
    # print(song['tracks']['items'][0])
    song = song['tracks']['items'][0]
    album = song['album']
    album_images = album['images']
    id = song['id']
    name = song['name']
    artist = (song['artists'][0]['id'], song['artists'][0]['name'])
    preview = song['preview_url']
    return id, name, artist, preview, album_images


def get_album():
    album_in = input('Search for an album: ')
    album = sp.search(album_in, type='album', limit=1, market='GB')
    album = album['albums']['items'][0]
    id = album['id']
    name = album['name']
    artist = (album['artists'][0]['id'], album['artists'][0]['name'])
    images = album['images']

    return id, name, artist, images

for item in get_song():
    print(item)

for item in get_album():
    print(item)