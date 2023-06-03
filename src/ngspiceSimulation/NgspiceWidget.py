from PyQt5 import QtWidgets, QtCore
from configuration.Appconfig import Appconfig
from frontEnd import TerminalUi
import os


# This Class creates NgSpice Window
class NgspiceWidget(QtWidgets.QWidget):

    def __init__(self, command, startSimulation):
        """
        - Creates constructor for NgspiceWidget class.
        - Checks whether OS is Linux or Windows and
          creates Ngspice window accordingly.
        """
        QtWidgets.QWidget.__init__(self)
        self.obj_appconfig = Appconfig()
        self.process = QtCore.QProcess(self)
        self.projDir = self.obj_appconfig.current_project["ProjectName"]
        self.args = ['-b', '-r', command.replace(".cir.out", ".raw"), command]
        self.terminalUi = TerminalUi.TerminalUi(self.process, self.args)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.terminalUi)
        print("Argument to ngspice command : ", command)

#       This variable makes sure that finished.connect is called exactly once
        self.process.isFinishConnected = False

        self.process.\
            started.\
            connect(lambda:
                    startSimulation(process=self.process,
                                    function=self.finishSimulation))

        self.process.setWorkingDirectory(self.projDir)
        self.process.start('ngspice', self.args)
        self.process.readyReadStandardOutput.connect(
            lambda: self.readyReadAll())
        self.obj_appconfig.process_obj.append(self.process)
        print(self.obj_appconfig.proc_dict)
        (
            self.obj_appconfig.proc_dict
            [self.obj_appconfig.current_project['ProjectName']].append(
                self.process.pid())
        )

        if os.name != "nt":
            self.gawProcess = QtCore.QProcess(self)
            self.gawCommand = "gaw " + command.replace(".cir.out", ".raw")
            self.gawProcess.start('sh', ['-c', self.gawCommand])
            print(self.gawCommand)

    def finishSimulation(self, exitCode, exitStatus, checkChangeInPlotData):
        """This function is intended to run when the ngspice
        simulation finishes. It singals to the function that generates
        the plots and also writes in the appropriate status of the
        simulation (Whether it was a success or not).

        :param exitCode: The exit code signal of the qprocess
            that runs ngspice
        :type exitCode: int
        :param exitStatus: The exit status signal of the
            qprocess that runs ngspice
        :type exitStatus: class:`QtCore.QProcess.ExitStatus`
        :param checkChangeInPlotData: Takes the plotting function
            as input and uses it to generate the plots. The reason
            why this is passed in such a way is to minimize the no.
            of functions passed through a chain of objects.
        :type checkChangeInPlotData: function
        """

#       To stop progressbar from running after simulation is completed
        self.terminalUi.progressBar.setMaximum(100)
        self.terminalUi.progressBar.setProperty("value", 100)

        # st = os.stat(os.path.join(self.projDir, "plot_data_i.txt"))
        # if st.st_mtime >= self.currTime:
        if exitStatus == QtCore.QProcess.NormalExit:
            checkChangeInPlotData(exitCode)
#            self.terminalUi.writeSimulationStatusToConsole()

            failedFormat = '<span style="color:#ff3333; font-size:26px;"> \
                            {} \
                            </span>'
            successFormat = '<span style="color:#00ff00; font-size:26px;"> \
                            {} \
                            </span>'
            if exitCode == 0:
                self.terminalUi.simulationConsole.append(
                    successFormat.format("Simulation Completed Successfully!"))
            else:
                self.terminalUi.simulationConsole.append(
                    failedFormat.format("Simulation Failed!"))

            self.terminalUi.simulationConsole.verticalScrollBar().setValue(
                self.terminalUi.simulationConsole.verticalScrollBar().maximum()
            )
        else:
            self.msg = QtWidgets.QErrorMessage()
            self.msg.setModal(True)
            self.msg.setWindowTitle("Error Message")
            self.msg.showMessage(
                'Ngspice simulation did not complete successfully.'
            )
            self.msg.exec_()

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
#       For suppressing the PrinterOnly error that batch mode throws
        stderror = '\n'.join([line for line in stderror.split('\n')
                              if ('PrinterOnly' not in line and
                              'viewport for graphics' not in line)])
        self.terminalUi.simulationConsole.insertPlainText(
            stderror
        )
