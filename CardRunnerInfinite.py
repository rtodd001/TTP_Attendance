from TTP_SpreadSheet_Function import *


cardUser = ''

 #Title adder
new_title_daily = sheet_title(sheetDaily.row_values(1))
currentTitleDaily = sheetDaily.row_values(1)

new_title_social = sheet_title(sheetSocial.row_values(1))
currentTitleSocial = sheetSocial.row_values(1)

new_title_seminar = sheet_title(sheetSeminar.row_values(1))
currentTitleSeminar = sheetSeminar.row_values(1)

# Unique messages to identify the state of the swipe
dailyMess = "Hello! Please Swipe Your Card to sign in: \n"
studySocailMess = "Study Jam/Social sign in! Please Swipe Your Card to sign in: \n"
seminarMess = "Welcome to the Seminar! Please Swipe Your Card to sign in: \n"


def main():
    if new_title_daily != currentTitleDaily:
                sheetDaily.delete_row(1)
                sheetDaily.insert_row(new_title_daily,1)
    if new_title_social != currentTitleSocial:
                sheetSocial.delete_row(1)
                sheetSocial.insert_row(new_title_social,1)
    if new_title_seminar != currentTitleSeminar:
                sheetSeminar.delete_row(1)
                sheetSeminar.insert_row(new_title_seminar,1)


    
    # Keep track of the current state
    # These variables will dictate the population of the Google Sheet
    # d : Daily/Regular days
    # s : Social/Study Jams 
    # w : Seminar/Workshops
    #
    # Default is Daily/Regular days
    state = menuLoop()

    while True:
        clear()
        checkinTime = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')


        # Print out the corresponding message for the state
        if(state ==  "d"):
            cardUser = getpass("Hello! Please Swipe Your Card to sign in: \n\n\n\nTo return to menu press '0' and press \"Enter\"\n\n\nBy signing-in you acknowledge that you have read and agree to abide by the Engineering Transfer Center (WCH 103) Space Policies.")
        elif(state == "s"):
            cardUser = getpass("Study Jam/Social sign in! Please Swipe Your Card to sign in: \n\n\n\nTo return to menu press '0' and press \"Enter\"\n\n\nBy signing-in you acknowledge that you have read and agree to abide by the Engineering Transfer Center (WCH 103) Space Policies.")
        elif(state == "w"):
            cardUser = getpass("Welcome to the Seminar! Please Swipe Your Card to sign in: \n\n\n\nTo return to menu press '0' and press \"Enter\"\n\n\nBy signing-in you acknowledge that you have read and agree to abide by the Engineering Transfer Center (WCH 103) Space Policies.")
        
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
            clear();

        #Card was swiped
        
        elif cardUser[0] == '%' and cardUser[len(cardUser) -1] == '?':

            #Extraction Current Swipes
            data = data_extraction(cardUser.upper(),checkinTime)

            #Input New Names and Update Information
            update_Sheets(data, state)
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