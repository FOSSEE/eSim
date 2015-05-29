
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
#  ORGANIZATION: eSim team at FOSSEE, IIT Bombay.
#       CREATED: Wednesday 12 February 2015 
#      REVISION:  ---
#===============================================================================

from PyQt4 import QtGui
from Validation import Validation
from configuration.Appconfig import Appconfig
import os
import json


class OpenProjectInfo(QtGui.QWidget):
    """
    This class is called when User click on Open Project Button
    """
    def __init__(self):
        super(OpenProjectInfo, self).__init__()
        self.obj_validation = Validation()
              
    def body(self):
        self.obj_Appconfig = Appconfig()
        self.openDir = self.obj_Appconfig.default_workspace["workspace"]
        #print "default workspace is now 1", self.openDir
        self.projDir=QtGui.QFileDialog.getExistingDirectory(self,"open",self.openDir)
        if self.obj_validation.validateOpenproj(self.projDir) == True:
            #print "Pass open project test"
            self.obj_Appconfig = Appconfig()
            self.obj_Appconfig.current_project['ProjectName'] = str(self.projDir)
            if os.path.isdir(self.projDir):
                print "true"
        
            for dirs, subdirs, filelist in os.walk(self.obj_Appconfig.current_project["ProjectName"]):
                directory = dirs
                files = filelist
            self.obj_Appconfig.project_explorer[dirs] = filelist
            json.dump(self.obj_Appconfig.project_explorer, open(self.obj_Appconfig.dictPath,'w'))
            return dirs, filelist
            
        else:
            #print "Failed open project test"
            reply = QtGui.QMessageBox.critical(None, "Error Message",'''<b> Error: The project doesn't contain .proj file.</b><br/>
                    <b>Please select the proper project directory else you won't be able to perform any operation</b>''',QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel)
            if reply == QtGui.QMessageBox.Ok:
                self.body()
            elif reply == QtGui.QMessageBox.Cancel:
                pass
            else:
                pass
                
  
        
            
        
        