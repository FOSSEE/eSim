from PyQt5 import QtCore, QtWidgets
import os
import sys
from esim_paths import resource_path  # ← add this import

class Welcome(QtWidgets.QWidget):
    """
    This class contains content of dock area part of initial eSim Window.
    It creates Welcome page of eSim.
    """
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.vlayout = QtWidgets.QVBoxLayout()
        self.browser = QtWidgets.QTextBrowser()

        html_path = resource_path('library', 'browser', 'welcome.html')  # ← clean one-liner
        self.browser.setSource(QtCore.QUrl.fromLocalFile(html_path))
        self.browser.setOpenExternalLinks(True)
        self.browser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.vlayout.addWidget(self.browser)
        self.setLayout(self.vlayout)
        self.show()