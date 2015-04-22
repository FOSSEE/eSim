
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
#  ORGANIZATION: eSim team at FOSSEE, IIT Bombay.
#       CREATED: Wednesday 12 February 2015 
#      REVISION:  ---
#===============================================================================
from PyQt4 import QtGui,QtCore
from Validation import Validation
from configuration.Appconfig import Appconfig
import os

class NewProjectInfo(QtGui.QWidget):
    """
    This class is called when User create new Project.
    """
    
    def __init__(self):
        super(NewProjectInfo, self).__init__()
        self.obj_validation = Validation()
        self.obj_appconfig = Appconfig()
        
    
    def body(self):
        """
        This function create gui for New Project Info
        """
        #print "Calling NewProjectInfo"
        self.projLabel = QtGui.QLabel("Enter Project Name :")
        self.projEdit = QtGui.QLineEdit()
                
        self.okbtn = QtGui.QPushButton("OK")
        self.okbtn.clicked.connect(self.createProject)
        
        self.cancelbtn = QtGui.QPushButton("Cancel")
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
      
        
    def createProject(self):
        """
        This function create Project related directories and files
        """
        #print "Create Project Called"
        self.workspace = self.obj_appconfig.default_workspace['workspace']
        self.projName = self.projEdit.text()
        self.projName = str(self.projName).rstrip().lstrip()  #Remove leading and trailing space
        
        self.projDir = os.path.join(self.workspace,str(self.projName))
        
               
        #Validation for newProject
        if self.projName == "":
            self.reply = "NONE"
        else:
            self.reply = self.obj_validation.validateNewproj(str(self.projDir))
        
        #Checking Validations Response
        if self.reply == "VALID":
            print "Validated : Creating project directory"
            #create project directory
            try:
                os.mkdir(self.projDir)
                self.close()
                self.projFile = os.path.join(self.projDir,self.projName+".proj")
                f = open(self.projFile,"w")
            except:
                #print "Some Thing Went Wrong"
                self.msg = QtGui.QErrorMessage(self)
                self.msg.showMessage('Unable to create project. Please make sure you have write permission on '+self.workspace)
                self.msg.setWindowTitle("Error Message")
            f.write("schematicFile " + self.projName+".sch\n")
            f.close()
            
            #Now Change the current working project
            self.obj_appconfig.current_project['ProjectName'] = self.projDir 
            
        elif self.reply == "CHECKEXIST":
            #print "Project already exist"
            self.msg = QtGui.QErrorMessage(self)
            self.msg.showMessage('The project "'+self.projName+'" already exist.Please select the different name or delete existing project')
            self.msg.setWindowTitle("Error Message")
            
            
        elif self.reply == "CHECKNAME":
            #print "Name is not proper"
            self.msg = QtGui.QErrorMessage(self)
            self.msg.showMessage('The project name should not contain space between them')
            self.msg.setWindowTitle("Error Message")
        
        elif self.reply == "NONE":
            #print "Empty Project Name"
            self.msg = QtGui.QErrorMessage(self)
            self.msg.showMessage('The project name cannot be empty')
            self.msg.setWindowTitle("Error Message")
        
    def cancelProject(self):
        self.close()
    
       
        
        
    