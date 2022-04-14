from lctdb import LCTDB
import sys


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
print("amount of quizzes the user has completed: " + str(db_connection.getQuizesCompleted('jackson')))

db_connection.closeCon()