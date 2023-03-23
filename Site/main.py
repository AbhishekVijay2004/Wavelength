from flask import Flask, render_template, url_for, redirect, request, session, jsonify, flash, make_response
import spotipy, re, mysql.connector, os, json
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from dbfunctions import *
from argon2 import PasswordHasher
from werkzeug.utils import secure_filename
from spotify_functions import *
#FOR TESTING
from random import randint


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
        if (session["topSong"] == None):
            return redirect(url_for('setup'))
        elif (session["bio"] == None):
            return redirect(url_for('setup'))
        elif (session["displayName"] == None):
            return redirect(url_for('setup'))
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('signOn'))

@app.route('/home')
def home():
    print(session)
    return render_template('home.html')

@app.route('/post', methods = ['GET', 'POST'] )
def post():
    print(session)

    if request.method == 'POST':
        db, cursor = connectdb()
        text = request.form['caption']
        songID = request.form['songID']
        song = request.form['song']
        # likes = request.form.get('likes')
        # if (likes == None):
        #     likes = "off"
        # comments = request.form.get('comments')
        # if (comments == None):
        #     comments = "off"
        # dislikes = request.form.get('dislikes')
        # if (dislikes == None):
        #     dislikes = "off"

        if (len(song) < 1 or len(songID) < 1):
            flash("Please enter a song", category="error")
            print("Error")
        elif (len(text) > 250):
            flash("Please restrict the caption to 250 characters", category="error")
            print("Error")
        else:
            create_post(cursor, db, session['username'], text, songID)
            db.commit()
            db.close()
            return redirect(url_for('home'))

    try:
        return render_template('new-post.html', text=text)
    except:
        return render_template('new-post.html')


@app.route('/friends')
def friends():
    try:
        print(session)
        db, cursor = connectdb()

        followers = get_following_accounts(cursor, session["username"])
        user_details = [get_user_details(cursor, username) for username in followers]

        usernames = [user_info[0] for user_info in user_details]
        # display_names = [user_info[6] for user_info in user_details]
        profile_pics = [user_info[2] for user_info in user_details]

        users_num_followers = [get_num_followers(cursor, username) for username in usernames]
        users_num_posts = [get_num_posts(cursor, username) for username in usernames]
        users_num_likes = [get_num_likes_received(cursor, username) for username in usernames]
        users_num_comments = [get_num_comments_received(cursor, username) for username in usernames]

        # add_follow(cursor, db, "zak.mitchell", session["username"])
        db.commit()
        db.close()
        return render_template('friends.html',
                            usernames=usernames, profile_pics=profile_pics,
                            users_num_followers=users_num_followers,
                            users_num_posts=users_num_posts, users_num_likes=users_num_likes,
                            users_num_comments=users_num_comments)
    except KeyError:
        return redirect(url_for('signOn'))

@app.route("/friendSearch/<query>")
def add_friend(query):
    db, cursor = connectdb()
    searchResults = search_for_user(cursor, query, session['username'])

    usernameResults = [user_info[0] for user_info in searchResults]
    profile_picResults = [user_info[2] for user_info in searchResults]
    users_num_followerResults = [get_num_followers(cursor, username) for username in usernameResults]
    users_num_postResults = [get_num_posts(cursor, username) for username in usernameResults]
    users_num_likeResults = [get_num_likes_received(cursor, username) for username in usernameResults]
    users_num_commentResults = [get_num_comments_received(cursor, username) for username in usernameResults]

    db.commit()
    db.close()
    # print(searchResults)
    # return "Yes"
    data = {
        "usernameResults": usernameResults,
        "profile_picResults": profile_picResults,
        "users_num_followerResults": users_num_followerResults,
        "users_num_postResults": users_num_postResults,
        "users_num_likeResults": users_num_likeResults,
        "users_num_commentResults": users_num_commentResults
    }
    json_data = json.dumps(data)
    response = make_response(json_data)

    return response

