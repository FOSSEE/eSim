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
#  ORGANIZATION: ecSim team at FOSSEE, IIT Bombay.
#       CREATED: Wednesday 04 February 2015 
#      REVISION:  ---
#===============================================================================


from PyQt4 import QtGui


class Appconfig(QtGui.QWidget):
        """
        All configuration goes here
        """
        def __init__(self):
            super(Appconfig, self).__init__()
            #Application Details
            self._APPLICATION = 'ecSim'
            self._VERSION = 'v1.1'
            self._AUTHOR = 'Fahim'
        
            #Application setting
            self.app_xpos = 100
            self.app_ypos = 100
            self.app_width = 600
            self.app_heigth = 400
            
            
            
            
           
            