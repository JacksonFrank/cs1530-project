from lctdb import LCTDB
import sys


if (len(sys.argv) == 3):
    db_connection = LCTDB(sys.argv[1], sys.argv[2])
else:
    print("Need to include username and password to database in cmd line arguments (Form: db_test.py <username> <password>")