@app.route("/friendSearch/follow/<query>")
def follow(query):
    print(query)
    db, cursor = connectdb()
    add_follow(cursor, db, session["username"], query)
    create_notification(cursor, db, query, session["username"], "follow")
    db.commit()
    db.close()
    return "User Followed"

@app.route("/friendSearch/unfollow/<query>")
def unfollow(query):
    db, cursor = connectdb()
    delete_follow(cursor, db, session["username"], query)
    db.commit()
    db.close()
    return "User Unfollowed"

@app.route('/profile')
def profile():
    if "username" in session:
        if (session["topSong"] == None):
            return redirect(url_for('setup'))
        elif (session["bio"] == None):
            return redirect(url_for('setup'))
        elif (session["displayName"] == None):
            return redirect(url_for('setup'))
        else:
            pass
    else:
        return redirect(url_for('signOn'))
    
    try:
        db, cursor = connectdb()
        
        # noFollowing = get_num_following(cursor, db, username)
        noFollowers = get_num_followers(cursor, session["username"])
        noPosts = get_num_posts(cursor, session["username"])
        noLikes = get_num_likes_received(cursor, session["username"])
        noComments = get_num_comments_received(cursor, session["username"])
        db.close()

        song_name = get_track_title(sp, session["topSong"])
        song_url = get_track_preview(sp, session["topSong"])
        artist_name = get_track_artist_name(sp, session["topSong"])
        album_image = get_track_image(sp, session["topSong"])

        return render_template('profile.html',
                            username=session["username"],
                            display_name=session["displayName"], profile_pic=session["profilePic"],
                            bio=session["bio"], title=song_name, song=song_url, artist = artist_name,
                            image=album_image, noFollowers=noFollowers, noPosts=noPosts,
                            noLikes=noLikes, noComments=noComments)
    except KeyError:
        return redirect(url_for('signOn'))
    
@app.route('/profile/<query>', methods = ['GET', 'POST'])
def friendProfile(query):
    print(session)
    db, cursor = connectdb()
    if (query == "undefined"):
        return redirect(url_for('profile'))

    friend_name = query
    display_name = get_user_detail(cursor, friend_name, "displayname")
    profile_pic = str("/../" + get_user_detail(cursor, friend_name, "profilePic"))
    print(profile_pic)
    bio = get_user_detail(cursor, friend_name, "bio")
    topSong = get_user_detail(cursor, friend_name, "topsong")

    # noFollowing = get_num_following(cursor, db, username)
    noFollowers = get_num_followers(cursor, friend_name)
    noPosts = get_num_posts(cursor, friend_name)
    noLikes = get_num_likes_received(cursor, friend_name)
    noComments = get_num_comments_received(cursor, friend_name)
    db.close()

    song_name = get_track_title(sp, topSong)
    song_url = get_track_preview(sp, topSong)
    artist_name = get_track_artist_name(sp, topSong)
    album_image = get_track_image(sp, topSong)

    return render_template('profile.html',
                        username=friend_name,
                        display_name=display_name, profile_pic=profile_pic,
                        bio=bio, title=song_name, song=song_url, artist = artist_name,
                        image=album_image, noFollowers=noFollowers, noPosts=noPosts,
                        noLikes=noLikes, noComments=noComments)

