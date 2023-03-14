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


def create_user(cursor, db, username, password, email, profilePic=None, bio=None, topsong=None, displayname=None):
	if displayname == None:
		displayname = username
	sql = """
		INSERT INTO users (username, password, profilePic, email, bio, topsong, displayname)
		VALUES (%s, %s, %s, %s, %s, %s, %s)"""
	cursor.execute(sql, (username, password, profilePic, email, bio, topsong, displayname))
	db.commit()
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
		INSERT INTO comments(postID, username, commentText, createdAt)
		VALUES (%s, %s, %s, NOW())"""
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

def add_comment_like(commentID, username, liketype, cursor, db):
	delete_comment_like(commentID, username, cursor, db)
	sql = """
		INSERT INTO commentlikes(commentID, username, type)
		VALUES (%s, %s, %s)"""
	cursor.execute(sql, (commentID, username, liketype))
	db.commit()

def delete_comment_like(commentID, username, cursor, db):
	## will function for both like and dislike
	sql = """
		DELETE FROM commentlikes
		WHERE (commentID = %s) AND (username = %s)"""
	cursor.execute(sql, (commentID, username))
	db.commit()
	print('like deleted')


def add_follow(username, followername, cursor, db):
	sql = """
		INSERT INTO following(username, username_follow)
		VALUES (%s, %s)"""
	cursor.execute(sql, (username, username_follow))
	db.commit()
	print(f'{followerID} followed {username}')

def delete_follow(username, followername, cursor, db):
	sql = """
		DELETE FROM following
		WHERE (username = %s) AND (username_follow = %s)"""
	cursor.execute(sql, (username, followername))
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

def get_user_detail(cursor, db, username, param='*'):
	if param not in ['username', 'password', 'profilePic', 'email', 'displayname', 'profilePic', 'topsong', 'bio', '*']:
		return 'invalid query'
	else:
		sql = f"""
			SELECT {param} FROM users
			WHERE (username = %s)"""
		cursor.execute(sql, (username, ))
		result = cursor.fetchone()
		if len(result) == 0:
			return None
		return result

def get_user_details(cursor, username):
	sql = """
		SELECT * FROM users
		WHERE (username = %s)"""
	cursor.execute(sql, (username, ))
	result = cursor.fetchall()
	if len(result) == 0:
		return None
	return result[0]

def get_user_details_by_email(cursor, email):
	sql = """
		SELECT * FROM users
		WHERE (email = %s)"""
	cursor.execute(sql, (email,))
	resultt = cursor.fetchall()
	if len(result) == 0:
		return None
	return result[0]

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
	if param not in ['username', 'postID', 'commentText', 'createdAt', '*']:
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
		SELECT SUM(username) FROM likes
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


def get_num_comment_likes(cursor, db, commentID, like='like'):
	sql """
		SELECT SUM(username) FROM commentlikes
		WHERE (type=%s AND commentID = %s)"""
	cursor.execute(sql, (like, commentID))
	result = cursor.fetchone()
	return result[0]

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



if __name__ == "__main__":
	db, cursor = connectdb()
	# create a user
	# create_user(cursor, db, 'matt', 'password', 'matt@uni.init')
	# create_post(cursor, db, 'matt', 'hello')
	# add_comment(2, 'matt', 'this is shit', cursor, db)
	# add_comment_like(3, 'matt', 'dislike', cursor, db)
	print(get_user_details(cursor, 'matt'))
