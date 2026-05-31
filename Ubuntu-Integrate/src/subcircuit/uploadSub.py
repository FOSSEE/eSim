from PyQt5 import QtWidgets, QtCore
from configuration.Appconfig import Appconfig
from projManagement.Validation import Validation
import os
import shutil


class UploadSub(QtWidgets.QWidget):
    """
    This class contain function for uploading subcircuits
    in SubcircuitLibrary present in src folder.
    A folder is created in library/SubcircuitLibrary
    and desired file is moved to that folder.
    """

    def __init__(self):
        super(UploadSub, self).__init__()
        self.obj_validation = Validation()
        self.obj_appconfig = Appconfig()

    def upload(self):
        """
        This method opens a dialog box when Upload subcircuit button is
        clicked and after entering folder name, it opens directory system
        to chose file for folder, it only shows file with extension .sub
        and with the name of project entered earlier as folder name.

            It then validates file if it is in proper format or not, for it
            the file is passed to the function **validateSub** and it returns
            true if file has valid format or else it shows an error message.
        """

        editfile = QtCore.QDir.toNativeSeparators(
            QtWidgets.QFileDialog.getOpenFileName(
                None, "Upload Subcircuit File",
                os.path.expanduser("~"), "*.sub"
            )[0]
        )

        if not editfile:
            return

        upload = os.path.basename(editfile)
        create_subcircuit, ext = os.path.splitext(upload)

        if ext != '.sub':
            self.msg = QtWidgets.QErrorMessage(self)
            self.msg.setModal(True)
            self.msg.setWindowTitle("Error Message")
            self.msg.showMessage("Please ensure that filename ends with .sub")
            self.msg.exec_()
            print("Invalid filename")
            return

        valid = self.obj_validation.validateSubcir(editfile, create_subcircuit)
        if not valid:
            self.msg = QtWidgets.QErrorMessage(self)
            self.msg.setModal(True)
            self.msg.setWindowTitle("Error Message")
            self.msg.showMessage(
                "Content of file does not meet the required format. " +
                "Please ensure that file starts with **.subckt " +
                create_subcircuit + " ** and ends with **.ends " +
                create_subcircuit + " **"
            )
            self.msg.exec_()
            print("Invalid file format")
            return

        init_path = '../../'
        if os.name == 'nt':
            init_path = ''

        subcircuit_path = os.path.join(
            os.path.abspath(init_path + 'library'),
            'SubcircuitLibrary', create_subcircuit
        )

        reply = self.obj_validation.validateNewproj(subcircuit_path)

        if reply == "VALID":
            print("Validated: Creating subcircuit directory")
            os.makedirs(subcircuit_path)
            subcircuit = os.path.join(subcircuit_path, upload)

            print("===================")
            print("Current path of subcircuit file is " + editfile)
            print("Selected file is " + upload)
            print("Final path of file is " + subcircuit)
            print("===================")
            shutil.copy(editfile, subcircuit)

        elif reply == "CHECKEXIST":
            print("Project name already exists.")
            print("==========================")
            msg = QtWidgets.QErrorMessage(self)
            msg.setModal(True)
            msg.setWindowTitle("Error Message")
            msg.showMessage(
                "The project already exist. Please select "
                "a different name or delete existing project")
            msg.exec_()

        elif reply == "CHECKNAME":
            print("Name can not contain space between them")
            print("===========================")
            msg = QtWidgets.QErrorMessage(self)
            msg.setModal(True)
            msg.setWindowTitle("Error Message")
            msg.showMessage(
                'The project name should not contain space between them')
            msg.exec_()
