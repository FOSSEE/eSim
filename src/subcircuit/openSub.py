from PyQt4 import QtGui
from configuration.Appconfig import Appconfig
from projManagement.Worker import WorkerThread
import os


class openSub(QtGui.QWidget):
    """
    This class is called when User click on Open Project Button
    """
    def __init__(self):
        super(openSub, self).__init__()
        self.obj_appconfig = Appconfig()
              
    def body(self):
        self.editfile = str(QtGui.QFileDialog.getExistingDirectory(None,"Open File","../SubcircuitLibrary"))
        if self.editfile:
            self.obj_Appconfig = Appconfig()
            self.obj_Appconfig.current_subcircuit['SubcircuitName'] = self.editfile
            self.schname = os.path.basename(self.editfile)
            self.editfile = os.path.join(self.editfile,self.schname)
            self.cmd = "eeschema "+self.editfile+".sch "
            self.obj_workThread = WorkerThread(self.cmd)
            self.obj_workThread.start()