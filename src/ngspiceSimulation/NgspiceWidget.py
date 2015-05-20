from PyQt4 import QtGui,QtCore


class NgspiceWidget(QtGui.QWidget):
    """
    This Class creates NgSpice Window
    """
    def __init__(self,command):
        QtGui.QWidget.__init__(self)
        self.command = "ngspice "+command
        
        self.process = QtCore.QProcess(self)
        self.terminal = QtGui.QWidget(self)
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.addWidget(self.terminal)
        
        #Creating argument for process
        self.args = ['-into', str(self.terminal.winId()),'-hold','-e', self.command]
        self.process.start('xterm', self.args)
        
        
        
        



