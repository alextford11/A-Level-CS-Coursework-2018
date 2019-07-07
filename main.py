#Imports the kivy library
import kivy
#Imports App library from kivy.app
from kivy.app import App
#Imports the Config library from kivy.config
from kivy.config import Config
#Imports the Window library from kivy.core.window
from kivy.core.window import Window
#Imports the ScreenManager and Screen library from kivy.uix.screenmanager
from kivy.uix.screenmanager import ScreenManager, Screen
#Imports the sqlite3 library
import sqlite3
#Imports Popup library from kivy.uix.popup
from kivy.uix.popup import Popup
#Imports Label library from kivy.uix.label
from kivy.uix.label import Label
#Imports the re library 
import re
#Imports date and datetime from datetime library
from datetime import date, datetime, timedelta
#Imports StringProperty from kivy.properties
from kivy.properties import StringProperty, ObjectProperty, ListProperty, NumericProperty
#Imports ListItemButton from kivy.uix.listview
from kivy.uix.listview import ListItemButton
#Imports the time library
import time
#Imports the time library 
from datetime import datetime
#Imports the hashlib library
import hashlib
#Makes a connection between sqlite3 and the database
connectiontoSI = sqlite3.connect("StudentInfo.db")
#Makes a cursor for the database to execute SQL code
cursorSI = connectiontoSI.cursor()
#Makes a connection between sqlite3 and the database
connectiontoRN = sqlite3.connect("RecentNews.db")
#Makes a cursor for the database to execute SQL code
cursorRN = connectiontoRN.cursor()
#Makes a connection between sqlite3 and the database
connectiontoDI = sqlite3.connect("DrivingInstructor.db")
#Makes a cursor for the database to execute SQL code
cursorDI = connectiontoDI.cursor()
#Uses the .clearcolor module found in the window import the background colour in...
#...based in RGB in percentage so my apps background colour is 86% red, green and blue
Window.clearcolor = (0.86, 0.86, 0.86, 1)
#The .set module sets the conditions in the parameters in this case the resizing of
#...the screen in not possible
Config.set('graphics','resizable', False)
#The .write module writes the .set data so it is permanent
Config.write()
#The .set module sets the conditions in the parameters in this case the screens...
#...width is set at 1080 pixels
Config.set('graphics', 'width', '360') #432 #360
#The .write module writes the .set data so it is permanent
Config.write()
#The .set module sets the conditions in the parameters in this case the screens...
#...height is set at 1920 pixels
Config.set('graphics', 'height', '640') #768 #640
#The .write module writes the .set data so it is permanent
Config.write()
#The .set module sets the conditions in the parameters in this case the screen...
#...allows the device to go into sleep mode, most effective on mobile
Config.set('graphics', 'allow_screensaver', True)
#The .write module writes the .set data so it is permanent
Config.write()
#Global list which stores the studentInformation
studentInformation = []

#Hashing procedure for passwords using MD5 and called when is needed
def md5Hash(password):
    hashObj = hashlib.md5()
    hashObj.update(password.encode('utf-8'))
    return hashObj.hexdigest()

#The class for the login screen with the library of Screen in its parameters
class LoginScreen(Screen):
#Defines the function dataGetter  
    def dataGetter(self, email):
#Deletes the contents of studentInformation
        del studentInformation[:]
#Executes the SQL code which gets the students ID that correspondes to the entered email
        cursorSI.execute("SELECT Student_ID FROM StudentLogin WHERE email = '"+email+"';")
#The database ID is stored in the ID variable       
        ID = cursorSI.fetchone()[0]
#Executes the SQL code which gets all the data from StudentInformation
        cursorSI.execute("SELECT * FROM StudentInformation WHERE Student_ID = '"+str(ID)+"';")
#Stores the retrieved data into the studentData variable
        studentData = cursorSI.fetchone()
#For loop for each index in studentData
        for item in studentData:
#Appends the current for loop item to the studentInformation 
            studentInformation.append(item)
            
#Define the procedure ErrorMessage
    def ErrorMessage(self):
#Creates a variable popup which contains the data to run a Popup, the Popup comes from the...
#...Popup import, it makes a box on the screen with a pop up notifications
        popup = Popup(title="Invalid Input", content=Label(text="The email or password\nyou entered was incorrect,\nplease try again."),size_hint=(None, None),size=(300,200))
#Runs the above variable which is a popup
        popup.open()
#Defines the procedure Validation which needs two variables to pass through its parameters
    def Validation(self,email,password):
#If the length of email or password is over 50 characters the function returns True
        if len(email) > 50 or len(password) > 50:
#returns True
            return True
#If the length of email and password is under 50 characters then the function returns False
        else:
#returns False 
            return False
#Defines the procedure FileWriter where 2 variables must be inputted into the parameters
    def FileWriter(self,Email,Password):
#The text files LoginDetails is opened and stored in the variable LoginDetails as a file object 
        LoginDetails = open("LoginDetails.txt","r+")
