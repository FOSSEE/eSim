# =========================================================================
#          FILE: Appconfig.py
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
#  ORGANIZATION: eSim team at FOSSEE, IIT Bombay.
#       CREATED: Tuesday 24 February 2015
#      REVISION: Friday 14 February 2020
# =========================================================================

from PyQt4 import QtGui
import os
import json
from configparser import SafeConfigParser


class Appconfig(QtGui.QWidget):
    """
    All configuration goes here.
    May change in future for code optimization.

    This class also contains function for
    - Printing error.
    - Showing warnings.
    - Displaying information.
    """

    # Home directory
    home = os.path.join(os.path.expanduser("~"), "eSim-Workspace")
    default_workspace = {"workspace": home}
    # Current Project detail
    current_project = {"ProjectName": None}
    # Current Subcircuit detail
    current_subcircuit = {"SubcircuitName": None}
    # Workspace detail
    workspace_text = "eSim stores your project in a folder called "
    workspace_text += "eSim-Workspace. You can choose a different "
    workspace_text += "workspace folder to use for this session."
    procThread_list = []
    proc_dict = {}
    # holds the pids of all external windows corresponds to the current project
    dock_dict = {}  # holds all dockwidgets
    dictPath = os.path.join(os.path.expanduser("~"), ".projectExplorer.txt")
    noteArea = {}

    parser_esim = SafeConfigParser()
    parser_esim.read(
        os.path.join(
            os.path.expanduser("~"),
            os.path.join(
                '.esim',
                'config.ini')))

    # Try catch added, since eSim cannot be accessed under parser for Win10
    try:
        modelica_map_json = parser_esim.get('eSim', 'MODELICA_MAP_JSON')
    except BaseException as e:
        print("===============================================")
        print("Cannot access Modelica map file --- .esim folder")
        print(str(e))
        print("===============================================")

    # Open file and read KiCad config path
    try:
        file = open('../supportFiles/kicad_config_path.txt', 'r')
        kicad_path = file.read().rstrip()
        file.close()
    except BaseException as e:
        kicad_path = None
        print("===============================================")
        print("Cannot access kicad path file --- supportFiles")
        print(str(e))
        print("===============================================")

    try:
        project_explorer = json.load(open(dictPath))
    except BaseException:
        project_explorer = {}
    process_obj = []

    def __init__(self):
        super(Appconfig, self).__init__()
        # Application Details
        self._APPLICATION = 'eSim'
        self._VERSION = 'v2.0.0'
        self._AUTHOR = 'Fahim, Rahul'

        # Application geometry setting
        self._app_xpos = 100
        self._app_ypos = 100
        self._app_width = 600
        self._app_heigth = 400

    def print_info(self, info):
        self.noteArea['Note'].append('[INFO]: ' + info)

    def print_warning(self, warning):
        self.noteArea['Note'].append('[WARNING]: ' + warning)

    def print_error(self, error):
        self.noteArea['Note'].append('[ERROR]: ' + error)
