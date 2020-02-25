from TTP_SpreadSheet_Function import *
#from cardRunnerFrontEnd import *


cardUser = ''

 #Title adder
new_title_daily = sheet_title(sheetDaily.row_values(1))
currentTitleDaily = sheetDaily.row_values(1)

new_title_social = sheet_title(sheetSocial.row_values(1))
currentTitleSocial = sheetSocial.row_values(1)

new_title_seminar = sheet_title(sheetSeminar.row_values(1))
currentTitleSeminar = sheetSeminar.row_values(1)


def main():
    # window()
    
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
        #Fast screen clear
        clear(pause=False)
        #record time of input
        checkinTime = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        #print out the welcome message and stores input into cardUser
        cardUser = welcomePrint(state)
        #passes card swipe or manual entry to parse and update spreadsheet
        parseData(cardUser,state,checkinTime)


if __name__=="__main__":
    while(True):
        try:
            main()
        except Exception as e:
            print("Main crashed. Error: %s", e)
            sleep(30)