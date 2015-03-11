
from PyQt4 import QtGui,QtCore
#import GroupBox

class Analysis(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        
        self.grid = QtGui.QGridLayout(self)
        self.grid.addWidget(self.createACgroup(),0,0)
        self.grid.addWidget(self.createDCgroup(),1,0)
        self.grid.addWidget(self.createTRANgroup(),2,0)
        
        self.setLayout(self.grid)
        self.show()
        
        
                
    def createACgroup(self):
        self.acbox = QtGui.QGroupBox()
        self.acbox.setTitle("AC")
        
        self.acgrid = QtGui.QGridLayout()
        
        self.btn1 = QtGui.QRadioButton("Radio button 1")
        self.btn2 = QtGui.QRadioButton("Radio button 2")
        self.acgrid.addWidget(self.btn1,0,0)
        self.acgrid.addWidget(self.btn2,0,1)
             
        self.acbox.setStyleSheet(" \
        QGroupBox { border: 1px solid gray; border-radius: 9px; margin-top: 0.5em; } \
        QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; } \
        ")
        
         
        self.acbox.setLayout(self.acgrid)
        
        return self.acbox
    
    def createDCgroup(self):
        self.dcbox = QtGui.QGroupBox()
        self.dcbox.setTitle("DC")
        self.dcgrid = QtGui.QGridLayout()
        
        self.btn3 = QtGui.QRadioButton("Radio button 3")
        self.btn4 = QtGui.QRadioButton("Radio button 4")
        self.dcgrid.addWidget(self.btn3,0,0)
        self.dcgrid.addWidget(self.btn4,0,1)
        
        self.dcbox.setStyleSheet(" \
        QGroupBox { border: 1px solid gray; border-radius: 9px; margin-top: 0.5em; } \
        QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; } \
        ")
        
        self.dcbox.setLayout(self.dcgrid)
        
        return self.dcbox
    
    def createTRANgroup(self):
        self.trbox = QtGui.QGroupBox()
        self.trbox.setTitle("DC")
        self.trgrid = QtGui.QGridLayout()
        
        self.btn5 = QtGui.QRadioButton("Radio button 5")
        self.btn6 = QtGui.QRadioButton("Radio button 6")
        self.trgrid.addWidget(self.btn5,0,0)
        self.trgrid.addWidget(self.btn6,0,1)
        
        self.trbox.setStyleSheet(" \
        QGroupBox { border: 1px solid gray; border-radius: 9px; margin-top: 0.5em; } \
        QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; } \
        ")
        
        self.trbox.setLayout(self.trgrid)
        
        return self.trbox