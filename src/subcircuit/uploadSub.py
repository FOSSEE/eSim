from PyQt4 import QtGui
from configuration.Appconfig import Appconfig
from projManagement.Validation import Validation
import os
import shutil


class UploadSub(QtGui.QWidget):
    """
    This class contain function for ulaoding subcircuits
    in Subcircuit library present in src folder.
        A folder is created in src/SubcircuitLibrary
    and desired file is moved to that folder.
    """

    def __init__(self):
        super(UploadSub, self).__init__()
        self.obj_validation = Validation()
        self.obj_appconfig = Appconfig()

    def upload(self):
        """
        This method opens a dialogue box when Upload subcircuit button is
        clicked and after entering folder name, it opens directory system
        to chose file for folder, it only shows file with extension .sub
        and with the name of project entered earlier as folder name.

            It then validates file if it is in proper format or not, for it
            the file is passed to the function **validateSub** and it returns
            true if file has valid format or else it shows an error message.
        """
        text, ok = QtGui.QInputDialog.getText(
            self, 'Subcircuit Info', 'Enter Subcircuit Name:')

        if ok:
            projname = (str(text))
            create_subcircuit = projname
            subcircuit_path = (os.path.join(os.path.abspath('..'), 'SubcircuitLibrary', create_subcircuit))

            if subcircuit_path == "":
                reply = "NONE"
            else:
                reply = self.obj_validation.validateNewproj(str(subcircuit_path))

            if reply == "VALID":
                print("Validated: Creating subcircuit directory")
                os.mkdir(subcircuit_path)
                editfile = str(
                    QtGui.QFileDialog.getOpenFileName(
                        None, "Upload File", os.path.expanduser("~"), (projname + ".sub")))

                upload = os.path.basename(editfile)
                print("===================")
                print("Current path of subcircuit file is " + editfile)
                print("===================")
                print("Selected file is " + upload)
                print("===================")
                self.valid = self.obj_validation.validateSubcir(str(editfile))
                print("===================")

                if self.valid is True:
                    print("Right file format!!!")
                    print("===================")
                    subcircuit = (os.path.join(subcircuit_path, upload))
                    print("Final path of file is " + subcircuit)
                    print("===================")
                    print("Copying file from " + editfile + " to " + subcircuit)
                    print("===================")
                    shutil.copy(editfile, subcircuit)
                else:
                    self.msg = QtGui.QErrorMessage(self)
                    self.msg.showMessage(
                        "Content of file does not meet the required format.\
                         Please make sure file starts with * .subckt \
                         " + upload + "** and ends with **.ends \
                         " + upload + "**")
                    self.msg.setWindowTitle("Error Message")
                    print("Invalid file format")
                    print("===================")
                    print("Removing directory " + subcircuit_path)
                    print("===================")
                    os.rmdir(subcircuit_path)

            elif reply == "CHECKEXIST":
                print("Project name already exists.")
                print("==========================")
                msg = QtGui.QErrorMessage(self)
                msg.showMessage(
                    "The project already exist. Please select  \
                    the different name or delete existing project")
                msg.setWindowTitle("Error Message")

            elif reply == "CHECKNAME":
                print("Name can not contain space between them")
                print("===========================")
                msg = QtGui.QErrorMessage(self)
                msg.showMessage(
                    'The project name should not contain space between them')
                msg.setWindowTitle("Error Message")
