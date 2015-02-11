
#===============================================================================
#
#          FILE: ViewManagement.py
# 
#         USAGE: --- 
# 
#   DESCRIPTION: It contain all the view for main Application
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Fahim Khan, fahim.elex@gmail.com
#  ORGANIZATION: ecSim team at FOSSEE, IIT Bombay.
#       CREATED: Wednesday 27 January 2015 
#      REVISION:  ---
#===============================================================================



from PyQt4 import QtCore
from PyQt4 import QtGui


class ViewManagement(QtGui.QSplitter):
    
    def __init__(self, *args):
        # call init method of superclass
        QtGui.QSplitter.__init__(self, *args)
        # Creating dictionary which hold all the views
        self.views = {}
        
        # define the basic framework of view areas for the
        # application
        self.createView()
        self.setupView()
        
    def createView(self):
        #Adding view into views dictionary
        self.addView(QtGui.QTextEdit, 'Project Explorer')
        self.addView(QtGui.QTextEdit, 'test2')
        self.addView(QtGui.QTextEdit, 'test3')
        
    def setupView(self):
        #setup views to define various areas, such as placement of individual views 
        # the right segment also is a splitter, but with vertical orientation
        self.right = QtGui.QSplitter()
        self.right.setOrientation(QtCore.Qt.Vertical)
        
        #Layout
        self.grid = QtGui.QGridLayout()
        
        
        #Button for QFrame
        self.kicad_btn = QtGui.QPushButton()
        self.kicad_btn.setIcon(QtGui.QIcon('../images/default.png'))
        self.kicad_btn.setIconSize(QtCore.QSize(50,50))
        self.grid.addWidget(self.kicad_btn,0,0)
        
        self.conversion_btn = QtGui.QPushButton()
        self.conversion_btn.setIcon(QtGui.QIcon('../images/default.png'))
        self.conversion_btn.setIconSize(QtCore.QSize(50,50))
        self.grid.addWidget(self.conversion_btn,0,1)
        
        
        self.ngspice_btn = QtGui.QPushButton()
        self.ngspice_btn.setIcon(QtGui.QIcon('../images/default.png'))
        self.ngspice_btn.setIconSize(QtCore.QSize(50,50))
        self.grid.addWidget(self.ngspice_btn,0,2)
        
        self.footprint_btn = QtGui.QPushButton()
        self.footprint_btn.setIcon(QtGui.QIcon('../images/default.png'))
        self.footprint_btn.setIconSize(QtCore.QSize(50,50))
        self.grid.addWidget(self.footprint_btn,1,0)
        
        self.pcb_btn = QtGui.QPushButton()
        self.pcb_btn.setIcon(QtGui.QIcon('../images/default.png'))
        self.pcb_btn.setIconSize(QtCore.QSize(50,50))
        self.grid.addWidget(self.pcb_btn,1,1)
        
    
        
             
        
        # bind the top level views into the framework
        self.views['Project Explorer'].setParent(self)
        
        self.views['test2'].setParent(self.right)
        self.views['test2'].setLayout(self.grid)
        self.views['test2'].setReadOnly(True)
        
        self.views['test3'].setParent(self.right)
        
        self.right.setParent(self)
        self.right.setSizes([20, 5])
        self.setSizes([5, 20])
        
    def addView(self, settype, name):
        
        #Adding views to dictionary
        #parameters:
        #settype             <class>     
        #name                <string>    
        
        self.views[name] = settype()
        
        
    

    
    
