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

def create_table_users(cursor):
	sql = """
		CREATE TABLE users (
			userID INT NOT NULL PRIMARY KEY,
			username VARCHAR(40),
			password VARCHAR(40),
			profilePic VARCHAR(60),
			url VARCHAR(60),
			followerCount INT,
			followingCount INT,
			spotifyID INT
		)"""
	cursor.execute(sql)
	print('users table created')

def create_table_posts(cursor):
	sql = """
		CREATE TABLE posts (
			postID INT NOT NULL PRIMARY KEY,
			createdAt DATETIME,
			postText VARCHAR(500),
			profilePic VARCHAR(60),
			postContent VARCHAR(60),
			user_id INT,
			likes INT,
			FOREIGN KEY(user_id) REFERENCES users(userID)
			)"""
	cursor.execute(sql)
	print('posts table created')

#creating like table for normalisation
def create_table_like(cursor):
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
def create_table_comments(cursor):
	sql = """
		CREATE TABLE comments(
			commentID INT NOT NULL,
			postID INT NOT NULL,
			userID INT NOT NULL,
			commentText VARCHAR(200),
			PRIMARY KEY (commentID),
			FOREIGN KEY (postID) REFERENCES posts(postID),
			FOREIGN KEY (userID) REFERENCES users(userID)
			)"""
	cursor.execute(sql)
	print('added comments table')



db, cursor = connectdb()
create_table_users(cursor)
create_table_posts(cursor)
create_table_like(cursor)


create_table_comments(cursor)

db.commit()
db.close()