#LoginDetailsList is a list of all the lines in the text file, I used read().splitlines() as this gets...
#...each line without the extra "\n" at the end of the line, this means new line, this means that when...
#...comparing strings and the contents the results will now be the same       
        LoginDetailsList = LoginDetails.read().splitlines()
#This checks whether there is any data in the List, if there is more than 0 lines then nothing happens       
        if len(LoginDetailsList) > 0:
#The checks whether the contents is the same as the inputted 
            if LoginDetailsList[0] == Email and LoginDetailsList[1] == Password:
#Passes, does nothing
                pass
#If the contents isn't the same the input
            else:
#Sets the text file pointer to 0
                LoginDetails.seek(0)
#Deletes the contents of the text file
                LoginDetails.truncate()
#.write allows data to be written into the text file, the data written into the text file is the Email...
#...followed by "\n" which is a new line, then the Password. 
                LoginDetails.write(Email+"\n"+Password)
#If there is nothing in the list then data gets written into the list
        else:
#.write allows data to be written into the text file, the data written into the text file is the Email...
#...followed by "\n" which is a new line, then the Password. 
            LoginDetails.write(Email+"\n"+Password)
#The text file is then closed.          
        LoginDetails.close()
#Defines the procdure InputChecker which needs two strings in its parameters when initiated
    def InputChecker(self, email, password):
#If email and password is good format and false is returned, the code is run to check the email and password...
#...is in the database
        if self.Validation(email,password) == False:
#The cursorSI is used to execute the SQL code, the SQL code counts the amount of emails...
#...that was inputted into the text box in the app from the table StudentLogin
            cursorSI.execute("SELECT COUNT(Email) FROM StudentLogin WHERE Email = '"+email+"';")
#The variable TrueOrFalseNum is called this because when the above SQL is run it will only...
#...return a 1 or a 0, 1 being true and 0 being false. 
            TrueOrFalseNum = cursorSI.fetchone()[0]
#If statement whether TrueOrFalseNum is equal to 1
            if TrueOrFalseNum == 1:
#If TrueOrFalseNum is true it then checks the password in the StudentLogin table
                cursorSI.execute("SELECT Password FROM StudentLogin WHERE email = '"+email+"';")
#The results from the SQL query is stored into PasswordCheck
                PasswordCheck = cursorSI.fetchone()[0]
                hashedPassword = md5Hash(password)
#If the password is correct and is equal to the password in the database then it will change screen
                if PasswordCheck == hashedPassword:
#Runs the FileWriter procedure and passes the variables email and password through the parameters
                    self.FileWriter(email,password)
                    self.dataGetter(email)
#Using a similar method in the KV file, here we are changing the current variable to the next screen name...
#...This works by self going to LoginScreen widget, then Parent to AppScreenManager as this is the parent widget
                    self.parent.current = "recentnews"
#Else is used when the password is incorrect
                else:
#Goes to the ErrorMessage procedure which opens a popup saying the input is wrong
                    self.ErrorMessage()
#Else is used when the email is incorrect
            else:
#Goes to the ErrorMessage procedure which opens a popup saying the input is wrong
                self.ErrorMessage()
#If the format is wrong then the ErrorMessage is called
        else:
#ErrorMessage is called
            self.ErrorMessage()
#The procedure is defined and called FileChecker in the class LoginScreen    
    def FileChecker(self):
#The text files LoginDetails is opened and stored in the variable LoginDetails as a file object      
        LoginDetails = open("LoginDetails.txt","r")
#LoginDetailsList is a list of all the lines in the text file, I used read().splitlines() as this gets...
#...each line without the extra "\n" at the end of the line, this means new line, this means that when...
#...comparing strings and the contents the results will now be the same
        LoginDetailsList = LoginDetails.read().splitlines()
#Checks if there is contents in the text file when the auto login button is pressed, if there is no data...
#...then the error message appears
        if len(LoginDetailsList) == 0:
#The ErrorMessage us run
            self.ErrorMessage()
#If their is contents in the text file then the code below is run
        else:
#The InputChecker procedure is run, instead of using the same code as in this procedure I just inputted the...
#...values from the text files which are stored in the list
            self.InputChecker(LoginDetailsList[0],LoginDetailsList[1])
#Closes the file
        LoginDetails.close()
#The class for the sign up screen with the library of Screen in its parameters
class SignupScreen(Screen):
#Define the procedure ErrorMessage
    def ErrorMessage(self,ErrorText):
#Creates a variable popup which contains the data to run a Popup, the Popup comes from the...
#...Popup import, it makes a box on the screen with a pop up notifications
        popup = Popup(title="Invalid Input", content=Label(text=ErrorText),size_hint=(None, None),size=(300,200))#300,200
#Runs the above variable which is a popup
        popup.open()
#Defines the procedure EmailValidation        
    def EmailValidation(self, EmailText):
