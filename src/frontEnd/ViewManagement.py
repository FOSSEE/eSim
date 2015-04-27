
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
from ProjectExplorer import ProjectExplorer


class ViewManagement(QtGui.QSplitter):
    """
    This class creates View on FrontWindow 
    """
    
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
        self.addView(ProjectExplorer, 'ProjectExplorer')
        self.addView(QtGui.QTextEdit, 'MainArea')
        self.addView(QtGui.QTextEdit, 'Plotting')
        self.addView(QtGui.QTextEdit, 'Browser')
        
        
        
    def setupView(self):
        #setup views to define various areas, such as placement of individual views 
        # the right segment also is a splitter, but with vertical orientation
        self.right = QtGui.QSplitter()
        self.right.setOrientation(QtCore.Qt.Vertical)
        
        #Layout
        self.grid = QtGui.QGridLayout()
        
        
        #Button for Project Tool Bar
        self.kicad = QtGui.QAction(QtGui.QIcon('../images/default.png'),'<b>Open Schematic</b>',self)
        self.kicad.triggered.connect(self.obj_kicad.openSchematic)
        
        self.conversion = QtGui.QAction(QtGui.QIcon('../images/default.png'),'<b>Convert Kicad to Ngspice</b>',self)
        self.conversion.triggered.connect(self.obj_kicad.openKicadToNgspice)
        
        
        self.ngspice = QtGui.QAction(QtGui.QIcon('../images/default.png'), '<b>Simulation</b>', self)
        
        self.footprint = QtGui.QAction(QtGui.QIcon('../images/default.png'),'<b>Footprint Editor</b>',self)
        self.footprint.triggered.connect(self.obj_kicad.openFootprint)
        
        self.pcb = QtGui.QAction(QtGui.QIcon('../images/default.png'),'<b>PCB Layout</b>',self)
        self.pcb.triggered.connect(self.obj_kicad.openLayout)
              
        self.lefttoolbar= QtGui.QToolBar()
        self.lefttoolbar.addAction(self.kicad)
        self.lefttoolbar.addAction(self.conversion)
        self.lefttoolbar.addAction(self.ngspice)
        self.lefttoolbar.addAction(self.footprint)
        self.lefttoolbar.addAction(self.pcb)
        #Adding one more splitter
        self.browser = QtGui.QSplitter()
        self.browser.setOrientation(QtCore.Qt.Vertical)
        
        # bind the top level views into the framework
        
        self.lefttoolbar.setParent(self)
        self.lefttoolbar.setOrientation(QtCore.Qt.Vertical)
        self.views['ProjectExplorer'].setParent(self)
        
        self.views['MainArea'].setParent(self.right)
        
        self.views['Plotting'].setParent(self.right)
        self.views['Plotting'].setReadOnly(True)
        
        self.views['Browser'].setParent(self.browser)
        self.views['Browser'].setReadOnly(True)
        
        self.right.setParent(self)
        self.browser.setParent(self)
        self.right.setSizes([20, 5])
        #self.setSizes([5, 20])
        
    def addView(self, settype, name):
        
        #Adding views to dictionary
        #parameters:
        #settype             <class>     
        #name                <string>    
        
        self.views[name] = settype()
        
        


    
    
