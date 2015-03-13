from PyQt4 import QtGui



class TabbedWidget(QtGui.QTabWidget):
    def __init__(self):
        QtGui.QTabWidget.__init__(self)
        self.setGeometry(300, 300, 600, 600)
        self.setWindowTitle('Kicad to Ngspice conversion')
