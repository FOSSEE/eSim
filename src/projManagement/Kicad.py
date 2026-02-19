# =========================================================================
#          FILE: Kicad.py
#
#         USAGE: ---
#
#   DESCRIPTION: It calls kicad schematic
#
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Fahim Khan, fahim.elex@gmail.com
#      MODIFIED: Rahul Paknikar, Partha Singh Roy
#  ORGANIZATION: eSim Team at FOSSEE, IIT Bombay
#       CREATED: Tuesday 17 February 2015
#      REVISION: Thursday 29 Jun 2023
# =========================================================================

import os
from . import Validation
from configuration.Appconfig import Appconfig
from . import Worker
from PyQt5 import QtWidgets, QtGui, QtCore


class Kicad:
    """
    This class called the Kicad Schematic, KicadtoNgspice Converter, Layout
    editor and Footprint Editor
    Initialise validation, appconfig and dockarea

    @params
        :dockarea   => passed from DockArea in frontEnd folder, consists
                        of all functions for dockarea

    @return
    """

    def __init__(self, dockarea):
        self.obj_validation = Validation.Validation()
        self.obj_appconfig = Appconfig()
        self.obj_dockarea = dockarea
        self.obj_workThread = Worker.WorkerThread(None)

    def check_open_schematic(self):
        """
        This function checks if any of the project's schematic is open or not

        @params

        @return
            True        => If the project's schematic is not open
            False       => If the project's schematic is open
        """
        if self.obj_workThread:
            procList = self.obj_workThread.get_proc_threads()[:]
            if procList:
                for proc in procList:
                    if proc.poll() is None:
                        return True
                    else:
                        self.obj_workThread.get_proc_threads().remove(proc)

        return False

    def openSchematic(self):
        """
        This function create command to open Kicad schematic after
        appropriate validation checks

        @params


        @return
        """
        print("Function : Open Kicad Schematic")
        self.projDir = self.obj_appconfig.current_project["ProjectName"]
        try:
            self.obj_appconfig.print_info(
                'Kicad Schematic is called for project ' + self.projDir)
        except BaseException:
            pass

        # Validating if current project is available or not
        if self.obj_validation.validateKicad(self.projDir):
            self.projName = os.path.basename(self.projDir)
            self.project = os.path.join(self.projDir, self.projName)

            # creating a command to open schematic
            schematic_file = self.project + ".kicad_sch"  # kicad6 file
            if not os.path.exists(schematic_file) and os.path.exists(
                    self.project + ".sch"):
                schematic_file = self.project + ".sch"    # kicad4 file

            # When running as Flatpak, use flatpak run to launch KiCad
            # (install: flatpak install flathub org.kicad.KiCad)
            if os.environ.get('ESIM_FLATPAK') == '1':
                self.cmd = (
                    "flatpak run --command=eeschema org.kicad.KiCad " +
                    schematic_file
                )
            else:
                self.cmd = "eeschema " + schematic_file

            self.obj_workThread.args = self.cmd
            self.obj_workThread.start()

        else:
            self.msg = QtWidgets.QErrorMessage()
            self.msg.setModal(True)
            self.msg.setWindowTitle("Error Message")
            self.msg.showMessage(
                'Please select the project first. You can either ' +
                'create new project or open an existing project')
            self.msg.exec_()
            self.obj_appconfig.print_warning(
                'Please select the project first. You can either ' +
                'create new project or open an existing project')

    '''
    # Commenting as it is no longer needed as PCB and Layout will open from
    # eeschema
    def openFootprint(self):
        """
        This function create command to open Footprint editor
        """
        print "Kicad Foot print Editor called"
        self.projDir = self.obj_appconfig.current_project["ProjectName"]
        try:
            self.obj_appconfig.print_info('Kicad Footprint Editor is called'
            + 'for project : ' + self.projDir)
        except:
            pass
        #Validating if current project is available or not

        if self.obj_validation.validateKicad(self.projDir):
            #print "calling Kicad FootPrint Editor ",self.projDir
            self.projName = os.path.basename(self.projDir)
            self.project = os.path.join(self.projDir,self.projName)

            #Creating a command to run
            self.cmd = "cvpcb "+self.project+".net "
            self.obj_workThread = Worker.WorkerThread(self.cmd)
            self.obj_workThread.start()

        else:
            self.msg = QtWidgets.QErrorMessage()
            self.msg.setModal(True)
            self.msg.setWindowTitle("Error Message")
            self.msg.showMessage('Please select the project first. You can'
            + 'either create new project or open an existing project')
            self.msg.exec_()
            self.obj_appconfig.print_warning('Please select the project'
            + 'first. You can either create new project or open an existing'
            + 'project')

    def openLayout(self):
        """
        This function create command to open Layout editor
        """
        print "Kicad Layout is called"
        self.projDir = self.obj_appconfig.current_project["ProjectName"]
        try:
            self.obj_appconfig.print_info('PCB Layout is called for project : '
            + self.projDir)
        except:
            pass
        #Validating if current project is available or not
        if self.obj_validation.validateKicad(self.projDir):
            print "calling Kicad schematic ",self.projDir
            self.projName = os.path.basename(self.projDir)
            self.project = os.path.join(self.projDir,self.projName)

            #Creating a command to run
            self.cmd = "pcbnew "+self.project+".net "
            self.obj_workThread = Worker.WorkerThread(self.cmd)
            self.obj_workThread.start()

        else:
            self.msg = QtWidgets.QErrorMessage()
            self.msg.setModal(True)
            self.msg.setWindowTitle("Error Message")
            self.msg.showMessage('Please select the project first. You can'
            + 'either create new project or open an existing project')
            self.msg.exec_()
            self.obj_appconfig.print_warning('Please select the project'
            + 'first. You can either create new project or open an existing'
            + 'project')
    '''

    def openKicadToNgspice(self):
        """
        This function create command to validate and then call
        KicadToNgSPice converter from DockArea file

        @params

        @return
        """
        print("Function: Open Kicad to Ngspice Converter")

        self.projDir = self.obj_appconfig.current_project["ProjectName"]
        try:
            self.obj_appconfig.print_info(
                'Kicad to Ngspice Conversion is called')
            self.obj_appconfig.print_info('Current Project is ' + self.projDir)
        except BaseException:
            pass
        # Validating if current project is available or not
        if self.obj_validation.validateKicad(self.projDir):
            # Checking if project has .cir file or not
            if self.obj_validation.validateCir(self.projDir):
                self.projName = os.path.basename(self.projDir)
                self.project = os.path.join(self.projDir, self.projName)

                # Creating a command to run
                """
                self.cmd = ("python3  ../kicadtoNgspice/KicadtoNgspice.py "
                + "self.project+".cir ")
                self.obj_workThread = Worker.WorkerThread(self.cmd)
                self.obj_workThread.start()
                """
                var = self.project + ".cir"
                self.obj_dockarea.kicadToNgspiceEditor(var)

            else:
                self.msg = QtWidgets.QErrorMessage()
                self.msg.setModal(True)
                self.msg.setWindowTitle("Error Message")
                self.msg.showMessage(
                    'The project does not contain any Kicad netlist file ' +
                    'for conversion.')
                self.obj_appconfig.print_error(
                    'The project does not contain any Kicad netlist file ' +
                    'for conversion.')
                self.msg.exec_()

        else:
            self.msg = QtWidgets.QErrorMessage()
            self.msg.setModal(True)
            self.msg.setWindowTitle("Error Message")
            self.msg.showMessage(
                'Please select the project first. You can either ' +
                'create new project or open an existing project')
            self.msg.exec_()
            self.obj_appconfig.print_warning(
                'Please select the project first. You can either ' +
                'create new project or open an existing project')


