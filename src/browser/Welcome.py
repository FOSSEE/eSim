from PyQt4 import QtGui, QtCore


class Welcome(QtGui.QWidget):
    """This class contains content of dock area part of initial esim Window."""

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.vlayout = QtGui.QVBoxLayout()

        self.browser = QtGui.QTextBrowser()
        self.browser.setSource(QtCore.QUrl("../browser/pages/welcome.html"))
        self.browser.setOpenExternalLinks(True)
        self.browser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.vlayout.addWidget(self.browser)
        self.setLayout(self.vlayout)
        self.show()
