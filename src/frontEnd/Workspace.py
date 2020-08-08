# =========================================================================
#          FILE: Workspace.py
#
#         USAGE: ---
#
#   DESCRIPTION: This define all configuration used in Application.
#
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Fahim Khan, fahim.elex@gmail.com
#      MODIFIED: Rahul Paknikar, rahulp@iitb.ac.in
#  ORGANIZATION: eSim Team at FOSSEE, IIT Bombay
#       CREATED: Wednesday 05 February 2015
#      REVISION: Saturday 25 July 2020
# =========================================================================

from PyQt5 import QtCore, QtGui, QtWidgets
from configuration.Appconfig import Appconfig
import time
import os
import json


class Workspace(QtWidgets.QWidget):
    """
    This class creates UI for WorkSpace selection window.

        - This window contains text area to select location of your choice \
          or browse location for workspace area.
        - By default workspace is set in ~/eSim-Workspace.
        - This workspace area contains all the projects made by user.

    """

    def __init__(self, parent=None):
        super(Workspace, self).__init__()
        self.obj_appconfig = Appconfig()

        # Initializing Workspace directory for project
        self.initWorkspace()

    def initWorkspace(self):

        self.mainwindow = QtWidgets.QVBoxLayout()
        self.split = QtWidgets.QSplitter()
        self.split.setOrientation(QtCore.Qt.Vertical)

        self.grid = QtWidgets.QGridLayout()
        self.note = QtWidgets.QTextEdit(self)
        self.note.append(self.obj_appconfig.workspace_text)
        self.note.setReadOnly(True)

        self.workspace_label = QtWidgets.QLabel(self)
        self.workspace_label.setText("Workspace:")
        self.workspace_loc = QtWidgets.QLineEdit(self)
        self.workspace_loc.setText(self.obj_appconfig.home)

        # Buttons
        self.browsebtn = QtWidgets.QPushButton('Browse')
        self.browsebtn.clicked.connect(self.browseLocation)
        self.okbtn = QtWidgets.QPushButton('OK')
        self.okbtn.clicked.connect(self.createWorkspace)
        self.cancelbtn = QtWidgets.QPushButton('Cancel')
        self.cancelbtn.clicked.connect(self.defaultWorkspace)

        # Checkbox
        self.chkbox = QtWidgets.QCheckBox('Set Default', self)
        self.chkbox.setCheckState(int(self.obj_appconfig.workspace_check))

        # Layout
        self.grid.addWidget(self.note, 0, 0, 1, 15)
        self.grid.addWidget(self.workspace_label, 2, 1)
        self.grid.addWidget(self.workspace_loc, 2, 2, 2, 12)
        self.grid.addWidget(self.browsebtn, 2, 14)
        self.grid.addWidget(self.chkbox, 4, 2)
        self.grid.addWidget(self.okbtn, 5, 13)
        self.grid.addWidget(self.cancelbtn, 5, 14)

        self.setGeometry(QtCore.QRect(500, 250, 400, 400))
        self.setMaximumSize(4000, 200)
        self.setWindowTitle("eSim")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowModality(2)

        init_path = '../../'
        if os.name == 'nt':
            init_path = ''

        self.setWindowIcon(QtGui.QIcon(init_path + 'images/logo.png'))
        self.setLayout(self.grid)

    def defaultWorkspace(self):
        print("Default workspace selected : " +
              self.obj_appconfig.default_workspace["workspace"])
        self.imp_var = 1
        self.obj_appconfig.print_info(
            'Default workspace selected : ' +
            self.obj_appconfig.default_workspace["workspace"])
        self.close()

        var_appView.obj_Mainview.obj_projectExplorer.treewidget.clear()
        for parent, children in self.obj_appconfig.project_explorer.items():
            var_appView.obj_Mainview.obj_projectExplorer.addTreeNode(
                parent, children
            )

        time.sleep(1.5)
        var_appView.splash.close()
        var_appView.show()

    def close(self, *args, **kwargs):
        self.window_open_close = 1
        self.close_var = 1
        return QtWidgets.QWidget.close(self, *args, **kwargs)

    def returnWhetherClickedOrNot(self, appView):
        global var_appView
        var_appView = appView

    def createWorkspace(self):
        print("Function : Create workspace")

        self.obj_appconfig.workspace_check = self.chkbox.checkState()
        print(self.workspace_loc.text())
        file = open(os.path.join(
            os.path.expanduser("~"), ".esim/workspace.txt"), 'w'
        )
        file.writelines(
            str(self.obj_appconfig.workspace_check) +
            " " + self.workspace_loc.text()
        )
        file.close()

        self.create_workspace = str(self.workspace_loc.text())
        self.obj_appconfig.print_info('Workspace : ' + self.create_workspace)
        # Checking if Workspace already exist or not
        if os.path.isdir(self.create_workspace):
            self.obj_appconfig.default_workspace["workspace"] \
                = self.create_workspace
        else:
            os.mkdir(self.create_workspace)
            self.obj_appconfig.default_workspace["workspace"] \
                = self.create_workspace
        self.imp_var = 1
        self.close()

        self.obj_appconfig.dictPath["path"] = os.path.join(
            self.obj_appconfig.default_workspace["workspace"],
            ".projectExplorer.txt"
        )

        try:
            self.obj_appconfig.project_explorer = json.load(
                open(self.obj_appconfig.dictPath["path"])
            )
        except BaseException:
            self.obj_appconfig.project_explorer = {}

        Appconfig.project_explorer = self.obj_appconfig.project_explorer

        var_appView.obj_Mainview.obj_projectExplorer.treewidget.clear()
        for parent, children in self.obj_appconfig.project_explorer.items():
            var_appView.obj_Mainview.obj_projectExplorer.addTreeNode(
                parent, children
            )

        time.sleep(1.5)
        var_appView.splash.close()
        var_appView.show()

    def browseLocation(self):
        print("Function : Browse Location")
        self.workspace_directory = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Browse Location", os.path.expanduser("~")
        )
        self.workspace_loc.setText(self.workspace_directory)
