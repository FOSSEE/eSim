from PyQt5 import QtWidgets
import subprocess
import os


class UserManual(QtWidgets.QWidget):
    """
    This class opens User-Manual page in new tab of web browser
    when help button is clicked.
    """

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.vlayout = QtWidgets.QVBoxLayout()

        manual = 'library/browser/User-Manual/eSim_Manual_2.4.pdf'

        if os.name == 'nt':
            os.startfile(os.path.realpath(manual))
        else:
            manual_path = '../../' + manual
            subprocess.Popen(
                ['xdg-open', os.path.realpath(manual_path)], shell=False
            )

        self.setLayout(self.vlayout)
        self.show()
