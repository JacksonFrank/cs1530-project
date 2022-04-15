from database_access.lctdb import LCTDB
from datetime import datetime, timezone
from forum_comment import ForumComment

class ForumPost:

    # will initialize with data if retrieving from database
    # if this object is a brand new post, don't need to initialize with data, instead use createPost method
    def __init__(self, data = None):
        self.title = None
        self.author = None
        self.time_posted = None
        self.content = None
        if (data != None):
            self.title = data[0]
            self.author = data[1]
            self.time_posted = data[2]
            self.content = data[3]
    
    # initializes post with required data (title, author, and content)
    # automatically sets post creation time
    # saves post to the database
    def createPost(self, title: str, author: str, content: str):
        self.title = title
        self.author = author
        self.content = content
        self.time_posted = datetime.now(timezone.utc)

        db_connection = LCTDB()
        db_connection.createForumPost(title, author, self.time_posted, content)
        db_connection.closeCon()
        
    def getTitle(self):
        return self.title
    def getAuthor(self):
        return self.author   
    def getTimePosted(self):
        return self.time_posted   
    def getContent(self):
        return self.content
    
    # gets the most recent comments made on this post
    # set num to the number of comments to be returned
    # set offset to skip those amount of most recent comments
    # returns a list of ForumComment objects
    def getRecentComments(self, num: int = 10, offset: int = 0):
        db_connection = LCTDB()
        result = db_connection.getRecentComments(self.title, self.author, self.time_posted, num, offset)
        comments = []
        for comment_data in result:
            comments.append(ForumComment(comment_data))
        db_connection.closeCon()
        return comments
    
    # adds the given comment to this post
    # saves the comment to the database
    def addComment(self, comment: ForumComment):
        db_connection = LCTDB()
        db_connection.createForumComment(comment.getAuthor(), comment.getTimeCommented(), comment.getContent(), self.title, self.author, self.time_posted)
        db_connection.closeCon()

    # deletes this post from the database
    def deletePost(self):
        db_connection = LCTDB()
        db_connection.deletePost(self.title, self.author, self.time_posted)
        db_connection.closeCon()

    # deletes the given comment from the database
    def deleteComment(self, comment: ForumComment):
        db_connection = LCTDB()
        db_connection.deleteComment(comment.getAuthor(), comment.getTimeCommented(), self.title, self.author, self.time_posted)
        db_connection.closeCon()

    # static method to retrieve the most recent posts from the database
    # set num to the number of posts to be returned
    # set offset to skip those amount of most recent posts
    # returns a list of ForumPost objects
    @staticmethod
    def getRecentPosts(num: int = 10, offset: int = 0):
        db_connection = LCTDB()
        post_data = db_connection.getRecentPosts()
        posts = []
        for post_info in post_data:
            posts.append(ForumPost(post_info))
        db_connection.closeCon()
        return posts

    # static method to retrieve a specific post based on its title, author, and timestamp
    # returns a ForumPost object
    @staticmethod
    def getPost(title: str, author: str, time_posted: datetime):
        db_connection = LCTDB()
        post_data = db_connection.getPost(title, author, time_posted)
        db_connection.closeCon()
        return ForumPost(post_data)
    

