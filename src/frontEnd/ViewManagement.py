
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
#  ORGANIZATION: eSim team at FOSSEE, IIT Bombay.
#       CREATED: Wednesday 27 January 2015 
#      REVISION:  ---
#===============================================================================



from PyQt4 import QtCore
from PyQt4 import QtGui
from projManagement.Kicad import Kicad
from kicadtoNgspice.KicadtoNgspice import *


class ViewManagement(QtGui.QSplitter):
    
    def __init__(self, *args):
        # call init method of superclass
        QtGui.QSplitter.__init__(self, *args)
        # Creating dictionary which hold all the views
        self.views = {}
        
        #Creating object of Kicad.py
        self.obj_kicad = Kicad()
        
        # define the basic framework of view areas for the
        # application
        self.createView()
        self.setupView()
        
    def createView(self):
        #Adding view into views dictionary
        self.addView(QtGui.QTextEdit, 'ProjectExplorer')
        self.addView(QtGui.QTextEdit, 'ProjectToolbar')
        self.addView(QtGui.QTextEdit, 'CurrentProject')
        
    def setupView(self):
        #setup views to define various areas, such as placement of individual views 
        # the right segment also is a splitter, but with vertical orientation
        self.right = QtGui.QSplitter()
        self.right.setOrientation(QtCore.Qt.Vertical)
        
        #Layout
        self.grid = QtGui.QGridLayout()
        
        
        #Button for Project Tool Bar
        self.kicad_btn = QtGui.QPushButton()
        self.kicad_btn.setIcon(QtGui.QIcon('../images/default.png'))
        self.kicad_btn.setIconSize(QtCore.QSize(50,50))
        self.kicad_btn.setToolTip('<b>Open Schematic</b>')
        self.kicad_btn.clicked.connect(self.obj_kicad.openSchematic)
        self.grid.addWidget(self.kicad_btn,0,0)
        
        self.conversion_btn = QtGui.QPushButton()
        self.conversion_btn.setIcon(QtGui.QIcon('../images/default.png'))
        self.conversion_btn.setIconSize(QtCore.QSize(50,50))
        self.conversion_btn.setToolTip('<b>Convert Kicad to Ngspice</b>')
        self.conversion_btn.clicked.connect(self.obj_kicad.openKicadToNgspice)
        self.grid.addWidget(self.conversion_btn,0,1)
        
        
        self.ngspice_btn = QtGui.QPushButton()
        self.ngspice_btn.setIcon(QtGui.QIcon('../images/default.png'))
        self.ngspice_btn.setIconSize(QtCore.QSize(50,50))
        self.ngspice_btn.setToolTip('<b>Simulation</b>')
        self.grid.addWidget(self.ngspice_btn,0,2)
        
        self.footprint_btn = QtGui.QPushButton()
        self.footprint_btn.setIcon(QtGui.QIcon('../images/default.png'))
        self.footprint_btn.setIconSize(QtCore.QSize(50,50))
        self.footprint_btn.setToolTip('<b>Footprint Editor</b>')
        self.footprint_btn.clicked.connect(self.obj_kicad.openFootprint)
        self.grid.addWidget(self.footprint_btn,1,0)
        
        self.pcb_btn = QtGui.QPushButton()
        self.pcb_btn.setIcon(QtGui.QIcon('../images/default.png'))
        self.pcb_btn.setIconSize(QtCore.QSize(50,50))
        self.pcb_btn.setToolTip('<b>PCB Layout</b>')
        self.pcb_btn.clicked.connect(self.obj_kicad.openLayout)
        self.grid.addWidget(self.pcb_btn,1,1)
              
        
        # bind the top level views into the framework
        self.views['ProjectExplorer'].setParent(self)
        
        self.views['ProjectToolbar'].setParent(self.right)
        self.views['ProjectToolbar'].setLayout(self.grid)
        self.views['ProjectToolbar'].setReadOnly(True)
        
        self.views['CurrentProject'].setParent(self.right)
        self.views['CurrentProject'].setReadOnly(True)
        
        self.right.setParent(self)
        self.right.setSizes([20, 5])
        self.setSizes([5, 20])
        
    def addView(self, settype, name):
        
        #Adding views to dictionary
        #parameters:
        #settype             <class>     
        #name                <string>    
        
        self.views[name] = settype()
        
        


    
    
