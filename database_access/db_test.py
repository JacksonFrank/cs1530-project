from lctdb import LCTDB
import sys
from datetime import datetime, timezone

sys.path.append("..")
from forum_post import ForumPost
from forum_comment import ForumComment

# gets an initial connection to the database
db_connection = LCTDB()

# checks if the user exists, then creates the user with a password, and checks to see if the user exists again
print("does the user we're about to create exist?: " + str(db_connection.doesUserExist('jackson')))
db_connection.registerUser('jackson', 'abc123')
print("does the user we just created exist?: " + str(db_connection.doesUserExist('jackson')))

# tries right and wrong credentials to authenticate the user that was just created
print("auth with right credentials: " + str(db_connection.authenticateUser('jackson', 'abc123')))
print("auth with wrong credentials: " + str(db_connection.authenticateUser('jackson', 'wrongpassword')))

# gets the amount of quizzes the user we just created has completed
print("number of quizzes the user has completed: " + str(db_connection.getQuizzesCompleted('jackson')))

# gets quiz questions of the given level, as well as other random answers
quiz_questions = db_connection.getQuizQuestions(1)
print("quiz questions for level 1:")
print(quiz_questions)
other_answers = db_connection.getRandomAnswers(True, quiz_questions[0][0], 3) # True indicates that we are looking for english answers, False would cause this to return mandarin answers
print("three other random answers besides " + quiz_questions[0][0] + ":")
print(other_answers)

# says that the user we created completed quiz 1
db_connection.quizCompleted('jackson', 1)
print("number of quizzes the user has completed after completing the first quiz: " + str(db_connection.getQuizzesCompleted('jackson')))

# create two posts and save them to the database
post1 = ForumPost()
post1.createPost('Post1', 'jackson', 'this is my first post!')
post2 = ForumPost()
post2.createPost('Post2', 'jackson', 'this is my second post!')

# retrieve the posts we just created from the database
print("the posts the user just made:")
retrieved_posts = ForumPost.getRecentPosts()
print(retrieved_posts)

# retrieving a specific post from the database again by having its title, author, and timestamp
requed_post = ForumPost.getPost(retrieved_posts[0].getTitle(), retrieved_posts[0].getAuthor(), retrieved_posts[0].getTimePosted())
print("original post: " + retrieved_posts[0].getTitle() + " by " + retrieved_posts[0].getAuthor())
print("re-queued post: " + requed_post.getTitle() + " by " + requed_post.getAuthor())

# create two comments and add them to the first post we created, saves comments to database
comment1 = ForumComment()
comment1.createComment('jackson', 'this is a comment on post1!')
post1.addComment(comment1)
comment2 = ForumComment()
comment2.createComment('jackson', 'this is another comment on post1!')
post1.addComment(comment2)

# retrieve the comments we just created from the database
retrieved_comments = post1.getRecentComments()
print("the comments on post 1 the user just made:")
print(retrieved_comments)

# delete the first comment we made on the 1st post from the database
post1.deleteComment(comment1)

# retrieve the comments from the database on post 1 again
new_retrieved_comments = post1.getRecentComments()
print("comments after 1 comment was deleted:")
print(new_retrieved_comments)

# deletes the first post that we made
post1.deletePost()

# retrieves the posts from the database again
new_retrieved_posts = ForumPost.getRecentPosts()
print("posts after 1 post was deleted:")
print(new_retrieved_posts)

# delete the user that we created from the database
# will also delete all forum entries in the database related to this user (authored posts and comments, comments made on posts that they authored)
db_connection.deleteUser('jackson')
print("does the user we just deleted exist?: " + str(db_connection.doesUserExist('jackson')))

# close the connection to the database
db_connection.closeCon()