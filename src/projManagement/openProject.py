
#===============================================================================
#
#          FILE: openProject.py
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

from PyQt4 import QtGui
from Validation import Validation
from configuration.Appconfig import Appconfig



class ProjectInfo(QtGui.QWidget):
    """
    Class ProjectInfo accept model information from user
    
    """
    def __init__(self):
        super(ProjectInfo, self).__init__()
        self.obj_validation = Validation()
              
    def body(self):
        self.proj_directory = QtGui.QFileDialog.getExistingDirectory()
               
        if self.obj_validation.validateOpenproj(self.proj_directory) == True:
            print "Pass open project test"
            self.obj_Appconfig = Appconfig()
            self.obj_Appconfig.current_project['ProjectName'] = self.proj_directory
            
            
        else:
            print "Failed open project test"
            reply = QtGui.QMessageBox.critical(None, "Error Message",'''<b> Error: The project doesn't contain .proj file.</b><br/>
                    <b>Please select the proper project directory else you won't be able to perform any operation</b>''',QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel)
            if reply == QtGui.QMessageBox.Ok:
                self.body()
            elif reply == QtGui.QMessageBox.Cancel:
                pass
            else:
                pass
                
  
        
            
        
        