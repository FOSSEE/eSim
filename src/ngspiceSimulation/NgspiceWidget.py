from PyQt5 import QtWidgets, QtCore
from configuration.Appconfig import Appconfig
from configparser import ConfigParser
from progressBar import progressBar
import os


# This Class creates NgSpice Window
class NgspiceWidget(QtWidgets.QWidget):

    def __init__(self, command, projPath, timer):
        """
        - Creates constructor for NgspiceWidget class.
        - Checks whether OS is Linux or Windows and
          creates Ngspice window accordingly.
        """
        QtWidgets.QWidget.__init__(self)
        self.obj_appconfig = Appconfig()
        self.process = QtCore.QProcess(self)
        self.terminal = QtWidgets.QWidget(self)
        self.qTimer = timer
        self.progressBarUi = progressBar.Ui_Form(self.process, self.qTimer)
        self.progressBarUi.setupUi(self.terminal)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.terminal)
        self.errorFlag = False

        print("Argument to ngspice command : ", command)

        if os.name == 'nt':     # For Windows OS
            parser_nghdl = ConfigParser()
            parser_nghdl.read(
                os.path.join('library', 'config', '.nghdl', 'config.ini')
            )

            msys_home = parser_nghdl.get('COMPILER', 'MSYS_HOME')

            tempdir = os.getcwd()
            projPath = self.obj_appconfig.current_project["ProjectName"]
            os.chdir(projPath)
            self.command = 'cmd /c '+'"start /min ' + \
                msys_home + "/usr/bin/mintty.exe ngspice -p " + command + '"'
            self.process.start(self.command)
            os.chdir(tempdir)

        else:                   # For Linux OS
            # self.command = "cd " + projPath + \
            #     ";ngspice -r " + command.replace(".cir.out", ".raw") + \
            #     " " + command
            # Creating argument for process
            self.args = ['-b', '-r', command.replace(".cir.out", ".raw"), command]
            self.process.setWorkingDirectory(projPath)
            self.process.start('ngspice', self.args)
            self.process.readyReadStandardOutput.connect(lambda: self.readyReadAll())
            self.process.finished.connect(self.progressBarUi.showProgressCompleted)
            self.obj_appconfig.process_obj.append(self.process)
            print(self.obj_appconfig.proc_dict)
            (
                self.obj_appconfig.proc_dict
                [self.obj_appconfig.current_project['ProjectName']].append(
                    self.process.pid())
            )
            self.gawProcess = QtCore.QProcess(self)
            self.gawCommand = "gaw " + command.replace(".cir.out", ".raw")
            self.gawProcess.start('sh', ['-c', self.gawCommand])
            print(self.gawCommand)

    @QtCore.pyqtSlot()
    def readyReadAll(self):
        self.progressBarUi.writeIntoConsole(
            str(self.process.readAllStandardOutput().data(), encoding='utf-8')
        )
        stderror = self.process.readAllStandardError()
        if stderror.toUpper().contains(b"ERROR"):
            self.errorFlag = True
        self.progressBarUi.writeIntoConsole(str(stderror.data(), encoding='utf-8'))

    # def launchProgressBar(self):
    #     self.progressBar = QtWidgets.QWidget()
    #     self.progressBarUi = progressBar.Ui_Dialog()
    #     self.progressBarUi.setupUi(self.progressBar)
    #     self.progressBar.show()
