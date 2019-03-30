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
import time
import os


class Workspace(QtGui.QWidget):
    """
    This class creates Workspace GUI.
    """
    def __init__(self,parent=None):
        super(Workspace, self).__init__()
        self.obj_appconfig = Appconfig()
        
        #Initializing Workspace directory for project
        self.initWorkspace()
        
            
    def initWorkspace(self):
        #print "Calling workspace"
        
        self.mainwindow = QtGui.QVBoxLayout()
        self.split = QtGui.QSplitter()
        self.split.setOrientation(QtCore.Qt.Vertical)
        
        self.grid = QtGui.QGridLayout()
        self.note = QtGui.QTextEdit(self)
        self.workspace_label = QtGui.QLabel(self)
        self.workspace_loc = QtGui.QLineEdit(self)
    
        self.note.append(self.obj_appconfig.workspace_text)
        self.workspace_label.setText("Workspace:")
        self.workspace_loc.setText(self.obj_appconfig.home)
        
        #Buttons
        self.browsebtn = QtGui.QPushButton('Browse')
        self.browsebtn.clicked.connect(self.browseLocation)
        self.okbtn = QtGui.QPushButton('OK')
        self.okbtn.clicked.connect(self.createWorkspace)
        self.cancelbtn = QtGui.QPushButton('Cancel')
        self.cancelbtn.clicked.connect(self.defaultWorkspace)
        #Layout
        self.grid.addWidget(self.note, 0,0,1,15)
        self.grid.addWidget(self.workspace_label, 2,1)
        self.grid.addWidget(self.workspace_loc,2,2,2,12)
        self.grid.addWidget(self.browsebtn, 2,14)
        self.grid.addWidget(self.okbtn, 4,13)
        self.grid.addWidget(self.cancelbtn, 4,14)
    
        self.setGeometry(QtCore.QRect(500,250,400,400))
        self.setMaximumSize(4000, 200)
        self.setWindowTitle("eSim")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.note.setReadOnly(True)
        self.setWindowIcon(QtGui.QIcon('../../images/logo.png'))
        self.setLayout(self.grid)
        self.show()
        
           
    def defaultWorkspace(self):
        print("Default workspace selected : "+self.obj_appconfig.default_workspace["workspace"])
        self.imp_var=1
        self.obj_appconfig.print_info('Default workspace selected : ' + self.obj_appconfig.default_workspace["workspace"]) 
        self.close()
        var_appView.show()
        time.sleep(1)
        var_appView.splash.close()
 


        
    def close(self, *args, **kwargs):
        self.window_open_close=1
        self.close_var=1
        return QtGui.QWidget.close(self, *args, **kwargs)


    def returnWhetherClickedOrNot(self,appView):
        global var_appView
        var_appView=appView

                   
    def createWorkspace(self):
        print("Function : Create workspace")
        self.create_workspace = str(self.workspace_loc.text())
        self.obj_appconfig.print_info('Workspace : ' + self.create_workspace)
        #Checking if Workspace already exist or not       
        if  os.path.isdir(self.create_workspace):
            self.obj_appconfig.default_workspace["workspace"] = self.create_workspace
        else:
            os.mkdir(self.create_workspace)
            self.obj_appconfig.default_workspace["workspace"] = self.create_workspace
        self.imp_var=1
        self.close()  
        var_appView.show()
        time.sleep(1)
        var_appView.splash.close()
        
            
    def browseLocation(self):
        print("Function : Browse Location")
        self.workspace_directory = QtGui.QFileDialog.getExistingDirectory(self, "Browse Location",os.path.expanduser("~"))
        self.workspace_loc.setText(self.workspace_directory)
        