#Checks if the variable follows the rule in the brackets        
        if re.match("[^@]+@[^@]+\.[^@]",EmailText):
#Checks if the lenght of the email is over or equal to 50 characters
            if len(EmailText) >= 50:
#Returns back False                
                return False
#If the if statement is false            
            else:
#Returns back True                 
                return True
#If the if statement is false             
        else:
#Returns back False              
            return False
#Defines the procedure PasswordValidation           
    def PasswordValidation(self, PasswordText):
#Checks if the variable follows the rule in the brackets         
        if re.match("[A-Za-z0-9@#$%^&+=]",PasswordText):
#Checks the lenght of the password to see if it is within the 8-25 character limtits          
            if len(PasswordText) > 25 or len(PasswordText) < 8:
#Returns back False                 
                return False
#If the if statement is false             
            else:
#Returns back True                
                return True
#If the if statement is false             
        else:
#Returns back False              
            return False
#Defines the procedure MobileNumberValidation           
    def MobileNumberValidation(self, MobileNumberText):
#Checks if the variable follows the rule in the brackets         
        if re.match("^(07[\d]{8,12}|447[\d]{7,11})$",MobileNumberText):
#Returns back True            
            return True
#If the if statement is false         
        else:
#Returns back False              
            return False
#Defines the procedure TownValidation           
    def TownValidation(self, TownText):
#Checks if the variable follows the rule in the brackets         
        if re.match("^[ .A-Za-z]+$",TownText):
#Checks if the lenght of the place is within the character limit of 2-30           
            if len(TownText) >= 30 or len(TownText) <= 2:
#Returns back False                  
                return False
#If the if statement is false             
            else:
#Returns back True                
                return True
#If the if statement is false 
        else:
#Returns back False              
            return False
#Defines the procedure DOBValidation           
    def DOBValidation(self, daySpinner, monthSpinner, yearSpinner):
#Returns true is the variable is just digits        
        DigitChecker1 = daySpinner.isdigit()
#Returns true is the variable is just digits   
        DigitChecker2 = monthSpinner.isdigit()
#Returns true is the variable is just digits   
        DigitChecker3 = yearSpinner.isdigit()
#If all the variables return true then the code will work out whether the user is old enough
        if DigitChecker1 == True and DigitChecker2 == True and DigitChecker3 == True:
#The text from the dropdown boxes is joint together as a string      
            dateinput = str(daySpinner+monthSpinner+yearSpinner)
#Turns the dateinput variable from a string to a date object       
            dateob = datetime.strptime(dateinput, "%d%m%Y").date()
#The today variable has the date of the current day        
            today = date.today()
#Age is the sum of the today variable and the user DOB, the result is given in days and time        
            age = today-dateob
#Checks whether the days part of age is greater than or equal to 6209, which is 17 years old of age
            if age.days >= 6205:
#Returns back True            
                return True
#If the if statement is false         
            else:
#Returns back False              
                return False
#If the if statement is false
        else:
#Returns back false
            return False
#Defines the procedure ValidationSystem           
    def ValidationSystem(self, EmailText, PasswordText, MobileNumberText, TownText, daySpinner, monthSpinner, yearSpinner):
#Checks whether the function outputs True or False        
        if self.EmailValidation(EmailText) == True:
#Checks whether the function outputs True or False             
            if self.PasswordValidation(PasswordText) == True:
#Checks whether the function outputs True or False                 
                if self.MobileNumberValidation(MobileNumberText) == True:
#Checks whether the function outputs True or False                     
                    if self.TownValidation(TownText) == True:
#Checks whether the function outputs True or False                         
                        if self.DOBValidation(daySpinner, monthSpinner, yearSpinner) == True:
#Returns back True                            
                            return True
#If the if statement is false                         
                        else:
#Calls the ErrorMessage procedure and the text in the parameters in outputted onto the pop up                            
                            self.ErrorMessage("You are must be atleast\n17 years old to sign up")
#If the if statement is false                             
                    else:
#Calls the ErrorMessage procedure and the text in the parameters in outputted onto the pop up                        
                        self.ErrorMessage("Input is invalid, please\ncheck city/town as it's\nwrong")
#If the if statement is false                         
                else:
#Calls the ErrorMessage procedure and the text in the parameters in outputted onto the pop up                    
                    self.ErrorMessage("The mobile number must\nstart with 07- or 447- and\nbe between 10 and 14\nnumbers")
#If the if statement is false             
            else:
#Calls the ErrorMessage procedure and the text in the parameters in outputted onto the pop up                
                self.ErrorMessage("Your password is incorrect,\ncan only use Uppercase,\nLowercase, Numbers and\n@#$%^&+= and between 8-25\ncharacters")
#If the if statement is false                 
        else:
#Calls the ErrorMessage procedure and the text in the parameters in outputted onto the pop up            
            self.ErrorMessage("Email is in an invalid\nformat, e.g.\nexample@example.com")    
