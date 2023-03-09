from flask import Flask, render_template, url_for, redirect, request, session, jsonify, flash
import spotipy, re
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# # ------- Variables for testing -------
# # ------- Remove once DB synced -------

email = "Email not linked"
username = "Username not linked"
display_name = "Display name not linked"
bio = "Bio not linked"
top_song = "Top song not linked"

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
        return redirect(url_for('signon'))

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/friends')
def friends():
    return render_template('friends.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/settings')
def settings():
    return render_template('settings.html', email=email, username=username, display_name=display_name, bio=bio, top_song=top_song)

@app.route('/post')
def post():
    return render_template('new-post.html')

@app.route('/signon')
def signon():
    return render_template('login.html')

@app.route('/login', methods = ['GET', 'POST'] )
def login():
    global email, username, password
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if (len(username) < 1):
            flash("Not a valid username", category="error")
            print("Error")
        elif (len(password) < 1):
            flash("Password must be over 1 character", category="error")
            print("Error")
        else:
            session["username"] = username

            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            if (re.search(regex,username)):
                email = username
            else:
                email = email

            print(f"Email: {email}, Username: {username}, Password: {password}")
            return redirect(url_for('home'))

    return redirect(url_for('signon'))

@app.route('/logout', methods = ['GET', 'POST'] )
def logout():
    session.pop('username', None)
    return redirect(url_for('signon'))

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/registration', methods = ['GET', 'POST'] )
def registration():
    global email, username, password
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

        if not (re.search(regex,email)):
            flash("Please enter a valid email", category="error")
            print("Error")
        elif (len(username) < 1):
            flash("Please enter a username", category="error")
            print("Error")
        # elif (username == checkUsername()):
        #     flash("Username taken", category="error")
        #     print("Error")
        elif (len(password1) < 7):
            flash("Password must be over 7 characters", category="error")
            print("Error")
        elif (password1 != password2):
            flash("Passwords do not match", category="error")
            print("Error")
        else:
            print(f"Email: {email}, Username: {username}, Password: {password1}")
            password = password1
            return redirect(url_for('setup'))

    return render_template('register.html')

@app.route('/setup')
def setup():
    return render_template('setup.html')

@app.route('/creation', methods = ['GET', 'POST'] )
def creation():
    global display_name, bio, top_song
    if request.method == 'POST':
        display_name = request.form['display_name']
        bio = request.form['bio']
        top_song = request.form['top_song']

        if (len(display_name) < 1):
            flash("Please enter a display name", category="error")
            print("Error")
        elif (len(bio) < 1):
            flash("Please enter a bio", category="error")
            print("Error")
        elif (len(top_song) < 1):
            flash("Please enter a top song", category="error")
            print("Error")
        else:
            print(f"Display Name: {display_name}, Bio: {bio}, Top Song: {top_song}")
            return redirect(url_for('home'))

    return render_template('setup.html')

@app.route('/song')
def search_song():
    #return the song based on query
    query = request.args.get('query')
    song = sp.search(query, type='track', limit=5, market='GB')
    songs = song['tracks']['items']
    data = []
    for song in songs:
        album = song['album']
        item = {}
        item['title'] = song['name']
        item['id'] = song['id']
        item['artist'] = song['artists'][0]['name']
        item['image'] = album['images'][2]['url']
        data.append(item)
    return jsonify(data)

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
