import re
import os
import datetime
import gspread
import pprint
from collections  import defaultdict
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
        

#Title Function
def sheet_title(current_title):
    #Google Sheet Code [Chanage Weekly]
    size_Current_Title = len(current_title)

    if size_Current_Title == 0:
        new_title = ['Last Name', 'First Name','SID',"Check in Time"]
        return (new_title)
    else:
        return current_title


#clear screen
def clear():
    #for window use 'cls'
    #for mac use 'clear'
    sleep(1)
    os.system('clear')

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
    