#The procedure SignupButton is defined here and is initiated when the signup button is pressed 
    def SignupButton(self, EmailText, PasswordText, MobileNumberText, TownText, daySpinner, monthSpinner, yearSpinner):
#Calls the ValidationSystem procedure and then checks whether the function returns True or False      
        if self.ValidationSystem(EmailText, PasswordText, MobileNumberText, TownText, daySpinner, monthSpinner, yearSpinner) == True:
#The cursorSI is used to execute the SQL code, the SQL code counts the amount of emails...
#...that was inputted into the text box in the app from the table StudentLogin
            cursorSI.execute("SELECT COUNT(Email) FROM StudentLogin WHERE Email = '"+EmailText+"';")
#The variable EmailCheck is called this because when the above SQL is run it will only...
#...return a 1 or a 0, 1 being true and 0 being false. 
            EmailCheck = cursorSI.fetchone()[0]
#If statement whether TrueOrFalseNum is equal to 0
            if EmailCheck == 0:
#The cursorSI is used to execute the SQL code, the SQL code counts the amount of mobile numbers...
#...that was inputted into the text box in the app from the table StudentInformation
                cursorSI.execute("SELECT COUNT(Mobile_Number) FROM StudentInformation WHERE Mobile_Number = '"+MobileNumberText+"';")
#The results from the SQL query is stored into MobileNumberText
                MobileNumberCheck = cursorSI.fetchone()[0]
#Checks if the amount of mobile numbers in the database is eqaul to 0 
                if MobileNumberCheck == 0:
                    hashedPassword = md5Hash(PasswordText)
#The variable is a tuple which holds the Email and Password 
                    new_record1 = (EmailText, hashedPassword)
#The variable is a tuple which holds the Town/City and the Mobile Number of the student 
                    new_record2 = (TownText, MobileNumberText)
#The details get inserted into the StudentInfo database and the StudentLogin table, it uses the new_record1 tuple as this is the data to be used
                    cursorSI.execute("INSERT INTO StudentLogin(Email,Password) VALUES (?,?)",new_record1)
#The details get inserted into the StudentInfo database and the StudentInformation table, it uses the new_record2 tuple as this is the data to be used
                    cursorSI.execute("INSERT INTO StudentInformation(City_Town,Mobile_Number) VALUES (?,?)",new_record2)
#The changes made in the database are written in and saved
                    connectiontoSI.commit()        
#Using a similar method in the KV file, here we are changing the current variable to the next screen name...
#...This works by self going to SignupScreen widget, then Parent to AppScreenManager as this is the parent widget
                    self.parent.current = "login"
#If the if statement is false                    
                else:
#The error message procedure is called and the message in the brackets is used on the pop up
                    self.ErrorMessage("This Mobile Number has\nalready been used.\nPlease use a different\nMobile Number")
#If the if statement is false                     
            else:
#The error message procedure is called and the message in the brackets is used on the pop up
                self.ErrorMessage("This Email address has\nalready been used.\nPlease use a different\nEmial address")
#The class for the recent news screen with the library of Screen in its parameters
class RecentNewsScreen(Screen):
#The procedure ChangeScreen is defined and needs the heading value to be passed through
    def ChangeScreen(self, heading):
#The cursor for the Recent News database gets all the information under the Heading feild
        cursorRN.execute("SELECT * FROM RecentNews WHERE Heading = '"+heading+"';")
#All the data under the Heading feild is stored in a 2D array as tuples in a list
        articledata = cursorRN.fetchall()
#The articles id is stored in the variable and retrieved from the tuple by [0][0]
        Article_ID = articledata[0][0]
#The articles image path is stored in the variable and retrieved from the tuple by [0][1]
        Article_Image = articledata[0][1]
#The articles heading is stored in the variable and retrieved from the tuple by [0][2]
        Aritcle_Heading = articledata[0][2]
#The articles body of text is stored in the variable and retrieved from the tuple by [0][3]
        Article_Body = articledata[0][3]
#Sets the BodyTxt StringProperty to the variable Article_Body
        self.parent.ids.screenarticle.BodyTxt = Article_Body
#Sets the HeadingTxt StringProperty to the variable Article_Body
        self.parent.ids.screenarticle.HeadingTxt = Aritcle_Heading
#Sets the PathImage StringProperty to the variable Article_Image
        self.parent.ids.screenarticle.PathImage = Article_Image
#Using a similar method in the KV file, here we are changing the current variable to the next screen name...
#...This works by self going to RecentNewsScreen widget, then Parent to AppScreenManager as this is the parent widget
        self.parent.current = "article"     
#The cursor for the Recent News database gets all the information under the Heading feild
    cursorRN.execute("SELECT Heading FROM RecentNews;")
#All the data under the Heading feild is stored in a 2D array as tuples in a list
    Headings = cursorRN.fetchall()
