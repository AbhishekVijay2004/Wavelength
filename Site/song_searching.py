import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = 'bd9c275a853c493ba51fdafefcb08578'
client_secret = 'ddf20a988de843b296a31d2e20e59d9d'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def song_searching(query):
    #return the song based on query
    song = sp.search(query, type='track', limit=5, market='GB')
    songs = song['tracks']['items']
    songs_out = []
    for song in songs:
        album = song['album']
        name = song['name']
        id = song['id']
        #name of the artist
        artist = song['artists'][0]['name']
        #get 64x64 album image
        album_image = album['images'][2]['url']
        songs_out.append({'id': id, 'name': name, 'artist': artist, 'image':album_image})
    return songs_out
