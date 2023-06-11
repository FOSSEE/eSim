from PyQt5 import QtCore, QtGui, QtWidgets, uic
import os


class TerminalUi(QtWidgets.QMainWindow):
    """This is a class that represents the GUI required to provide
    details regarding the ngspice simulation. This GUI consists of
    a progress bar, a console window which displays the log of the
    simulation and button required for re-simulation and cancellation
    of the simulation"""
    def __init__(self, qProcess, args):
        """The constructor of the TerminalUi class
        param: qProcess: a PyQt QProcess that runs ngspice
        type: qProcess: :class:`QtCore.QProcess`
        param: args: arguments to be passed on to the ngspice call
        type: args: list
        """
        super(TerminalUi, self).__init__()

        # Other variables
        self.darkColor = True
        self.qProcess = qProcess
        self.args = args
        self.iconDir = "../../images"

        # Load the ui file
        uic.loadUi("TerminalUi.ui", self)

        # Define Our Widgets
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
        self.cancelSimulationButton.setEnabled(True)

        self.redoSimulationButton = self.findChild(
            QtWidgets.QPushButton,
            "redoSimulationButton"
        )
        self.redoSimulationButton.setEnabled(False)

        # Add functionalities to Widgets
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

        self.simulationCancelled = False
        self.show()

    def cancelSimulation(self):
        """This function cancels the ongoing ngspice simulation.
        """
        self.cancelSimulationButton.setEnabled(False)
        self.redoSimulationButton.setEnabled(True)

        if (self.qProcess.state() == QtCore.QProcess.NotRunning):
            return

        self.simulationCancelled = True
        self.qProcess.kill()

        # To show progressBar completed
        self.progressBar.setMaximum(100)
        self.progressBar.setProperty("value", 100)

        cancelFormat = '<span style="color:#FF8624; font-size:26px;">{}</span>'
        self.simulationConsole.append(
            cancelFormat.format("Simulation Cancelled!"))
        self.simulationConsole.verticalScrollBar().setValue(
            self.simulationConsole.verticalScrollBar().maximum()
        )

    def redoSimulation(self):
        """This function reruns the ngspice simulation
        """
        self.cancelSimulationButton.setEnabled(True)
        self.redoSimulationButton.setEnabled(False)

        if (self.qProcess.state() != QtCore.QProcess.NotRunning):
            return

        # To make the progressbar running
        self.progressBar.setMaximum(0)
        self.progressBar.setProperty("value", -1)

        self.simulationConsole.setText("")
        self.simulationCancelled = False

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
