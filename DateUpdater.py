#Imports sqlite3
import sqlite3
#Imports date from datetime module
from datetime import date 
#Imports timedelta from datetime module
from datetime import timedelta 
#Creates a connection between sqlite3 and the database "DrivingInstructor.db"
connection2 = sqlite3.connect("DrivingInstructor.db") 
#Creates a cursor for the connection to the database
c2 = connection2.cursor()
#This executes the SQL code which gets all the Schedule_IDs from the DIFilters Table
c2.execute("SELECT Schedule_ID FROM DIFilters;")
#All the data gathered by the above line gets stored in the list, ScheduleList
ScheduleList = c2.fetchall()
#Defines the procedure Date_Updater which requires some data in the parameters 
def Date_Updater(Table):
#today is equal to the date that the code is run on    
    today = date.today()

#Calculates the day befores date
    yesterdays_date = today + timedelta(days=-1) ####IF MESSED UP!!! MINUS HOW MANY DAYS YOU MISSED

#Executes the SQL code that deletes and records which have yesterdays date as the date 
    c2.execute("DELETE FROM "+Table+" WHERE Date='"+str(yesterdays_date)+"';")
    
#new_date holds the value of the date in 6 days time which is the 7th date in the database
    new_date = today + timedelta(days=6) ####IF MESSED UP!!! MINUS HOW MANY DAYS YOU MISSED
    
#new_record is the whole record that will be inserted into the database 
    new_record = (new_date, "false", "false", "false", "false", "false", "false", "false", "false", "false")
#This executes the SQL code which the above tuple is inserted into the table
    c2.execute("INSERT INTO "+Table+" VALUES (?,?,?,?,?,?,?,?,?,?)",new_record)
#This saves the values written into the database
    connection2.commit()
#For loop which ranges from 0 to the amount of records in the table DIFilters
for item in range(len(ScheduleList)):
#Calls the Date_Updater() with the value from the list of ScheduleList, the item increments by one...
#...so this allows the procedure to get the next table name 
    Date_Updater(ScheduleList[item][0])
#This saves the values written into the database
connection2.commit()
#This closes the connection between the sqlite3 and database
connection2.close()

