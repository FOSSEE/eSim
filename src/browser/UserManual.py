from PyQt6 import QtWidgets
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

        manual = 'library/browser/User-Manual/eSim_Manual_2.5.pdf'
        init_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")) + os.sep
        manual_path = os.path.join(init_path, manual)

        if os.name == 'nt':
            os.startfile(os.path.realpath(manual_path))
        else:
            import sys
            opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
            subprocess.Popen(
                [opener, os.path.realpath(manual_path)], shell=False
            )

        self.setLayout(self.vlayout)
        self.show()
