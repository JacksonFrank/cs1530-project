from lctdb import LCTDB
import sys
from datetime import datetime, timezone


if (len(sys.argv) == 3):
    db_connection = LCTDB(sys.argv[1], sys.argv[2])
else:
    print("Need to include username and password to database in cmd line arguments (Form: db_test.py <username> <password>")
    sys.exit()

print("does the user we're about to create exist?: " + str(db_connection.doesUserExist('jackson')))
db_connection.registerUser('jackson', 'abc123')
print("does the user we just created exist?: " + str(db_connection.doesUserExist('jackson')))
print("auth with right credentials: " + str(db_connection.authenticateUser('jackson', 'abc123')))
print("auth with wrong credentials: " + str(db_connection.authenticateUser('jackson', 'wrongpassword')))
print("number of quizzes the user has completed: " + str(db_connection.getQuizzesCompleted('jackson')))
db_connection.quizCompleted('jackson', 1)
print("number of quizzes the user has completed after completing the first quiz: " + str(db_connection.getQuizzesCompleted('jackson')))
db_connection.createForumPost('Post1', 'jackson', 'this is my first post!')
db_connection.createForumPost('Post2', 'jackson', 'this is my second post!')
print("the posts the user just made:")
posts = db_connection.getRecentPosts()
print(posts)
db_connection.createForumComment('jackson', 'this is a comment on post 1!', posts[1][0], posts[1][1], posts[1][2])
db_connection.createForumComment('jackson', 'this is another comment on post 1!', posts[1][0], posts[1][1], posts[1][2])
comments = db_connection.getRecentComments(posts[1][0], posts[1][1], posts[1][2])
print("the comments on post 1 the user just made:")
print(comments)
db_connection.deleteComment('jackson', comments[0][1], posts[1][0], posts[1][1], posts[1][2])
new_comments = db_connection.getRecentComments(posts[1][0], posts[1][1], posts[1][2])
print("comments after 1 comment was deleted:")
print(new_comments)
db_connection.deletePost(posts[1][0], posts[1][1], posts[1][2])
new_posts = db_connection.getRecentPosts()
print("posts after 1 post was deleted:")
print(new_posts)


db_connection.deleteUser('jackson')
print("does the user we just deleted exist?: " + str(db_connection.doesUserExist('jackson')))


db_connection.closeCon()