'''
make updated database schema for normalised tables

what's needed
creating a user
creating a post
adding a like/dislike
adding a comment
deleting a user
deleting a post
removing a like/dislike
removing a comment'''

import mysql.connector

def connectdb():
	db = mysql.connector.connect(
		host="dbhost.cs.man.ac.uk",
		user="r01479mo",
		password="dbPass+man",
		database="2022_comp10120_z11"
		)

	cursor = db.cursor()
	return db, cursor



def create_user(username, password, profilePic=None, url=None, spotifyID=0):
	global cursor
	sql = """
		INSERT INTO users (username, password, profilePic, url, spotifyID)
		VALUES (%s, %s, %s, %s, %s)"""
	cursor.execute(sql, (username, password, profilePic, url, spotifyID))
	print('user added')

def delete_user(id):
	global cursor
	id = (id, )
	sql = """
		DELETE FROM users 
		WHERE userID = %s"""
	cursor.execute(sql, id)
	print('user deleted')


def create_post(userID, postText='', postContent=''):
	global cursor
	sql = """
		INSERT INTO posts (userID, postText, postContent, createdAt)
		VALUES (%s, %s, %s, NOW())"""
	cursor.execute(sql, (userID, postText, postContent))

def delete_post(postID):
	global cursor
	#make a tuple value
	postID = (postID, )
	sql = """
		DELETE FROM posts
		WHERE postID = %s"""
	cursor.execute(sql, postID)


def add_like(postID, userID):
	global cursor
	delete_like(postID, userID)
	sql = """
		INSERT INTO likes(postID, userID, type)
		VALUES (%s, %s, 'like')"""
	cursor.execute(sql, (postID, userID))
	print(f'{userID} liked {postID}')

def delete_like(postID, userID):
	## will function for both like and dislike
	global cursor
	sql = """
		DELETE FROM likes
		WHERE (postID = %s) AND (userID = %s)"""
	cursor.execute(sql, (postID, userID))
	print('like deleted')


def add_dislike(postID, userID):
	global cursor
	delete_like(postID, userID)
	sql = """
		INSERT INTO likes(postID, userID, type)
		VALUES (%s, %s, 'dislike')"""
	cursor.execute(sql, (postID, userID))
	print(f'{userID} disliked {postID}')


def add_comment(postID, userID, text):
	global cursor
	sql = """
		INSERT INTO comments(postID, userID, commentText)
		VALUES (%s, %s, %s)"""
	cursor.execute(sql, (postID, userID, text))
	print(f'{userID} commented {text} on {postID}')

def delete_comment(commentID):
	global cursor
	commentID = (commentID, )
	sql = """
		DELETE FROM comments
		WHERE (commentID = %s)"""
	cursor.execute(sql, commentID)
	print(f'comment {commentID[0]} deleted')


def add_follow(userID, followerID):
	global cursor
	sql = """
		INSERT INTO following(userID, followerID)
		VALUES (%s, %s)"""
	cursor.execute(sql, (userID, followerID))
	print(f'{followerID} followed {userID}')

def delete_follow(userID, followerID):
	global cursor
	sql = """
		DELETE FROM following
		WHERE (userID = %s) AND (followerID = %s)"""
	cursor.execute(sql, (userID, followerID))
	print('friendship deleted')

def alter_user(userID, key, value):
	global cursor
	sql = f"""
		UPDATE users
		SET {key} = %s
		WHERE (userID = %s)"""
	cursor.execute(sql, (value, userID))
	print(f'{key} changed to {value}')





db, cursor = connectdb()
create_user('matt', 'hello')
create_user('milly', 'useless', spotifyID=10)
create_post(1, postText='What a song', postContent='professor X')
create_post(2, postText='banger', postContent='starships')
add_follow(1, 2)
add_follow(2, 1)
add_like(1, 1)
add_comment(1, 1, 'tune')


db.commit()
db.close()