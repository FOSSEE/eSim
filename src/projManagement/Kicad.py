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
#  ORGANIZATION: eSim team at FOSSEE, IIT Bombay.
#       CREATED: Tuesday 17 Feb 2015 
#      REVISION:  ---
#===============================================================================

import os
from . import Validation
from configuration.Appconfig import Appconfig
from . import Worker
from PyQt4 import QtGui

class Kicad:
    """
    This class called the Kicad Schematic,KicadtoNgspice Converter,Layout editor and Footprint Editor
    """
    def __init__(self,dockarea):
        self.obj_validation = Validation.Validation()
        self.obj_appconfig = Appconfig()
        self.obj_dockarea= dockarea
    
    def openSchematic(self):
        """
        This function create command to open Kicad schematic
        """
        print("Function : Open Kicad Schematic")
        self.projDir = self.obj_appconfig.current_project["ProjectName"]
        try:
            self.obj_appconfig.print_info('Kicad Schematic is called for project ' + self.projDir)
        except:
            pass              
        #Validating if current project is available or not
        
        if self.obj_validation.validateKicad(self.projDir):
            #print "calling Kicad schematic ",self.projDir
            self.projName = os.path.basename(self.projDir)
            self.project = os.path.join(self.projDir,self.projName)
            
            #Creating a command to run
            self.cmd = "eeschema "+self.project+".sch "
            self.obj_workThread = Worker.WorkerThread(self.cmd)
            self.obj_workThread.start()
            
        else:
            self.msg = QtGui.QErrorMessage(None)
            self.msg.showMessage('Please select the project first. You can either create new project or open existing project')
            self.obj_appconfig.print_warning('Please select the project first. You can either create new project or open existing project')
            self.msg.setWindowTitle("Error Message")
        
        
    '''
    #Commenting as it is no longer needed as PBC and Layout will open from eeschema 
    def openFootprint(self):
        """
        This function create command to open Footprint editor 
        """
        print "Kicad Foot print Editor called"
        self.projDir = self.obj_appconfig.current_project["ProjectName"]
        try: 
            self.obj_appconfig.print_info('Kicad Footprint Editor is called for project : ' + self.projDir)      
        except:
            pass
        #Validating if current project is available or not
        
        if self.obj_validation.validateKicad(self.projDir):
            #print "calling Kicad FootPrint Editor ",self.projDir
            self.projName = os.path.basename(self.projDir)
            self.project = os.path.join(self.projDir,self.projName)
            
            #Creating a command to run
            self.cmd = "cvpcb "+self.project+".net "
            self.obj_workThread = Worker.WorkerThread(self.cmd)
            self.obj_workThread.start()
            
        else:
            self.msg = QtGui.QErrorMessage(None)
            self.msg.showMessage('Please select the project first. You can either create new project or open existing project')
            self.obj_appconfig.print_warning('Please select the project first. You can either create new project or open existing project')
            self.msg.setWindowTitle("Error Message")
        
    def openLayout(self):
        """
        This function create command to open Layout editor
        """
        print "Kicad Layout is called"
        self.projDir = self.obj_appconfig.current_project["ProjectName"]
        try:
            self.obj_appconfig.print_info('PCB Layout is called for project : ' + self.projDir)
        except:
            pass       
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
            self.obj_appconfig.print_warning('Please select the project first. You can either create new project or open existing project')
            self.msg.setWindowTitle("Error Message")     
    
    '''
            
    def openKicadToNgspice(self):
        """
        This function create command to call kicad to Ngspice converter.
        """
        print("Function: Open Kicad to Ngspice Converter")
        
        self.projDir = self.obj_appconfig.current_project["ProjectName"]
        try:
            self.obj_appconfig.print_info('Kicad to Ngspice Conversion is called')
            self.obj_appconfig.print_info('Current Project is ' + self.projDir)
        except:
            pass
        #Validating if current project is available or not
        if self.obj_validation.validateKicad(self.projDir):
            #Cheking if project has .cir file or not
            if self.obj_validation.validateCir(self.projDir):
                self.projName = os.path.basename(self.projDir)
                self.project = os.path.join(self.projDir,self.projName)
                            
                #Creating a command to run
                """
                self.cmd = "python  ../kicadtoNgspice/KicadtoNgspice.py " +self.project+".cir "
                self.obj_workThread = Worker.WorkerThread(self.cmd)
                self.obj_workThread.start()
                """
                var=self.project+".cir"
                self.obj_dockarea.kicadToNgspiceEditor(var)
                
         
                
            else:
                self.msg = QtGui.QErrorMessage(None)
                self.msg.showMessage('The project does not contain any Kicad netlist file for conversion.')
                self.obj_appconfig.print_error('The project does not contain any Kicad netlist file for conversion.')
                self.msg.setWindowTitle("Error Message")  
           
        else:
            self.msg = QtGui.QErrorMessage(None)
            self.msg.showMessage('Please select the project first. You can either create new project or open existing project')
            self.obj_appconfig.print_warning('Please select the project first. You can either create new project or open existing project')
            self.msg.setWindowTitle("Error Message")  
           
    