@app.route('/settings', methods = ['GET', 'POST'] )
def settings():
    if "username" in session:
        if (session["topSong"] == None):
            return redirect(url_for('setup'))
        elif (session["bio"] == None):
            return redirect(url_for('setup'))
        elif (session["displayName"] == None):
            return redirect(url_for('setup'))
        else:
            pass
    else:
        return redirect(url_for('signOn'))
    try: 
        print(session)
        song_name = get_track_title(sp, session["topSong"])
        song_url = get_track_preview(sp, session["topSong"])
        artist_name = get_track_artist_name(sp, session["topSong"])
        album_image = get_track_image(sp, session["topSong"])
        cachedList = []
        change = False

        if request.method == 'POST':
            db, cursor = connectdb()
            email = request.form['email']
            display_name = request.form['display_name']
            bio = request.form['bio']
            top_song = request.form['songID']
            regex = r"^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9\-\.]+)\.([a-zA-Z]{2,5})$"

            # Password Changing
            oldPassword = request.form['password1']
            newPassword = request.form['password2']
            passConfirm = request.form['password3']
            if (len(oldPassword) >= 1):
                change = True
                try:
                    if (ph.verify(session["password"], oldPassword)):
                        if (len(newPassword) < 7):
                            flash("New password must be over 7 characters", category="error")
                            print("Error")
                        elif (newPassword == session["username"]):
                            flash("Password and username must not match", category="error")
                            print("Error")
                        elif (newPassword != passConfirm):
                            flash("Passwords do not match", category="error")
                            print("Error")
                        else:
                            hashed_password = ph.hash(newPassword)
                            hashed_password = hashed_password[:199]
                            alter_user(cursor, db, session["username"], "password", hashed_password)
                            db.commit()
                            db.close()
                            session["password"] = hashed_password
                            flash("Password updated", category="success")
                            print("Success")
                except:
                    flash("Password is incorrect", category="error")
                    print("Error")

            # Profile Picture Changing
            if (change == False):
                try:
                    profile_pic = request.files['profile_pic']
                    if (profile_pic.filename != ''):
                        filename = secure_filename(profile_pic.filename)
                        profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        session["profilePic"] = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        alter_user(cursor, db, session["username"], "profilePic", session["profilePic"])
                        change = True
                        flash("Profile picture updated", category="success")
                        print("Success")
                        db.commit()
                        db.close()
                except:
                    pass

            # Form Changing
            if (change == True):
                cachedList = [email, display_name, bio, top_song]
                pass
            elif not (re.search(regex,email)):
                flash("Please enter a valid email", category="error")
                print("Error")
            elif (len(display_name) < 1):
                flash("Please enter a display name", category="error")
                print("Error")
            elif (len(bio) < 1):
                flash("Please enter a bio", category="error")
                print("Error")
            elif (len(top_song) < 1):
                flash("Please select a top song", category="error")
                print("Error")
            else:
                if (email != session["email"] and get_user_details_by_email(cursor, email)):
                    flash("Email already taken", category="error")
                    print("Error")
                else:
                    if (session["email"] != email):
                        alter_user(cursor, db, session["username"], "email", email)
                        session["email"] = email
                    if (session["bio"] != bio):
                        alter_user(cursor, db, session["username"], "bio", bio)
                        session["bio"] = bio
                    if (session["topSong"] != top_song):
                        alter_user(cursor, db, session["username"], "topSong", top_song)
                        session["topSong"] = top_song
                    if (session["displayName"] != display_name):
                        alter_user(cursor, db, session["username"], "displayName", display_name)
                        session["displayName"] = display_name

                    session["profilePic"] = get_user_detail(cursor, session["username"], "profilePic")
                    db.commit()
                    db.close()

                    song_name = get_track_title(sp, session["topSong"])
                    song_url = get_track_preview(sp, session["topSong"])
                    artist_name = get_track_artist_name(sp, session["topSong"])
                    album_image = get_track_image(sp, session["topSong"])

                    flash("Settings saved", category="success")
                    print("Success")

        if (len(cachedList) > 0):
            return render_template('settings.html',
                                email=cachedList[0], username=session["username"],
                                password=session["password"], display_name=cachedList[1],
                                profile_pic=session["profilePic"], bio=cachedList[2],
                                top_song=cachedList[3], title=song_name, song=song_url,
                                artist = artist_name, image=album_image)
        else:
            return render_template('settings.html',
                                email=session["email"], username=session["username"],
                                password=session["password"], display_name=session["displayName"],
                                profile_pic=session["profilePic"], bio=session["bio"],
                                top_song=session["topSong"], title=song_name, song=song_url,
                                artist = artist_name, image=album_image)
    
    except KeyError:
        return redirect(url_for('signOn'))

