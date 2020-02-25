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
        
def menu():
    while(True):
        clear(pause=False)
        state = input("TTP CARD SCANNER MENU\n\n 1 : Daily/Regular days\n 2 : Social/Study Jams \n 3 : Seminar/Workshops\n\n Enter number and press \"Enter\": ")
        if(state is '1' or state is '2' or state is '3'):
            return state

def menuLoop():
    while(True):
        clear(pause=False)
        state1 = menu()
        if(state1 == '1'):
            return 'd'
        elif(state1 == '2'):
            return 's'
        elif(state1 == '3'):
            return 'w'            


#Title Function
def sheet_title(current_title):
    #Google Sheet Code [Chanage Weekly]
    size_Current_Title = len(current_title)

    if size_Current_Title == 0:
        new_title = ['Last Name', 'First Name','SID',"Check in Time"]
        return (new_title)
    else:
        return current_title

#Manual Entry
def manual(checkinTime,state):
    clear(pause=False)
    firstName=''
    lastName=''
    sid =''
    sid2 =''
    completeData = False
    while(True):
        firstName = input("Please Enter First Name (Press Enter to Continue or q to Exit): ").upper()
        while(firstName == ''):
            firstName = input("Error!! Please Enter First Name Again (Press Enter to Continue or q to Exit): ").upper()
        if(firstName == 'Q'): break;
        lastName = input("Please Enter Last Name (Press Enter to Continue or q to Exit): ").upper()
        while(lastName == ''):
            lastName = input("Error!! Please Enter Last Name Again (Press Enter to Continue or q to Exit): ").upper()
        if(lastName == 'Q'): break;
        sid = getpass("Please Enter SID  (Press Enter to Continue or q to Exit): ")
        if(sid == 'q'): break;
        sid2 = getpass("Please Enter SID again (Press Enter to Continue or q to Exit): ")
        if(sid2 == 'q'): break;
        while(sid != sid2):
            print("Error!!! SIDs do not match")
            sid = getpass("Please Enter SID  (Press Enter to Continue or q to Exit): ")
            if(sid == 'q'): break;
            sid2 = getpass("Please Enter SID again (Press Enter to Continue or q to Exit): ")
            if(sid2 == 'q'): break;
        if(sid == sid2): completeData = True
        break;
        
    if(completeData):
        data = [lastName,firstName,sid,checkinTime]
        print()
        #Updated function below to handle the new state changes 
        update_Sheets(data, state)
    clear()

#Welcome print prompts
def welcomePrint(state):
    # Print out the corresponding message for the state
    if(state ==  "d"):
        cardUser = getpass("Hello! Please Swipe Your Card to sign in: \n\nPress 'm' and press \"Enter\" for manual entry\n\nTo return to menu press '0' and press \"Enter\"\n\n\nBy signing-in you acknowledge that you have read and agree to abide by the Engineering Transfer Center (WCH 103) Space Policies.")
    elif(state == "s"):
        cardUser = getpass("Study Jam/Social sign in! Please Swipe Your Card to sign in: \n\nPress 'm' and press \"Enter\" for manual entry\n\nTo return to menu press '0' and press \"Enter\"\n\n\nBy signing-in you acknowledge that you have read and agree to abide by the Engineering Transfer Center (WCH 103) Space Policies.")
    elif(state == "w"):
        cardUser = getpass("Welcome to the Seminar! Please Swipe Your Card to sign in: \n\nPress 'm' and press \"Enter\" for manual entry\n\nTo return to menu press '0' and press \"Enter\"\n\n\nBy signing-in you acknowledge that you have read and agree to abide by the Engineering Transfer Center (WCH 103) Space Policies.")
    return cardUser

#Bulk work of parsing the card swipe and then recording the data    
def parseData(cardUser,state,checkinTime):
    temp = cardUser.lower()
    #Invalid swipe
    if(cardUser == '' or not cardUser):
        print("Invalid Swipe..... Please Swipe again")
        clear()
    
    # Back to main menu
    elif(temp == "0"):
        state = menuLoop()

    # Change the state based on input
    elif(temp == "d" or temp == "s" or temp == "w"):
        state = cardUser.lower()
        completeData = False

    #Manual Entry
    elif(temp == "m"):
        manual(checkinTime,state)

    #Card was swiped
    
    elif cardUser[0] == '%' and cardUser[len(cardUser) -1] == '?':

        #Extraction Current Swipes
        data = data_extraction(cardUser.upper(),checkinTime)

        #Input New Names and Update Information
        update_Sheets(data, state)
        clear()

    else:
        print("Invalid Swipe..... Please Swipe again")
        clear()


#clear screen
def clear(pause = True):
    #for window use 'cls'
    #for mac use 'clear'
    if(pause):
        sleep(1)
    system('cls' if name == 'nt' else 'clear')
    #system('clear')

#Extraction Formula
def data_extraction(input,checkinTime):
    sortNames = []
    #regular expression to delete uncessary information
    regword = re.sub("([%].*([0-9]\^))|(( *0* +\?;[0-9]).*)", '', input)
    regword = regword.strip(" ")
    #split the line into lastName & firstName
    data = re.split("[/^]",regword)
    data[1] = re.sub(r"\s+$", "", data[1])
    #reformat SID number
    data[2] = re.search("8[0-9]+",data[2]).group(0)
    #append date
    data.append(checkinTime)
    return(data)

#Updating

def update_Sheets(student, state):
    clear(pause=False)
    print("Welcome to TTP")
    print(student[1] + " " + student[0])
    if credentials.access_token_expired:
        client.login()  # refreshes the token
    if(state == "s"):
        if(not checkDuplicates(student, state)):
            sheetSocial.append_row(student)
    elif(state == "w"):
        if(not checkDuplicates(student, state)):
            sheetSeminar.append_row(student)
    sheetDaily.append_row(student)
    

#Clean Sheet (Adjust in Alphabetical order )
# def sheet_Cleaner():
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

#Check the special events columns to make sure students are not getting recorded
#more than once in the same day
def checkDuplicates(student, state):
    #Get all the values from the time 
    if(state=="s"):
        cell_list = sheetSocial.get_all_values()
        cell_list = cell_list[1:]
        #print(cell_list)
        for i in cell_list:
            return (student[2]==i[2] and student[3][:9] == i[3][:9])
        return False
        #cell = [elem[:9] for elem in cell1]
    elif(state=="w"):
        cell_list = sheetSeminar.get_all_values()
        cell_list = cell_list[1:]
        for i in cell_list:
            return (student[2]==i[2] and student[3][:9] == i[3][:9])
        return False
    