#Heading1Text is a variable which links to the StringProperty import, the values found...
#...in the 2d array are used in the parameters of the import. Heading1Text links to...
#...the Kivy code.
    Heading1Text = StringProperty(Headings[0][0])
#Heading2Text is a variable which links to the StringProperty import, the values found...
#...in the 2d array are used in the parameters of the import. Heading2Text links to...
#...the Kivy code.    
    Heading2Text = StringProperty(Headings[1][0])
#The class for the recent news article screen with the library of Screen in its parameters
class ArticleScreen(Screen):
#Creates a blank HeadingTxt StringProperty which links to the label in the KV file
    HeadingTxt = StringProperty("")
#Creates a blank BodyTxt StringProperty which links to the label in the KV file
    BodyTxt = StringProperty("")
#Creates a blank PathImage StringProperty which links to the label in the KV file
    PathImage = StringProperty("")
#The class for the account settings screen with the library of Screen in its parameters
class AccountScreen(Screen):
    pass
#Creates a global list 
listOfDrivingInstructors = []
#Creates the class for all driving instructors
class DrivingInstructors(object):
#Creates all the required attributes needed for the list screen
    DI_id = 0
    DI_name = ""
    DI_price = 0
    DI_teach_type = ""
#Makes a construct for the class where data is passed through and stored in the object
    def __init__(self, ID, name, price, teachtype):
        self.DI_id = ID
        self.DI_name = name
        self.DI_price = price
        self.DI_teach_type = teachtype
#The class for the filter system screen with the library of Screen in its parameters
class FilterScreen(Screen):
#Define the procedure ErrorMessage
    def ErrorMessage(self,ErrorText):
#Creates a variable popup which contains the data to run a Popup, the Popup comes from the...
#...Popup import, it makes a box on the screen with a pop up notifications
        popup = Popup(title="Invalid Input", content=Label(text=ErrorText),size_hint=(None, None),size=(300,200))#300,200
#Runs the above variable which is a popup
        popup.open()
#Define the procedure NameSearch
    def NameSearch(self,nameInput):
#The cursorDI which links to the Driving Instructor DB execute the following SQL code
        cursorDI.execute("SELECT * From DIBasic WHERE Full_Name like '%"+nameInput+"%';")
#The values that are returned from the DB are saved in the variable foundDI
        foundDI = cursorDI.fetchall()
#Checks if the length is 0
        if len(foundDI) == 0:
#If the length is 0 then the error message is displayed
            self.ErrorMessage("No Results\nFound")
#If the len isn't 0 
        else:
#Calls the DI_creator and passing through the list of found driving instructors
            self.DI_creator(foundDI)
#Defines the filtersearch propcedure
    def filterSearch(self, maxPrice, minPrice, manOrAuto, city, lessonTime):
#Converts the lessonTime varible to the correct format, for example 60 mins = 1.0 hours or 30 mins = 0.5 hours
        LTconverted = int(lessonTime)/60
#Turns the maxprice into an integer
        maxPriceCon = int(maxPrice)
#Turns the minprice into an integer
        minPriceCon = int(minPrice)
#The cursorDI which links to the Driving Instructor DB execute the following SQL code
        cursorDI.execute("SELECT Instructor_ID,Full_Name,Price,Teach_Type From DIFilters WHERE (Price BETWEEN '"+str(minPriceCon)+"' AND '"+str(maxPriceCon)+"') AND (Teach_Type = '"+manOrAuto+"') AND (City_Town1 = '"+city+"' OR City_Town2 = '"+city+"') AND (Lesson_Time = '"+str(LTconverted)+"');")
#The values that are returned from the DB are saved in the variable foundDI
        foundDI = cursorDI.fetchall()
#Checks if the length is 0
        if len(foundDI) == 0:
#If the length is 0 then the error message is displayed
            self.ErrorMessage("No Results\nFound")
#If the len isn't 0 
        else:
#Calls the DI_creator and passing through the list of found driving instructors
            self.DI_creator(foundDI)
#Defines the DI_creator procedure
    def DI_creator(self,foundDI):
#This deletes the contents of the list and not the list itself
        del listOfDrivingInstructors [:]
#This deletes all the data in the listview
        del self.parent.ids.screenlist.search_results.adapter.data[:]
#Creates a for loop where DI is the current item in the list
        for DI in foundDI:
#Creates an object stored in DriveInstructor using the information from the foundDI list
            DriveInstructor = DrivingInstructors(DI[0], DI[1], DI[2], DI[3])
#Each object gets appended to the list of driving instructors which is a global data structure
            listOfDrivingInstructors.append(DriveInstructor)
#Calls the list_updater procedure from the ListScreen Class
        self.parent.ids.screenlist.list_updater()
#Changes the screen to the list screen
        self.parent.current = "list"
#This is the class which is a template for the listview design is just basic at the moment
class DIButton(ListItemButton):
#Creates the list items as buttons to be changed in kivy file
    didata = ListProperty()