@app.route('/signOn')
def signOn():
    return render_template('login.html')

@app.route('/login', methods = ['GET', 'POST'] )
def login():
    regex = r"^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9\-\.]+)\.([a-zA-Z]{2,5})$"
    user = False
    db, cursor = connectdb()

    if request.method == 'POST':
        usernameOrEmail = request.form['username']
        password = request.form['password']

        if (len(usernameOrEmail) < 1):
            flash("Please enter your username or email", category="error")
            print("Error")
        elif (len(password) < 1):
            flash("Please enter your password", category="error")
            print("Error")
        else:
            if (re.search(regex,usernameOrEmail)):
                userDetailsList = get_user_details_by_email(cursor, usernameOrEmail)
                if (userDetailsList != False):
                    user = True
            else:
                userDetailsList = get_user_details(cursor, usernameOrEmail)
                if (userDetailsList != False):
                    user = True

        if (user == True):
            try:
                if (ph.verify(userDetailsList[1], password)):
                    for i, val in enumerate(['username', 'password', 'profilePic', 'email', 'bio', 'topSong', 'displayName']):
                        session[val] = userDetailsList[i]
                    print(session)

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
    return redirect(url_for('signOn'))

@app.route('/logout', methods = ['GET', 'POST'] )
def logout():
    session.pop('username', None)
    session.pop('password', None)
    session.pop('email', None)
    session.pop('profilePic', None)
    session.pop('bio', None)
    session.pop('topSong', None)
    session.pop('displayName', None)
    return redirect(url_for('signOn'))

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
    display_name, bio, top_song, song_name = "", "", "", ""
    db, cursor = connectdb()

    if request.method == 'POST':
        change = False
        display_name = request.form['display_name']
        bio = request.form['bio']
        top_song = request.form['songID']
        song_name = request.form['cachedName']

        try:
            profile_pic = request.files['profile_pic']
        except:
            pass
        if ('profile_pic' not in request.files or profile_pic.filename == ''):
            try:
                session["profilePic"]
            except KeyError:
                session["profilePic"] = 'static/media/icons/profile-icon-transparent.png'
                try:
                    alter_user(cursor, db, username, "profilePic", session["profilePic"])
                except NameError:
                    return redirect(url_for('signOn'))
        else:
            profile_pic = request.files['profile_pic']
            filename = secure_filename(profile_pic.filename)
            profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            session["profilePic"] = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            alter_user(cursor, db, session["username"], "profilePic", session["profilePic"])
            change = True
            flash("Profile picture updated", category="success")
            print("Success")

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
            alter_user(cursor, db, session["username"], "bio", session["bio"])
            session["topSong"] = top_song
            alter_user(cursor, db, session["username"], "topSong", session["topSong"])
            session["displayName"] = display_name
            alter_user(cursor, db, session["username"], "displayName", session["displayName"])

            session["profilePic"] = get_user_detail(cursor, session["username"], "profilePic")
            db.commit()
            db.close()
            return redirect(url_for('home'))

    db.commit()
    db.close()
    
    try:
        return render_template('setup.html', profile_pic=session["profilePic"], display_name=display_name, bio=bio, top_song=top_song, cachedName=song_name)
    except:
        return render_template('setup.html', profile_pic='static/media/icons/profile-icon-transparent.png', display_name=display_name, bio=bio, top_song=top_song)



