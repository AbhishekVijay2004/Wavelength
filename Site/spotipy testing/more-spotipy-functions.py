import spotipy
from spotipy.oauth2 import SpotifyOAuth

username= '	31nnar4zwyfy6pklbisp2qqo23ua'
redirect_uri= 'http://localhost:3000/'
client_id = "a62a9af9f04a479d8bbcb8dec52120cf"
client_secret = "bbf668b140b5428ba215b30fdf0ea6bd"
scope = "user-library-read, user-read-playback-state, user-follow-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret= client_secret, redirect_uri= redirect_uri, scope=scope))


def get_followed_artists():
    # gets the first 50 followed artists and returns artist names
    followed_array = []
    response = sp.current_user_followed_artists(limit=50, after=None)
    for artist in response['artists']['items']:
       followed_array.append(artist['name']) 
    return followed_array


def get_top_artists():
    #gets top 10 artists and returns artist names
    array = []
    response= sp.current_user_top_artists(limit=10, offset=0, time_range='medium_term')
    for i, item in enumerate(response['items']):
            array.append(item['name'])
    return array


def get_top_tracks():
    #gets top 5 tracks of the user
    tracks=[]
    response= sp.current_user_top_tracks(limit=5, offset=0, time_range='medium_term')
    for i, item in enumerate(response['items']):
        tracks.append(item['name'])
    return tracks



