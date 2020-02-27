import re
from os import system
from os import name
import datetime
import gspread
#from collections  import defaultdict
from getpass import getpass
from time import sleep
from oauth2client.service_account import ServiceAccountCredentials



#Access to google sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('TPP_CLIENT.json', scope)
client = gspread.authorize(credentials)

#sheet = client.open('Attendance Sheet TTP').get_worksheet(11)
#Should there be multiple sheets?
sheetDaily = client.open('Attendance Sheet TTP').get_worksheet(13)
sheetSocial = client.open('Attendance Sheet TTP').get_worksheet(14)
sheetSeminar = client.open('Attendance Sheet TTP').get_worksheet(15)

class Student:
    first = ""
    last = ""
    sid = 0
    state = 1
    checkinTime = 1

    #------------------GETTER----------------#
    def getFirst(self):
        return self.first
    
    def getLast(self):
        return self.last
    
    def getSID(self):
        return self.sid    

    def getState(self):
        return self.state

    def getCheckTime(self):
        return self.checkinTime
    #Returns name, sid, and time as an array for Spreadsheet update
    def getSheetArray(self):
        return [self.getLast(),self.getFirst(),self.getSID(),self.getCheckTime()]
    #------------------SETTER----------------#
    def setFirst(self, fname):
        self.first = fname
    
    def setLast(self, lname):
        self.last = lname
    
    def setSID(self, SID):
        self.sid = SID

    def setState(self, st):
        self.state = st

    def setCheckTime(self, cTime):
        self.checkinTime = cTime

    def setAll(self, fname,lname,sd,cTime):
        self.first = fname
        self.last = lname
        self.sid = sd
        self.checkinTime = cTime
    #Resets the data variables
    def clearData(self):
        self.first = ""
        self.last = ""
        self.sid = 0    

        #clear screen
    #Clears the output screen quickly or slowly
    def clear(self,pause = True):
        #for window use 'cls'
        #for mac use 'clear'
        if(pause):
            sleep(1)
        system('cls' if name == 'nt' else 'clear')
        #system('clear')
    #The main function called to make all the magic work
    def run(self):
        cardUser = self.welcomePrint()
        #record time of input
        self.setCheckTime(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
        #passes card swipe or manual entry to parse and update spreadsheet
        self.parseData(cardUser)
    #Opens the menu to change the state depending on the event at the center
    def menu(self):
        while(True):
            self.clear(pause=False)
            state = input("TTP CARD SCANNER MENU\n\n 1 : Daily/Regular days\n 2 : Social/Study Jams \n 3 : Seminar/Workshops\n\n Enter number and press \"Enter\": ")
            if(state is '1' or state is '2' or state is '3'):
                self.setState(state)
                break

    #Welcome print prompts
    def welcomePrint(self):
        # Print out the corresponding message for the state
        state = self.getState()
        cardUser = ''
        if(state ==  '1'):
            cardUser = getpass("Hello! Please Swipe Your Card to sign in: \n\nPress 'm' and press \"Enter\" for manual entry\n\nTo return to menu press '0' and press \"Enter\"\n\n\nBy signing-in you acknowledge that you have read and agree to abide by the Engineering Transfer Center (WCH 103) Space Policies.")
        elif(state == '2'):
            cardUser = getpass("Study Jam/Social sign in! Please Swipe Your Card to sign in: \n\nPress 'm' and press \"Enter\" for manual entry\n\nTo return to menu press '0' and press \"Enter\"\n\n\nBy signing-in you acknowledge that you have read and agree to abide by the Engineering Transfer Center (WCH 103) Space Policies.")
        elif(state == '3'):
            cardUser = getpass("Welcome to the Seminar! Please Swipe Your Card to sign in: \n\nPress 'm' and press \"Enter\" for manual entry\n\nTo return to menu press '0' and press \"Enter\"\n\n\nBy signing-in you acknowledge that you have read and agree to abide by the Engineering Transfer Center (WCH 103) Space Policies.")
        return cardUser

    #Bulk work of parsing the card swipe and then recording the data    
    def parseData(self,cardUser):
        # Print out the corresponding message for the state
        temp = cardUser.lower()
        #Invalid swipe
        if(cardUser == '' or not cardUser):
            print("Invalid Swipe..... Please Swipe again")
            self.clear()
        # Back to main menu
        elif(temp == "0"):
            self.menu()

        #Manual Entry
        elif(temp == "m"):
            self.manual(self.getCheckTime())

        #Card was swiped
        elif cardUser[0] == '%' and cardUser[len(cardUser) -1] == '?':

            #Extraction Current Swipes
            self.data_extraction(cardUser.upper(),self.getCheckTime())

            #Input New Names and Update Information
            self.update_Sheets()
            self.clear()

        else:
            print("Invalid Swipe..... Please Swipe again")
            self.clear()

    #Manual Entry
    def manual(self,checkTime):
        self.clear(pause=False)
        firstName=''
        lastName=''
        sid =''
        sid2 =''
        completeData = False
        while(True):
            firstName = input("Please Enter First Name (Press Enter to Continue or q to Exit): ").upper()
            while(firstName == ''):
                firstName = input("Error!! Please Enter First Name Again (Press Enter to Continue or q to Exit): ").upper()
            if(firstName == 'Q'): break
            lastName = input("Please Enter Last Name (Press Enter to Continue or q to Exit): ").upper()
            while(lastName == ''):
                lastName = input("Error!! Please Enter Last Name Again (Press Enter to Continue or q to Exit): ").upper()
            if(lastName == 'Q'): break
            sid = getpass("Please Enter SID  (Press Enter to Continue or q to Exit): ")
            if(sid == 'q'): break;
            sid2 = getpass("Please Enter SID again (Press Enter to Continue or q to Exit): ")
            if(sid2 == 'q'): break
            while(sid != sid2):
                print("Error!!! SIDs do not match")
                sid = getpass("Please Enter SID  (Press Enter to Continue or q to Exit): ")
                if(sid == 'q'): break
                sid2 = getpass("Please Enter SID again (Press Enter to Continue or q to Exit): ")
                if(sid2 == 'q'): break
            if(sid == sid2): completeData = True
            break
            
        if(completeData):
            self.setAll(firstName,lastName,sid,checkTime)
            self.update_Sheets()
        self.clear()

    #Extract the name and sid from the card swipe and package in the checkinTime
    def data_extraction(self,input,checkTime):
        #regular expression to delete uncessary information
        regword = re.sub("([%].*([0-9]\^))|(( *0* +\?;[0-9]).*)", '', input)
        regword = regword.strip(" ")
        #split the line into lastName & firstName
        data = re.split("[/^]",regword)
        data[1] = re.sub(r"\s+$", "", data[1])
        #reformat SID number
        data[2] = re.search("8[0-9]+",data[2]).group(0)
        #append date
        data.append(checkTime)
        self.setAll(data[1],data[0],data[2],data[3])

    #Add the collected data into the spreadsheet
    def update_Sheets(self):
        self.clear(pause=False)
        print("Welcome to TTP")
        print(self.getFirst() + " " + self.getLast())
        if credentials.access_token_expired:
            client.login()  # refreshes the token
        if(self.getState() == '2'):
            if(not checkDuplicates()):
                sheetSocial.append_row(self.getSheetArray())
        elif(self.getState() == '3'):
            if(not checkDuplicates()):
                sheetSeminar.append_row(self.getSheetArray())
        sheetDaily.append_row(self.getSheetArray())
        
    #Check the special events columns to make sure students are not getting recorded
    #more than once in the same day
    def checkDuplicates(self):
        #Get all the values from the time 
        sd = self.getSID()
        ct = self.getCheckTime()[:9]
        if(self.getState()=='2'):
            cell_list = sheetSocial.get_all_values()
            cell_list = cell_list[1:]
           
        elif(self.getState()=='3'):
            cell_list = sheetSeminar.get_all_values()
            cell_list = cell_list[1:]

        for i in cell_list:
            return (sd==i[2] and ct == i[3][:9])
        return False

    #Title Function
    def sheet_title(self,current_title):
        #Google Sheet Code [Chanage Weekly]
        size_Current_Title = len(current_title)

        if size_Current_Title == 0:
            new_title = ['Last Name', 'First Name','SID',"Check in Time"]
            return (new_title)
        else:
            return current_title

    #Clean Sheet (Adjust in Alphabetical order )
    # def sheet_Cleaner(self):
    #     currentTitle = sheet.row_values(1)
    #     sheet.delete_row(1)
    #     sheet_Values = sorted(sheet.get_all_values())
    #     sheet.clear()
    #     rowindex=1
    #     for entry in sheet_Values:
    #         sheet.insert_row(entry, rowindex)
    #         rowindex +=1

    #     sheet.insert_row(currentTitle, 1)
    #     sheet.resize(len(sheet.get_all_values()))         