import sqlite3
#The module sqlite3 is imported.
connection1 = sqlite3.connect("StudentInfo.db")
#The access the database a connection must be made between sqlite3 and "StudentInfo.db".
c1 = connection1.cursor()
#c is a cursor to help ease of access to the database.
c1.execute("""CREATE TABLE StudentLogin 
(Student_ID INTEGER PRIMARY KEY,
Email,
Password)""")
#c.execute() is where you can input SQL into the brackets and it will run using sqlite3.
#CREATE TABLE creates a table by the name of he following string.
#Student_ID is the feild name, INTEGER defines it as a integer, PRIMARY KEY defines...
#...it as a primary key and increments by one when a new record in written in.
#Email and Password are default feild names which do not need to be altered. 
