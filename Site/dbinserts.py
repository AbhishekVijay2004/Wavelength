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

def delete_user(username):
	global cursor
	username = (username, )
	sql = """
		DELETE FROM users 
		WHERE username = %s"""
	cursor.execute(sql, username)
	print('user deleted')


def create_post(username, postText='', postContent=''):
	global cursor
	sql = """
		INSERT INTO posts (username, postText, postContent, createdAt)
		VALUES (%s, %s, %s, NOW())"""
	cursor.execute(sql, (username, postText, postContent))

def delete_post(postID):
	global cursor
	#make a tuple value
	postID = (postID, )
	sql = """
		DELETE FROM posts
		WHERE postID = %s"""
	cursor.execute(sql, postID)


def add_like(postID, username):
	global cursor
	delete_like(postID, username)
	sql = """
		INSERT INTO likes(postID, username, type)
		VALUES (%s, %s, 'like')"""
	cursor.execute(sql, (postID, username))
	print(f'{username} liked {postID}')

def delete_like(postID, username):
	## will function for both like and dislike
	global cursor
	sql = """
		DELETE FROM likes
		WHERE (postID = %s) AND (username = %s)"""
	cursor.execute(sql, (postID, username))
	print('like deleted')


def add_dislike(postID, username):
	global cursor
	delete_like(postID, username)
	sql = """
		INSERT INTO likes(postID, username, type)
		VALUES (%s, %s, 'dislike')"""
	cursor.execute(sql, (postID, username))
	print(f'{username} disliked {postID}')


def add_comment(postID, username, text):
	global cursor
	sql = """
		INSERT INTO comments(postID, username, commentText)
		VALUES (%s, %s, %s)"""
	cursor.execute(sql, (postID, username, text))
	print(f'{username} commented {text} on {postID}')

def delete_comment(commentID):
	global cursor
	commentID = (commentID, )
	sql = """
		DELETE FROM comments
		WHERE (commentID = %s)"""
	cursor.execute(sql, commentID)
	print(f'comment {commentID[0]} deleted')


def add_follow(username, followerID):
	global cursor
	sql = """
		INSERT INTO following(username, followerID)
		VALUES (%s, %s)"""
	cursor.execute(sql, (username, followerID))
	print(f'{followerID} followed {username}')

def delete_follow(username, followerID):
	global cursor
	sql = """
		DELETE FROM following
		WHERE (username = %s) AND (followerID = %s)"""
	cursor.execute(sql, (username, followerID))
	print('friendship deleted')

def alter_user(username, key, value):
	global cursor
	sql = f"""
		UPDATE users
		SET {key} = %s
		WHERE (username = %s)"""
	cursor.execute(sql, (value, username))
	print(f'{key} changed to {value}')




if __name__ == "__main__":
	db, cursor = connectdb()
	db.commit()
	db.close()