class KicadWidget(QtWidgets.QWidget):
    """
    A modern, themed QWidget for Kicad actions, matching the Application.py style.
    This does not affect any backend logic.
    """
    def __init__(self, parent=None):
        super(KicadWidget, self).__init__(parent)
        self.setObjectName("KicadWidget")
        self.setStyleSheet("""
            QWidget#KicadWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #23273a, stop:1 #181b24);
                border-radius: 16px;
                border: 1.5px solid #23273a;
            }
            QPushButton {
                background-color: #23273a;
                color: #e8eaed;
                border: 1.5px solid #353b48;
                border-radius: 10px;
                padding: 10px 24px;
                font-family: 'Inter', 'Segoe UI', 'Roboto', 'Arial', sans-serif;
                font-size: 15px;
                font-weight: 500;
                letter-spacing: 0.1px;
            }
            QPushButton:hover {
                background-color: #353b48;
                color: #40c4ff;
            }
            QPushButton:pressed {
                background-color: #181b24;
                color: #40c4ff;
            }
            QLabel {
                color: #e8eaed;
                font-size: 18px;
                font-weight: bold;
                padding-bottom: 12px;
            }
        """)
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(18)
        layout.setContentsMargins(32, 32, 32, 32)

        title = QtWidgets.QLabel("Kicad Project Actions")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        btn_open_schematic = QtWidgets.QPushButton("Open Schematic")
        btn_open_layout = QtWidgets.QPushButton("Open Layout")
        btn_open_footprint = QtWidgets.QPushButton("Open Footprint Editor")
        btn_convert_ngspice = QtWidgets.QPushButton("Convert to Ngspice")

        # These are placeholders for connecting to actual logic
        btn_open_schematic.clicked.connect(lambda: print("Open Schematic clicked"))
        btn_open_layout.clicked.connect(lambda: print("Open Layout clicked"))
        btn_open_footprint.clicked.connect(lambda: print("Open Footprint Editor clicked"))
        btn_convert_ngspice.clicked.connect(lambda: print("Convert to Ngspice clicked"))

        layout.addWidget(btn_open_schematic)
        layout.addWidget(btn_open_layout)
        layout.addWidget(btn_open_footprint)
        layout.addWidget(btn_convert_ngspice)
        layout.addStretch(1)
        self.setLayout(layout)
