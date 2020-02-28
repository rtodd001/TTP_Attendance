import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QFormLayout
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5 import QtGui

def window():
   app = QApplication(sys.argv)
   window = QWidget() #running window acts like a container 
   layout = QVBoxLayout() #stacks widgets vertically make
   formLayout = QFormLayout() #2 column layout left is string val and right is field widget
   
   #fields
   firstName = QLineEdit()
   lastName = QLineEdit()
   idCard = QLineEdit()
   idCard.setEchoMode(QLineEdit.Password)
   
   #center window
   

   textLabel = QLabel(window)
   textLabel.setText("Welcome to TPP Center")
   textLabel.setAlignment(Qt.AlignCenter)
   # textLabel.adjustSize(16)

   #Form input field layout
   formLayout.addRow("First Name ",firstName)
   formLayout.addRow("Last Name ",lastName)
   formLayout.addRow("ID ",idCard)

   layout.addWidget(QLabel(textLabel)) #title of window
   # layout.addChildLayout(QFormLayout(formLayout))
   layout.addWidget(QPushButton("Submit"))   

   # window.setLayout(layout)
   window.setLayout(formLayout)
   centerWindow(window)
   window.show()
   sys.exit(app.exec_())

def centerWindow(ui):
   ui.setGeometry(0,0,400,600)
   ui.setWindowTitle("TTP Card Scanner")
   qr = ui.frameGeometry()
   cp = QDesktopWidget().availableGeometry().center()
   qr.moveCenter(cp)
   ui.move(qr.topLeft())
   ui.setWindowIcon(QtGui.QIcon('./img/ttpLogo.png'))

#object class
# class Window(QtGui.QMainWindow):

#    def __init__(self):
#       super(Window, self).__init__()
#       self.setGeometry(0,0,400,600)
#       self.setWindowTitle("TTP Card Scanner")
#       self.setWindowIcon(QtGui.QIcon('./img/ttpLogo.png'))
#       qr = self.frameGeometry()
#       cp = QDesktopWidget().availableGeometry().center()
#       qr.moveCenter(cp)
#       self.move(qr.topLeft())
#       self.home()
