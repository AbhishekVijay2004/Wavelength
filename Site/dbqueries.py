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

def get_user_details(username, param='*'):
	global cursor
	if param not in ['username', 'password', 'profilePic', 'url', 'spotifyID', '*']:
		return 'invalid query'
	else:
		sql = f"""
			SELECT {param} FROM users
			WHERE (username = %s)"""
		cursor.execute(sql, (username, ))
		result = cursor.fetchone()
		return result

def get_post_details(postid, param='*'):
	global cursor
	if param not in ['createdAt', 'postText', 'postContent', 'username', '*']:
		return 'invalid query'
	else:
		sql = f"""
			SELECT {param} from posts
			WHERE (postID = %s)"""
		cursor.execute(sql, (postid, ))
		result = cursor.fetchone()
		return result

def get_comment_details(commentid, param='*'):
	global cursor
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
def list_user_posts(username):
	global cursor
	sql = """
		SELECT * FROM posts
		WHERE (username = %s)"""
	cursor.execute(sql, (username, ))
	result = cursor.fetchall()
	return result

def get_num_likes(postid, like='like'):
	# get num likes or dislikes depending on parameter passed
	global cursor
	sql = """
		SELECT SUM(postID) FROM likes
		WHERE (type = %s AND postID = %s)"""
	cursor.execute(sql, (like, postid))
	result = cursor.fetchone()
	return result[0]


def get_like_accounts(postid, like='like'):
	global cursor
	sql = """
		SELECT username FROM likes
		WHERE (type=%s AND postID = %s)"""
	cursor.execute(sql, (like, postid))
	results = cursor.fetchall()
	# change into list of usernames
	accounts = [result[0] for result in results]
	return accounts

def get_num_following(username):
	global cursor
	sql = """
		SELECT SUM(username) FROM following
		WHERE (followerID = %s)"""
	cursor.execute(sql, (username, ))
	results = cursor.fetchone()
	return results[0]

def get_following_accounts(username):
	global cursor
	sql = """
		SELECT username FROM following
		WHERE (followerID = %s)"""
	cursor.execute(sql, (username, ))
	results = cursor.fetchall()
	accounts = [result[0] for result in results]
	return accounts

def get_num_followers(username):
	global cursor
	sql = """
		SELECT SUM(followerID) FROM following
		WHERE (username = %s)"""
	cursor.execute(sql, (username, ))
	results = cursor.fetchone()
	return results[0]

def get_follower_accounts(username):
	global cursor
	sql = """
		SELECT followerID FROM following
		WHERE (username = %s)"""
	cursor.execute(sql, (username, ))
	results = cursor.fetchall()
	accounts = [result[0] for result in results]
	return accounts



if __name__ == "__main__":
	db, cursor = connectdb()


	print(get_num_followers(2))
	print(get_follower_accounts(2))


	db.close()