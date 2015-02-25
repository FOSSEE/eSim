#===============================================================================
#
#          FILE: openKicad.py
# 
#         USAGE: --- 
# 
#   DESCRIPTION: It call kicad schematic
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Fahim Khan, fahim.elex@gmail.com
#  ORGANIZATION: ecSim team at FOSSEE, IIT Bombay.
#       CREATED: Tuesday 17 Feb 2015 
#      REVISION:  ---
#===============================================================================

import os
import Validation
from configuration.Appconfig import Appconfig
import Worker
from PyQt4 import QtGui

class Kicad:
    """
    Class Kicad open Schematic,PCB and Layout
    """
    def __init__(self):
        self.obj_validation = Validation.Validation()
        self.obj_appconfig = Appconfig()
        
    
    def openSchematic(self):
        print "Kicad Schematic is called"
        self.projDir = self.obj_appconfig.current_project["ProjectName"]       
        #Validating if current project is available or not
        
        if self.obj_validation.validateKicad(self.projDir):
            print "calling Kicad schematic ",self.projDir
            self.projName = os.path.basename(self.projDir)
            self.project = os.path.join(self.projDir,self.projName)
            
            #Creating a command to run
            self.cmd = "eeschema "+self.project+".sch "
            self.obj_workThread = Worker.WorkerThread(self.cmd)
            self.obj_workThread.start()
            
        else:
            self.msg = QtGui.QErrorMessage(None)
            self.msg.showMessage('Please select the project first. You can either create new project or open existing project')
            self.msg.setWindowTitle("Error Message")
        
        
        
    def openFootprint(self):
        print "Kicad Foot print Editor called"
        self.projDir = self.obj_appconfig.current_project["ProjectName"]       
        #Validating if current project is available or not
        
        if self.obj_validation.validateKicad(self.projDir):
            print "calling Kicad FootPrint Editor ",self.projDir
            self.projName = os.path.basename(self.projDir)
            self.project = os.path.join(self.projDir,self.projName)
            
            #Creating a command to run
            self.cmd = "cvpcb "+self.project+".net "
            self.obj_workThread = Worker.WorkerThread(self.cmd)
            self.obj_workThread.start()
            
        else:
            self.msg = QtGui.QErrorMessage(None)
            self.msg.showMessage('Please select the project first. You can either create new project or open existing project')
            self.msg.setWindowTitle("Error Message")
        
    def openLayout(self):
        print "Kicad Layout is called"
        self.projDir = self.obj_appconfig.current_project["ProjectName"]       
        #Validating if current project is available or not
        if self.obj_validation.validateKicad(self.projDir):
            print "calling Kicad schematic ",self.projDir
            self.projName = os.path.basename(self.projDir)
            self.project = os.path.join(self.projDir,self.projName)
            
            #Creating a command to run
            self.cmd = "pcbnew "+self.project+".net "
            self.obj_workThread = Worker.WorkerThread(self.cmd)
            self.obj_workThread.start()
            
        else:
            self.msg = QtGui.QErrorMessage(None)
            self.msg.showMessage('Please select the project first. You can either create new project or open existing project')
            self.msg.setWindowTitle("Error Message")        