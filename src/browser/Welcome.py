from PyQt5 import QtCore, QtWidgets
import os


class Welcome(QtWidgets.QWidget):
    """
    It contains class responsible for content of dock area part of initial esim Window.
    It creates Welcome page of eSim as shown below in image. The library/browser/welcome.html file is used for html content.
    """

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.vlayout = QtWidgets.QVBoxLayout()
        self.browser = QtWidgets.QTextBrowser()

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
