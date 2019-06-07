from PyQt4 import QtGui, QtCore
from configuration.Appconfig import Appconfig
import platform
import os


# This Class creates NgSpice Window
class NgspiceWidget(QtGui.QWidget):
    """
    Includes functions that checks whether OS is linux or windows
    and creates NgSpice window accordingly.
    """

    def __init__(self, command, projPath):
        QtGui.QWidget.__init__(self)
        self.obj_appconfig = Appconfig()
        self.process = QtCore.QProcess(self)
        self.terminal = QtGui.QWidget(self)
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.addWidget(self.terminal)

        print("Argument to ngspice command : ", command)
        # For Linux OS
        if platform.system() == 'Linux':
            self.command = "cd " + projPath + ";ngspice " + command
            # Creating argument for process
            self.args = ['-hold', '-e', self.command]
            self.process.start('xterm', self.args)
            self.obj_appconfig.process_obj.append(self.process)
            print(self.obj_appconfig.proc_dict)
            (
                self.obj_appconfig.proc_dict
                [self.obj_appconfig.current_project['ProjectName']].append(
                    self.process.pid())
            )

        # For Windows OS
        elif platform.system() == 'Windows':
            tempdir = os.getcwd()
            projPath = self.obj_appconfig.current_project["ProjectName"]
            os.chdir(projPath)
            self.command = "ngspice " + command
            self.process.start(self.command)
            os.chdir(tempdir)
