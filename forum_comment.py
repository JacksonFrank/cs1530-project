from datetime import datetime, timezone

class ForumComment:

    # will initialize with data if retrieving from database
    # if this object is a brand new comment, don't need to initialize with data, instead use setting methods below
    def __init__(self, data = None):
        self.author = None
        self.time_commented = None
        self.content = None
        if (data != None):
            self.author = data[0]
            self.time_commented = data[1]
            self.content = data[2]
    
    # Initializes comment data for this instance of a forum comment
    # Doesn't save the comment to the database
    def createComment(self, author: str, content: str):
        self.author = author
        self.time_commented = datetime.now(timezone.utc)
        self.content = content
    
    def getAuthor(self):
        return self.author 
    def getTimeCommented(self):
        return self.time_commented
    def getContent(self):
        return self.content

    