#The class for the driving instructor list screen with the library of Screen in its parameters
class ListScreen(Screen):
#Links the listview widget from the Kivy to the python
    search_results = ObjectProperty()
#The list_updater procedure is defined
    def list_updater(self):
#Creates a for loop for each item in listOfDrivingInstructors list
        for DI in listOfDrivingInstructors:
#Using the DI as the current item in the list, we format the string text_format to be added into the listview
            text_format = "Name: "+DI.DI_name+"\n"+"Teach Type: "+DI.DI_teach_type+"\n"+"Price: £"+str(DI.DI_price)+"0"
#Add each text_format string into the listview which has a list of its own      
            self.search_results.adapter.data.extend([text_format])
#This code here just here to make the list work 
            self.search_results._trigger_reset_populate()
#Procedure to recieve the index value from the kivy code            
    def indexPasser(self,index):
#Passes the index to the Profile screen by using the screen manager
        self.parent.ids.screenprofile.dataGetter(index)
#Global list so the profile details are stored to be access by other screens/classes
profileInfoList = []    
#The class for the driving instructor profile screen with the library of Screen in its parameters
class ProfileScreen(Screen):
#Defines the image id as a Object Property
    pic_profile = ObjectProperty()
#Defines the text of the label as a String Property
    infoText = StringProperty()
#Defines the procedure dataGetter
    def dataGetter(self,index):
#Deletes the profileInfoList lists data so the data doesnt repeat in the list
        del profileInfoList[:]
#Gets the data from the database from all the field names in the DIFilters table when the ID is equal to the selected...
#...driving instructor
        cursorDI.execute("SELECT * From DIFilters WHERE Instructor_ID = '"+str(listOfDrivingInstructors[index].DI_id)+"';")
#All of the data retrieved from the above line, gets stored in the tuple called profileInfo
        profileInfo = cursorDI.fetchall()
#A for loop to append each information of the tuple into the global list so it is organised
        for info in profileInfo[0]:
#Appends each index of the retrieved data into the profileInfoList
            profileInfoList.append(info)
#Calls the widget_updater in the profile screen class
        self.widget_updater()
#Defines the procedure widget_updater, this updates the image source and the label text
    def widget_updater(self):
#textFormat is holds the data require to be displayed in the label for the screen, the data comes from the database...
#...which is stored in the profileInfoList list as indexes.
        textFormat = ("Name: "+profileInfoList[1]+
                      "\nTeach Type: "+profileInfoList[3]+ 
                      "\nPrice: £"+str(profileInfoList[2])+"0"+
                      "\nTowns: "+profileInfoList[4]+", "+profileInfoList[5]+
                      "\nMobile Number: "+profileInfoList[7]+
                      "\nBio: "+profileInfoList[6])
#Sets the images profile to the value found in the database
        self.ids.pic_profile.source = profileInfoList[9]
#Sets the labels text to the value of textFormat
        self.ids.infoText.text = textFormat
#Defines the textSetter procedure 
    def textSetter(self, dates):
#Sets the date1 button to the value in the dates tuple
        self.parent.ids.screendate.date1.text = dates[0][0]
#Sets the date2 button to the value in the dates tuple        
        self.parent.ids.screendate.date2.text = dates[1][0]
#Sets the date3 button to the value in the dates tuple        
        self.parent.ids.screendate.date3.text = dates[2][0]
#Sets the date4 button to the value in the dates tuple        
        self.parent.ids.screendate.date4.text = dates[3][0]
#Sets the date5 button to the value in the dates tuple        
        self.parent.ids.screendate.date5.text = dates[4][0]
#Sets the date6 button to the value in the dates tuple        
        self.parent.ids.screendate.date6.text = dates[5][0]
#Sets the date7 button to the value in the dates tuple        
        self.parent.ids.screendate.date7.text = dates[6][0]
#Defines the procedure ChangeScreen which calls the procedures from the DateScreen...
#...class, this procedure is found in the ProfileScreen class as the button is...
#...pressed on the profile screen
    def ChangeScreen(self):
#Calls the dateGetter class found in the DateScreen class
        dates = DateScreen.dateGetter()
#Calls the textSetter procedure and passes through dates
        self.textSetter(dates)
#Changes the screen to the date screen
        self.parent.current = "date"
#The class for the date screen with the library of Screen in its parameters
class DateScreen(Screen):
#Links the widget in the kivy file to python 
    date1 = ObjectProperty()
#Links the widget in the kivy file to python     
    date2 = ObjectProperty()
#Links the widget in the kivy file to python     
    date3 = ObjectProperty()
#Links the widget in the kivy file to python     
    date4 = ObjectProperty()
#Links the widget in the kivy file to python     
    date5 = ObjectProperty()
#Links the widget in the kivy file to python     
    date6 = ObjectProperty()
