import os
from PyQt5 import QtWidgets, QtCore
from configuration.Appconfig import Appconfig
from frontEnd import TerminalUi


# This Class creates NgSpice Window
class NgspiceWidget(QtWidgets.QWidget):

    def __init__(self, netlist, simEndSignal, plotFlag):
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
        self.projPath = self.projDir

        self.process = QtCore.QProcess(self)
        self.terminalUi = TerminalUi.TerminalUi(self.process, self.args)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.terminalUi)

        # --- Ensure the correct theme is applied immediately ---
        app_parent = self.parent()
        is_dark_theme = False
        while app_parent is not None:
            if hasattr(app_parent, 'is_dark_theme'):
                is_dark_theme = app_parent.is_dark_theme
                break
            app_parent = app_parent.parent() if hasattr(app_parent, 'parent') else None
        if hasattr(self, 'terminalUi') and hasattr(self.terminalUi, 'set_theme'):
            self.terminalUi.set_theme(is_dark_theme)

        # Receiving the plotFlag
        self.plotFlag = plotFlag
        print("Value of plotFlag: ", self.plotFlag)
        self.command = netlist

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

        """ Get the plotFlag from process if it exists, otherwise use current plotFlag, plotFlag2 is for pop which appears when resimulate is clicked on ngSpice window """
        newPlotFlag = self.process.property("plotFlag")
        if newPlotFlag is not None:
            self.plotFlag = newPlotFlag
        
        newPlotFlag2 = self.process.property("plotFlag2")
        if newPlotFlag2 is not None:
            self.plotFlag = newPlotFlag2

        if self.plotFlag:
            self.plotFlagFunc(self.projPath, self.command)

        simEndSignal.emit(exitStatus, exitCode)

    def plotFlagFunc(self,projPath,command):
        if self.plotFlag == True:
            print("reached here too")
            if os.name == 'nt':
                parser_nghdl = ConfigParser()
                parser_nghdl.read(
                    os.path.join('library', 'config', '.nghdl', 'config.ini')
                )

                msys_home = parser_nghdl.get('COMPILER', 'MSYS_HOME')

                tempdir = os.getcwd()
                projPath = self.obj_appconfig.current_project["ProjectName"]
                os.chdir(projPath)
                self.command = 'cmd /c ' + '"start /min ' + \
                               msys_home + "/usr/bin/mintty.exe ngspice -p " + command + '"'

                self.process.start(self.command)
                os.chdir(tempdir)
            else:
                print("reached .. 4")
                self.commandi = "cd " + projPath + \
                                ";ngspice -r " + command.replace(".cir.out", ".raw") + \
                                " " + command
                self.xtermArgs = ['-hold', '-e', self.commandi]
                print("xTerm")

                self.xtermProcess = QtCore.QProcess(self)
                self.xtermProcess.start('xterm', self.xtermArgs)

                self.obj_appconfig.process_obj.append(self.xtermProcess)
                print(self.obj_appconfig.proc_dict)
                (
                    self.obj_appconfig.proc_dict
                    [self.obj_appconfig.current_project['ProjectName']].append(
                        self.xtermProcess.pid())
                )

                self.gawProcess.start('sh', ['-c', self.gawCommand])
                print("last:", self.gawCommand)
