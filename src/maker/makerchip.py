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
        self.maker_widget = None
        self.ngveri_widget = None
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
        global filecount
        self.convertWindow = QtWidgets.QWidget()

        # Get current theme from parent Application if possible
        is_dark_theme = False
        parent = self.parent()
        if parent and hasattr(parent, 'is_dark_theme'):
            is_dark_theme = parent.is_dark_theme

        self.MakerTab = QtWidgets.QScrollArea()
        self.maker_widget = Maker.Maker(filecount, is_dark_theme=is_dark_theme)
        self.MakerTab.setWidget(self.maker_widget)
        self.MakerTab.setWidgetResizable(True)

        self.NgVeriTab = QtWidgets.QScrollArea()
        self.ngveri_widget = NgVeri.NgVeri(filecount, is_dark_theme=is_dark_theme)
        self.NgVeriTab.setWidget(self.ngveri_widget)
        self.NgVeriTab.setWidgetResizable(True)

        self.tabWidget = QtWidgets.QTabWidget()
        self.tabWidget.addTab(self.MakerTab, "Makerchip")
        self.tabWidget.addTab(self.NgVeriTab, "NgVeri")
        
        # Re-apply theme on tab change
        self.tabWidget.currentChanged.connect(self._on_tab_changed)
        
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setContentsMargins(15, 15, 15, 15)  # Add margins
        self.mainLayout.setSpacing(15)  # Add spacing
        self.mainLayout.addWidget(self.tabWidget)
        
        self.convertWindow.setLayout(self.mainLayout)
        self.convertWindow.show()
        
        filecount = filecount + 1
        return self.convertWindow

    def set_theme(self, is_dark_theme):
        """Update the theme for both Maker and NgVeri widgets."""
        if self.maker_widget:
            self.maker_widget.set_theme(is_dark_theme)
        if self.ngveri_widget:
            self.ngveri_widget.set_theme(is_dark_theme)

    def _on_tab_changed(self, index):
        # Ensure the correct theme is always applied to the active tab
        is_dark_theme = False
        parent = self.parent()
        if parent and hasattr(parent, 'is_dark_theme'):
            is_dark_theme = parent.is_dark_theme
        if index == 0 and self.maker_widget:
            self.maker_widget.set_theme(is_dark_theme)
        elif index == 1 and self.ngveri_widget:
            self.ngveri_widget.set_theme(is_dark_theme)
