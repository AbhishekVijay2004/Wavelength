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



def create_user(cursor, username, password, profilePic=None, url=None, spotifyID=0):
	sql = """
		INSERT INTO users (username, password, profilePic, url, spotifyID)
		VALUES (%s, %s, %s, %s, %s)"""
	cursor.execute(sql, (username, password, profilePic, url, spotifyID))
	print('user added')

def delete_user(username, cursor, db):
	username = (username, )
	sql = """
		DELETE FROM users 
		WHERE username = %s"""
	cursor.execute(sql, username)
	db.commit()
	print('user deleted')


def create_post(cursor, db, username, postText='', postContent=''):
	sql = """
		INSERT INTO posts (username, postText, postContent, createdAt)
		VALUES (%s, %s, %s, NOW())"""
	cursor.execute(sql, (username, postText, postContent))
	db.commit()

def delete_post(postID, cursor, db):
	#make a tuple value
	postID = (postID, )
	sql = """
		DELETE FROM posts
		WHERE postID = %s"""
	cursor.execute(sql, postID)
	db.commit()


def add_like(postID, username, cursor, db):
	delete_like(postID, username)
	sql = """
		INSERT INTO likes(postID, username, type)
		VALUES (%s, %s, 'like')"""
	cursor.execute(sql, (postID, username))
	db.commit()
	print(f'{username} liked {postID}')

def delete_like(postID, username, cursor, db):
	## will function for both like and dislike
	sql = """
		DELETE FROM likes
		WHERE (postID = %s) AND (username = %s)"""
	cursor.execute(sql, (postID, username))
	db.commit()
	print('like deleted')


def add_dislike(postID, username, cursor, db):
	delete_like(postID, username)
	sql = """
		INSERT INTO likes(postID, username, type)
		VALUES (%s, %s, 'dislike')"""
	cursor.execute(sql, (postID, username))
	db.commit()
	print(f'{username} disliked {postID}')


def add_comment(postID, username, text, cursor, db):
	sql = """
		INSERT INTO comments(postID, username, commentText)
		VALUES (%s, %s, %s)"""
	cursor.execute(sql, (postID, username, text))
	db.commit()
	print(f'{username} commented {text} on {postID}')

def delete_comment(commentID, cursor, db):
	commentID = (commentID, )
	sql = """
		DELETE FROM comments
		WHERE (commentID = %s)"""
	cursor.execute(sql, commentID)
	db.commit()
	print(f'comment {commentID[0]} deleted')


def add_follow(username, followerID, cursor, db):
	sql = """
		INSERT INTO following(username, followerID)
		VALUES (%s, %s)"""
	cursor.execute(sql, (username, followerID))
	db.commit()
	print(f'{followerID} followed {username}')

def delete_follow(username, followerID, cursor, db):
	sql = """
		DELETE FROM following
		WHERE (username = %s) AND (followerID = %s)"""
	cursor.execute(sql, (username, followerID))
	db.commit()
	print('friendship deleted')

def alter_user(username, key, value, cursor, db):
	sql = f"""
		UPDATE users
		SET {key} = %s
		WHERE (username = %s)"""
	cursor.execute(sql, (value, username))
	db.commit()
	print(f'{key} changed to {value}')

def get_user_details(cursor, db, username, param='*'):
	if param not in ['username', 'password', 'profilePic', 'url', 'spotifyID', '*']:
		return 'invalid query'
	else:
		sql = f"""
			SELECT {param} FROM users
			WHERE (username = %s)"""
		cursor.execute(sql, (username, ))
		result = cursor.fetchone()
		return result

def get_post_details(cursor, db, postid, param='*',):
	if param not in ['createdAt', 'postText', 'postContent', 'username', '*']:
		return 'invalid query'
	else:
		sql = f"""
			SELECT {param} from posts
			WHERE (postID = %s)"""
		cursor.execute(sql, (postid, ))
		result = cursor.fetchone()
		return result

def get_comment_details(cursor, db, commentid, param='*'):
	if param not in ['username', 'postID', 'commentText', '*']:
		return 'invalid query'
	else:
		sql = f"""
			SELECT {param} from comments
			WHERE (commentID = %s)"""
		cursor.execute(sql, (commentid, ))
		result = cursor.fetchone
		return result

##get list of users posts
def list_user_posts(username, cursor):
	sql = """
		SELECT * FROM posts
		WHERE (username = %s)"""
	cursor.execute(sql, (username, ))
	result = cursor.fetchall()
	return result

def get_num_likes(cursor, db, postid, like='like'):
	# get num likes or dislikes depending on parameter passed
	sql = """
		SELECT SUM(postID) FROM likes
		WHERE (type = %s AND postID = %s)"""
	cursor.execute(sql, (like, postid))
	result = cursor.fetchone()
	return result[0]


def get_like_accounts(cursor,postid, like='like'):
	sql = """
		SELECT username FROM likes
		WHERE (type=%s AND postID = %s)"""
	cursor.execute(sql, (like, postid))
	results = cursor.fetchall()
	# change into list of usernames
	accounts = [result[0] for result in results]
	return accounts

def get_num_following(username, cursor):
	sql = """
		SELECT SUM(username) FROM following
		WHERE (followerID = %s)"""
	cursor.execute(sql, (username, ))
	results = cursor.fetchone()
	return results[0]

def get_following_accounts(username, cursor):
	sql = """
		SELECT username FROM following
		WHERE (followerID = %s)"""
	cursor.execute(sql, (username, ))
	results = cursor.fetchall()
	accounts = [result[0] for result in results]
	return accounts

def get_num_followers(username, cursor):
	sql = """
		SELECT SUM(followerID) FROM following
		WHERE (username = %s)"""
	cursor.execute(sql, (username, ))
	results = cursor.fetchone()
	return results[0]

def get_follower_accounts(username, cursor):
	sql = """
		SELECT followerID FROM following
		WHERE (username = %s)"""
	cursor.execute(sql, (username, ))
	results = cursor.fetchall()
	accounts = [result[0] for result in results]
	return accounts

