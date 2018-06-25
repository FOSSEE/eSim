from PyQt4 import QtGui,QtCore
from configuration.Appconfig import Appconfig
import platform
import os

class NgspiceWidget(QtGui.QWidget):
    """
    This Class creates NgSpice Window
    """
    def __init__(self,command,projPath):
        QtGui.QWidget.__init__(self)
        self.obj_appconfig = Appconfig()
        self.process = QtCore.QProcess(self)
        self.terminal = QtGui.QWidget(self)
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.addWidget(self.terminal)
        
        print "Argument to ngspice command : ",command        
        print "\nngspice simulation starts : \n"
        if platform.system() == 'Linux':
            self.command = "cd "+projPath+" && ngspice "+command
            os.system(self.command)
	    self.obj_appconfig.proc_dict[self.obj_appconfig.current_project['ProjectName']].append(self.process.pid())
                     
        elif platform.system() == 'Windows':
            tempdir= os.getcwd()
            projPath = self.obj_appconfig.current_project["ProjectName"]
            os.chdir(projPath)
            self.command = "ngspice "+command
            self.process.start(self.command)
            os.chdir(tempdir)
        print "\n simulation finished"    

