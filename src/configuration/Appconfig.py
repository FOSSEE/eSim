#===============================================================================
#
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
#  ORGANIZATION: eSim team at FOSSEE, IIT Bombay.
#       CREATED: Wednesday 04 February 2015 
#      REVISION:  ---
#===============================================================================


from PyQt4 import QtGui
import os
import json
from configparser import SafeConfigParser


class Appconfig(QtGui.QWidget):
        """
        All configuration goes here.
        May change in future for code optimization.
        """
        
        #Home directory
        home = os.path.join(os.path.expanduser("~"),"eSim-Workspace")
        default_workspace = {"workspace":home}
        #Current Project detail
        current_project = {"ProjectName":None}
        #Current Subcircuit detail
        current_subcircuit = {"SubcircuitName":None}
        #Workspace detail
        workspace_text = '''eSim stores your project in a folder called a eSim-Workspace. You can choose a different workspace folder to use for this session.'''
        procThread_list = []
        proc_dict={}	#holds the pids of all external windows corresponds to the current project
        dock_dict={}	#holds all dockwidgets
        dictPath = os.path.join(os.path.expanduser("~"), ".projectExplorer.txt")
        noteArea = {}

        parser_esim = SafeConfigParser()
        parser_esim.read(os.path.join(os.path.expanduser("~"), os.path.join('.esim','config.ini')))
        modelica_map_json = parser_esim.get('eSim', 'MODELICA_MAP_JSON')        
        try:
            project_explorer = json.load(open(dictPath))
        except:
            project_explorer= {}
        process_obj = []
        
        def __init__(self):
            super(Appconfig, self).__init__()
            #Application Details
            self._APPLICATION = 'eSim'
            self._VERSION = 'v1.1'
            self._AUTHOR = 'Fahim'
        
            #Application geometry setting
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
            
            
            
            
           
            
