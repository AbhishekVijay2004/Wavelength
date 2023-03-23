import mysql.connector

def connectdb():
	db = mysql.connector.connect(
		host="dbhost.cs.man.ac.uk",
		user="u38792zm",
		password="databasepassword",
		database="2022_comp10120_z11"
		)

	cursor = db.cursor()
	return db, cursor


def create_user(cursor, db, username, password, email, profilePic=None, bio=None, topsong=None, displayname=""):
	# if displayname == None:
	# 	displayname = username
	sql = """
		INSERT INTO users (username, password, profilePic, email, bio, topsong, displayname)
		VALUES (%s, %s, %s, %s, %s, %s, %s)"""
	cursor.execute(sql, (username, password, profilePic, email, bio, topsong, displayname))
	db.commit()
	print('user added')

def delete_user(cursor, db, username):
	username = (username, )
	sql = """
		DELETE FROM users
		WHERE username = %s"""
	cursor.execute(sql, username)
	db.commit()
	print('user deleted')

def create_post(cursor, db, username, postText='', postContent='', noLike='1', noDislike='1', noComment='1'):
	sql = """
		INSERT INTO posts (username, postText, postContent, createdAt, noLike, noDislike, noComment)
		VALUES (%s, %s, %s, NOW(), %s, %s, %s)"""
	cursor.execute(sql, (username, postText, postContent, noLike, noDislike, noComment))
	db.commit()

def delete_post(cursor, db, postID):
	#make a tuple value
	postID = (postID, )
	sql = """
		DELETE FROM posts
		WHERE postID = %s"""
	cursor.execute(sql, postID)
	db.commit()

def add_like(cursor, db, postID, username):
	#No longer required as handled on frontend:
	#delete_like(cursor, db, postID, username)
	sql = """
		INSERT INTO likes(postID, username, type)
		VALUES (%s, %s, 'like')"""
	cursor.execute(sql, (postID, username))
	db.commit()
	print(f'{username} liked {postID}')

def delete_like(cursor, db, postID, username):
	## will function for both like and dislike
	sql = """
		DELETE FROM likes
		WHERE (postID = %s) AND (username = %s)"""
	cursor.execute(sql, (postID, username))
	db.commit()
	print('like deleted')

def add_dislike(cursor, db, postID, username):
	#No longer required as handled on frontend:
	#delete_like(cursor, db, postID, username)
	sql = """
		INSERT INTO likes(postID, username, type)
		VALUES (%s, %s, 'dislike')"""
	cursor.execute(sql, (postID, username))
	db.commit()
	print(f'{username} disliked {postID}')

def add_comment(cursor, db, postID, username, text):
	sql = """
		INSERT INTO comments(postID, username, commentText, createdAt)
		VALUES (%s, %s, %s, NOW())"""
	cursor.execute(sql, (postID, username, text))
	db.commit()
	print(f'{username} commented {text} on {postID}')

def delete_comment(cursor, db, commentID):
	commentID = (commentID, )
	sql = """
		DELETE FROM comments
		WHERE (commentID = %s)"""
	cursor.execute(sql, commentID)
	db.commit()
	print(f'comment {commentID[0]} deleted')

def add_comment_like(cursor, db, commentID, username, liketype):
	delete_comment_like(commentID, username, cursor, db)
	sql = """
		INSERT INTO commentlikes(commentID, username, type)
		VALUES (%s, %s, %s)"""
	cursor.execute(sql, (commentID, username, liketype))
	db.commit()

def delete_comment_like(cursor, db, commentID, username):
	## will function for both like and dislike
	sql = """
		DELETE FROM commentlikes
		WHERE (commentID = %s) AND (username = %s)"""
	cursor.execute(sql, (commentID, username))
	db.commit()
	print('like deleted')

def add_follow(cursor, db, user, following):
	sql = """
		INSERT INTO following(user, following)
		VALUES (%s, %s)"""
	cursor.execute(sql, (user, following))
	db.commit()
	print(f'{user} followed {following}')

