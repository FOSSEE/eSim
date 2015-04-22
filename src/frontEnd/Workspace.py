#===============================================================================
#
#          FILE: Workspace.py
# 
#         USAGE: --- 
# 
#   DESCRIPTION: This define all configuration used in Application. 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Fahim Khan, fahim.elex@gmail.com
#  ORGANIZATION: eSim team at FOSSEE, IIT Bombay.
#       CREATED: Wednesday 05 February 2015 
#      REVISION:  ---
#===============================================================================
from PyQt4 import QtCore, QtGui
from configuration.Appconfig import Appconfig

import os


class Workspace(QtGui.QWidget):
    """
    This class creates Workspace GUI.
    """
    def __init__(self):
        super(Workspace, self).__init__()
           
        self.obj_appconfig = Appconfig()
        
        #Initializing Workspace directory for project
        self.initWorkspace()
        
            
    def initWorkspace(self):
        #print "Calling workspace"
        self.note = QtGui.QTextEdit(self)
        self.workspace_label = QtGui.QLabel(self)
        self.worspace_loc = QtGui.QLineEdit(self)
            
        #Add text to text edit,label and line edit
        self.note.append(self.obj_appconfig.workspace_text)
        self.workspace_label.setText("Workspace:")
        self.worspace_loc.setText(self.obj_appconfig.home)
          
        #Buttons
        self.browsebtn = QtGui.QPushButton('Browse')
        self.browsebtn.clicked.connect(self.browseLocation)
        self.okbtn = QtGui.QPushButton('OK')
        self.okbtn.clicked.connect(self.createWorkspace)
        self.cancelbtn = QtGui.QPushButton('Cancel')
        self.cancelbtn.clicked.connect(self.defaultWorkspace)
            
        #Set Geometry
        #Need to set Geometry properly
        self.note.setGeometry(QtCore.QRect(0, 0, 400, 100))
        self.workspace_label.setGeometry(QtCore.QRect(10, 130, 81, 17))
        self.worspace_loc.setGeometry(QtCore.QRect(100, 150, 200, 100))
        self.browsebtn.setGeometry(QtCore.QRect(290, 120, 98, 27))
        self.okbtn.setGeometry(QtCore.QRect(290, 250, 98, 27))
        self.cancelbtn.setGeometry(QtCore.QRect(180, 250, 98, 27))
              
            
            
        #Layout
        self.hbox = QtGui.QHBoxLayout()
        self.hbox.addWidget(self.note)
            
        self.grid = QtGui.QGridLayout()
        self.grid.addChildLayout(self.hbox)
         
            
        self.grid.addWidget(self.workspace_label,2,0)
        self.grid.addWidget(self.worspace_loc, 2, 1)
        self.grid.addWidget(self.browsebtn, 2, 2)
        self.grid.addWidget(self.okbtn,3,2)
        self.grid.addWidget(self.cancelbtn,3,3)
        self.setLayout(self.grid)
                     
        self.setGeometry(QtCore.QRect(200,200,400,400))
        self.setWindowTitle("Workspace Launcher")
        #self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.note.setReadOnly(True)
        self.show()
        
           
    def defaultWorkspace(self):
        print "Default location selected" 
        self.close()
               
    def createWorkspace(self):
        print "Create workspace is called"
        self.create_workspace = str(self.worspace_loc.text())
        #Checking if Workspace already exist or not       
        if  os.path.isdir(self.create_workspace):
            print "Already present"
            self.obj_appconfig.default_workspace["workspace"] = self.create_workspace
        
        else:
            os.mkdir(self.create_workspace)
            self.obj_appconfig.default_workspace["workspace"] = self.create_workspace
        self.close()
        
        
            
    def browseLocation(self):
        print "Browse Location called"
        self.workspace_directory = QtGui.QFileDialog.getExistingDirectory(self, "Browse Location",os.path.expanduser("~"))
        print "Path file :", self.workspace_directory
        self.worspace_loc.setText(self.workspace_directory)
        