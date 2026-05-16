# =========================================================================
#      FILE: Application.py
#
#     USAGE: ---
#
#   DESCRIPTION: This main file use to start the Application
#
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Fahim Khan, fahim.elex@gmail.com
#    MAINTAINED: Rahul Paknikar, rahulp@iitb.ac.in
#                Sumanto Kar, sumantokar@iitb.ac.in
#                Pranav P, pranavsdreams@gmail.com
#  ORGANIZATION: eSim Team at FOSSEE, IIT Bombay
#       CREATED: Tuesday 24 February 2015
#      REVISION: Wednesday 07 June 2023
# =========================================================================

import os
import sys
import traceback
import webbrowser

if os.name == 'nt':
    from frontEnd import pathmagic  # noqa:F401
    init_path = ''
else:
    import pathmagic    # noqa:F401
    init_path = '../../'

from PyQt6 import QtGui, QtCore, QtWidgets
from PyQt6.QtCore import QSize
from configuration.Appconfig import Appconfig
from frontEnd import ProjectExplorer
from frontEnd import Workspace
from frontEnd import DockArea
from projManagement.openProject import OpenProjectInfo
from projManagement.newProject import NewProjectInfo
from projManagement.Kicad import Kicad
from projManagement.Validation import Validation
from projManagement import Worker

# Its our main window of application.


