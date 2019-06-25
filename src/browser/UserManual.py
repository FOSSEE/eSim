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

        self.url = "../browser/pages/User-Manual/eSim.html"
        self.test = webbrowser.open(
            "../browser/pages/User-Manual/eSim.html", new=2)

        self.setLayout(self.vlayout)
        self.show()