def delete_follow(cursor, db, user, following):
	sql = """
		DELETE FROM following
		WHERE (user = %s) AND (following = %s)"""
	cursor.execute(sql, (user, following))
	db.commit()
	print('friendship deleted')

def alter_user(cursor, db, username, key, value):
	sql = f"""
		UPDATE users
		SET {key} = %s
		WHERE (username = %s)"""
	cursor.execute(sql, (value, username))
	db.commit()
	print(f'{key} changed to {value}')

def get_user_detail(cursor, username, param='*'):
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
		elif (param != '*'):
			return result[0]
		return result

def get_user_details(cursor, username):
	sql = """
		SELECT * FROM users
		WHERE (username = %s)"""
	cursor.execute(sql, (username, ))
	result = cursor.fetchall()
	try:
		return result[0]
	except IndexError:
		return False

def get_user_details_by_email(cursor, email):
	sql = """
		SELECT * FROM users
		WHERE (email = %s)"""
	cursor.execute(sql, (email, ))
	result = cursor.fetchall()
	print(result)
	try:
		return result[0]
	except IndexError:
		return False

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
	elif param != '*':
		if param == "createdAt":
			sql = f"""
				SELECT DATE_FORMAT(createdAt, '%d/%m/%y %H:%i') from comments
				WHERE (commentID = %s)"""
			cursor.execute(sql, (commentid, ))
			result = cursor.fetchone()
			return result
		else:
			sql = f"""
				SELECT {param} from comments
				WHERE (commentID = %s)"""
			cursor.execute(sql, (commentid, ))
			result = cursor.fetchone()
			return result
	else:
		sql = """
			SELECT commentID, postID, username, commentText, DATE_FORMAT(createdAt, '%d/%m/%y %H:%i') FROM comments
			WHERE (commentID = %s)"""
		cursor.execute(sql, (commentid, ))
		result = cursor.fetchall()
		return result

def get_post_comments(cursor, db, postID):
	sql = f"""
		SELECT commentID from comments
		WHERE (postID = %s)"""
	cursor.execute(sql, (postID, ))
	result = cursor.fetchall()
	return result

##get list of users posts
def list_user_posts(cursor, username):
	sql = """
		SELECT postID, DATE_FORMAT(createdAt, '%d/%m/%y %H:%i'), postText, postContent, username, noLike, noDislike, noComment FROM posts
		WHERE (username = %s)
		ORDER BY createdAt DESC"""
	cursor.execute(sql, (username, ))
	result = cursor.fetchall()
	return result

def get_num_comments(cursor, db, postid):
	# get number of comments
	sql = """
		SELECT COUNT(commentID) FROM comments
		WHERE (postID = %s)"""
	cursor.execute(sql, (postid, ))
	result = cursor.fetchone()
	return result[0]

