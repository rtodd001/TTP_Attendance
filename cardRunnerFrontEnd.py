import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QFormLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

def window():
   app = QApplication(sys.argv)
   window = QWidget() #running window acts like a container 
   layout = QVBoxLayout() #stacks widgets vertically make
   formLayout = QFormLayout() #2 column layout left is string val and right is field widget
   firstName = QLineEdit()
   lastName = QLineEdit()
   idCard = QLineEdit()
   idCard.setEchoMode(QLineEdit.Password)
   

   textLabel = QLabel(window)
   textLabel.setText("Welcome to TPP Center")
   # textLabel.adjustSize(16)

   #Form input field layout
   formLayout.addRow("First Name ",firstName)
   formLayout.addRow("Last Name ",lastName)
   formLayout.addRow("ID ",idCard)

   layout.addWidget(QLabel(textLabel)) #title of window
   # layout.addChildLayout(QFormLayout(formLayout))
   layout.addWidget(QPushButton("Submit"))   

   window.setGeometry(50,50,320,200)
   window.setWindowTitle("TTP Card Scanner")
   # window.setLayout(layout)
   window.setLayout(formLayout)
   window.show()
   sys.exit(app.exec_())