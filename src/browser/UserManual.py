from PyQt4 import QtGui, QtCore
import webbrowser

class UserManual(QtGui.QWidget):
    """
    This class creates Welcome page of eSim.
    """
    def __init__(self):
        QtGui.QWidget.__init__(self)
        
        self.vlayout = QtGui.QVBoxLayout()
        
        """
        self.browser = QtGui.QTextBrowser()
        self.browser.setSource(QtCore.QUrl("../browser/pages/User-Manual/eSim.html"))
        self.browser.setOpenExternalLinks(True)
        """
        
        self.url = "../browser/pages/User-Manual/eSim.html"
        self.test = webbrowser.open("../browser/pages/User-Manual/eSim.html",new=2)
                
        #self.vlayout.addWidget(self.browser)  
        self.setLayout(self.vlayout)
        self.show()