class Application(QtWidgets.QMainWindow):
    """This class initializes all objects used in this file."""
    global project_name
    simulationEndSignal = QtCore.pyqtSignal(QtCore.QProcess.ExitStatus, int)

    def __init__(self, *args):
        """Initialize main Application window."""

        # Calling __init__ of super class
        QtWidgets.QMainWindow.__init__(self, *args)

        # Set slot for simulation end signal to plot simulation data
        self.simulationEndSignal.connect(self.plotSimulationData)

        #the plotFlag
        self.plotFlag = False

        # Creating require Object
        self.obj_workspace = Workspace.Workspace()
        self.obj_Mainview = MainView()
        self.obj_kicad = Kicad(self.obj_Mainview.obj_dockarea)
        self.obj_appconfig = Appconfig()
        self.obj_validation = Validation()
        # Initialize all widget
        self.setCentralWidget(self.obj_Mainview)
        self.initToolBar()

        self.setGeometry(self.obj_appconfig._app_xpos,
                         self.obj_appconfig._app_ypos,
                         self.obj_appconfig._app_width,
                         self.obj_appconfig._app_heigth)
        self.setWindowTitle(
            self.obj_appconfig._APPLICATION + "-" + self.obj_appconfig._VERSION
        )
        self.showMaximized()
        self.setWindowIcon(QtGui.QIcon(init_path + 'images/logo.png'))

        self.systemTrayIcon = QtWidgets.QSystemTrayIcon(self)
        self.systemTrayIcon.setIcon(QtGui.QIcon(init_path + 'images/logo.png'))
        self.systemTrayIcon.setVisible(True)

    def initToolBar(self):
        """
        This function initializes Tool Bars.
        It setups the icons, short-cuts and defining functonality for:

            - Top-tool-bar (New project, Open project, Close project, \
                Mode switch, Help option)
            - Left-tool-bar (Open Schematic, Convert KiCad to Ngspice, \
                Simuation, Model Editor, Subcircuit, NGHDL, Modelica \
                Converter, OM Optimisation)
        """
        # Top Tool bar
        self.newproj = QtGui.QAction(
            QtGui.QIcon(init_path + 'images/newProject.png'),
            '<b>New Project</b>', self
        )
        self.newproj.setShortcut('Ctrl+N')
        self.newproj.triggered.connect(self.new_project)

        self.openproj = QtGui.QAction(
            QtGui.QIcon(init_path + 'images/openProject.png'),
            '<b>Open Project</b>', self
        )
        self.openproj.setShortcut('Ctrl+O')
        self.openproj.triggered.connect(self.open_project)

        self.closeproj = QtGui.QAction(
            QtGui.QIcon(init_path + 'images/closeProject.png'),
            '<b>Close Project</b>', self
        )
        self.closeproj.setShortcut('Ctrl+X')
        self.closeproj.triggered.connect(self.close_project)

        self.wrkspce = QtGui.QAction(
            QtGui.QIcon(init_path + 'images/workspace.ico'),
            '<b>Change Workspace</b>', self
        )
        self.wrkspce.setShortcut('Ctrl+W')
        self.wrkspce.triggered.connect(self.change_workspace)

        self.helpfile = QtGui.QAction(
            QtGui.QIcon(init_path + 'images/helpProject.png'),
            '<b>Help</b>', self
        )
        self.helpfile.setShortcut('Ctrl+H')
        self.helpfile.triggered.connect(self.help_project)

        # added devDocs logo and called functions
        self.devdocs = QtGui.QAction(
            QtGui.QIcon(init_path + 'images/dev_docs.png'),
            '<b>Dev Docs</b>', self
        )
        self.devdocs.setShortcut('Ctrl+D')
        self.devdocs.triggered.connect(self.dev_docs)

        self.topToolbar = self.addToolBar('Top Tool Bar')
        self.topToolbar.addAction(self.newproj)
        self.topToolbar.addAction(self.openproj)
        self.topToolbar.addAction(self.closeproj)
        self.topToolbar.addAction(self.wrkspce)
        self.topToolbar.addAction(self.helpfile)
        self.topToolbar.addAction(self.devdocs)

        # This part is setting fossee logo to the right
        # corner in the application window.
        self.spacer = QtWidgets.QWidget()
        self.spacer.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding)
        self.topToolbar.addWidget(self.spacer)
        self.logo = QtWidgets.QLabel()
        self.logopic = QtGui.QPixmap(
            os.path.join(
                os.path.abspath(''), init_path + 'images', 'fosseeLogo.png'
            ))
        self.logopic = self.logopic.scaled(
            QSize(150, 150), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.logo.setPixmap(self.logopic)
        self.logo.setStyleSheet("padding:0 15px 0 0;")
        self.topToolbar.addWidget(self.logo)

        # Left Tool bar Action Widget
        self.kicad = QtGui.QAction(
            QtGui.QIcon(init_path + 'images/kicad.png'),
            '<b>Open Schematic</b>', self
        )
        self.kicad.triggered.connect(self.obj_kicad.openSchematic)

        self.conversion = QtGui.QAction(
            QtGui.QIcon(init_path + 'images/ki-ng.png'),
            '<b>Convert KiCad to Ngspice</b>', self
        )
        self.conversion.triggered.connect(self.obj_kicad.openKicadToNgspice)

        self.ngspice = QtGui.QAction(
            QtGui.QIcon(init_path + 'images/ngspice.png'),
            '<b>Simulate</b>', self
        )
        self.ngspice.triggered.connect(self.plotFlagPopBox)

        self.model = QtGui.QAction(
            QtGui.QIcon(init_path + 'images/model.png'),
            '<b>Model Editor</b>', self
        )
        self.model.triggered.connect(self.open_modelEditor)

        self.subcircuit = QtGui.QAction(
            QtGui.QIcon(init_path + 'images/subckt.png'),
            '<b>Subcircuit</b>', self
        )
        self.subcircuit.triggered.connect(self.open_subcircuit)

        self.nghdl = QtGui.QAction(
            QtGui.QIcon(init_path + 'images/nghdl.png'), '<b>NGHDL</b>', self
        )
        self.nghdl.triggered.connect(self.open_nghdl)

        self.makerchip = QtGui.QAction(
            QtGui.QIcon(init_path + 'images/makerchip.png'),
            '<b>Makerchip-NgVeri</b>', self
        )
        self.makerchip.triggered.connect(self.open_makerchip)

        self.omedit = QtGui.QAction(
            QtGui.QIcon(init_path + 'images/omedit.png'),
            '<b>Modelica Converter</b>', self
        )
        self.omedit.triggered.connect(self.open_OMedit)

        self.omoptim = QtGui.QAction(
            QtGui.QIcon(init_path + 'images/omoptim.png'),
            '<b>OM Optimisation</b>', self
        )
        self.omoptim.triggered.connect(self.open_OMoptim)

        self.conToeSim = QtGui.QAction(
            QtGui.QIcon(init_path + 'images/icon.png'),
            '<b>Schematic converter</b>', self
        )
        self.conToeSim.triggered.connect(self.open_conToeSim)

        # Adding Action Widget to tool bar
        self.lefttoolbar = QtWidgets.QToolBar('Left ToolBar')
        self.addToolBar(QtCore.Qt.ToolBarArea.LeftToolBarArea, self.lefttoolbar)
        self.lefttoolbar.addAction(self.kicad)
        self.lefttoolbar.addAction(self.conversion)
        self.lefttoolbar.addAction(self.ngspice)
        self.lefttoolbar.addAction(self.model)
        self.lefttoolbar.addAction(self.subcircuit)
        self.lefttoolbar.addAction(self.makerchip)
        self.lefttoolbar.addAction(self.nghdl)
        self.lefttoolbar.addAction(self.openroad)
        self.lefttoolbar.addAction(self.omedit)
        self.lefttoolbar.addAction(self.omoptim)
        self.lefttoolbar.addAction(self.conToeSim)
        self.lefttoolbar.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.lefttoolbar.setIconSize(QSize(40, 40))

    def plotFlagPopBox(self):
        """Displays a pop-up box for Ngspice plots."""

        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setWindowTitle("Ngspice Plots")
        msg_box.setText("Do you want Ngspice plots?")
        
        yes_button = msg_box.addButton("Yes", QtWidgets.QMessageBox.ButtonRole.YesRole)
        no_button = msg_box.addButton("No", QtWidgets.QMessageBox.ButtonRole.NoRole)

        msg_box.exec()

        if msg_box.clickedButton() == yes_button:
            self.plotFlag = True  
        else:
            self.plotFlag = False  

        self.open_ngspice()

    def closeEvent(self, event):
        '''Closes the ongoing program.'''
        exit_msg = "Are you sure you want to exit the program?"
        exit_msg += " All unsaved data will be lost."
        reply = QtWidgets.QMessageBox.question(
            self, 'Message', exit_msg, QtWidgets.QMessageBox.StandardButton.Yes,
            QtWidgets.QMessageBox.StandardButton.No
        )

        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            for proc in self.obj_appconfig.procThread_list:
                try:
                    proc.terminate()
                except BaseException:
                    pass
            try:
                for process_object in self.obj_appconfig.process_obj:
                    try:
                        process_object.close()
                    except BaseException:
                        pass
            except BaseException:
                pass

            try:
                self.project.close()
            except BaseException:
                pass
            event.accept()
            self.systemTrayIcon.showMessage('Exit', 'eSim is Closed.')

        elif reply == QtWidgets.QMessageBox.StandardButton.No:
            event.ignore()

    def new_project(self):
        """Calls New Project Info class."""
        text, ok = QtWidgets.QInputDialog.getText(
            self, 'New Project Info', 'Enter Project Name:'
        )
        updated = False

        if ok:
            self.projname = (str(text))
            self.project = NewProjectInfo()
            directory, filelist = self.project.createProject(self.projname)

            if directory and filelist:
                self.obj_Mainview.obj_projectExplorer.addTreeNode(
                    directory, filelist
                )
                updated = True

        if not updated:
            print("No new project created")
            self.obj_appconfig.print_info('No new project created')
            try:
                self.obj_appconfig.print_info(
                    'Current project is : ' +
                    self.obj_appconfig.current_project["ProjectName"]
                )
            except BaseException:
                pass

    def open_project(self):
        """Calls Open Project Info class."""
        print("Function : Open Project")
        self.project = OpenProjectInfo()
        try:
            directory, filelist = self.project.body()
            self.obj_Mainview.obj_projectExplorer.addTreeNode(
                directory, filelist)
        except BaseException:
            pass

    def close_project(self):
        """Closes the saved project."""
        print("Function : Close Project")
        current_project = self.obj_appconfig.current_project['ProjectName']
        if current_project is None:
            pass
        else:
            temp = self.obj_appconfig.current_project['ProjectName']
            for pid in self.obj_appconfig.proc_dict[temp]:
                try:
                    os.kill(pid, 9)
                except BaseException:
                    pass
            self.obj_Mainview.obj_dockarea.closeDock()
            self.obj_appconfig.current_project['ProjectName'] = None
            self.systemTrayIcon.showMessage(
                'Close', 'Current project ' +
                os.path.basename(current_project) + ' is Closed.'
            )

    def change_workspace(self):
        """Changes Workspace"""
        print("Function : Change Workspace")
        self.obj_workspace.returnWhetherClickedOrNot(self)
        self.hide()
        self.obj_workspace.show()

    def help_project(self):
        """Opens usermanual in dockarea."""
        print("Function : Help")
        self.obj_appconfig.print_info('Help is called')
        print("Current Project is : ", self.obj_appconfig.current_project)
        self.obj_Mainview.obj_dockarea.usermanual()

    def dev_docs(self):
        """Guides user to readthedocs"""
        print("Function : DevDocs")
        self.obj_appconfig.print_info('DevDocs is called')
        print("Current Project is : ", self.obj_appconfig.current_project)
        webbrowser.open("https://esim.readthedocs.io/en/latest/index.html")

    @QtCore.pyqtSlot(QtCore.QProcess.ExitStatus, int)
    def plotSimulationData(self, exitCode, exitStatus):
        """Enables interaction for new simulation"""
        self.ngspice.setEnabled(True)
        self.conversion.setEnabled(True)
        self.closeproj.setEnabled(True)
        self.wrkspce.setEnabled(True)

        if exitStatus == QtCore.QProcess.ExitStatus.NormalExit and exitCode == 0:
            try:
                self.obj_Mainview.obj_dockarea.plottingEditor()
            except Exception as e:
                self.msg = QtWidgets.QErrorMessage()
                self.msg.setModal(True)
                self.msg.setWindowTitle("Error Message")
                self.msg.showMessage(
                    'Data could not be plotted. Please try again.'
                )
                self.msg.exec()
                print("Exception Message:", str(e), traceback.format_exc())
                self.obj_appconfig.print_error('Exception Message : '
                                               + str(e))

    def open_ngspice(self):
        """Executes ngspice on current project."""
        projDir = self.obj_appconfig.current_project["ProjectName"]

        if projDir is not None:
            projName = os.path.basename(projDir)
            ngspiceNetlist = os.path.join(projDir, projName + ".cir.out")

            if not os.path.isfile(ngspiceNetlist):
                print("Netlist file (*.cir.out) not found.")
                self.msg = QtWidgets.QErrorMessage()
                self.msg.setModal(True)
                self.msg.setWindowTitle("Error Message")
                self.msg.showMessage(
                    'Netlist (*.cir.out) not found.'
                )
                self.msg.exec()
                return

            self.obj_Mainview.obj_dockarea.ngspiceEditor(
                projName, ngspiceNetlist, self.simulationEndSignal, self.plotFlag)

            self.ngspice.setEnabled(False)
            self.conversion.setEnabled(False)
            self.closeproj.setEnabled(False)
            self.wrkspce.setEnabled(False)

        else:
            self.msg = QtWidgets.QErrorMessage()
            self.msg.setModal(True)
            self.msg.setWindowTitle("Error Message")
            self.msg.showMessage(
                'Please select the project first.'
            )
            self.msg.exec()

    def open_subcircuit(self):
        """Opens 'subcircuit' option."""
        print("Function : Subcircuit editor")
        self.obj_appconfig.print_info('Subcircuit editor is called')
        self.obj_Mainview.obj_dockarea.subcircuiteditor()

    def open_nghdl(self):
        """Calls NGHDL option."""
        print("Function : NGHDL")
        self.obj_appconfig.print_info('NGHDL is called')

        if self.obj_validation.validateTool('nghdl'):
            self.cmd = 'nghdl -e'
            self.obj_workThread = Worker.WorkerThread(self.cmd)
            self.obj_workThread.start()
        else:
            self.msg = QtWidgets.QErrorMessage()
            self.msg.setModal(True)
            self.msg.setWindowTitle('NGHDL Error')
            self.msg.showMessage('Error while opening NGHDL. ' +
                                 'Please make sure it is installed')
            self.obj_appconfig.print_error('Error while opening NGHDL. ' +
                                           'Please make sure it is installed')
            self.msg.exec()

    def open_makerchip(self):
        """Opens makerchip option."""
        print("Function : Makerchip and Verilator to Ngspice Converter")
        self.obj_appconfig.print_info('Makerchip is called')
        self.obj_Mainview.obj_dockarea.makerchip()

    # --- FINAL OPENROAD FUNCTION ---
    def run_openroad_flow(self):

        try:

            import os
            import subprocess
            from PyQt5 import QtWidgets
            from maker import OpenROAD

            projDir = self.obj_appconfig.current_project["ProjectName"]

            if projDir is None:

                QtWidgets.QMessageBox.warning(
                    self,
                    "No Project",
                    "Please open or create a project first!"
                )

                return

            print(f"Function : OpenROAD Flow for {projDir}")

            cir_file, _ = QtWidgets.QFileDialog.getOpenFileName(
                self,
                "Select .cir.out File",
                projDir,
                "CIR OUT Files (*.cir.out)"
            )

            if not cir_file:

                QtWidgets.QMessageBox.warning(
                    self,
                    "No File Selected",
                    "Please select a .cir.out file."
                )

                return

            if not cir_file.endswith(".cir.out"):

                QtWidgets.QMessageBox.critical(
                    self,
                    "Wrong File",
                    "Wrong file selected.\nPlease select a .cir.out file."
                )

                return

            cir_filename = os.path.basename(cir_file)

            design_name = cir_filename.replace(".cir.out", "")

            print(f"\nUsing Netlist:\n{cir_file}\n")

            netlist_script = os.path.join(
                os.path.dirname(__file__),
                "..",
                "maker",
                "netlist2rtl.py"
            )

            print("\n[1] Running Netlist to RTL Conversion\n")

            cmd = [
                "python3",
                netlist_script,
                cir_file
            ]

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            for line in process.stdout:

                print(line, end="")

            process.wait()

            if process.returncode != 0:

                QtWidgets.QMessageBox.critical(
                    self,
                    "Conversion Error",
                    "Netlist to RTL conversion failed."
                )

                return

            verilog_file = os.path.join(
                projDir,
                design_name + ".v"
            )

            if not os.path.exists(verilog_file):

                QtWidgets.QMessageBox.critical(
                    self,
                    "Verilog Missing",
                    f"Generated Verilog not found:\n{verilog_file}"
                )

                return

            print("\n[2] Generated Verilog Found\n")
            print(verilog_file)

            print("\n[3] Starting OpenROAD Flow\n")

            self.or_logic = OpenROAD.OpenROADFlow(
                design_name=design_name,
                verilog_file=verilog_file
            )

            self.or_logic.run()

            gds_file = os.path.join(
                projDir,
                design_name + ".gds"
            )

            if not os.path.exists(gds_file):

                QtWidgets.QMessageBox.critical(
                    self,
                    "GDS Missing",
                    "OpenROAD finished but GDS not found."
                )

                return

            print("\n[4] Opening GDS in KLayout\n")

            subprocess.Popen(["klayout", gds_file])

            QtWidgets.QMessageBox.information(
                self,
                "Flow Completed",
                f"GDS Generated Successfully:\n\n{gds_file}"
            )

        except ImportError as e:

            print(f"Import Error: {e}")

            QtWidgets.QMessageBox.critical(
                self,
                "Import Error",
                str(e)
            )

        except Exception as e:

            import traceback

            print(traceback.format_exc())

            QtWidgets.QMessageBox.critical(
                self,
                "OpenROAD Error",
                str(e)
            )
    # ----------------------------------------

    def open_modelEditor(self):
        """Opens model editor."""
        print("Function : Model editor")
        self.obj_appconfig.print_info('Model editor is called')
        self.obj_Mainview.obj_dockarea.modelEditor()

    def open_OMedit(self):
        """Calls ngspice to OMEdit converter."""
        self.obj_appconfig.print_info('OMEdit is called')
        self.projDir = self.obj_appconfig.current_project["ProjectName"]

        if self.projDir is not None:
            if self.obj_validation.validateCirOut(self.projDir):
                self.projName = os.path.basename(self.projDir)
                self.ngspiceNetlist = os.path.join(
                    self.projDir, self.projName + ".cir.out"
                )
                self.modelicaNetlist = os.path.join(
                    self.projDir, self.projName + ".mo"
                )

                """
                try:
                    # Creating a command for Ngspice to Modelica converter
                    self.cmd1 = "
                        python3 ../ngspicetoModelica/NgspicetoModelica.py "\
                            + self.ngspiceNetlist
                    self.obj_workThread1 = Worker.WorkerThread(self.cmd1)
                    self.obj_workThread1.start()
                    if self.obj_validation.validateTool("OMEdit"):
                        # Creating command to run OMEdit
                        self.cmd2 = "OMEdit "+self.modelicaNetlist
                        self.obj_workThread2 = Worker.WorkerThread(self.cmd2)
                        self.obj_workThread2.start()
                    else:
                        self.msg = QtWidgets.QMessageBox()
                        self.msgContent = "There was an error while
                            opening OMEdit.<br/>\
                        Please make sure OpenModelica is installed in your\
                            system. <br/>\
                        To install it on Linux : Go to\
                            <a href=https://www.openmodelica.org/download/\
                                download-linux>OpenModelica Linux</a> and  \
                                    install nigthly build release.<br/>\
                        To install it on Windows : Go to\
                         <a href=https://www.openmodelica.org/download/\
                        download-windows>OpenModelica Windows</a>\
                         and install latest version.<br/>"
                        self.msg.setTextFormat(QtCore.Qt.TextFormat.RichText)
                        self.msg.setText(self.msgContent)
                        self.msg.setWindowTitle("Missing OpenModelica")
                        self.obj_appconfig.print_info(self.msgContent)
                        self.msg.exec()

                except Exception as e:
                    self.msg = QtWidgets.QErrorMessage()
                    self.msg.setModal(True)
                    self.msg.setWindowTitle(
                        "Ngspice to Modelica conversion error")
                    self.msg.showMessage(
                        'Unable to convert NgSpice netlist to\
                            Modelica netlist :'+str(e))
                    self.msg.exec()
                    self.obj_appconfig.print_error(str(e))
                """

                self.obj_Mainview.obj_dockarea.modelicaEditor(self.projDir)
            else:
                self.msg = QtWidgets.QErrorMessage()
                self.msg.setModal(True)
                self.msg.setWindowTitle("Missing Ngspice Netlist")
                self.msg.showMessage(
                    'Current project does not contain any Ngspice file. ' +
                    'Please create Ngspice file with extension .cir.out'
                )
                self.msg.exec()
        else:
            self.msg = QtWidgets.QErrorMessage()
            self.msg.setModal(True)
            self.msg.setWindowTitle("Error Message")
            self.msg.showMessage(
                'Please select the project first. You can either ' +
                'create a new project or open an existing project'
            )
            self.msg.exec()

    def open_OMoptim(self):
        """Opens OMOptim."""
        print("Function : OMOptim")
        self.obj_appconfig.print_info('OMOptim is called')
        if self.obj_validation.validateTool("OMOptim"):
            self.cmd = "OMOptim"
            self.obj_workThread = Worker.WorkerThread(self.cmd)
            self.obj_workThread.start()
        else:
            self.msg = QtWidgets.QMessageBox()
            self.msgContent = (
                "There was an error while opening OMOptim.<br/>"
                "Please make sure OpenModelica is installed in your"
                " system.<br/>"
                "To install it on Linux : Go to <a href="
                "https://www.openmodelica.org/download/download-linux"
                ">OpenModelica Linux</a> and install nightly build"
                " release.<br/>"
                "To install it on Windows : Go to <a href="
                "https://www.openmodelica.org/download/download-windows"
                ">OpenModelica Windows</a> and install latest version.<br/>"
            )
            self.msg.setTextFormat(QtCore.Qt.TextFormat.RichText)
            self.msg.setText(self.msgContent)
            self.msg.setWindowTitle("Error Message")
            self.obj_appconfig.print_info(self.msgContent)
            self.msg.exec()

    def open_conToeSim(self):
        print("Function : Schematic converter")
        self.obj_appconfig.print_info('Schematic converter is called')
        self.obj_Mainview.obj_dockarea.eSimConverter()


# This class initialize the Main View of Application
class MainView(QtWidgets.QWidget):
    def __init__(self, *args):
        QtWidgets.QWidget.__init__(self, *args)
        self.obj_appconfig = Appconfig()
        self.leftSplit = QtWidgets.QSplitter()
        self.middleSplit = QtWidgets.QSplitter()
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.middleContainer = QtWidgets.QWidget()
        self.middleContainerLayout = QtWidgets.QVBoxLayout()
        self.noteArea = QtWidgets.QTextEdit()
        self.noteArea.setReadOnly(True)

        # Set explicit scrollbar policy
        self.noteArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.noteArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.obj_appconfig.noteArea['Note'] = self.noteArea
        self.obj_appconfig.noteArea['Note'].append('        eSim Started......')
        self.obj_appconfig.noteArea['Note'].append('Project Selected : None\n')

        self.noteArea.setStyleSheet("""
        QTextEdit { border-radius: 15px; border: 1px solid gray; padding: 5px; background-color: white; }
        """)

        self.obj_dockarea = DockArea.DockArea()
        self.obj_projectExplorer = ProjectExplorer.ProjectExplorer()

        # Adding content to vertical middle Split.
        self.middleSplit.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.middleSplit.addWidget(self.obj_dockarea)
        self.middleSplit.addWidget(self.noteArea)
        self.middleContainerLayout.addWidget(self.middleSplit)
        self.middleContainer.setLayout(self.middleContainerLayout)
        self.leftSplit.addWidget(self.obj_projectExplorer)
        self.leftSplit.addWidget(self.middleContainer)
        self.mainLayout.addWidget(self.leftSplit)
        self.leftSplit.setSizes([int(self.width() / 4.5), self.height()])
        self.middleSplit.setSizes([self.width(), int(self.height() / 2)])
        self.setLayout(self.mainLayout)


def main(args):
    print("Starting eSim......")
    # Set non-native dialogs globally
    # NOTE: AA_DontUseNativeDialogs removed in Qt6.
    # Native dialog behavior is now controlled per-dialog via QFileDialog.Option.
    app = QtWidgets.QApplication(args)
    appView = Application()
    appView.hide()
    splash_pix = QtGui.QPixmap(init_path + 'images/splash_screen_esim.png')
    splash = QtWidgets.QSplashScreen(
        splash_pix, QtCore.Qt.WindowType.WindowStaysOnTopHint
    )
    splash.setMask(splash_pix.mask())
    splash.setDisabled(True)
    splash.show()
    appView.splash = splash
    appView.obj_workspace.returnWhetherClickedOrNot(appView)

    try:
        user_home = os.path.join('library', 'config') if os.name == 'nt' else os.path.expanduser('~')
        file = open(os.path.join(user_home, ".esim/workspace.txt"), 'r')
        work = int(file.read(1))
        file.close()
    except IOError:
        work = 0

    if work != 0:
        appView.obj_workspace.defaultWorkspace()
    else:
        appView.obj_workspace.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    try:
        main(sys.argv)
    except Exception as err:
        print("Error: ", err)
