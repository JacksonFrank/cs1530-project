# Class for accessing application database
# Dependency: pip install psycopg2-binary

import psycopg2

class LCTDB: 
    
    def __init__(self, username: str, password: str):
        print("Initializing database connection...")

        try:
            self.conn = psycopg2.connect("dbname=lctdb user=" + username + " password=" + password + " host=localhost")
        except:
            sys.exit("Could not connect to the database")
        
        print("Connected to Database!")
    
    