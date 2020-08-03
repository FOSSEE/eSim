from PyQt5 import QtWidgets, QtCore
from configuration.Appconfig import Appconfig
from configparser import SafeConfigParser
import os


# This Class creates NgSpice Window
class NgspiceWidget(QtWidgets.QWidget):

    def __init__(self, command, projPath):
        """
        - Creates constructor for NgspiceWidget class.
        - Checks whether OS is Linux or Windows and
          creates Ngspice window accordingly.
        """
        QtWidgets.QWidget.__init__(self)
        self.obj_appconfig = Appconfig()
        self.process = QtCore.QProcess(self)
        self.terminal = QtWidgets.QWidget(self)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.terminal)

        print("Argument to ngspice command : ", command)

        if os.name == 'nt':     # For Windows OS
            home = os.path.expanduser("~")

            parser_nghdl = SafeConfigParser()
            parser_nghdl.read(os.path.join(
                home, os.path.join('.nghdl', 'config.ini')))

            msys_bin = parser_nghdl.get('COMPILER', 'MSYS_HOME')

            tempdir = os.getcwd()
            projPath = self.obj_appconfig.current_project["ProjectName"]
            os.chdir(projPath)
            self.command = 'cmd /c '+'"start /min ' + \
                msys_bin + "/mintty.exe ngspice " + command + '"'
            self.process.start(self.command)
            os.chdir(tempdir)

        else:                   # For Linux OS
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
