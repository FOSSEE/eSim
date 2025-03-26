# =========================================================================
#             FILE: makerchip.py
#
#            USAGE: ---
#
#      DESCRIPTION: This defines all components of the Makerchip.
#
#          OPTIONS: ---
#     REQUIREMENTS: ---
#             BUGS: ---
#            NOTES: ---
#           AUTHOR: Sumanto Kar, sumantokar@iitb.ac.in, FOSSEE, IIT Bombay
# ACKNOWLEDGEMENTS: Rahul Paknikar, rahulp@iitb.ac.in, FOSSEE, IIT Bombay
#                Digvijay Singh, digvijay.singh@iitb.ac.in, FOSSEE, IIT Bombay
#                Prof. Maheswari R. and Team, VIT Chennai
#     GUIDED BY: Steve Hoover, Founder Redwood EDA
#                Kunal Ghosh, VLSI System Design Corp.Pvt.Ltd
#                Anagha Ghosh, VLSI System Design Corp.Pvt.Ltd
# OTHER CONTRIBUTERS:
#                Prof. Madhuri Kadam, Shree L. R. Tiwari College of Engineering
#                Rohinth Ram, Madras Institue of Technology
#                Charaan S., Madras Institue of Technology
#                Nalinkumar S., Madras Institue of Technology
#  ORGANIZATION: eSim Team at FOSSEE, IIT Bombay
#       CREATED: Monday 29, November 2021
#      REVISION: Tuesday 25, January 2022
# =========================================================================

# importing the files and libraries
from PyQt5 import QtWidgets
from . import Maker
from . import NgVeri

# filecount is used to count thenumber of objects created
filecount = 0


# This class creates objects for creating the Maker and the Ngveri tabs
class makerchip(QtWidgets.QWidget):

    # initialising the variables
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self)

        # filecount=int(open("a.txt",'r').read())
        print(filecount)
        # self.splitter.setOrientation(QtCore.Qt.Vertical)
        print("==================================")
        print("Makerchip and Verilog to Ngspice Converter")
        print("==================================")
        self.createMainWindow()

    # Creating the main Window(Main tab)

    def createMainWindow(self):
        self.vbox = QtWidgets.QVBoxLayout()
        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addStretch(1)
        self.vbox.addWidget(self.createWidget())
        self.vbox.addLayout(self.hbox)

        self.setLayout(self.vbox)
        self.setWindowTitle("Makerchip and Verilog to Ngspice Converter")
        self.show()

    # Creating the maker and ngveri widgets
    def createWidget(self):
        global obj_Maker
        global filecount
        self.convertWindow = QtWidgets.QWidget()

        self.MakerTab = QtWidgets.QScrollArea()
        obj_Maker = Maker.Maker(filecount)
        self.MakerTab.setWidget(obj_Maker)
        self.MakerTab.setWidgetResizable(True)

        global obj_NgVeri
        self.NgVeriTab = QtWidgets.QScrollArea()
        obj_NgVeri = NgVeri.NgVeri(filecount)
        self.NgVeriTab.setWidget(obj_NgVeri)
        self.NgVeriTab.setWidgetResizable(True)
        self.tabWidget = QtWidgets.QTabWidget()
        self.tabWidget.addTab(self.MakerTab, "Makerchip")
        self.tabWidget.addTab(self.NgVeriTab, "NgVeri")
        # The object refresh gets destroyed when Ngspice\
        # to verilog converter is called
        # so calling refresh_change to start toggling of refresh again
        self.tabWidget.currentChanged.connect(obj_Maker.refresh_change)
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addWidget(self.tabWidget)
        self.convertWindow.setLayout(self.mainLayout)
        self.convertWindow.show()
        # incrementing filecount for every new window
        filecount = filecount + 1
        return self.convertWindow
