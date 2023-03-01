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
    images = []
    titles = []
    artists = []
    ids = []
    for song in songs:
        album = song['album']
        titles.append(song['name'])
        ids.append(song['id'])
        #name of the artist
        artists.append(song['artists'][0]['name'])
        #get 64x64 album image
        images.append(album['images'][2]['url'])
        # songs_out.append({'id': id, 'name': name, 'artist': artist, 'image':album_image})
    return images, titles, artists, ids


for thing in song_searching('star'):
    print(thing)

#array of images 
# array of titles
# array of artists
# array of song id