@app.route('/song')
def search_song():
    #return the song based on query
    query = request.args.get('query')
    # print(query)
    song = sp.search(query, type='track', limit=5, market='GB')
    # print(song)
    songs = song['tracks']['items']
    if len(songs) == 0:
        return []
    if len(query) == 0:
        return []
    data = []
    for song in songs:
        album = song['album']
        item = {}
        item['title'] = song['name']
        item['id'] = song['id']
        item['artist'] = song['artists'][0]['name']
        item['image'] = album['images'][0]['url']
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
    #Constructs return as single-element dict array
    data = [{
    "title"  : song["name"],
    "artist" : song["artists"][0]["name"],
    "image"  : song["album"]["images"][0]["url"],
    "audio"  : song["preview_url"]
    }]
    if song['preview_url'] == None:
        # run a search on the name to find the preview url
        song = sp.search(data[0]['title'] + data[0]['artist'], type='track', limit=1, market='GB')
        preview = song['tracks']['items'][0]['preview_url']
        data[0]['audio'] = preview
    print(data)
    return jsonify(data)

@app.route('/sendNotification')
def send_notification():
    '''
    Sends a notification to a user

    Arguments:
    - recipient (string)
    - sender (string)
    - version (string)
    - postID (int) default: None

    Returns: None
    '''
    postID = None
    recipient = request.args.get("recipient")
    sender = request.args.get("sender")
    version = request.args.get("version")
    postID = request.args.get("postID")
    db, cursor = connectdb()
    create_notification(cursor, db, recipient, sender, version, postID)

@app.route('/clearNotification')
def clear_notification():
    db, cursor = connectdb()
    delete_notification(cursor, db, request.args.get("notificationID"))
    return "done"

@app.route('/fetchNotification')
def fetch_notifications():
    '''
    Fetches all of a users notifications

    Arguments:
    - recipient (string)

    Returns:
    - data (JSON string): Array containing following information about each
        * notificationID (int)
        * recipient (string)
        * sender (string)
        * senderPic (string)
        * type (string)
        * postID (int) often None
    '''
    #recipient = request.args.get("recipient")
    recipient = session["username"]
    db, cursor = connectdb()
    notifications = view_notifications(cursor, recipient)
    data = []

    for notification in notifications:
        item = {}
        for i, val in enumerate(['notificationID', 'recipient', 'sender', 'type', 'postID']):
            item[val] = notification[i]
        item["senderPic"] = get_user_detail(cursor, recipient, "profilePic")
        data.append(item)
    return jsonify(data)

@app.route("/fetchPosts")
def fetch_posts():
    """
    Returns a list posts by users that the given user is following, sorted by time.

    Arguments:
    - user (string)     : The username of the user.
    - startIndex (int)  : The point in the ordered list to begin returning posts.
    - numToReturn (int) : The number of posts the function should return. 0 = return all posts.

    Returns:
    - data (JSON string): Array containing posts with the following information:
        * postID         : ID of the post in the database.
        * songTitle      : Title of post's song.
        * artistName     : Name of the artist of post's song.
        * songImage      : Album art for post's song.
        * songPreview    : Preview URL for song audio.
        * posterName     : Display name of user who posted the post.
        * posterUsername : Username of the user who posted the post.
        * posterPic      : Profile picture of the user who posted the post.
        * postTime       : Time that the post was created.
        * postCaption    : Caption to be displayed with post.
        * postLikes      : Number of likes on the post.
        * postDislikes   : Number of dislikes on the post.
        * postComments   : Number of comments on the post.
        * liked          : Whether the user has liked the post.
        * disliked       : Whether the user has disliked the post.
    """

    user = session["username"]
    db, cursor = connectdb()
    startIndex = request.args.get("startIndex")
    numToReturn = request.args.get("numToReturn")
    postList = []

    if request.args.get("userProfile") == "":
        following = get_following_accounts(cursor, user)
        for f in following:
            for post in list_user_posts(cursor, f):
                postList.append(post)

    else:
        for post in list_user_posts(cursor, request.args.get("userProfile")):
            postList.append(post)

    postList.sort(reverse = True, key=lambda x: x[1])

    data = []
    for post in postList:
        song = sp.track(post[3])
        data.append({
        "postID"         : post[0],
        "songTitle"      : song["name"],
        "artistName"     : song["artists"][0]["name"],
        "songImage"      : song["album"]["images"][0]["url"],
        "songPreview"    : song["preview_url"],
        "posterName"     : get_user_detail(cursor, post[4], "displayname"),
        "posterUsername" : post[4],
        "posterPic"      : get_user_detail(cursor, post[4], "profilePic"),
        "postTime"       : post[1],
        "postCaption"    : post[2],
        "postLikes"      : get_num_likes(cursor, db, post[0], "like"),
        "postDislikes"   : get_num_likes(cursor, db, post[0], "dislike"),
        "postComments"   : get_num_comments(cursor, db, post[0]),
        "liked"          : user in get_like_accounts(cursor, post[0], like='like'),
        "disliked"       : user in get_like_accounts(cursor, post[0], like='dislike')
        })

        if song['preview_url'] == None:
            # run a search on the name to find the preview url
            song = sp.search(song["name"] + song["artists"][0]["name"], type='track', limit=1, market='GB')
            preview = song["tracks"]["items"][0]["preview_url"]
            data[len(data) - 1]["songPreview"] = preview

    return jsonify(data)

