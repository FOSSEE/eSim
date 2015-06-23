from PyQt4 import QtGui

import TrackWidget
from projManagement import Validation


class SubcircuitTab(QtGui.QWidget):
    """
    This class creates Subcircuit Tab in KicadtoNgspice Window
    It dynamically creates the widget for subcircuits.
    """
    
    def __init__(self,schematicInfo):
        QtGui.QWidget.__init__(self)
                     
        #Creating track widget object
        self.obj_trac = TrackWidget.TrackWidget()
        
        #Creating validation object
        self.obj_validation = Validation.Validation()
        #Row and column count
        self.row = 0
        self.count = 1  #Entry count
        self.entry_var = {}
        
        #List to hold information about device
        self.subDetail = {}
        
        #Stores the number of ports in each subcircuit
        self.numPorts = []
                
        #Set Layout
        self.grid = QtGui.QGridLayout()
        self.setLayout(self.grid)
        
        for eachline in schematicInfo:
            words = eachline.split()
            if eachline[0] == 'x':
                print "Words",words[0]
                self.obj_trac.subcircuitList.append(words)
                subbox=QtGui.QGroupBox()
                subgrid=QtGui.QGridLayout()
                subbox.setTitle("Add subcircuit for "+words[len(words)-1])
                self.entry_var[self.count] = QtGui.QLineEdit()
                self.entry_var[self.count].setText("")
                subgrid.addWidget(self.entry_var[self.count],self.row,1)
                self.addbtn = QtGui.QPushButton("Add")
                self.addbtn.setObjectName("%d" %self.count)
                #Send the number of ports specified with the given subcircuit for verification.
                #eg. If the line is 'x1 4 0 3 ua741', there are 3 ports(4, 0 and 3).
                self.numPorts.append(len(words)-2)
                print "NUMPORTS",self.numPorts
                self.addbtn.clicked.connect(self.trackSubcircuit)
                subgrid.addWidget(self.addbtn,self.row,2)
                subbox.setLayout(subgrid)
                
                #CSS
                subbox.setStyleSheet(" \
                QGroupBox { border: 1px solid gray; border-radius: 9px; margin-top: 0.5em; } \
                QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; } \
                ")
                
                self.grid.addWidget(subbox)
                
                #Adding Device Details
                self.subDetail[self.count] = words[0]
                                
                #Increment row and widget count
                self.row = self.row+1
                self.count = self.count+1
                   
            self.show()
        
                  
    def trackSubcircuit(self):
        """
        This function is use to keep track of all Device Model widget
        """
        print "Calling Track Subcircuit function"
        sending_btn = self.sender()
        #print "Object Called is ",sending_btn.objectName()
        self.widgetObjCount = int(sending_btn.objectName())
        
        self.subfile = str(QtGui.QFileDialog.getExistingDirectory(self,"Open Subcircuit","../SubcircuitLibrary"))
        self.reply = self.obj_validation.validateSub(self.subfile,self.numPorts[self.widgetObjCount - 1])
        if self.reply == "True":
            #Setting Library to Text Edit Line
            self.entry_var[self.widgetObjCount].setText(self.subfile)
            self.subName = self.subDetail[self.widgetObjCount]
            
            #Storing to track it during conversion
            
            self.obj_trac.subcircuitTrack[self.subName] = self.subfile
        elif self.reply == "PORT":
            self.msg = QtGui.QErrorMessage(self)
            self.msg.showMessage("Please select a Subcircuit with correct number of ports.")
            self.msg.setWindowTitle("Error Message")
            self.msg.show()
        elif self.reply == "DIREC":
            self.msg = QtGui.QErrorMessage(self)
            self.msg.showMessage("Please select a valid Subcircuit directory (Containing '.sub' file).")
            self.msg.setWindowTitle("Error Message")
            self.msg.show()