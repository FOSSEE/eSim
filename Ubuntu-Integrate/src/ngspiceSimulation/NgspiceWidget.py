import os
from PyQt5 import QtWidgets, QtCore
from configuration.Appconfig import Appconfig
from frontEnd import TerminalUi


# This Class creates NgSpice Window
class NgspiceWidget(QtWidgets.QWidget):

    def __init__(self, netlist, simEndSignal):
        """
        - Creates constructor for NgspiceWidget class.
        - Creates NgspiceWindow and runs the process
        - Calls the logs the ngspice process, returns
          it's simulation status and calls the plotter
        - Checks whether it is Linux and runs gaw
        :param netlist: The file .cir.out file that
            contains the instructions.
        :type netlist: str
        :param simEndSignal: A signal that will be emitted to Application class
            for enabling simulation interaction and plotting data if the
            simulation is successful
        :type simEndSignal: PyQt Signal
        """
        QtWidgets.QWidget.__init__(self)
        self.obj_appconfig = Appconfig()
        self.projDir = self.obj_appconfig.current_project["ProjectName"]
        self.args = ['-b', '-r', netlist.replace(".cir.out", ".raw"), netlist]
        print("Argument to ngspice: ", self.args)

        self.process = QtCore.QProcess(self)
        self.terminalUi = TerminalUi.TerminalUi(self.process, self.args)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.terminalUi)

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
        print(self.obj_appconfig.proc_dict)
        (
            self.obj_appconfig.proc_dict
            [self.obj_appconfig.current_project['ProjectName']].append(
                self.process.pid())
        )

        if os.name != "nt":     # Linux OS
            self.gawProcess = QtCore.QProcess(self)
            self.gawCommand = "gaw " + netlist.replace(".cir.out", ".raw")
            self.gawProcess.start('sh', ['-c', self.gawCommand])
            print(self.gawCommand)

    @QtCore.pyqtSlot()
    def readyReadAll(self):
        """Outputs the ngspice process standard output and standard error
        to :class:`TerminalUi.TerminalUi` console
        """
        self.terminalUi.simulationConsole.insertPlainText(
            str(self.process.readAllStandardOutput().data(), encoding='utf-8')
        )

        stderror = str(self.process.readAllStandardError().data(),
                       encoding='utf-8')

        # Suppressing the Ngspice PrinterOnly error that batch mode throws
        stderror = '\n'.join([errLine for errLine in stderror.split('\n')
                              if ('PrinterOnly' not in errLine and
                              'viewport for graphics' not in errLine)])

        self.terminalUi.simulationConsole.insertPlainText(stderror)

    def finishSimulation(self, exitCode, exitStatus,
                         simEndSignal, hasErrorOccurred):
        """This function is intended to run when the Ngspice
        simulation finishes. It singals to the function that generates
        the plots and also writes in the appropriate status of the
        simulation (Whether it was a success or not).

        :param exitCode: The exit code signal of the QProcess
            that runs ngspice
        :type exitCode: int
        :param exitStatus: The exit status signal of the
            qprocess that runs ngspice
        :type exitStatus: class:`QtCore.QProcess.ExitStatus`
        :param simEndSignal: A signal passed from constructor
            for enabling simulation interaction and plotting data if the
            simulation is successful
        :type simEndSignal: PyQt Signal
        """

        # Canceling simulation triggers both finished and
        # errorOccurred signals...need to skip finished signal in this case.
        if not hasErrorOccurred and self.terminalUi.simulationCancelled:
            return

        # Stop progressbar from running after simulation is completed
        self.terminalUi.progressBar.setMaximum(100)
        self.terminalUi.progressBar.setProperty("value", 100)
        self.terminalUi.cancelSimulationButton.setEnabled(False)
        self.terminalUi.redoSimulationButton.setEnabled(True)

        if exitCode is None:
            exitCode = self.process.exitCode()

        errorType = self.process.error()
        if errorType < 3:   # 0, 1, 2 ==> failed to start, crashed, timedout
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

        elif exitStatus == QtCore.QProcess.NormalExit and exitCode == 0 \
                and errorType == QtCore.QProcess.UnknownError:
            # Redo-simulation does not set correct exit status and code.
            # So, need to check the error type ==>
            #   UnknownError along with NormalExit seems successful simulation

            successFormat = '<span style="color:#00ff00; font-size:26px;">\
                        {} \
                        </span>'
            self.terminalUi.simulationConsole.append(
                successFormat.format("Simulation Completed Successfully!"))

        else:
            failedFormat = '<span style="color:#ff3333; font-size:26px;"> \
                        {} \
                        </span>'
            self.terminalUi.simulationConsole.append(
                failedFormat.format("Simulation Failed!"))

            errMsg = 'Simulation '
            if errorType == QtCore.QProcess.FailedToStart:
                errMsg += 'failed to start. ' + \
                          'Ensure that eSim is installed correctly.'
            elif errorType == QtCore.QProcess.Crashed:
                errMsg += 'crashed. Try again later.'
            elif errorType == QtCore.QProcess.Timedout:
                errMsg += ' has timed out. Try to reduce the ' + \
                          ' simulation time or the simulation step interval.'
            else:
                errMsg += ' could not complete. Try again later.'

            msg = QtWidgets.QErrorMessage()
            msg.setModal(True)
            msg.setWindowTitle("Error Message")
            msg.showMessage(errMsg)
            msg.exec()

        self.terminalUi.simulationConsole.verticalScrollBar().setValue(
            self.terminalUi.simulationConsole.verticalScrollBar().maximum()
        )

        simEndSignal.emit(exitStatus, exitCode)
