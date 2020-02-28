from Student import *
#from cardRunnerFrontEnd import *

student = Student()

 #Title adder
new_title_daily = student.sheet_title(sheetDaily.row_values(1))
currentTitleDaily = sheetDaily.row_values(1)

new_title_social = student.sheet_title(sheetSocial.row_values(1))
currentTitleSocial = sheetSocial.row_values(1)

new_title_seminar = student.sheet_title(sheetSeminar.row_values(1))
currentTitleSeminar = sheetSeminar.row_values(1)


def main():
    window()
    
    if new_title_daily != currentTitleDaily:
                sheetDaily.delete_row(1)
                sheetDaily.insert_row(new_title_daily,1)
    if new_title_social != currentTitleSocial:
                sheetSocial.delete_row(1)
                sheetSocial.insert_row(new_title_social,1)
    if new_title_seminar != currentTitleSeminar:
                sheetSeminar.delete_row(1)
                sheetSeminar.insert_row(new_title_seminar,1)

    #Initiailze the state on boot
    student.menu()

    while True:
        #Fast screen clear
        student.clear(pause=False)
        #Run the card swiping program
        student.run()


if __name__=="__main__":
    while(True):
        try:
            main()
        except Exception as e:
            print("Main crashed. Error: %s", e)
            sleep(30)