#Links the widget in the kivy file to python     
    date7 = ObjectProperty()
#Defines the dateGetter procedure
    def dateGetter():
#Executes the SQL code which get the table name for the selected driving instructors schedule
        cursorDI.execute("SELECT Schedule_ID From DIFilters WHERE Instructor_ID = '"+str(profileInfoList[0])+"';")
#Gets the found ID and stores it in the tuple scheduleID
        scheduleID = cursorDI.fetchall()
#Executes the SQL code that gets all the dates in the selected driving instructors schedule
        cursorDI.execute("SELECT Date From "+str(scheduleID[0][0])+ ";")
#Stores the found dates in the tuple dates
        dates = cursorDI.fetchall()
#Returns the dates found in the driving instructors schedule table
        return dates
#Defines the buttonDeactivator procedure
    def buttonDeactivator(self, timeValues):
#If the value in the list is not false then the buttons will be disabled
        if timeValues[0][0] != "false":
            self.parent.ids.screentime.tim1.disabled = True
        if timeValues[0][1] != "false":
            self.parent.ids.screentime.tim2.disabled = True            
        if timeValues[0][2] != "false":            
            self.parent.ids.screentime.tim3.disabled = True            
        if timeValues[0][3] != "false":            
            self.parent.ids.screentime.tim4.disabled = True            
        if timeValues[0][4] != "false":            
            self.parent.ids.screentime.tim5.disabled = True            
        if timeValues[0][5] != "false":            
            self.parent.ids.screentime.tim6.disabled = True            
        if timeValues[0][6] != "false":            
            self.parent.ids.screentime.tim7.disabled = True            
        if timeValues[0][7] != "false":            
            self.parent.ids.screentime.tim8.disabled = True            
        if timeValues[0][8] != "false":            
            self.parent.ids.screentime.tim9.disabled = True        
#Defines ChangeScreen procedure found in DateScreen class
    def ChangeScreen(self, date):
#Calls the procedure to retrieve the time values from the schedules
        timeValues = TimeScreen.timeValuesGetter(date)
#Calls the procedure to deactivate buttons
        self.buttonDeactivator(timeValues)
#Changes the screen to the time screen
        self.parent.current = "time"
#The class for the time screen with the library of Screen in its parameters
class TimeScreen(Screen):
#Links the widget in the kivy file to python 
    tim1 = ObjectProperty()
#Links the widget in the kivy file to python 
    tim2 = ObjectProperty()
#Links the widget in the kivy file to python 
    tim3 = ObjectProperty()
#Links the widget in the kivy file to python 
    tim4 = ObjectProperty()
#Links the widget in the kivy file to python 
    tim5 = ObjectProperty()
#Links the widget in the kivy file to python 
    tim6 = ObjectProperty()
#Links the widget in the kivy file to python 
    tim7 = ObjectProperty()
#Links the widget in the kivy file to python 
    tim8 = ObjectProperty()
#Links the widget in the kivy file to python 
    tim9 = ObjectProperty()
#String with the dateOfLesson picked, changes in the timeValuesGetter procedure
    dateOfLesson = ""
#Define the procedure timeValuesGetter
    def timeValuesGetter(date):
#dateOfLesson string changes to the date passed through to this procedure
        TimeScreen.dateOfLesson = date
#Executes SQL code to get all the values for each time in the selected schedule and where the date was the one selected
        cursorDI.execute("SELECT Time1,Time2,Time3,Time4,Time5,Time6,Time7,Time8,Time9 From "+profileInfoList[10]+" WHERE Date = '"+date+"';")
#timeVales is a tuple of the values
        timeValues = cursorDI.fetchall()
#Returns the timeValues tuple
        return timeValues
#Defines the disableReset procedure
    def disableReset(self):
#Changes the disabled attribute to False
        self.tim1.disabled = False
        self.tim2.disabled = False
        self.tim3.disabled = False
        self.tim4.disabled = False
        self.tim5.disabled = False
        self.tim6.disabled = False
        self.tim7.disabled = False
        self.tim8.disabled = False
        self.tim9.disabled = False
#Changes the screen to the date screen
        self.parent.current = "date"
#Defines the buttonDeactivator procedure
    def buttonDeactivator(self, timeValues):
#If the value in the list is not false then the buttons will be disabled
        if timeValues[0][0] != "false":
            self.parent.ids.screentime.tim1.disabled = True
        if timeValues[0][1] != "false":
            self.parent.ids.screentime.tim2.disabled = True            
        if timeValues[0][2] != "false":            
            self.parent.ids.screentime.tim3.disabled = True            
        if timeValues[0][3] != "false":            
            self.parent.ids.screentime.tim4.disabled = True            
        if timeValues[0][4] != "false":            
            self.parent.ids.screentime.tim5.disabled = True            
        if timeValues[0][5] != "false":            
            self.parent.ids.screentime.tim6.disabled = True            
        if timeValues[0][6] != "false":            
            self.parent.ids.screentime.tim7.disabled = True            
        if timeValues[0][7] != "false":            
            self.parent.ids.screentime.tim8.disabled = True            
        if timeValues[0][8] != "false":            
            self.parent.ids.screentime.tim9.disabled = True 

