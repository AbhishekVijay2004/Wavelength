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


def create_table_users():
	global cursor
	sql = """
		CREATE TABLE users (
			userID INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
			username VARCHAR(40) NOT NULL,
			password VARCHAR(40) NOT NULL,
			profilePic VARCHAR(60),
			url VARCHAR(60),
			spotifyID int
			)"""
	cursor.execute(sql)
	print('Users table created')

def create_table_posts():
	global cursor
	sql = """
		CREATE TABLE posts (
			postID INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
			createdAt DATETIME,
			postText VARCHAR(500),
			postContent VARCHAR(60),
			userID INT,
			FOREIGN KEY(userID) REFERENCES users(userID)
			)"""
	cursor.execute(sql)
	print('posts table created')

#creating like table for normalisation
def create_table_like():
	global cursor
	sql = """
		CREATE TABLE likes (
			postID INT NOT NULL,
			userID INT NOT NULL,
			type VARCHAR(10),
			PRIMARY KEY (postID, userID),
			FOREIGN KEY(postID) REFERENCES posts(postID),
			FOREIGN KEY (userID) REFERENCES users(userID)
			)"""
	cursor.execute(sql)
	print('added likes table')

#comment table
# primary key oof comment id as user could comment multiple times
# has postID and userID as foreigns for joins
def create_table_comments():
	global cursor
	sql = """
		CREATE TABLE comments(
			commentID INT AUTO_INCREMENT NOT NULL,
			postID INT NOT NULL,
			userID INT NOT NULL,
			commentText VARCHAR(200),
			PRIMARY KEY (commentID),
			FOREIGN KEY (postID) REFERENCES posts(postID),
			FOREIGN KEY (userID) REFERENCES users(userID)
			)"""
	cursor.execute(sql)
	print('added comments table')

def create_table_following():
	global cursor
	sql = """
		CREATE TABLE following(
			userID INT NOT NULL,
			followerID INT NOT NULL,
			PRIMARY KEY(userID, followerID),
			FOREIGN KEY(userID) REFERENCES users(userID),
			FOREIGN KEY (followerID) REFERENCES users(userID)
			)"""
	cursor.execute(sql)
	print('added following table')


def drop_all():
	global cursor
	for table in ['comments', 'likes', 'posts', 'users', 'following']:
		try:
			cursor.execute(f'DROP TABLE {table}')
		except:
			print("table doesn't exist")
	print('tables dropped')

db, cursor = connectdb()
drop_all()

create_table_users()
create_table_posts()
create_table_like()
create_table_comments()
create_table_following()


db.commit()
db.close()