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

def get_user_details(userid, param='*'):
	global cursor
	if param not in ['username', 'password', 'profilePic', 'url', 'spotifyID', '*']:
		return 'invalid query'
	else:
		sql = f"""
			SELECT {param} FROM users
			WHERE (userID = %s)"""
		cursor.execute(sql, (userid, ))
		result = cursor.fetchone()
		return result

def get_post_details(postid, param='*'):
	global cursor
	if param not in ['createdAt', 'postText', 'postContent', 'userID', '*']:
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
	if param not in ['userID', 'postID', 'commentText', '*']:
		return 'invalid query'
	else:
		sql = f"""
			SELECT {param} from comments
			WHERE (commentID = %s)"""
		cursor.execute(sql, (commentid, ))
		result = cursor.fetchone
		return result

##get list of users posts
def list_user_posts(userid):
	global cursor
	sql = """
		SELECT * FROM posts
		WHERE (userID = %s)"""
	cursor.execute(sql, (userid, ))
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
		SELECT userID FROM likes
		WHERE (type=%s AND postID = %s)"""
	cursor.execute(sql, (like, postid))
	results = cursor.fetchall()
	# change into list of userIDs
	accounts = [result[0] for result in results]
	return accounts

def get_num_following(userid):
	global cursor
	sql = """
		SELECT SUM(userID) FROM following
		WHERE (followerID = %s)"""
	cursor.execute(sql, (userid, ))
	results = cursor.fetchone()
	return results[0]

def get_following_accounts(userid):
	global cursor
	sql = """
		SELECT userID FROM following
		WHERE (followerID = %s)"""
	cursor.execute(sql, (userid, ))
	results = cursor.fetchall()
	accounts = [result[0] for result in results]
	return accounts

def get_num_followers(userid):
	global cursor
	sql = """
		SELECT SUM(followerID) FROM following
		WHERE (userID = %s)"""
	cursor.execute(sql, (userid, ))
	results = cursor.fetchone()
	return results[0]

def get_follower_accounts(userid):
	global cursor
	sql = """
		SELECT followerID FROM following
		WHERE (userID = %s)"""
	cursor.execute(sql, (userid, ))
	results = cursor.fetchall()
	accounts = [result[0] for result in results]
	return accounts



if __name__ == "__main__":
	db, cursor = connectdb()


	print(get_num_followers(2))
	print(get_follower_accounts(2))


	db.close()