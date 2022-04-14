from lctdb import LCTDB
import sys


if (len(sys.argv) == 3):
    db_connection = LCTDB(sys.argv[1], sys.argv[2])
else:
    print("Need to include username and password to database in cmd line arguments (Form: db_test.py <username> <password>")
    sys.exit()

db_connection.registerUser("jackson", "abc123")
print("auth with right credentials: " + str(db_connection.authenticateUser("jackson", "abc123")))
print("auth with wrong credentials: " + str(db_connection.authenticateUser("jackson", "wrongpassword")))

db_connection.closeCon()