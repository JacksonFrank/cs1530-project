# Class for accessing application database
# Dependency: pip install psycopg2-binary

import psycopg2

class LCTDB: 

    # initalizing this class will create a new connection to the database
    def __init__(self, username: str, password: str):
        print("Initializing database connection...")

        try:
            self.con = psycopg2.connect("dbname=lctdb user=" + username + " password=" + password + " host=localhost")
        except:
            sys.exit("Could not connect to the database")
        
        print("Connected to Database!")

    # closes the connection to the database
    def closeCon(self):
        self.con.close()
    
    # registers a new user to the database
    # make sure not to register a user that has already been registered!
    def registerUser(self, username: str, password: str):
        cur = self.con.cursor()
        sql = """CALL register_user(%s, %s);"""

        try:
            cur.execute(sql, (username, password))
        except:
            print("could not register user " + username)

        self.con.commit()
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
    def getQuizesCompleted(self, username: str):
        cur = self.con.cursor()
        result = -1
        sql = """SELECT QUIZES_COMPLETED FROM LCTUSER WHERE USERNAME = %s;"""
        try:
            cur.execute(sql, (username,))
            result = cur.fetchone()[0]
        except:
            print("error retrieving the amount of quizzes " + username + " completed")

        cur.close()
        return result
