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
	cursor.execute(sql, (postid, ))
	result = cursor.fetchall()
	return result

db, cursor = connectdb()
print(get_post_details(2))

db.close()