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
    
    def setAuthor(self, author: str):
        self.author = author
    def getAuthor(self):
        return self.author
    
    def createNow(self):
        self.time_commented = datetime.now(timezone.utc)
    def getTimeCommented(self):
        return self.time_commented

    def setContent(self, content: str):
        self.content = content
    def getContent(self):
        return self.content