def get_num_likes(cursor, db, postid, like='like'):
	# get num likes or dislikes depending on parameter passed
	sql = """
		SELECT COUNT(username) FROM likes
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
	sql = """
		SELECT COUNT(username) FROM commentlikes
		WHERE (type=%s AND commentID = %s)"""
	cursor.execute(sql, (like, commentID))
	result = cursor.fetchone()
	return result[0]

def get_num_following(cursor, username):
	sql = """
		SELECT COUNT(following) FROM following
		WHERE (user = %s)"""
	cursor.execute(sql, (username, ))
	results = cursor.fetchone()
	return results[0]

def get_following_accounts(cursor, username):
	sql = """
		SELECT following FROM following
		WHERE (user = %s)"""
	cursor.execute(sql, (username, ))
	results = cursor.fetchall()
	accounts = [result[0] for result in results]
	return accounts

def get_num_followers(cursor, username):
	sql = """
		SELECT COUNT(user) FROM following
		WHERE (following = %s)"""
	cursor.execute(sql, (username, ))
	results = cursor.fetchone()
	return results[0]

def get_follower_accounts(cursor, username):
	sql = """
		SELECT user FROM following
		WHERE (following = %s)"""
	cursor.execute(sql, (username, ))
	results = cursor.fetchall()
	accounts = [result[0] for result in results]
	return accounts

def create_notification(cursor, db, recipient, sender, type, postID=None):
	sql = """
		INSERT INTO notifications (recipient, sender, type, postID)
		VALUES(%s, %s, %s, %s)"""
	cursor.execute(sql, (recipient, sender, type, postID))
	db.commit()

def view_notifications(cursor, recipient):
	sql = """
		SELECT * FROM notifications
		WHERE (recipient = %s)"""
	cursor.execute(sql, (recipient, ))
	result = cursor.fetchall()
	return result

def delete_notification(cursor, db, notificationID):
	sql = """
		DELETE FROM notifications
		WHERE (notificationID = %s)"""
	cursor.execute(sql, (notificationID, ))
	db.commit()

def search_for_user(cursor, query, username):
	sql = """
		SELECT users.* FROM users
		LEFT JOIN following ON users.username = following.following AND following.user = %s
		WHERE (username like %s AND following.following IS NULL AND username != %s)
		ORDER BY (username)
		LIMIT 20"""
	cursor.execute(sql, (username, query + '%', username))
	result = cursor.fetchall()
	return result


def get_num_posts(cursor, username):
	sql = """
		SELECT COUNT(postID) FROM posts
		WHERE (username = %s)"""
	cursor.execute(sql, (username, ))
	result = cursor.fetchone()
	return result[0]

def get_num_likes_received(cursor, username, type = 'like'):
	sql = """
		SELECT COUNT(likes.username) FROM likes
		INNER JOIN posts ON posts.postID = likes.postID
		WHERE (posts.username = %s AND type = %s)"""
	cursor.execute(sql, (username, type))
	result = cursor.fetchone()
	return result[0]

def get_num_comments_received(cursor, username):
	sql = """
		SELECT COUNT(comments.commentID) FROM comments
		INNER JOIN posts ON posts.postID = comments.postID
		WHERE (posts.username = 'matt')"""
	# cursor.execute(sql, (username, ))
	cursor.execute(sql)
	result = cursor.fetchone()
	return result[0]

if __name__ == "__main__":
	db, cursor = connectdb()
	# create a user
	# create_user(cursor, db, 'matt', 'password', 'matt@uni.init')
	# create_post(cursor, db, 'matt', 'hello')
	# add_comment(2, 'matt', 'this is shit', cursor, db)
	# add_comment_like(3, 'matt', 'dislike', cursor, db)
	# print(get_user_details(cursor, 'matt'))
	# print(get_user_details_by_email(cursor, 'jonny.breeze2003@gmail.com'))
	# create_notification(cursor, db, 'matt', 'jonnytest', 'follow')
	# create_notification(cursor, db, 'matt', 'jonnytest', 'comment', '2')
	# print(view_notifications(cursor, 'matt'))
	# print(get_user_details(cursor, 'atsu'))
	# print(search_for_user(cursor, "jon"))
	# add_follow('test', 'jonnybreez3', cursor, db)
	# print(get_following_posts(cursor, 'jonnybreez3', 0))
	# print(get_num_comments(cursor, db, 2))
	# print(get_num_comment_likes(cursor, db, 3, 'dislike'))
	# print(get_num_posts(cursor, 'matt'))

	# add_like(cursor, db, 2, 'jonnybreez3')
	# add_like(cursor, db, 2, 'jonnytest')
	# print(get_num_likes_received(cursor, 'matt', 'like'))
	# print(get_num_comments_received(cursor, 'matt'))
	# print(list_user_posts(cursor, 'jonnybreez3'))
	create_notification(cursor, db, 'testusername', 'matt', 'comment', '2')
