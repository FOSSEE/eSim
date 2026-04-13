# =========================================================================
#          FILE: openProject.py
#
#         USAGE: ---
#
#   DESCRIPTION: It is called whenever new project is being called.
#
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Fahim Khan, fahim.elex@gmail.com
#      MODIFIED: Rahul Paknikar, rahulp@iitb.ac.in
#  ORGANIZATION: eSim Team at FOSSEE, IIT Bombay
#       CREATED: Wednesday 12 February 2015
#      REVISION: Sunday 26 July 2020
# =========================================================================

from PyQt5 import QtWidgets, QtCore
from .Validation import Validation
from configuration.Appconfig import Appconfig
import os
import json


class OpenProjectInfo(QtWidgets.QWidget):
    """
    This class is called when User click on Open Project Button
    """

    def __init__(self):
        super(OpenProjectInfo, self).__init__()
        self.obj_validation = Validation()

    def body(self):
        """
        Open a project directory using Qt GUI and validate
        if .proj file present in it using `Validation` class

        @params

        @return
            :dirs        => The directories inside the project folder
            :filelist    => The files inside the project folder
        """
        self.obj_Appconfig = Appconfig()
        self.openDir = self.obj_Appconfig.default_workspace["workspace"]
        self.projDir = QtCore.QDir.toNativeSeparators(
            QtWidgets.QFileDialog.getExistingDirectory(
                self, "open", self.openDir
            )
        )

        if self.obj_validation.validateOpenproj(self.projDir):
            self.obj_Appconfig.current_project['ProjectName'] = str(
                self.projDir)
            if os.path.isdir(self.projDir):
                print("True")

            for dirs, subdirs, filelist in os.walk(
                    self.obj_Appconfig.current_project["ProjectName"]):
                # directory = dirs
                # files = filelist
                # above 'directory' and 'files' variable never used
                pass
            self.obj_Appconfig.project_explorer[dirs] = filelist
            json.dump(
                self.obj_Appconfig.project_explorer, open(
                    self.obj_Appconfig.dictPath["path"], 'w'))
            self.obj_Appconfig.print_info('Open Project called')
            self.obj_Appconfig.print_info('Current Project is ' + self.projDir)
            return dirs, filelist

        else:
            self.obj_Appconfig.print_error(
                "The project doesn't contain .proj file. Please select the " +
                "proper directory else you won't be able to perform any " +
                "operation"
            )
            reply = QtWidgets.QMessageBox.critical(
                None, "Error Message",
                "<b>Error: The project doesn't contain .proj file.</b><br/>"
                "<b>Please select the proper project directory else you won't"
                " be able to perform any operation</b>",
                QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
            )

            if reply == QtWidgets.QMessageBox.Ok:
                self.body()
                self.obj_Appconfig.print_info('Open Project called')
                self.obj_Appconfig.print_info(
                    'Current Project is ' + self.projDir)
            elif reply == QtWidgets.QMessageBox.Cancel:
                self.obj_Appconfig.print_info('No Project opened')
