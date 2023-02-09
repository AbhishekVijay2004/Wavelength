import spotipy
from spotipy.oauth2 import SpotifyOAuth



"""scope is what the api is able to access about a user, list of scopes on 
https://developer.spotify.com/documentation/general/guides/authorization/scopes/"""
scope = 'user-top-read user-library-modify'
#client and secret ids passed to api
#ids of the website not of the individual user
client_id = 'bd9c275a853c493ba51fdafefcb08578'
client_secret = 'ddf20a988de843b296a31d2e20e59d9d'
#kind of nothing website for now
#where it goes to if the spotify log in doesn't call
#should be our actual website when done
redirect_uri = 'http://localhost:8888/callback'

#create a spotify object allowing us to access the apii
# has the authorisation code flow authetification method
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret,  redirect_uri=redirect_uri, scope=scope))



def get_artist():
    artist_in = input('Search for an artist: ')
    #return the first artist found based no the search query
    artist = sp.search(artist_in, type='artist', limit=1)  
    artist = artist['artists']['items'][0]
    id = artist['id']
    name = artist['name']
    images = artist['images']

    return id, name, images

def get_song():
    song_in = input('Search for a song: ')
    #return first song based on query, specified to gb market
    song = sp.search(song_in, type='track', limit=10, market='GB')
    # print(song['tracks']['items'][0])
    song = song['tracks']['items'][0]
    album = song['album']
    album_images = album['images']
    id = song['id']
    name = song['name']
    artist = (song['artists'][0]['id'], song['artists'][0]['name'])
    preview = song['preview_url']
    return id, name, artist, preview, album_images

def song_searching(query):
    #return the song based on query
    song = sp.search(query, type='track', limit=5, market='GB')
    song = song['tracks']['items'][0]
    album = song['album']
    name = song['name']
    id = song['id']
    artist = song['artists'][0]['name']
    album_image = album['images'][2]['url']
    return id, name, artist, album_image


def get_album():
    album_in = input('Search for an album: ')
    #return first album found in gb market for the search query
    album = sp.search(album_in, type='album', limit=1, market='GB')
    album = album['albums']['items'][0]
    id = album['id']
    name = album['name']
    artist = (album['artists'][0]['id'], album['artists'][0]['name'])
    images = album['images']

    return id, name, artist, images

print(song_searching('professor x'))