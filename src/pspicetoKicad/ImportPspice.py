from PyQt4 import QtGui,QtCore
from configuration.Appconfig import Appconfig
import os
import platform
import shutil
import glob

class ImportPspiceLibrary(QtGui.QWidget):
    """
    This is used to import the Pspice Library and convert it inot Kicad library
    """
    def __init__(self):
        super(ImportPspiceLibrary, self).__init__()
        self.obj_Appconfig = Appconfig()
        
    def imortLib(self):
        self.home = os.path.expanduser("~")
        self.worspace_loc = self.obj_Appconfig.default_workspace['workspace']
        self.destinationLoc = os.path.join(self.worspace_loc,"ConvertedLib")
        self.libLocation = QtGui.QFileDialog.getOpenFileNames(self,"open",self.home,"*.slb")
        self.tempList = [] #Hold library file in the form of string
        
        if self.libLocation:
            for item in self.libLocation:
                self.tempList.append(str(item))
            
            self.obj_Appconfig.print_info('File selected : '+str(self.tempList))
            self.arg = ' '.join(self.tempList)
            #Create command to run
            if platform.system() == 'Linux':
                #Check for 32 or 64 bit
                if platform.architecture()[0] == '64bit':
                    self.cmd = "../pspicetoKicad/libConverter64 "+self.arg
                else:
                    self.cmd = "../pspicetoKicad/libConverter32 "+self.arg
            elif platform.system() == 'Windows':
                print "Needs to include for Windows"
                
            self.status =  os.system(str(self.cmd))
            
            if self.status == 0:
                self.libLocation = os.path.join(self.worspace_loc,"ConvertedLib")
            
                #Check if library is present
                if os.path.isdir(self.libLocation):
                    pass
                else:
                    os.mkdir(self.libLocation)
                try:
                    #Moving files to necessary location
                    for libfile in glob.glob('*.lib'):
                        self.obj_Appconfig.print_info('Copying file '+libfile+' to ' +self.libLocation)
                        shutil.copy(libfile, self.libLocation)
                        self.obj_Appconfig.print_info('Removing file '+libfile)
                        os.remove(libfile)
                        
                    self.msg = QtGui.QMessageBox()
                    self.msgContent = "Successfully imported and converted PSPICE library to Kicad library.<br/>"
                    self.msg.setTextFormat(QtCore.Qt.RichText)
                    self.msg.setText(self.msgContent)
                    self.msg.setWindowTitle("Message")
                    self.obj_Appconfig.print_info(self.msgContent)
                    self.msg.exec_()
                except Exception as e:
                    self.msg = QtGui.QErrorMessage(None)
                    self.msg.showMessage('Error while moving libaray to '+self.libLocation+ " "+str(e))
                    self.obj_Appconfig.print_error('Error while moving libaray to '+self.libLocation+ " "+str(e))
                    self.msg.setWindowTitle('Error Message')
            else:
                self.msg = QtGui.QErrorMessage(None)
                self.msg.showMessage('Error while converting PSPICE library to Kicad library')
                self.obj_Appconfig.print_error('Error while converting PSPICE library to Kicad library')
                self.msg.setWindowTitle("Error Message")
     
        else:
            self.obj_Appconfig.print_info('No files selected. Process Aborted')
        
           
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
        self.worspace_loc = self.obj_Appconfig.default_workspace['workspace']
        
        self.pspiceSchFileLoc = QtGui.QFileDialog.getOpenFileName(self,"open",self.home)
        
        if self.pspiceSchFileLoc:
            self.pspiceSchFileName = os.path.basename(str(self.pspiceSchFileLoc))
            self.pspiceProjName = os.path.splitext(self.pspiceSchFileName)[0]
            self.outputDir = os.path.join(self.worspace_loc,self.pspiceProjName)       
            
            #Check if project is already exists
            if  os.path.isdir(self.outputDir):
                self.obj_Appconfig.print_info("Output Directory already present")
                self.obj_Appconfig.print_info("Output Project "+self.outputDir+" is already present")
                reply = QtGui.QMessageBox.question(self, 'Message',"eSim project with same name is already exist. Do you want to delete it ?", \
                                                   QtGui.QMessageBox.Yes |QtGui.QMessageBox.No, QtGui.QMessageBox.No)
                if reply == QtGui.QMessageBox.Yes:
                    print "Deleting Project and creating new"
                    self.obj_Appconfig.print_info("Deleting Project and creating new")
                    shutil.rmtree(self.outputDir, ignore_errors=False, onerror=self.errorRemove)
                    os.mkdir(self.outputDir)
                    #Calling Function
                    self.createProjectFile(self.pspiceSchFileLoc,self.outputDir)
                else:
                    self.msg = QtGui.QMessageBox()
                    self.msgContent = "PSPICE to Kicad schematic conversion aborted.<br/>\
                    You can change the Pspice schematic file name and upload it again.<br/>"
                    self.msg.setTextFormat(QtCore.Qt.RichText)
                    self.msg.setText(self.msgContent)
                    self.msg.setWindowTitle("Message")
                    self.obj_Appconfig.print_info(self.msgContent)
                    self.msg.exec_()
            else:
                os.mkdir(self.outputDir)
                #Calling Function
                self.createProjectFile(self.pspiceSchFileLoc,self.outputDir)
        else:
            self.obj_Appconfig.print_info('No file selected. Process Aborted')
            
    def createProjectFile(self,pspiceSchFileLoc,outputDir):
        print "Create Project File is called"
        print "Schematic File Location---------->",pspiceSchFileLoc
        print "Output Directory-------------->",outputDir
        #Create command to be run
        if platform.system() == 'Linux':
            #Check for 32 or 64 bit
            if platform.architecture()[0] == '64bit':
                self.cmd = "../pspicetoKicad/schConverter64 "+pspiceSchFileLoc+" "+outputDir
            else:
                self.cmd = "../pspicetoKicad/schConverter32 "+pspiceSchFileLoc+" "+outputDir
        elif platform.system() == 'Windows':
            print "Needs to include for Windows"
               
        #Running command
        self.status = os.system(str(self.cmd))
                    
        if self.status == 0:
            self.msg = QtGui.QMessageBox()
            self.msgContent = "Successfully converted PSPICE schematic to Kicad Schematic.<br/>\
            Project is available in eSim workspace at <b>"+outputDir+"</b>.<br/>\
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
            
    def errorRemove(self,func, path, exc):
        self.msg = QtGui.QErrorMessage(None)
        self.msg.showMessage('Error while removing existing project. <br/> Please check whether directory is Read only.')
        self.obj_Appconfig.print_error('Error while removing existing project')
        self.msg.setWindowTitle("Error Message")