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
#  ORGANIZATION: ecSim team at FOSSEE, IIT Bombay.
#       CREATED: Wednesday 05 February 2015 
#      REVISION:  ---
#===============================================================================
from PyQt4 import QtCore, QtGui
from configuration.Appconfig import Appconfig

import os


class Workspace(QtGui.QWidget):
    """
    Start workspace gui
    """
    def __init__(self):
        super(Workspace, self).__init__()
        
        #Button status lable
        #self.status_label = QtGui.QLabel('NO')

        self.obj = Appconfig()
       
        #Initializing Workspace directory for project
        self.initWorkspace()
        
            
    def initWorkspace(self):
        print "Calling workspace"
        self.tedit = QtGui.QTextEdit(self)
        self.label = QtGui.QLabel(self)
        self.ledit = QtGui.QLineEdit(self)
            
        #Add text to text edit,label and line edit
        self.tedit.append(self.obj.workspace_text)
        self.label.setText("Workspace:")
        self.ledit.setText(self.obj.home)
          
        #Buttons
        self.browsebtn = QtGui.QPushButton('Browse')
        self.browsebtn.clicked.connect(self.browseLocation)
        self.okbtn = QtGui.QPushButton('OK')
        self.okbtn.clicked.connect(self.createWorkspace)
        self.cancelbtn = QtGui.QPushButton('Cancel')
        self.cancelbtn.clicked.connect(self.defaultWorkspace)
            
        #Set Geometry
        self.tedit.setGeometry(QtCore.QRect(0, 0, 400, 100))
        self.label.setGeometry(QtCore.QRect(10, 130, 81, 17))
        self.ledit.setGeometry(QtCore.QRect(100, 150, 200, 100))
        self.browsebtn.setGeometry(QtCore.QRect(290, 120, 98, 27))
        self.okbtn.setGeometry(QtCore.QRect(290, 250, 98, 27))
        self.cancelbtn.setGeometry(QtCore.QRect(180, 250, 98, 27))
              
            
            
        #Layout
        self.hbox = QtGui.QHBoxLayout()
        self.hbox.addWidget(self.tedit)
            
        self.grid = QtGui.QGridLayout()
        self.grid.addChildLayout(self.hbox)
         
            
        self.grid.addWidget(self.label,2,0)
        self.grid.addWidget(self.ledit, 2, 1)
        self.grid.addWidget(self.browsebtn, 2, 2)
        self.grid.addWidget(self.okbtn,3,2)
        self.grid.addWidget(self.cancelbtn,3,3)
        self.setLayout(self.grid)
                     
        self.setGeometry(QtCore.QRect(200,200,400,400))
        self.setWindowTitle("Workspace Launcher")
        #self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.tedit.setReadOnly(True)
        self.show()
        
           
    def defaultWorkspace(self):
        print "Default location selected" 
        self.close()
               
    def createWorkspace(self):
        print "Create workspace is called"
        self.create_workspace = str(self.ledit.text())
               
        if  os.path.isdir(self.create_workspace):
            pass
            print "Already present"
            self.obj.default_workspace["workspace"] = self.create_workspace
        
        else:
            os.mkdir(self.create_workspace)
            self.obj.default_workspace["workspace"] = self.create_workspace
        
        
            
    def browseLocation(self):
        print "Browse Location called"
        self.workspace_directory = QtGui.QFileDialog.getExistingDirectory()
        print "Path file :", self.workspace_directory
        self.ledit.setText(self.workspace_directory)
        