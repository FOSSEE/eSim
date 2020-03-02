from PyQt4 import QtGui
import webbrowser


class UserManual(QtGui.QWidget):
    """
    This class opens User-Manual page in new tab of web browser
    when help button is clicked.
    """

    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.vlayout = QtGui.QVBoxLayout()

        self.url = "library/browser/User-Manual/eSim_Manual_2019_Dec_31.pdf"
        self.test = webbrowser.open(
            "library/browser/User-Manual/eSim_Manual_2019_Dec_31.pdf", new=2)

        self.setLayout(self.vlayout)
        self.show()
