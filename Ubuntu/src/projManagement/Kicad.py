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
from PyQt5 import QtWidgets


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
            self.cmd = "eeschema " + self.project + ".kicad_sch"  # kicad6 file
            if not os.path.exists(self.project + ".kicad_sch") \
                    and os.path.exists(self.project + ".sch"):
                self.cmd = "eeschema " + self.project + ".sch"    # kicad4 file

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
