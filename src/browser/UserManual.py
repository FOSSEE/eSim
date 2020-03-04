from PyQt4 import QtGui
import subprocess
import platform
import os


class UserManual(QtGui.QWidget):
    """
    This class opens User-Manual page in new tab of web browser
    when help button is clicked.
    """

    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.vlayout = QtGui.QVBoxLayout()

        file = os.path.realpath(
            'library/browser/User-Manual/eSim_Manual_2019_Dec_31.pdf'
        )

        if 'Win' in platform.system():
            os.startfile(file)
        else:
            subprocess.Popen(['xpdf.real', file], shell=False)

        self.setLayout(self.vlayout)
        self.show()