#Defines bookLesson procedure
    def bookLesson(self, timeValue):
#Use the time import to get the UTC time
        timeNow = datetime.utcnow()
        timeInSeconds = int(timeNow.timestamp())
#DateAndTime is equal to the date and the timestamp joined together
        DateAndTime = datetime.fromtimestamp(timeInSeconds).strftime('%Y%m%d%H%M%S')
#The users ID is added to the DateAndTime variable 
        DateAndTime += str(studentInformation[0])        
#Executes the SQL in the brackets which sets the value of the time selected to "true" 
        cursorDI.execute("UPDATE "+profileInfoList[10]+" SET "+timeValue+" = '"+DateAndTime+"' WHERE Date = '"+self.dateOfLesson+"';")
#Writes the changes into the database
        connectiontoDI.commit()
#Executes SQL code to get all the values for each time in the selected schedule and where the date was the one selected
        cursorDI.execute("SELECT Time1,Time2,Time3,Time4,Time5,Time6,Time7,Time8,Time9 From "+profileInfoList[10]+" WHERE Date = '"+self.dateOfLesson+"';")
#timeVales is a tuple of the values
        timeValues = cursorDI.fetchall()
#Calls the buttonDeactivator procedure found in TimeScreen
        self.buttonDeactivator(timeValues)

    def confirmationMessage(self,timeSlot):
#Creates a variable popup which contains the data to run a Popup, the Popup comes from the...
#...Popup import, it makes a box on the screen with a pop up notifications
        popup = Popup(title="Confirmation Message",
                      content=Label(text="Date: "+self.dateOfLesson+"\n"+"Time: "+timeSlot+"\n"+"With: "+profileInfoList[1]),
                      size_hint=(None, None),size=(300,200))
#Runs the above variable which is a popup
        popup.open()

#Class for the Change Password Screen
class ChangePasswordScreen(Screen):
#Creates an error message with a variable message
    def ErrorMessage(self,ErrorText):
        popup = Popup(title="Invalid Input", content=Label(text=ErrorText),size_hint=(None, None),size=(300,200))
        popup.open()
#Checks the inputted password to the password found in the database, then returns True or False depending on result
    def CurrentPasswordChecker(self, CurrentPasswordInput):
        cursorSI.execute("SELECT Password FROM StudentLogin WHERE Student_ID = '"+str(studentInformation[0])+"';")
        CurrentDBPassword = cursorSI.fetchone()[0]
        HashedCPI = md5Hash(CurrentPasswordInput)
        if HashedCPI == CurrentDBPassword:
            return True
        else:
            return False
#Changes the password in the database to the new password in a hashed value
    def ChangeDBPassword(self, NewPassword):
        HashedNP = md5Hash(NewPassword)
        cursorSI.execute("UPDATE StudentLogin SET Password = '"+HashedNP+"' WHERE Student_ID = '"+str(studentInformation[0])+"';")
        connectiontoSI.commit()
#Checks if the new password is in the correct format and is eligible to be put in the database
    def PasswordValidation(self, PasswordText):       
        if re.match("[A-Za-z0-9@#$%^&+=]",PasswordText):        
            if len(PasswordText) > 25 or len(PasswordText) < 8:        
                return False            
            else:       
                return True           
        else:         
            return False
#The main procedure, which is run when the Change Password button is pressed, this runs all the functions above to change the password        
    def ChangePassword(self, CurrentPassword,NewPassword):
        if self.CurrentPasswordChecker(CurrentPassword) == True:
            if self.PasswordValidation(NewPassword) == True:
                self.ChangeDBPassword(NewPassword)
                self.parent.current = "account"
                popup = Popup(title="Password Changed",
                              content=Label(text="Your password has\nsuccessfully been\nchanged."),
                              size_hint=(None, None),size=(300,200))
                popup.open()
            else:
                self.ErrorMessage("""Your new password is incorrect.\n
                                  You can only use Uppercase,\n
                                  Lowercase, Numbers and\n
                                  @#$%^&+= and between 8-25\ncharacters""")
        else:
            self.ErrorMessage("The current password\nyou entered is incorrect.")
            
#The class for the screen manager with the library of ScreenManager in its parameters...
#...this is what helps navigate between screens when there is more than one
class AppScreenManager(ScreenManager):
    pass
#This procedure uses the App library going through it's...
#...parameters to be linked to kivy.app and use its modules
class LessonBookingApp(App):
    pass
#This means that the name of the python must always be...
#...named as "main"
if __name__ == '__main__':
#This gets the class and goes into the App library to...
#...to get the run module which opens the window
    LessonBookingApp().run() 
