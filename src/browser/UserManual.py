from PyQt4 import QtGui
import subprocess
import os


class UserManual(QtGui.QWidget):
    """
    This class opens User-Manual page in new tab of web browser
    when help button is clicked.
    """

    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.vlayout = QtGui.QVBoxLayout()

        manual = 'library/browser/User-Manual/eSim_Manual_2.1.pdf'

        if os.name == 'nt':
            os.startfile(os.path.realpath(manual))
        else:
            manual_path = '../../' + manual
            subprocess.Popen(
                ['xdg-open', os.path.realpath(manual_path)], shell=False
            )

        self.setLayout(self.vlayout)
        self.show()
