from PyQt4 import QtGui,QtCore
from configuration.Appconfig import Appconfig
import os
import platform

class ImportPspiceLibrary(QtGui.QWidget):
    """
    This is used to import the Pspice Library and convert it inot Kicad library
    """
    def __init__(self):
        super(ImportPspiceLibrary, self).__init__()
        self.obj_Appconfig = Appconfig()
        
    def imortLib(self):
        self.home = os.path.expanduser("~")
        self.libLocation = QtGui.QFileDialog.getOpenFileName(self,"open",self.home)
        self.obj_Appconfig.print_info('File selected : '+self.libLocation)
        
        #Create command to run
        self.cmd = "../pspicetoKicad/libConverter "+self.libLocation
        os.system(str(self.cmd))
        
    
    
class ConvertPspiceKicad(QtGui.QWidget):
    """
    This is used to convert Pspice schematic into Kicad schematic
    """
    def __init__(self):
        super(ConvertPspiceKicad, self).__init__()
        self.obj_Appconfig = Appconfig()
    
    def runConverter(self):
        self.obj_Appconfig.print_info('Running PSPICE to Kicad converter')
        self.home = os.path.expanduser("~")
        self.pspiceSchFileLoc = QtGui.QFileDialog.getOpenFileName(self,"open",self.home)
        self.pspiceSchFileName = os.path.basename(str(self.pspiceSchFileLoc))
        self.worspace_loc = self.obj_Appconfig.default_workspace['workspace']
        self.outputDir = os.path.join(self.worspace_loc,self.pspiceSchFileName)
        
        #Create command to be run
        if platform.system() == 'Linux':
            #Check for 32 or 64 bit
            if platform.architecture()[0] == '64bit':
                self.cmd = "../pspicetoKicad/schConverter64 "+self.pspiceSchFileLoc+" "+self.outputDir
            else:
                self.cmd = "../pspicetoKicad/schConverter32 "+self.pspiceSchFileLoc+" "+self.outputDir
                          
        elif platform.system() == 'Windows':
            print "Needs to include for Windows"
               
        #Running command
        self.status =  os.system(str(self.cmd))
        
               
        if self.status == 0:
            self.msg = QtGui.QMessageBox()
            self.msgContent = "Successfully converted PSPICE schematic to Kicad Schematic.<br/>\
            Project is available in eSim workspace at <b>"+self.outputDir+"</b>.<br\>\
            You can open the project from eSim workspace"
            self.msg.setTextFormat(QtCore.Qt.RichText)
            self.msg.setText(self.msgContent)
            self.msg.setWindowTitle("Message")
            self.obj_Appconfig.print_info(self.msgContent)
            self.msg.exec_()
            
        else:
            self.msg = QtGui.QErrorMessage(None)
            self.msg.showMessage('Error while converting PSPICE schematic to Kicad Schematic')
            self.obj_Appconfig.print_error('Error while converting PSPICE schematic to Kicad Schematic')
            self.msg.setWindowTitle("Error Message")
            
        
        
        
        
        