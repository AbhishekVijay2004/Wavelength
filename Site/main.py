from flask import Flask, render_template, url_for, redirect, request, session, jsonify, flash
import spotipy, re, mysql.connector, os
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from dbfunctions import *
from argon2 import PasswordHasher
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = "abhishek"
app.use_static = True
app.config['UPLOAD_FOLDER'] = 'static/media/profilePictures/'

scope = "user-top-read"

ph = PasswordHasher()

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
    print(session)
    return render_template('profile.html')

@app.route('/friends')
def friends():
    print(session)
    return render_template('friends.html')

@app.route('/home')
def home():
    print(session)
    return render_template('home.html')

@app.route('/settings', methods = ['GET', 'POST'] )
def settings():
    print(session)
    db, cursor = connectdb()

    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        display_name = request.form['display_name']
        bio = request.form['bio']
        top_song = request.form['top_song']

        regex = r"^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9\-\.]+)\.([a-zA-Z]{2,5})$"

        try:
            profile_pic = request.files['profile_pic']
            if (profile_pic.filename != ''):
                filename = secure_filename(profile_pic.filename)
                profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                session["profilePic"] = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                alter_user(session["username"], "profilePic", session["profilePic"], cursor, db)
        except:
            pass         

        if not (re.search(regex,email)):
            flash("Please enter a valid email", category="error")
            print("Error")
        elif (len(username) < 1):
            flash("Please enter a username", category="error")
            print("Error")
        elif (len(display_name) < 1):
            flash("Please enter a display name", category="error")
            print("Error")
        elif (len(bio) < 1):
            flash("Please enter a bio", category="error")
            print("Error")
        elif (len(top_song) < 1):
            flash("Please enter a top song", category="error")
            print("Error")
        else:
            session["bio"] = bio
            alter_user(session["username"], "bio", session["bio"], cursor, db)
            session["topSong"] = top_song
            alter_user(session["username"], "topSong", session["topSong"], cursor, db)
            session["displayName"] = display_name
            alter_user(session["username"], "displayName", session["displayName"], cursor, db)

            #Please change to singular form when fixed
            userDetailsList = get_user_details(cursor, session["username"])
            session["profilePic"] =  userDetailsList[2]
            #Please change to singular form when fixed

            db.commit()
            db.close()
            return redirect(url_for('home'))
    
    db.commit()
    db.close()
    try:
        return render_template('settings.html', email=session["email"], username=session["username"], password=session["password"], display_name=session["displayName"], profile_pic=session["profilePic"], bio=session["bio"], top_song=session["topSong"])
    except:
        return redirect(url_for('signon'))

@app.route('/post')
def post():
    print(session)
    return render_template('new-post.html')

@app.route('/signon')
def signon():
    return render_template('login.html')

@app.route('/login', methods = ['GET', 'POST'] )
def login():
    regex = r"^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9\-\.]+)\.([a-zA-Z]{2,5})$" 
    user = False          
    db, cursor = connectdb()

    if request.method == 'POST':
        usernameOrEmail = request.form['username']
        password = request.form['password']
<<<<<<< HEAD
        print(username)
        if (len(username) < 1):
            flash("Not a valid username", category="error")
=======

        if (len(usernameOrEmail) < 1):
            flash("Please enter your username or email", category="error")
>>>>>>> origin
            print("Error")
        elif (len(password) < 1):
            flash("Please enter your password", category="error")
            print("Error")
        else:
<<<<<<< HEAD
            if (re.search(regex,username)):
                userDetailsList = get_user_details_by_email(cursor, username)
                print(userDetailsList)
=======
            if (re.search(regex,usernameOrEmail)):
                userDetailsList = get_user_details_by_email(cursor, usernameOrEmail)
>>>>>>> origin
                if (userDetailsList != False):
                    user = True
            else:
                userDetailsList = get_user_details(cursor, usernameOrEmail)
                if (userDetailsList != False):
                    user = True

        if (user == True):
<<<<<<< HEAD
            # session["username"] = userDetailsList[0]
            # session["password"] = userDetailsList[1]
            # session["email"] = userDetailsList[2]
            # session["profilePic"] = userDetailsList[3]
            # session["bio"] = userDetailsList[4]
            # session["topSong"] = userDetailsList[5]
            # session["displayName"] = userDetailsList[6]

            for i, val in enumerate(['username', 'password', 'email', 'profilePic', 'bio', 'topSong', 'displayName']):
                session[val] = userDetailsList[i]

            db.commit()
            db.close()
            print(session)

            return redirect(url_for('home'))
