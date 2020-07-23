from PyQt4 import QtGui, QtCore
import os


class Welcome(QtGui.QWidget):
    """
    This class contains content of dock area part of initial esim Window.
    It creates Welcome page of eSim.
    """

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.vlayout = QtGui.QVBoxLayout()
        self.browser = QtGui.QTextBrowser()

        init_path = '../../'
        if os.name == 'nt':
            init_path = ''

        self.browser.setSource(QtCore.QUrl(
            init_path + "library/browser/welcome.html")
        )
        self.browser.setOpenExternalLinks(True)
        self.browser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.vlayout.addWidget(self.browser)
        self.setLayout(self.vlayout)
        self.show()
