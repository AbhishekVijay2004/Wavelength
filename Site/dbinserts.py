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

def create_user(**kwargs):
	global cursor
	# print(list(kwargs.keys()))
	keys = ['username', 'password', 'profilePic', 'url', 'followerCount', 'followingCount', 'spotifyID']
	#add the non named parameters to the dictionary as null or 0
	for key in keys:
		if key not in list(kwargs):
			if key in ['followerCount', 'followingCount', 'spotifyID']:
				kwargs[key] = 0
			else:
				kwargs[key] = None
	print(kwargs)
	keys = list(kwargs)
	sql = f"""
		INSERT INTO users ({', '.join(list(kwargs))})
		VALUES (
			%({keys[0]})s,
			%({keys[1]})s,
			%({keys[2]})s,
			%({keys[3]})s,
			%({keys[4]})s,
			%({keys[5]})s,
			%({keys[6]})s
			)"""
	cursor.execute(sql, kwargs)
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
		INSERT INTO posts (userID, postText, postContent, likes, createdAt)
		VALUES (%s, %s, %s, %s, NOW())"""
	cursor.execute(sql, (userID, postText, postContent, 0))

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



def alter_user(userID, key, value):
	global cursor
	sql = f"""
		UPDATE users
		SET {key} = %s
		WHERE (userID = %s)"""
	cursor.execute(sql, (value, userID))
	print(f'{key} changed to {value}')



db, cursor = connectdb()
# create_user(username='matt', password='pass', url='nothign', spotifyID=50)

# create_post(1, 'banger', 'funky friday')
# delete_post(1)
# add_like(5, 1)
# delete_like(5, 1)
# add_dislike(2, 1)
# add_comment(5, 1, 'what a tune')
# delete_comment(1)
alter_user(1, 'spotifyID', '76')
db.commit()
db.close()