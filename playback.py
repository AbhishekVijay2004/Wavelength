import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import simpleaudio as sa
import requests
from pydub import AudioSegment

scope = "user-top-read"

load_dotenv()


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
did = '882877fdf0118bbe3c5761b3dc811c5192dd5324'
listening = sp.current_user_top_tracks(limit=2)
track = listening['items'][0]
preview_url = track['preview_url']

response = requests.get(preview_url)
open("preview.wav", "wb").write(response.content)

sound = AudioSegment.from_mp3("preview.wav")
sound.export("preview.wav", format="wav")

wave_obj = sa.WaveObject.from_wave_file("preview.wav")
play_obj = wave_obj.play()
play_obj.wait_done()
