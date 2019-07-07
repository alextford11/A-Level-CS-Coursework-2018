#imports sqlite3
import sqlite3
#imports date from datetime module
from datetime import date 
#imports timedelta from datetime module
from datetime import timedelta 
#creates a connection between sqlite3 and the database "DrivingInstructor.db"
connection2 = sqlite3.connect("DrivingInstructor.db") 
#creates a cursor for the connection to the database
c2 = connection2.cursor()  
#This is where i will manually change the number until 20, in future this would change depending on the new users id
instructor_ID = "20" 
#This creates the string schedule_ID which is the ID found in the driving instructors filter database
schedule_ID = "Table"+instructor_ID
#This creates the table, in the example, "Table1" which is the value of the schedule_ID variable. It makes a date...
#...and time1 to time9 field names. 
c2.execute("CREATE TABLE " +schedule_ID+ """(
Date NOT NULL,
Time1 NOT NULL,
Time2 NOT NULL,
Time3 NOT NULL,
Time4 NOT NULL,
Time5 NOT NULL,
Time6 NOT NULL,
Time7 NOT NULL,
Time8 NOT NULL,
Time9 NOT NULL)""")
#today is equal to the date that the code is run on
today = date.today()
#creates an empty list called datelist
datelist = []
#A for loop that iterates for 7 times 
for i in range(0,7):
#That date gets appended to the datelist list and the date increments by 1, next day, every iteration of the for loop. 
    datelist.append(str(today + timedelta(days=i)))
#Records is a array of tuples which holds all the data to be put into the schedule table
records = [(datelist[0], "false", "false", "false", "false", "false", "false", "false", "false", "false"),
           (datelist[1], "false", "false", "false", "false", "false", "false", "false", "false", "false"),
           (datelist[2], "false", "false", "false", "false", "false", "false", "false", "false", "false"),
           (datelist[3], "false", "false", "false", "false", "false", "false", "false", "false", "false"),
           (datelist[4], "false", "false", "false", "false", "false", "false", "false", "false", "false"),
           (datelist[5], "false", "false", "false", "false", "false", "false", "false", "false", "false"),
           (datelist[6], "false", "false", "false", "false", "false", "false", "false", "false", "false")]
#This inserts the values from records in the database which is called schedule_ID, this executes on many lines by...
#...using .executemany()
c2.executemany("INSERT INTO "+schedule_ID+" VALUES (?,?,?,?,?,?,?,?,?,?)",records)
#This saves the values written into the database
connection2.commit()
#This closes the connection between the sqlite3 and database
connection2.close()


