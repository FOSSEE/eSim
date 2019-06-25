# =========================================================================
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
# =========================================================================
from PyQt4 import QtCore
import subprocess
from configuration.Appconfig import Appconfig
from utils.logger import logger


class WorkerThread(QtCore.QThread):
    """
    Initialise a QThread with the passed arguments
    WorkerThread uses QThread to support threading operations for
    other PyQT windows
    This is a helper functions, used to create threads for various commands


    @params
        :args   => takes a space separated string of comamnds to be execute
                   in different child processes (see subproces.Popen())

    @return
        None
    """

    def __init__(self, args):
        QtCore.QThread.__init__(self)
        self.args = args

    def __del__(self):
        """
        __del__ is a called whenever garbage collection is initialised
        Here, it waits (self.wait()) for the thread to finish executing
        before garbage collecting it

        @params

        @return
            None
        """
        self.wait()

    def run(self):
        """
        run is the function that is called, when we start the thread as
        thisThread.start()
        Here, it makes system calls for all args passed (self.args)

        @params

        @return
            None
        """
        logger.info("Worker Thread Calling Command :", self.args)
        self.call_system(self.args)

    def call_system(self, command):
        """
        call_system is used to create childprocess for the passed arguments
        (self.args) and also pass the process created and its id to config file
        Apponfig() object contains procThread and proc_dist used to
        track processes called

        @params
            :command    => (self.args) takes space separated string of\
                        comamnds to be executed in different child processes
                        (see subproces.Popen())
        """

        procThread = Appconfig()
        proc = subprocess.Popen(command.split())
        procThread.procThread_list.append(proc)
        procThread.proc_dict[procThread.current_project['ProjectName']].append(
            proc.pid)
