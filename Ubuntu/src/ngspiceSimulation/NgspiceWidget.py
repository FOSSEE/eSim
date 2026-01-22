import os
import sys
from PyQt5 import QtWidgets, QtCore
from configuration.Appconfig import Appconfig
from frontEnd import TerminalUi
from configparser import ConfigParser


def installed_path(relative_path):
    return os.path.join(os.path.dirname(sys.executable), relative_path)


class NgspiceWidget(QtWidgets.QWidget):
    def __init__(self, netlist, simEndSignal, plotFlag):
        super().__init__()
        self.obj_appconfig = Appconfig()
        self.projDir = os.path.abspath(self.obj_appconfig.current_project["ProjectName"])
        self.netlist = os.path.abspath(netlist)
        self.raw_file = self.netlist.replace(".cir.out", ".raw")
        self.args = ['-b', '-r', self.raw_file, self.netlist]

        self.process = QtCore.QProcess(self)
        self.terminalUi = TerminalUi.TerminalUi(self.process, self.args)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.terminalUi)

        self.plotFlag = plotFlag
        self.process.setWorkingDirectory(self.projDir)
        self.process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self.process.readyRead.connect(self.readyReadAll)
        self.process.finished.connect(
            lambda exitCode, exitStatus:
            self.finishSimulation(exitCode, exitStatus, simEndSignal, False)
        )
        self.process.errorOccurred.connect(
            lambda: self.finishSimulation(None, None, simEndSignal, True))
        self.process.start('ngspice', self.args)

        self.obj_appconfig.process_obj.append(self.process)
        self.obj_appconfig.proc_dict[self.obj_appconfig.current_project['ProjectName']].append(self.process.pid())

    @QtCore.pyqtSlot()
    def readyReadAll(self):
        self.terminalUi.simulationConsole.insertPlainText(
            str(self.process.readAllStandardOutput().data(), encoding='utf-8')
        )
        stderror = str(self.process.readAllStandardError().data(), encoding='utf-8')
        stderror = '\n'.join([errLine for errLine in stderror.split('\n')
                              if ('PrinterOnly' not in errLine and 'viewport for graphics' not in errLine)])
        self.terminalUi.simulationConsole.insertPlainText(stderror)

    def finishSimulation(self, exitCode, exitStatus, simEndSignal, hasErrorOccurred):
        if not hasErrorOccurred and self.terminalUi.simulationCancelled:
            return

        self.terminalUi.progressBar.setMaximum(100)
        self.terminalUi.progressBar.setProperty("value", 100)
        self.terminalUi.cancelSimulationButton.setEnabled(False)
        self.terminalUi.redoSimulationButton.setEnabled(True)

        if exitCode is None:
            exitCode = self.process.exitCode()
        errorType = self.process.error()
        if errorType < 3:
            exitStatus = QtCore.QProcess.CrashExit
        elif exitStatus is None:
            exitStatus = self.process.exitStatus()

        if self.terminalUi.simulationCancelled:
            msg = QtWidgets.QMessageBox()
            msg.setModal(True)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Warning Message")
            msg.setText("Simulation was cancelled.")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec()
        elif exitStatus == QtCore.QProcess.NormalExit and exitCode == 0 and errorType == QtCore.QProcess.UnknownError:
            self.terminalUi.simulationConsole.append(
                '<span style="color:#00ff00; font-size:26px;">Simulation Completed Successfully!</span>')
        else:
            self.terminalUi.simulationConsole.append(
                '<span style="color:#ff3333; font-size:26px;">Simulation Failed!</span>')
            errMsg = 'Simulation '
            if errorType == QtCore.QProcess.FailedToStart:
                errMsg += 'failed to start. Ensure that eSim is installed correctly.'
            elif errorType == QtCore.QProcess.Crashed:
                errMsg += 'crashed. Try again later.'
            elif errorType == QtCore.QProcess.Timedout:
                errMsg += 'timed out. Try to reduce simulation time or step interval.'
            else:
                errMsg += 'could not complete. Try again later.'

            msg = QtWidgets.QErrorMessage()
            msg.setModal(True)
            msg.setWindowTitle("Error Message")
            msg.showMessage(errMsg)
            msg.exec()

        self.terminalUi.simulationConsole.verticalScrollBar().setValue(
            self.terminalUi.simulationConsole.verticalScrollBar().maximum())

        newPlotFlag = self.process.property("plotFlag")
        if newPlotFlag is not None:
            self.plotFlag = newPlotFlag
        newPlotFlag2 = self.process.property("plotFlag2")
        if newPlotFlag2 is not None:
            self.plotFlag = newPlotFlag2

        if self.plotFlag:
            self.plotFlagFunc(self.projDir, self.netlist)

        simEndSignal.emit(exitStatus, exitCode)

    def plotFlagFunc(self, projPath, command):
        if self.plotFlag == True:
            if os.name == 'nt':
                parser_nghdl = ConfigParser()
                config_path = os.path.join('library', 'config', '.nghdl', 'config.ini')
                parser_nghdl.read(config_path)
                msys_home = parser_nghdl.get('COMPILER', 'MSYS_HOME')
                tempdir = os.getcwd()
                projPath = self.obj_appconfig.current_project["ProjectName"]
                os.chdir(projPath)
                
                self.command = (
                'cmd /c "start /min ' +
                msys_home + '/usr/bin/mintty.exe ngspice -p ' + command + '"'
                )

                # Create a new QProcess for mintty
                self.minttyProcess = QtCore.QProcess(self)
                self.minttyProcess.start(self.command)

                os.chdir(tempdir)
            else:
                # For Linux: use .raw file in xterm and gaw
                raw_file = os.path.abspath(command.replace(".cir.out", ".raw"))
                commandi = f'cd "{projPath}"; ngspice -p "{raw_file}"'

                xtermArgs = ['-hold', '-e', commandi]
                self.xtermProcess = QtCore.QProcess(self)
                self.xtermProcess.start('xterm', xtermArgs)

                self.obj_appconfig.process_obj.append(self.xtermProcess)
                self.obj_appconfig.proc_dict[self.obj_appconfig.current_project['ProjectName']].append(
                    self.xtermProcess.pid()
                )