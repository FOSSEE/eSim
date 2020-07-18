from PyQt4 import QtGui, QtCore
from configuration.Appconfig import Appconfig
from configparser import SafeConfigParser
import platform
import os

# This Class creates NgSpice Window


class NgspiceWidget(QtGui.QWidget):

    def __init__(self, command, projPath):
        """
        - Creates constructor for NgspiceWidget class.
        - Checks whether OS is linux or windows
        and creates NgSpice window accordingly.
        """
        QtGui.QWidget.__init__(self)
        self.obj_appconfig = Appconfig()
        self.process = QtCore.QProcess(self)
        self.terminal = QtGui.QWidget(self)
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.addWidget(self.terminal)

        if os.name == 'nt':
            home = os.path.expanduser("~")

            parser_nghdl = SafeConfigParser()
            parser_nghdl.read(os.path.join(
                home, os.path.join('.nghdl', 'config.ini')))
            try:
                msys_bin = parser_nghdl.get('COMPILER', 'MSYS_HOME')
            except BaseException:
                pass

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
            self.command = 'cmd /c '+'"start /min ' + \
                msys_bin + "/mintty.exe ngspice " + command + '"'
            self.process.start(self.command)
            os.chdir(tempdir)
