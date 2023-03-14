from flask import Flask, render_template, url_for, redirect, request, session, jsonify, flash
import spotipy, re
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from dbfunctions import *
import mysql.connector 
import argon2

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
    db, cursor = connectdb()
    get_user_details(cursor, db, session["username"], username, password, profilePic, url)
    db.commit()
    db.close()
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
            db, cursor = connectdb()
            bytePass = bytes(password1, 'utf-8')
            hashed_password = argon2.hash_password(bytePass)
            hashed_password  = hashed_password[:199]
            print(hashed_password)
            create_user(cursor, username, hashed_password)
            db.commit()
            db.close()
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

@app.route('/selectResult')
def select_result():
    '''
    Adds the selected song to the database and returns information about the song.

    Arguments (passed in the GET request):
    - id (string)   : Spotify ID of the song.
    - page (string) : Name of the page that the request has come from.

    Returns:
    - data (JSON string) : Array containing the following information about the song:
        * title  : Title of the song.
        * artist : Artist of the song.
        * image  : Album art of the song.
        * audio  : Preview url of the audio for the song.
    '''
    #Gets the song ID and page name from the GET request
    songID = request.args.get("id")
    pageID = request.args.get("page")
    if pageID == "settings" or pageID == "setup":
        #TODO: Add song as user's top song in database
        pass
    #If the page ID is new post, this should be handled on the frontend
    #Searches for the song using the song ID
    # searchResult = sp.search(songID, type="track", limit=1, market="GB")
    # searching for song using songid uses the .track method
    song = sp.track(songID)
    print(list(song))
    #Constructs return as single-element dict array
    data = [{
    "title"  : song["name"],
    "artist" : song["artists"][0]["name"],
    "image"  : song["album"]["images"][2]["url"],
    "audio"  : song["preview_url"]
    }]
    print(data)
    return jsonify(data)

@app.route('/getNotifications')
def get_notifications():
    data = []
    ###TODO: GET NOTIFICATIONS###
    from random import randint
    titles = ["Follow Request", "Like", "Comment"]
    letters = "a b c d e f g h i j k l m n o p q r s t u v w x y z".split(" ")
    for i in range(20):
        nameLength = randint(3, 12)
        name = ""
        for j in range(nameLength): name += letters[randint(0, 25)]
        item = {
            "title"      : titles[randint(0, 2)],
            "name"       : name,
            "profilePic" : "https://i.ytimg.com/vi/zCNyuzQZRVM/maxresdefault.jpg"
        }
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
