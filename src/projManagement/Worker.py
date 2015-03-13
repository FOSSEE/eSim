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
import os


class WorkerThread(QtCore.QThread):
    def __init__(self,args):
        QtCore.QThread.__init__(self)
        self.args = args
    
    def __del__(self):
        self.wait()
        
    def run(self):
        print "Calling :",self.args
        self.call_system(self.args)
        
    def call_system(self,command):
        print "System called"
        os.system(command)
    
    