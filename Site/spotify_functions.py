import spotipy
from spotipy.oauth2 import SpotifyOAuth



"""scope is what the api is able to access about a user, list of scopes on 
https://developer.spotify.com/documentation/general/guides/authorization/scopes/"""
scope = scope = 'user-top-read, user-library-modify, ugc-image-upload, user-read-playback-state, app-remote-control, user-modify-playback-state, playlist-read-private, user-follow-modify, playlist-read-collaborative, user-follow-read'
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




def get_album_ids():
    #returns the id for all albums of a searched artist (50 maximum)
    artist_lookup = input("Search for an artist: ")
    artist = sp.search(artist_lookup, type="artist", limit=1, market="GB")
    artist_id = artist["artists"]["items"][0]["id"]
    albums = sp.artist_albums(artist_id, limit=50) #max 50
    album_ids = [album["id"] for album in albums["items"]]
    return album_ids

def get_album_name(album_id):
    #returns the name of an album given an album id
    album_name = sp.album(album_id)["name"]
    return album_name

def get_album_images(album_id):
    #returns the urls of the album images given an album id
    album_images = [image["url"] for image in sp.album(album_id)["images"]]
    return album_images

def get_album_songs(album_id):
    #return the track ids of the songs in an album based on album id
    songs = sp.album_tracks(album_id)
    track_ids = [song["id"] for song in songs["items"]]
    return track_ids

def get_track_title(track_id):
    #returns the song title given a track id
    song = sp.track(track_id)
    title = song["name"]
    return title

def get_track_preview(track_id):
    #returns the url of a track preview given a track id
    song = sp.track(track_id)
    preview = song["preview_url"]
    return preview

def get_track_image(track_id):
    # returns teh album image of a track given a track id
    album_image = sp.track(track_id)["album"]["images"][0]["url"]
    return album_image

def get_track_artist_name(track_id):
    #returns the artist name of the track
    song_name = sp.track(track_id)["artists"][0]["name"]
    return song_name

def get_spotify_link(track_id):
    #returns the spotify link of a song based on a track id
    song = sp.track(track_id)
    link = song["external_urls"]["spotify"]
    return link

def get_current_user_followed_artists():
    #returns a list artist ids of the artists folowed by the cuurent user (max 50)
    followed_artists_info = sp.current_user_followed_artists(limit=50, after=None)
    followed_artists = [artists["id"] for artists in followed_artists_info["artists"]["items"]]
    return followed_artists

def get_followed_artist_names(followed_artists):
    #returns a list names of the artists folowed by the cuurent user (max 50) given a list of artist ids
    artist_names = [sp.artist(artist)["name"] for artist in followed_artists]
    return artist_names

def get_artist_name(artist_id):
    #returns the name of an artist given an artist id
    artist_name = sp.artist(artist_id)["name"]
    return artist_name

def get_artist_images(artist_id):
    #returns a list of artist image urls in different fixed sizes given an artist id
    urls = [image["url"] for image in sp.artist(artist_id)["images"]]
    return urls

