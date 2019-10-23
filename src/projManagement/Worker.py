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
#      MODIFIED: Rahul Paknikar, rahulp@iitb.ac.in
#  ORGANIZATION: eSim team at FOSSEE, IIT Bombay.
#       CREATED: Tuesday 24 Feb 2015
#      REVISION: Thursday 3 Oct 2019
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
        self.my_workers = []
        
    def __del__(self):
        self.wait()

    def get_proc_threads(self):
        return self.my_workers
          
    def run(self):
        print "Worker Thread Calling Command :",self.args
        self.call_system(self.args)
        
    def call_system(self,command):
        procThread = Appconfig()
        proc = subprocess.Popen(command.split())
        self.my_workers.append(proc)
        procThread.procThread_list.append(proc)
	procThread.proc_dict[procThread.current_project['ProjectName']].append(proc.pid)
        
        
    
    
