from PyQt4 import QtGui,QtCore
from projManagement.Validation import Validation
from projManagement import Worker
from configuration.Appconfig import Appconfig
import os

class convertSub(QtGui.QWidget):
    """
    This class is called when User create new Project.
    """
    
    def __init__(self,dockarea):
        super(convertSub, self).__init__()
        self.obj_validation = Validation()
        self.obj_appconfig=Appconfig()
        self.obj_dockarea=dockarea
    
    def createSub(self):
        """
        This function create command to call kicad to Ngspice converter.
        """
        print "Open Kicad to Ngspice Conversion"
        self.projDir = self.obj_appconfig.current_subcircuit["SubcircuitName"]
        #Validating if current project is available or not
        if self.obj_validation.validateKicad(self.projDir):
            #print "Project is present"
            #Checking if project has .cir file or not
            if self.obj_validation.validateCir(self.projDir):
                #print "CIR file present"
                self.projName = os.path.basename(self.projDir)
                self.project = os.path.join(self.projDir,self.projName)
                
                #Creating a command to run
                #self.cmd = "python  ../kicadtoNgspice/KicadtoNgspice.py "+self.project+".cir "+"sub"
                #os.system(self.cmd)
                
                var1=self.project+".cir"
                var2="sub"
                self.obj_dockarea.kicadToNgspiceEditor(var1,var2)
#                 self.obj_workThread = Worker.WorkerThread(self.cmd)
#                 self.obj_workThread.start()
            else:
                self.msg = QtGui.QErrorMessage(None)
                self.msg.showMessage('The subcircuit does not contain any Kicad netlist file for conversion.')
                self.msg.setWindowTitle("Error Message")  
           
        else:
            self.msg = QtGui.QErrorMessage(None)
            self.msg.showMessage('Please select the subcircuit first. You can either create new subcircuit or open existing subcircuit')
            self.msg.setWindowTitle("Error Message") 