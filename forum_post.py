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
        self.forum_comments = []
        if (data != None):
            self.title = data[0]
            self.author = data[1]
            self.time_posted = data[2]
            self.content = data[3]
    
    def createPost(self, title: str, author: str, content: str):
        self.title = title
        self.author = author
        self.content = content
        self.time_posted = datetime.now(timezone.utc)
        
    def getTitle(self):
        return self.title

    def getAuthor(self):
        return self.author
    
    def getTimePosted(self):
        return self.time_posted
    
    def getContent(self):
        return self.content
    
    def populateComments(self, num: int, offset: int):

