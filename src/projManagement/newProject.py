
#===============================================================================
#
#          FILE: newProject.py
# 
#         USAGE: --- 
# 
#   DESCRIPTION: It is called whenever new project is being called. 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Fahim Khan, fahim.elex@gmail.com
#  ORGANIZATION: ecSim team at FOSSEE, IIT Bombay.
#       CREATED: Wednesday 12 February 2015 
#      REVISION:  ---
#===============================================================================
from PyQt4 import QtGui,QtCore


class NewProjectInfo(QtGui.QWidget):
    """
    Class ProjectInfo accept model information from user
    """
    
    def __init__(self):
        super(NewProjectInfo, self).__init__()
        
    
    def body(self):
        print "Calling NewProjectInfo"
        self.projLabel = QtGui.QLabel("Enter Project Name :")
        self.projEdit = QtGui.QLineEdit()
                
        self.okbtn = QtGui.QPushButton("OK")
        self.okbtn.clicked.connect(self.createProject)
        
        self.cancelbtn = QtGui.QPushButton("Cancel")
        self.cancelbtn = QtGui.QPushButton('Cancel')
        self.cancelbtn.clicked.connect(self.cancelProject)
        
        
        #Layout
        self.grid = QtGui.QGridLayout()
        self.grid.addWidget(self.projLabel,2,0)
        self.grid.addWidget(self.projEdit, 2,1,1,5)
        self.grid.addWidget(self.okbtn,3,1)
        self.grid.addWidget(self.cancelbtn,3,2)
        self.setLayout(self.grid)
                     
        self.setGeometry(QtCore.QRect(80,80,80,80))
        self.setWindowTitle("New Project")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.show()
        
        
        '''
        self.LEGroup = QtGui.QGroupBox()
        self.LElayout = QtGui.QHBoxLayout()
        self.LElayout.addWidget(self.projLabel)
        self.LElayout.addWidget(self.projEdit)
        self.LEGroup.setLayout(self.LElayout)
        
        self.BtnGroup = QtGui.QGroupBox()
        self.Btnlayout = QtGui.QVBoxLayout()
        self.Btnlayout.addWidget(self.okbtn)
        self.Btnlayout.addWidget(self.cancelbtn)
        self.BtnGroup.setLayout(self.Btnlayout)
        
        self.mainlayout = QtGui.QHBoxLayout()
        self.mainlayout.addWidget(self.LEGroup)
        self.mainlayout.addWidget(self.BtnGroup)
        self.mainlayout.addStretch(1)
        
        self.setLayout(self.mainlayout)
        '''
        self.show()
        
    def createProject(self):
        print "Create Project Called"
        
    def cancelProject(self):
        self.close()
    
       
        
        
    