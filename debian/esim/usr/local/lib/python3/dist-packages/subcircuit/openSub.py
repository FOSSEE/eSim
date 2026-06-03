import os
from PyQt6 import QtWidgets, QtCore
from configuration.Appconfig import Appconfig
from projManagement.Worker import WorkerThread


# This class is called when User clicks on Edit Subcircuit Button.
class openSub(QtWidgets.QWidget):
    """
    It opens the existing subcircuit projects that are present in
    Subcircuit directory.
    """

    def __init__(self):
        super(openSub, self).__init__()
        self.obj_appconfig = Appconfig()

    def body(self):

        init_path = '../../'
        if os.name == 'nt':
            init_path = ''

        self.editfile = QtCore.QDir.toNativeSeparators(
            QtWidgets.QFileDialog.getExistingDirectory(
                None, "Open File", init_path + "library/SubcircuitLibrary"
            )
        )

        if self.editfile:
            self.obj_Appconfig = Appconfig()
            self.obj_Appconfig.current_subcircuit['SubcircuitName'] \
                = self.editfile

            self.schname = os.path.basename(self.editfile)
            self.editfile = os.path.join(self.editfile, self.schname)
            self.cmd = "eeschema " + self.editfile + ".sch "
            self.obj_workThread = WorkerThread(self.cmd)
            self.obj_workThread.start()
