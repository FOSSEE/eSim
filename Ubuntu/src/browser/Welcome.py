from PyQt5 import QtCore, QtWidgets
import os
import sys


class Welcome(QtWidgets.QWidget):
    """
    This class contains content of dock area part of initial eSim Window.
    It creates Welcome page of eSim.
    """

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.vlayout = QtWidgets.QVBoxLayout()
        self.browser = QtWidgets.QTextBrowser()

        # Only this block is changed:
        # Point to welcome.html relative to the installed .exe location
        base_path = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
        html_path = os.path.abspath(os.path.join(base_path, "library/browser/welcome.html"))

        self.browser.setSource(QtCore.QUrl.fromLocalFile(html_path))
        self.browser.setOpenExternalLinks(True)
        self.browser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.vlayout.addWidget(self.browser)
        self.setLayout(self.vlayout)
        self.show()