=======
            try:
                if (ph.verify(userDetailsList[1], password)):
                    session["username"] = userDetailsList[0]
                    session["password"] = userDetailsList[1]
                    session["email"] = userDetailsList[3]
                    session["profilePic"] = userDetailsList[2]
                    session["bio"] = userDetailsList[4]
                    session["topSong"] = userDetailsList[5]
                    session["displayName"] = userDetailsList[6]
                    print(session)
>>>>>>> origin

                    db.commit()
                    db.close()
                    return redirect(url_for('home'))
            except:
                flash("Password is incorrect", category="error")
                print("Error")
        else:
            if (len(usernameOrEmail) >= 1 and len(password) >= 1):
                flash("User does not exist", category="error")
                print("Error")

    db.commit()
    db.close()
    return redirect(url_for('signon'))

@app.route('/logout', methods = ['GET', 'POST'] )
def logout():
    session.pop('username', None)
    session.pop('password', None)
    session.pop('email', None)
    session.pop('profilePic', None)
    session.pop('bio', None)
    session.pop('topSong', None)
    session.pop('displayName', None)
    return redirect(url_for('signon'))

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/registration', methods = ['GET', 'POST'] )
def registration():
    global email, username, password
    if request.method == 'POST':
        db, cursor = connectdb()
        email = request.form['email']
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
        regex = r"^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9\-\.]+)\.([a-zA-Z]{2,5})$"

        if not (re.search(regex,email)):
            flash("Please enter a valid email", category="error")
            print("Error")
        elif (len(username) < 1):
            flash("Please enter a username", category="error")
            print("Error")
        elif (len(password1) < 7):
            flash("Password must be over 7 characters", category="error")
            print("Error")
        elif (password1 == username):
            flash("Password and username must not match", category="error")
            print("Error")
        elif (password1 != password2):
            flash("Passwords do not match", category="error")
            print("Error")
        else:
            if (get_user_details(cursor, username)):
                flash("Username taken", category="error")
                print("Error")
            elif (get_user_details_by_email(cursor, email)):
                flash("Email already taken", category="error")
                print("Error")
            else:
                hashed_password = ph.hash(password1)
                hashed_password = hashed_password[:199]
                print(hashed_password)
                print(email)
                create_user(cursor, db, username, hashed_password, email)
                db.commit()
                db.close()
                session["username"] = username
                session["password"] = hashed_password
                session["email"] = email
                return redirect(url_for('setup'))
    
    db.commit()
    db.close()
    return render_template('register.html')

@app.route('/setup')
def setup():
    return render_template('setup.html')

@app.route('/creation', methods = ['GET', 'POST'] )
def creation():
    display_name, bio, top_song = "", "", ""

    if request.method == 'POST':
        change = False
        display_name = request.form['display_name']
        bio = request.form['bio']
        top_song = request.form['top_song']
        db, cursor = connectdb()

        try:
            profile_pic = request.files['profile_pic']
        except:
            pass
        if ('profile_pic' not in request.files or profile_pic.filename == ''):
            session["profilePic"] = 'static/media/icons/profile-icon-transparent.png'
            alter_user(username, "profilePic", session["profilePic"], cursor, db)
        else:
            profile_pic = request.files['profile_pic']
            filename = secure_filename(profile_pic.filename)
            profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            session["profilePic"] = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            alter_user(session["username"], "profilePic", session["profilePic"], cursor, db)
            change = True            

        if (change == True):
            pass
        elif (len(display_name) < 1):
            flash("Please enter a display name", category="error")
            print("Error")
        elif (len(bio) < 1):
            flash("Please enter a bio", category="error")
            print("Error")
        elif (len(top_song) < 1):
            flash("Please enter a top song", category="error")
            print("Error")
        else:
            session["bio"] = bio
            alter_user(session["username"], "bio", session["bio"], cursor, db)
            session["topSong"] = top_song
            alter_user(session["username"], "topSong", session["topSong"], cursor, db)
            session["displayName"] = display_name
            alter_user(session["username"], "displayName", session["displayName"], cursor, db)

            #Please change to singular form when fixed
            userDetailsList = get_user_details(cursor, session["username"])
            session["profilePic"] =  userDetailsList[2]
            #Please change to singular form when fixed

            db.commit()
            db.close()
            return redirect(url_for('home'))
    
    db.commit()
    db.close()    
    try:
        return render_template('setup.html', profile_pic=session["profilePic"], display_name=display_name, bio=bio, top_song=top_song)
    except:
        return render_template('setup.html', profile_pic='static/media/icons/profile-icon-transparent.png', display_name=display_name, bio=bio, top_song=top_song)

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
