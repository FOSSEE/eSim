from PyQt5 import QtCore, QtWidgets
from ngspiceSimulation.pythonPlotting import plotWindow
from ngspiceSimulation.NgspiceWidget import NgspiceWidget
from configuration.Appconfig import Appconfig
from modelEditor.ModelEditor import ModelEditorclass
from subcircuit.Subcircuit import Subcircuit
from maker.makerchip import makerchip
from kicadtoNgspice.KicadtoNgspice import MainWindow
from browser.Welcome import Welcome
from browser.UserManual import UserManual
from ngspicetoModelica.ModelicaUI import OpenModelicaEditor
import os

dockList = ['Welcome']
count = 1
dock = {}


class DockArea(QtWidgets.QMainWindow):
    """
    This class contains function for designing UI of all the editors
    in dock area part:

        - Test Editor.
        - Model Editor.
        - Python Plotting.
        - Ngspice Editor.
        - Kicad to Ngspice Editor.
        - Subcircuit Editor.
        - Modelica editor.
    """

    def __init__(self):
        """This act as constructor for class DockArea."""
        QtWidgets.QMainWindow.__init__(self)
        self.obj_appconfig = Appconfig()

        for dockName in dockList:
            dock[dockName] = QtWidgets.QDockWidget(dockName)
            self.welcomeWidget = QtWidgets.QWidget()
            self.welcomeLayout = QtWidgets.QVBoxLayout()
            self.welcomeLayout.addWidget(Welcome())  # Call browser

            # Adding to main Layout
            self.welcomeWidget.setLayout(self.welcomeLayout)
            dock[dockName].setWidget(self.welcomeWidget)
            # CSS
            dock[dockName].setStyleSheet(" \
            QWidget { border-radius: 15px; border: 1px solid gray;\
                padding: 5px; width: 200px; height: 150px;  } \
            ")
            self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dock[dockName])

        # self.tabifyDockWidget(dock['Notes'],dock['Blank'])
        self.show()

    def createTestEditor(self):
        """This function create widget for Library Editor"""
        global count

        self.testWidget = QtWidgets.QWidget()
        self.testArea = QtWidgets.QTextEdit()
        self.testLayout = QtWidgets.QVBoxLayout()
        self.testLayout.addWidget(self.testArea)

        # Adding to main Layout
        self.testWidget.setLayout(self.testLayout)
        dock['Tips-' + str(count)] = \
            QtWidgets.QDockWidget('Tips-' + str(count))
        dock['Tips-' + str(count)].setWidget(self.testWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea,
                           dock['Tips-' + str(count)])
        self.tabifyDockWidget(
            dock['Welcome'], dock['Tips-' + str(count)])

        dock['Tips-' + str(count)].setVisible(True)
        dock['Tips-' + str(count)].setFocus()

        dock['Tips-' + str(count)].raise_()

        temp = self.obj_appconfig.current_project['ProjectName']
        if temp:
            self.obj_appconfig.dock_dict[temp].append(
                dock['Tips-' + str(count)]
            )
        count = count + 1

    def plottingEditor(self):
        """This function create widget for interactive PythonPlotting."""
        self.projDir = self.obj_appconfig.current_project["ProjectName"]
        self.projName = os.path.basename(self.projDir)
        # self.project = os.path.join(self.projDir, self.projName)

        global count
        self.plottingWidget = QtWidgets.QWidget()

        self.plottingLayout = QtWidgets.QVBoxLayout()
        self.plottingLayout.addWidget(plotWindow(self.projDir, self.projName))

        # Adding to main Layout
        self.plottingWidget.setLayout(self.plottingLayout)
        dock['Plotting-' + str(count)
             ] = QtWidgets.QDockWidget('Plotting-' + str(count))
        dock['Plotting-' + str(count)].setWidget(self.plottingWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea,
                           dock['Plotting-' + str(count)])
        self.tabifyDockWidget(dock['Welcome'], dock['Plotting-' + str(count)])

        dock['Plotting-' + str(count)].setVisible(True)
        dock['Plotting-' + str(count)].setFocus()
        dock['Plotting-' + str(count)].raise_()

        temp = self.obj_appconfig.current_project['ProjectName']
        if temp:
            self.obj_appconfig.dock_dict[temp].append(
                dock['Plotting-' + str(count)]
            )
        count = count + 1

    def ngspiceEditor(self, projDir, timer):
        """ This function creates widget for Ngspice window."""
        self.projDir = projDir
        self.qTimer = timer
        self.projName = os.path.basename(self.projDir)
        self.ngspiceNetlist = os.path.join(
            self.projDir, self.projName + ".cir.out")

        # Edited by Sumanto Kar 25/08/2021
        if os.path.isfile(self.ngspiceNetlist) is False:
            return False

        global count
        self.ngspiceWidget = QtWidgets.QWidget()

        self.ngspiceLayout = QtWidgets.QVBoxLayout()
        self.ngspiceLayout.addWidget(
            NgspiceWidget(self.ngspiceNetlist, self.projDir, self.qTimer)
        )

        # Adding to main Layout
        self.ngspiceWidget.setLayout(self.ngspiceLayout)
        dock['NgSpice-' + str(count)
             ] = QtWidgets.QDockWidget('NgSpice-' + str(count))
        dock['NgSpice-' + str(count)].setWidget(self.ngspiceWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea,
                           dock['NgSpice-' + str(count)])
        self.tabifyDockWidget(dock['Welcome'], dock['NgSpice-' + str(count)])

        # CSS
        dock['NgSpice-' + str(count)].setStyleSheet(" \
        .QWidget { border-radius: 15px; border: 1px solid gray; padding: 0px;\
            width: 200px; height: 150px;  } \
        ")

        dock['NgSpice-' + str(count)].setVisible(True)
        dock['NgSpice-' + str(count)].setFocus()
        dock['NgSpice-' + str(count)].raise_()

        temp = self.obj_appconfig.current_project['ProjectName']
        if temp:
            self.obj_appconfig.dock_dict[temp].append(
                dock['NgSpice-' + str(count)]
            )
        count = count + 1

    def modelEditor(self):
        """This function defines UI for model editor."""
        print("in model editor")
        global count
        self.modelwidget = QtWidgets.QWidget()

        self.modellayout = QtWidgets.QVBoxLayout()
        self.modellayout.addWidget(ModelEditorclass())

        # Adding to main Layout
        self.modelwidget.setLayout(self.modellayout)

        dock['Model Editor-' +
             str(count)] = QtWidgets.QDockWidget('Model Editor-' + str(count))
        dock['Model Editor-' + str(count)].setWidget(self.modelwidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea,
                           dock['Model Editor-' + str(count)])
        self.tabifyDockWidget(dock['Welcome'],
                              dock['Model Editor-' + str(count)])

        # CSS
        dock['Model Editor-' + str(count)].setStyleSheet(" \
            .QWidget { border-radius: 15px; border: 1px solid gray; \
                padding: 5px; width: 200px; height: 150px;  } \
            ")

        dock['Model Editor-' + str(count)].setVisible(True)
        dock['Model Editor-' + str(count)].setFocus()
        dock['Model Editor-' + str(count)].raise_()

        count = count + 1

    def kicadToNgspiceEditor(self, clarg1, clarg2=None):
        """
        This function is creating Editor UI for Kicad to Ngspice conversion.
        """
        global count
        self.kicadToNgspiceWidget = QtWidgets.QWidget()
        self.kicadToNgspiceLayout = QtWidgets.QVBoxLayout()
        self.kicadToNgspiceLayout.addWidget(MainWindow(clarg1, clarg2))

        self.kicadToNgspiceWidget.setLayout(self.kicadToNgspiceLayout)
        dock['kicadToNgspice-' + str(count)] = \
            QtWidgets.QDockWidget('kicadToNgspice-' + str(count))
        dock['kicadToNgspice-' +
             str(count)].setWidget(self.kicadToNgspiceWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea,
                           dock['kicadToNgspice-' + str(count)])
        self.tabifyDockWidget(dock['Welcome'],
                              dock['kicadToNgspice-' + str(count)])

        # CSS
        dock['kicadToNgspice-' + str(count)].setStyleSheet(" \
        .QWidget { border-radius: 15px; border: 1px solid gray;\
            padding: 5px; width: 200px; height: 150px;  } \
        ")

        dock['kicadToNgspice-' + str(count)].setVisible(True)
        dock['kicadToNgspice-' + str(count)].setFocus()
        dock['kicadToNgspice-' + str(count)].raise_()
        dock['kicadToNgspice-' + str(count)].activateWindow()

        temp = self.obj_appconfig.current_project['ProjectName']
        if temp:
            self.obj_appconfig.dock_dict[temp].append(
                dock['kicadToNgspice-' + str(count)]
            )
        count = count + 1

    def subcircuiteditor(self):
        """This function creates a widget for different subcircuit options."""
        global count
        self.subcktWidget = QtWidgets.QWidget()
        self.subcktLayout = QtWidgets.QVBoxLayout()
        self.subcktLayout.addWidget(Subcircuit(self))

        self.subcktWidget.setLayout(self.subcktLayout)
        dock['Subcircuit-' +
             str(count)] = QtWidgets.QDockWidget('Subcircuit-' + str(count))
        dock['Subcircuit-' + str(count)].setWidget(self.subcktWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea,
                           dock['Subcircuit-' + str(count)])
        self.tabifyDockWidget(dock['Welcome'],
                              dock['Subcircuit-' + str(count)])

        # CSS
        dock['Subcircuit-' + str(count)].setStyleSheet(" \
        .QWidget { border-radius: 15px; border: 1px solid gray;\
            padding: 5px; width: 200px; height: 150px;  } \
        ")

        dock['Subcircuit-' + str(count)].setVisible(True)
        dock['Subcircuit-' + str(count)].setFocus()
        dock['Subcircuit-' + str(count)].raise_()

        count = count + 1

    def makerchip(self):
        """This function creates a widget for different subcircuit options."""
        global count
        self.makerWidget = QtWidgets.QWidget()
        self.makerLayout = QtWidgets.QVBoxLayout()
        self.makerLayout.addWidget(makerchip(self))

        self.makerWidget.setLayout(self.makerLayout)
        dock['Makerchip-' +
             str(count)] = QtWidgets.QDockWidget('Makerchip-' + str(count))
        dock['Makerchip-' + str(count)].setWidget(self.makerWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea,
                           dock['Makerchip-' + str(count)])
        self.tabifyDockWidget(dock['Welcome'],
                              dock['Makerchip-' + str(count)])

        # CSS
        dock['Makerchip-' + str(count)].setStyleSheet(" \
        .QWidget { border-radius: 15px; border: 1px solid gray;\
            padding: 5px; width: 200px; height: 150px;  } \
        ")

        dock['Makerchip-' + str(count)].setVisible(True)
        dock['Makerchip-' + str(count)].setFocus()
        dock['Makerchip-' + str(count)].raise_()

        count = count + 1

    def usermanual(self):
        """This function creates a widget for user manual."""
        global count
        self.usermanualWidget = QtWidgets.QWidget()
        self.usermanualLayout = QtWidgets.QVBoxLayout()
        self.usermanualLayout.addWidget(UserManual())

        self.usermanualWidget.setLayout(self.usermanualLayout)
        dock['User Manual-' +
             str(count)] = QtWidgets.QDockWidget('User Manual-' + str(count))
        dock['User Manual-' + str(count)].setWidget(self.usermanualWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea,
                           dock['User Manual-' + str(count)])
        self.tabifyDockWidget(dock['Welcome'],
                              dock['User Manual-' + str(count)])

        # CSS
        dock['User Manual-' + str(count)].setStyleSheet(" \
        .QWidget { border-radius: 15px; border: 1px solid gray;\
            padding: 5px; width: 200px; height: 150px;  } \
        ")

        dock['User Manual-' + str(count)].setVisible(True)
        dock['User Manual-' + str(count)].setFocus()
        dock['User Manual-' + str(count)].raise_()

        count = count + 1

    def modelicaEditor(self, projDir):
        """This function sets up the UI for ngspice to modelica conversion."""
        global count
        self.modelicaWidget = QtWidgets.QWidget()
        self.modelicaLayout = QtWidgets.QVBoxLayout()
        self.modelicaLayout.addWidget(OpenModelicaEditor(projDir))

        self.modelicaWidget.setLayout(self.modelicaLayout)
        dock['Modelica-' + str(count)
             ] = QtWidgets.QDockWidget('Modelica-' + str(count))
        dock['Modelica-' + str(count)].setWidget(self.modelicaWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea,
                           dock['Modelica-' + str(count)])
        self.tabifyDockWidget(dock['Welcome'], dock['Modelica-' + str(count)])

        dock['Modelica-' + str(count)].setVisible(True)
        dock['Modelica-' + str(count)].setFocus()
        dock['Modelica-' + str(count)].raise_()

        # CSS
        dock['Modelica-' + str(count)].setStyleSheet(" \
        .QWidget { border-radius: 15px; border: 1px solid gray;\
            padding: 5px; width: 200px; height: 150px;  } \
        ")
        temp = self.obj_appconfig.current_project['ProjectName']
        if temp:
            self.obj_appconfig.dock_dict[temp].append(
                dock['Modelica-' + str(count)]
            )

        count = count + 1

    def closeDock(self):
        """
        This function checks for the project in **dock_dict**
        and closes it.
        """
        self.temp = self.obj_appconfig.current_project['ProjectName']
        for dockwidget in self.obj_appconfig.dock_dict[self.temp]:
            dockwidget.close()
