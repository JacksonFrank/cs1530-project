# Class for accessing application database
# Dependency: pip install psycopg2-binary

import psycopg2

class LCTDB: 

    def __init__(self, username: str, password: str):
        print("Initializing database connection...")

        try:
            self.con = psycopg2.connect("dbname=lctdb user=" + username + " password=" + password + " host=localhost")
        except:
            sys.exit("Could not connect to the database")
        
        print("Connected to Database!")

    def closeCon(self):
        self.con.close()
    
    def registerUser(self, username: str, password: str):
        cur = self.con.cursor()
        sql = """CALL register_user(%s, %s);"""
        cur.execute(sql, (username, password))
        self.con.commit()
        cur.close()

    def authenticateUser(self, username: str, password: str):
        cur = self.con.cursor()
        cur.callproc('authenticate_user', (username, password))
        result = cur.fetchall()
        print(result)
        cur.close()