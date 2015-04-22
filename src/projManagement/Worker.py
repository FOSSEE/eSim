#===============================================================================
#
#          FILE: WorkerThread.py
# 
#         USAGE: --- 
# 
#   DESCRIPTION: This class open all third party application using QT Thread
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Fahim Khan, fahim.elex@gmail.com
#  ORGANIZATION: eSim team at FOSSEE, IIT Bombay.
#       CREATED: Tuesday 24 Feb 2015 
#      REVISION:  ---
#===============================================================================
from PyQt4 import QtCore
import subprocess
from configuration.Appconfig import Appconfig


class WorkerThread(QtCore.QThread):
    """
    This is Thread class use to run the command
    """
    def __init__(self,args):
        QtCore.QThread.__init__(self)
        self.args = args
    
    def __del__(self):
        self.wait()
        
        
    def run(self):
        print "Calling Command:",self.args
        self.call_system(self.args)
        
    def call_system(self,command):
        procThread = Appconfig()
        proc = subprocess.Popen(command.split())
        procThread.procThread_list.append(proc)
        
    
    