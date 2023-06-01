from PyQt5 import QtCore, QtGui, QtWidgets, uic
import os


class TerminalUi(QtWidgets.QMainWindow):
    def __init__(self, qProcess, args):
        super(TerminalUi, self).__init__()

#        Other variables
        self.darkColor = True
        self.qProcess = qProcess
        self.args = args
        self.iconDir = "../../images"

#       Load the ui file
        uic.loadUi("TerminalUi.ui", self)

#       Define Our Widgets
        self.progressBar = self.findChild(
            QtWidgets.QProgressBar,
            "progressBar"
            )
        self.simulationConsole = self.findChild(
            QtWidgets.QTextEdit,
            "simulationConsole"
            )

        self.lightDarkModeButton = self.findChild(
            QtWidgets.QPushButton,
            "lightDarkModeButton"
            )
        self.cancelSimulationButton = self.findChild(
            QtWidgets.QPushButton,
            "cancelSimulationButton"
            )
        self.redoSimulationButton = self.findChild(
            QtWidgets.QPushButton,
            "redoSimulationButton"
            )

#       Add functionalities to Widgets
        self.lightDarkModeButton.setIcon(
            QtGui.QIcon(
                os.path.join(
                    self.iconDir,
                    'light_mode.png'
                )
            )
        )
        self.lightDarkModeButton.clicked.connect(self.changeColor)
        self.cancelSimulationButton.clicked.connect(self.cancelSimulation)
        self.redoSimulationButton.clicked.connect(self.redoSimulation)

#       show app
        self.show()

    def writeSimulationStatusToConsole(self, isSuccess):
        """Writes simulation status to the console with appropriate style
        to the :class:`Form_Ui` console.

        :param isSuccess: A boolean flag used to indicate whether the
            simulation was a success or not
        :type isSuccess: bool
        """
        failedFormat = '<span style="color:#ff3333; font-size:18px;"> \
                        {} \
                        </span>'
        successFormat = '<span style="color:#00ff00; font-size:18px;"> \
                        {} \
                        </span>'

        if self.qProcess.exitStatus() == QtCore.QProcess.NormalExit:
            if isSuccess:
                self.simulationConsole.append(
                    successFormat.format("Simulation Completed Successfully!"))
            else:
                self.simulationConsole.append(
                    failedFormat.format("Simulation Failed!"))

    def cancelSimulation(self):
        """This function cancels the ongoing ngspice simulation.
        """
        if (self.qProcess.state() == QtCore.QProcess.NotRunning):
            return
        cancelFormat = '<span style="color:#3385ff; font-size:18px;">{}</span>'
        self.qProcess.kill()

#       To show progressBar completed
        self.progressBar.setMaximum(100)
        self.progressBar.setProperty("value", 100)

        self.simulationConsole.append(
            cancelFormat.format("Simulation Cancelled!"))
        self.simulationConsole.verticalScrollBar().setValue(
            self.simulationConsole.verticalScrollBar().maximum()
        )

    def redoSimulation(self):
        """This function reruns the ngspice simulation
        """
        if (self.qProcess.state() == QtCore.QProcess.Running):
            return

#        To make the progressbar running
        self.progressBar.setMaximum(0)
        self.progressBar.setProperty("value", -1)

        self.simulationConsole.setText("")
        self.qProcess.start('ngspice', self.args)

    def changeColor(self):
        """Toggles the :class:`Ui_Form` console between dark mode
                        and light mode
        """
        if self.darkColor is True:
            self.simulationConsole.setStyleSheet("QTextEdit {\n \
                background-color: white;\n \
                color: black;\n \
            }")
            self.lightDarkModeButton.setIcon(
                QtGui.QIcon(
                    os.path.join(
                        self.iconDir,
                        "dark_mode.png"
                        )
                    )
                )
            self.darkColor = False
        else:
            self.simulationConsole.setStyleSheet("QTextEdit {\n \
                background-color: rgb(36, 31, 49);\n \
                color: white;\n \
            }")
            self.lightDarkModeButton.setIcon(
                QtGui.QIcon(
                    os.path.join(
                        self.iconDir,
                        "light_mode.png"
                        )
                    )
                )
            self.darkColor = True
