from TTP_SpreadSheet_Function import *

checkinTime = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
cardUser = ''

 #Title adder
new_title = sheet_title(sheet.row_values(1))
currentTitle = sheet.row_values(1)

# Unique messages to identify the state of the swipe
dailyMess = "Hello! Please Swipe Your Card to sign in: \n"
studySocailMess = "Study Jam sign in! Please Swipe Your Card to sign in: \n"
seminarMess = "Welcome to the Seminar! Please Swipe Your Card to sign in: \n"


def main():
    if new_title != currentTitle:
                sheet.delete_row(1)
                sheet.insert_row(new_title,1)
    
    # Keep track of the current state
    # These variables will dictate the population of the Google Sheet
    # d : Daily/Regular days
    # s : Social/Study Jams 
    # w : Seminar/Workshops
    #
    # Default is Daily/Regular days
    state = 'd'

    while True:
        clear()



        # Print out the corresponding message for the state
        if(state ==  "d"):
            cardUser = getpass("Hello! Please Swipe Your Card to sign in: \n")
        elif(state == "s"):
            cardUser = getpass("Study Jam sign in! Please Swipe Your Card to sign in: \n")
        elif(state == "w"):
            cardUser = getpass("Welcome to the Seminar! Please Swipe Your Card to sign in: \n")
        
        temp = cardUser.lower()

        #Invalid swipe
        if(cardUser == '' or not cardUser):
            print("Invalid Swipe..... Please Swipe again")
            clear()
        
        # Change the state based on input
        elif(temp == "d" or temp == "s" or temp == "w"):
            state = cardUser.lower()
            completeData = False

        #Manual Entry
        elif(temp == "m"):
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
                update_Sheets(data)
            clear();

        #Card was swiped
        
        elif cardUser[0] == '%' and cardUser[len(cardUser) -1] == '?':

            #Extraction Current Swipes
            data = data_extraction(cardUser.upper(),checkinTime)

            #Input New Names and Update Information
            update_Sheets(data)
            clear();

        else:
            print("Invalid Swipe..... Please Swipe again")
            clear()


if __name__=="__main__":
    while(True):
        try:
            main()
        except Exception as e:
            print("Main crashed. Error: %s", e)
            sleep(30)
