from PyQt5 import QtWidgets
from projManagement.Validation import Validation
from configuration.Appconfig import Appconfig
from projManagement import Worker
import os


# This class is called when User creates new Project.
class NewSub(QtWidgets.QWidget):
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

        init_path = '../../'
        if os.name == 'nt':
            init_path = ''

        self.create_schematic = subName
        # Checking if Workspace already exist or not
        self.schematic_path = (
            os.path.join(
                os.path.abspath(init_path + 'library'),
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
            print("Validated : Creating subcircuit directory")
            try:
                os.mkdir(self.schematic_path)
                self.schematic = os.path.join(
                    self.schematic_path, self.create_schematic)
                self.cmd = "eeschema " + self.schematic + ".sch"
                self.obj_workThread = Worker.WorkerThread(self.cmd)
                self.obj_workThread.start()
                self.close()
            except BaseException:
                self.msg = QtWidgets.QErrorMessage(self)
                self.msg.setModal(True)
                self.msg.setWindowTitle("Error Message")
                self.msg.showMessage(
                    'Unable to create subcircuit. Please make sure ' +
                    'you have write permission on ' + self.schematic_path
                )
                self.msg.exec_()

            self.obj_appconfig.current_subcircuit['SubcircuitName'] \
                = self.schematic_path

        elif self.reply == "CHECKEXIST":
            self.msg = QtWidgets.QErrorMessage(self)
            self.msg.setModal(True)
            self.msg.setWindowTitle("Error Message")
            self.msg.showMessage(
                'The subcircuit "' + self.create_schematic +
                '" already exist.Please select the different name or delete' +
                'existing subcircuit'
            )
            self.msg.exec_()

        elif self.reply == "CHECKNAME":
            self.msg = QtWidgets.QErrorMessage(self)
            self.msg.setModal(True)
            self.msg.setWindowTitle("Error Message")
            self.msg.showMessage(
                'The subcircuit name should not contain space between them'
            )
            self.msg.exec_()

        elif self.reply == "NONE":
            self.msg = QtWidgets.QErrorMessage(self)
            self.msg.setModal(True)
            self.msg.setWindowTitle("Error Message")
            self.msg.showMessage('The subcircuit name cannot be empty')
            self.msg.exec_()
