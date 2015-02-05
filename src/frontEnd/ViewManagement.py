
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
        self.addView(QtGui.QTextEdit, 'test1')
        self.addView(QtGui.QTextEdit, 'test2')
        self.addView(QtGui.QTextEdit, 'test3')
        
    def setupView(self):
        
        #setup views to define various areas, such as placement of individual views 
              
        # the right segment also is a splitter, but with vertical orientation
        right = QtGui.QSplitter()
        right.setOrientation(QtCore.Qt.Vertical)
        
        # bind the top level views into the framework
        self.views['test1'].setParent(self)
        
        right.setParent(self)
        
        self.views['test2'].setParent(right)
        self.views['test3'].setParent(right)
        right.setSizes([20, 5])
        self.setSizes([5, 20])
        
    def addView(self, settype, name):
        
        #Adding views to dictionary
        #parameters:
        #settype             <class>     
        #name                <string>    
        
        self.views[name] = settype()
        
        
    

    
    
