# =========================================================================
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
#  ORGANIZATION: eSim Team at FOSSEE, IIT Bombay
#       CREATED: Tuesday 24 February 2015
#      REVISION: Sunday 16 August 2020
# =========================================================================

from PyQt5 import QtCore, QtWidgets
import subprocess
from configuration.Appconfig import Appconfig


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
        self.my_workers = []

    def __del__(self):
        """
        __del__ is a called whenever garbage collection is initialised
        Here, it waits (self.wait()) for the thread to finish executing
        before garbage collecting it

        @params

        @return
            None
        """
        try:
            self.wait()
        except BaseException:
            pass

    def get_proc_threads(self):
        """
        This function is a getter for the list of project's workers,
        and is called to check if project's schematic is open or not.

        @params

        @return
            :self.my_workers
        """
        return self.my_workers

    def run(self):
        """
        run is the function that is called, when we start the thread as
        thisThread.start()
        Here, it makes system calls for all args passed (self.args)

        @params

        @return
            None
        """
        print("Worker Thread Calling Command :", self.args)
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
                        (see subprocess.Popen())
        """

        procThread = Appconfig()
        projDir = procThread.current_project["ProjectName"]

        if (projDir is None) and ('nghdl' not in command):
            msg = QtWidgets.QErrorMessage()
            msg.setModal(True)
            msg.setWindowTitle("Error Message")
            msg.showMessage(
                'Please select the project first. You can either ' +
                'create a new project or open an existing project.'
            )
            msg.exec_()

            return

        proc = subprocess.Popen(command.split())

        if 'nghdl' in command:
            return

        self.my_workers.append(proc)
        procThread.procThread_list.append(proc)
        procThread.proc_dict[procThread.current_project['ProjectName']].append(
            proc.pid)
