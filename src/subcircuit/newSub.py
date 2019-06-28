from PyQt4 import QtGui
from projManagement.Validation import Validation
from configuration.Appconfig import Appconfig
from projManagement import Worker
import os
from utils.logger import logger

# This class is called when User create new Project.


class NewSub(QtGui.QWidget):
    """
    Contains functions to check :
    - Name of project should not be blank.
    - Name should not contain space between them.
    - Name does not match with existing project.
    """

    def __init__(self):
        super(NewSub, self).__init__()
        self.obj_validation = Validation()
        self.obj_appconfig = Appconfig()

    def createSubcircuit(self, subName):
        """
        - This function create workspace for subcircuit.
        - It also validate file names for Subcircuits:
            - File name should not contain space.
            - Name can not be empty.
            - File name already exists.
        """
        self.create_schematic = subName
        # Checking if Workspace already exist or not
        self.schematic_path = (
            os.path.join(
                os.path.abspath('..'),
                'SubcircuitLibrary',
                self.create_schematic))

        # Validation for new subcircuit
        if self.schematic_path == "":
            self.reply = "NONE"
        else:
            self.reply = self.obj_validation.validateNewproj(
                str(self.schematic_path))

        # Checking Validations Response
        if self.reply == "VALID":
            logger.info("Validated : Creating subcircuit directory")
            try:
                os.mkdir(self.schematic_path)
                self.schematic = os.path.join(
                    self.schematic_path, self.create_schematic)
                self.cmd = "eeschema " + self.schematic + ".sch"
                self.obj_workThread = Worker.WorkerThread(self.cmd)
                self.obj_workThread.start()
                self.close()
            except BaseException:
                # print "Some Thing Went Wrong"
                self.msg = QtGui.QErrorMessage(self)
                self.msg.showMessage(
                    'Unable to create subcircuit. Please make sure\
                     you have write permission on ' +
                    self.schematic_path)
                self.msg.setWindowTitle("Error Message")

            self.obj_appconfig.current_subcircuit['SubcircuitName'] \
                = self.schematic_path

        elif self.reply == "CHECKEXIST":
            # print "Project already exist"
            self.msg = QtGui.QErrorMessage(self)
            self.msg.showMessage(
                'The subcircuit "' +
                self.create_schematic +
                '" already exist.Please select the different name or delete'
                + 'existing subcircuit')
            self.msg.setWindowTitle("Error Message")

        elif self.reply == "CHECKNAME":
            # print "Name is not proper"
            self.msg = QtGui.QErrorMessage(self)
            self.msg.showMessage(
                'The subcircuit name should not contain space between them')
            self.msg.setWindowTitle("Error Message")

        elif self.reply == "NONE":
            self.msg = QtGui.QErrorMessage(self)
            self.msg.showMessage('The subcircuit name cannot be empty')
            self.msg.setWindowTitle("Error Message")
