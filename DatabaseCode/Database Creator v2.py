import sqlite3
connection1 = sqlite3.connect("StudentInfo.db")
connection2 = sqlite3.connect("DrivingInstructor.db")
connection3 = sqlite3.connect("RecentNews.db")
c1 = connection1.cursor()
c2 = connection2.cursor()
c3 = connection3.cursor()


c1.execute("""CREATE TABLE StudentLogin 
(Student_ID INTEGER PRIMARY KEY,
Email NOT NULL,
Password NOT NULL)""")

c1.execute("""CREATE TABLE StudentInformation 
(Student_ID INTEGER PRIMARY KEY,
City_Town NOT NULL,
Mobile_Number NOT NULL)""")


c2.execute("""CREATE TABLE DIBasic
(Instructor_ID INTEGER PRIMARY KEY,
Full_Name NOT NULL,
Price NOT NULL,
Teach_Type NOT NULL)""")

c2.execute("""CREATE TABLE DIFilters 
(Instructor_ID INTEGER PRIMARY KEY,
Full_Name NOT NULL,
Price NOT NULL,
Teach_Type NOT NULL,
City_Town1 NOT NULL,
City_Town2 NOT NULL,
Bio NOT NULL,
Mobile_Number NOT NULL,
Lesson_Time NOT NULL,
Profile_Pic NOT NULL,
Schedule_ID NOT NULL)""")


c3.execute("""CREATE TABLE RecentNews (
Article_ID INTEGER PRIMARY KEY,
Picture NOT NULL,
Heading NOT NULL,
Body NOT NULL)""")
