from flask import Flask, render_template, url_for, redirect, request, session
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv




app = Flask(__name__)
app.secret_key = "abhishek"
app.use_static = True

scope = "user-top-read"

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

@app.route('/')
def index():
    if "username" in session:
        return redirect(url_for('home'))
    else:
        return render_template('signIn.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/friends')
def friends():
    return render_template('friends.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/post')
def post():
    return render_template('newPost.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/creation')
def creation():
    return render_template('creation.html')

@app.route('/login', methods = ['GET', 'POST'] )
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session["username"] = username

        print(username, password)

    return redirect(url_for('home'))

@app.route('/logout', methods = ['GET', 'POST'] )
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug = True)



'''
@app.route('/song', methods=['POST'])
def play_song():
    song_name = request.form['song_name']
    results = sp.search(q=song_name, type='track', limit=1, market='GB')
    track = results['tracks']['items'][0]
    preview_url = track['preview_url']
    return render_template('index.html', song_preview = preview_url)'''
