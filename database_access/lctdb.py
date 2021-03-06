# Class for accessing application database
# Dependency: pip install psycopg2-binary

import psycopg2
from datetime import datetime, timezone
import sys

from configparser import ConfigParser

class LCTDB: 

    # initalizing this class will create a new connection to the database
    def __init__(self):
        print("Initializing database connection...")

        # this is a hardcoded solution, might want to change this
        parser = ConfigParser()
        parser.read('config/database.ini')
        params = parser.items('postgresql')
        db_params = {}
        for param in params:
            db_params[param[0]] = param[1]

        try:
            self.con = psycopg2.connect(**db_params)
        except:
            sys.exit("Could not connect to the database")
        
        print("Connected to Database!")

    # closes the connection to the database
    def closeCon(self):
        self.con.close()


    '''
    ---------------------------------------------------------------------------------------------
    USER DATABASE
    ---------------------------------------------------------------------------------------------
    '''
  
    # registers a new user to the database
    # make sure not to register a user that has already been registered!
    # username at most can be 20 characters
    def registerUser(self, username: str, password: str):
        cur = self.con.cursor()
        sql = """CALL register_user(%s, %s);"""

        try:
            cur.execute(sql, (username, password))
            self.con.commit()
        except:
            print("could not register user " + username)

        cur.close()

    # authenticates a user's credentials
    # returns true if the given credentials are accurate, false otherwise
    # returns false if an error occured
    def authenticateUser(self, username: str, password: str):
        cur = self.con.cursor()
        result = False

        try:
            cur.callproc('authenticate_user', (username, password))
            result = cur.fetchone()[0]
        except:
            print("error authenticating user " + username)

        cur.close()
        return result

    # checks to see if a user exists
    # returns true if the given user has been registered, false otherwise
    # return false if an error occured
    def doesUserExist(self, username: str):
        cur = self.con.cursor()
        result = []
        sql = """SELECT * FROM LCTUSER WHERE USERNAME = %s;"""
        
        try:
            cur.execute(sql, (username,))
            result = cur.fetchall()
        except:
            print("error checking if " + username + " exists")

        cur.close()
        return len(result) >= 1
    
    # checks to see the number of quizzes completed by the given user
    # returns the number of quizzes completed
    # returns -1 if an error occured
    def getQuizzesCompleted(self, username: str):
        cur = self.con.cursor()
        result = -1
        sql = """SELECT QUIZZES_COMPLETED FROM LCTUSER WHERE USERNAME = %s;"""

        try:
            cur.execute(sql, (username,))
            result = cur.fetchone()[0]
        except:
            print("error retrieving the amount of quizzes " + username + " completed")

        cur.close()
        return result
    
    # saves that the given user has completed the given amount of quizzes in the database
    def quizCompleted(self, username: str, quizzesCompleted: int):
        cur = self.con.cursor()
        sql = """UPDATE LCTUSER SET quizzes_completed = %s WHERE username = %s;"""

        try:
            cur.execute(sql, (quizzesCompleted, username))
            self.con.commit()
        except:
            print("Couldn't update " + username + " quiz taken count")
        
        cur.close()

    # removes the given user from the database
    # will also remove all of the user's posts and comments, and all comments of the user's posts
    def deleteUser(self, username: str):
        cur = self.con.cursor()
        usr_sql = """DELETE FROM LCTUSER WHERE USERNAME = %s;"""
        post_sql = """DELETE FROM FORUM_POST WHERE AUTHOR = %s;"""
        comment_sql = """DELETE FROM FORUM_COMMENT WHERE AUTHOR = %s OR POST_AUTHOR = %s;"""

        try:
            cur.execute(comment_sql, (username, username))
            cur.execute(post_sql, (username,))
            cur.execute(usr_sql, (username,))
            self.con.commit()
        except:
            print("error deleting the user " + username)

        cur.close()


    '''
    ---------------------------------------------------------------------------------------------
    FORUM DATABASE
    ---------------------------------------------------------------------------------------------
    '''

    # add a forum post to the database
    # automatically generates current timestamp for post
    # title at most can be 140 characters
    def createForumPost(self, title: str, author: str, post_time: datetime, content: str):
        cur = self.con.cursor()
        current_time = datetime.now(timezone.utc)
        sql = """INSERT INTO FORUM_POST VALUES (%s, %s, %s, %s);"""

        try:
            cur.execute(sql, (title, author, post_time, content))
            self.con.commit()
        except:
            print("error saving forum post: " + title + " by " + author)

        cur.close()

    # add a comment to a forum post in the database
    # automatically generates current timestamp for comment
    # must provide the title, author, and timestamp of a valid post
    def createForumComment(self, author: str, comment_time: datetime, content: str, post_title: str, post_author: str, post_time: datetime):
        cur = self.con.cursor()
        sql = """INSERT INTO FORUM_COMMENT VALUES (%s, %s, %s, %s, %s, %s);"""

        try:
            cur.execute(sql, (author, comment_time, content, post_title, post_author, post_time))
            self.con.commit()
        except:
            print("error saving forum comment on " + post_title + " by " + author)
        
        cur.close()

    # retrieves a specific post based on its title, author, and timestamp
    def getPost(self, title: str, author: str, time_posted: datetime):
        cur = self.con.cursor()
        sql = """SELECT * FROM FORUM_POST WHERE title = %s AND author = %s AND time_posted = %s;"""
        result = None

        try:
            cur.execute(sql, (title, author, time_posted))
            result = cur.fetchone()
        except:
            print("error retrieving post " + title + " by " + author)
        
        cur.close()
        return result

    # retrieves recent posts from the database
    # retrieves only up to the given limit number of posts, default limit is 10
    # will skip the given start amount of posts when retrieving most recent posts, default start is 0
    # returns empty if there are no posts found
    # returns None if there was an error
    def getRecentPosts(self, limit: int = 10, start: int = 0):
        cur = self.con.cursor()
        sql = """SELECT * FROM FORUM_POST ORDER BY time_posted DESC LIMIT %s OFFSET %s;"""
        result = None

        try:
            cur.execute(sql, (limit, start))
            result = cur.fetchall()
        except:
            print("error retrieving recent posts")
        
        cur.close()
        return result
    
    # retrieves recent comments of the given post from the database
    # retrieves only up to the given limit number of comments, default limit is 10
    # will skip the given start amount of comments when retrieving most recent comments, default start is 0
    # returns empty if there are no comments found
    # returns None if there was an error
    def getRecentComments(self, post_title: str, post_author: str, post_time: datetime, limit: int = 10, start: int = 0):
        cur = self.con.cursor()
        sql = """SELECT author, time_commented, content FROM FORUM_COMMENT WHERE post_title = %s AND post_author = %s AND post_time = %s ORDER BY time_commented DESC LIMIT %s OFFSET %s;"""
        result = None
        
        try:
            cur.execute(sql, (post_title, post_author, post_time, limit, start))
            result = cur.fetchall()
        except:
            print("error retrieving recent comments for post " + post_title + " by " + post_author)
        
        cur.close()
        return result

    # retrieves a given comment from the given post from the database
    # returns none if an error occurs
    def getComment(self, post_title: str, post_author: str, post_time: str, author: str, time_commented: str):
        cur = self.con.cursor()
        sql = """SELECT author, time_commented, content FROM FORUM_COMMENT
                 WHERE post_title = %s AND post_author = %s AND post_time = %s AND
                 author = %s AND time_commented = %s;"""
        result = None

        try:
            cur.execute(sql, (post_title, post_author, post_time, author, time_commented))
            result = cur.fetchone()
        except:
            print("error retrieving comment on " + post_title + " by " + author)
        
        cur.close()
        return result
    
    # deletes the given post from the database
    # will also delete all of the comments on the given post
    def deletePost(self, title: str, author: str, post_time: datetime):
        cur = self.con.cursor()
        comment_sql = """DELETE FROM FORUM_COMMENT WHERE post_title = %s AND post_author = %s AND post_time = %s;"""
        post_sql = """DELETE FROM FORUM_POST WHERE title = %s AND author = %s AND time_posted = %s;"""
        
        try:
            cur.execute(comment_sql, (title, author, post_time))
            cur.execute(post_sql, (title, author, post_time))
            self.con.commit()
        except:
            print("error deleting post " + title + " by " + author)
        
        cur.close()
    
    # delete a comment from a post
    def deleteComment(self, author: str, time_commented: datetime, post_title: str, post_author: str, post_time: datetime):
        cur = self.con.cursor()
        sql = """DELETE FROM FORUM_COMMENT WHERE author = %s AND time_commented = %s AND post_title = %s AND post_author = %s AND post_time = %s;"""

        try:
            cur.execute(sql, (author, time_commented, post_title, post_author, post_time))
            self.con.commit()
        except:
            print("error deleting comment on " + post_title + " by " + author)

        cur.close()   

    '''
    ---------------------------------------------------------------------------------------------
    QUIZ DATABASE
    ---------------------------------------------------------------------------------------------
    '''

    # Gets translation pairs to act as quiz questions of given level
    # Returns translation pairs
    # Returns null if there was an error
    def getQuizQuestions(self, level: int):
        cur = self.con.cursor()
        sql = """SELECT english_tr, mandarin_tr FROM QUIZ WHERE level = %s ORDER BY RANDOM();"""
        result = None

        try:
            cur.execute(sql, (level,))
            result = cur.fetchall()
        except:
            print("error retrieving quiz questions")
        
        cur.close()
        return result
    
    # Gets the specified number of random quiz answers for a certain kind of translation answer excluding the given right answer
    # Returns the random quiz answers
    # Returns None if there was an error
    # May return less answers than specified if the Quiz table doesn't have enough translation pairs
    def getRandomAnswers(self, english_ans: bool, correct_ans: str, num_ans: int):
        cur = self.con.cursor()
        sql = """"""
        if (english_ans):
            sql = """SELECT english_tr FROM QUIZ WHERE english_tr != %s ORDER BY RANDOM() LIMIT %s;"""
        else:
            sql = """SELECT mandarin_tr FROM QUIZ WHERE mandarin_tr != %s ORDER BY RANDOM() LIMIT %s;"""
        result = None

        try:
            cur.execute(sql, (correct_ans, num_ans))
            result = cur.fetchall()
        except:
            print("error retrieving random quiz answers")
        
        cur.close()
        return result