@app.route("/getComments")
def get_comments():
    db, cursor = connectdb()
    postID = int(request.args.get("postID"))
    data = [{"userPic" : get_user_detail(cursor, session["username"], "profilePic")}]
    rawCommentIDs = list(get_post_comments(cursor, db, postID))
    commentIDs = []
    for id in rawCommentIDs: commentIDs.append(id[0])
    for id in commentIDs:
        commentInfo = get_comment_details(cursor, db, id)[0]
        item = {
        "commentID"       : id,
        "commentUsername" : commentInfo[2],
        "commentPic"      : get_user_detail(cursor, commentInfo[2], "profilePic"),
        "commentText"     : commentInfo[3],
        "commentLikes"    : get_num_comment_likes(cursor, db, id, like="like"),
        "commentDislikes" : get_num_comment_likes(cursor, db, id, like="dislike"),
        "commentDate"     : get_comment_details(cursor, db, id, "createdAt")
        }
        data.append(item)
    return jsonify(data)

@app.route("/changeLike")
def change_like():
    db, cursor = connectdb()
    type = request.args.get("type")
    postID = int(request.args.get("postID"))
    amount = int(request.args.get("amount"))
    user = session["username"]
    delete_like(cursor, db, postID, user)
    if amount == -1:
        return "done"
    if type == "like":
        add_like(cursor, db, postID, user)
        create_notification(cursor, db, get_post_details(cursor, db, postID, "username")[0], user, "Like")
        return "done"
    add_dislike(cursor, db, postID, user)
    create_notification(cursor, db, get_post_details(cursor, db, postID, "username")[0], user, "Dislike")
    return "done"

@app.route("/postComment")
def post_comment():
    db, cursor = connectdb()
    user = session["username"]
    comment = request.args.get("text")
    postID = request.args.get("postID")
    add_comment(cursor, db, postID, user, comment)
    create_notification(cursor, db, get_post_details(cursor, db, postID, "username")[0], user, "Comment")
    return "done"


if __name__ == '__main__':
    app.run(debug = True)

"""
@app.route('/getNotifications')
def get_notifications():
    '''
    Returns the notifications for the user.

    Arguments: None

    Returns:
    - data (JSON string):
        * title (string)      : Type of notification e.g. follow request, like.
        * name (string)       : Username of the notification causer.
        * profilePic (string) : URL of notification causer's profile picture.
    '''
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
"""

'''
@app.route('/song', methods=['POST'])
def play_song():
    song_name = request.form['song_name']
    results = sp.search(q=song_name, type='track', limit=1, market='GB')
    track = results['tracks']['items'][0]
    preview_url = track['preview_url']
    return render_template('index.html', song_preview = preview_url)'''
