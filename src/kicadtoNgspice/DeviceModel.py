from PyQt4 import QtGui

import TrackWidget


class DeviceModel(QtGui.QWidget):
    """
    This class creates Device Library  Tab in KicadtoNgspice Window
    It dynamically creates the widget for device like diode,mosfet,transistor and jfet.
    """
    
    def __init__(self,schematicInfo):
        QtGui.QWidget.__init__(self)
                     
        #Creating track widget object
        self.obj_trac = TrackWidget.TrackWidget()
        
        #Row and column count
        self.row = 0
        self.count = 1  #Entry count
        self.entry_var = {}
                
        #For MOSFET
        self.widthLabel = {}
        self.lengthLabel = {}
        self.multifactorLable = {}
              
        
        #List to hold information about device
        self.deviceDetail = {}
                
        #Set Layout
        self.grid = QtGui.QGridLayout()
        self.setLayout(self.grid)
        
        for eachline in schematicInfo:
            words = eachline.split()
            if eachline[0] == 'q':
                print "Words ",words[0]
                transbox=QtGui.QGroupBox()
                transgrid=QtGui.QGridLayout()
                transbox.setTitle("Add library for Transistor "+words[0]+" : "+words[4])
                self.entry_var[self.count] = QtGui.QLineEdit()
                self.entry_var[self.count].setText("")
                transgrid.addWidget(self.entry_var[self.count],self.row,1)
                self.addbtn = QtGui.QPushButton("Add")
                self.addbtn.setObjectName("%d" %self.count)
                self.addbtn.clicked.connect(self.trackLibrary)
                transgrid.addWidget(self.addbtn,self.row,2)
                transbox.setLayout(transgrid)
                
                #CSS
                transbox.setStyleSheet(" \
                QGroupBox { border: 1px solid gray; border-radius: 9px; margin-top: 0.5em; } \
                QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; } \
                ")
                
                self.grid.addWidget(transbox)
                
                #Adding Device Details
                self.deviceDetail[self.count] = words[0]
                                
                #Increment row and widget count
                self.row = self.row+1
                self.count = self.count+1
                
            elif eachline[0] == 'd':
                print "Words",words[0]
                diodebox=QtGui.QGroupBox()
                diodegrid=QtGui.QGridLayout()
                diodebox.setTitle("Add library for Diode "+words[0]+" : "+words[3])
                self.entry_var[self.count] = QtGui.QLineEdit()
                self.entry_var[self.count].setText("")
                diodegrid.addWidget(self.entry_var[self.count],self.row,1)
                self.addbtn = QtGui.QPushButton("Add")
                self.addbtn.setObjectName("%d" %self.count)
                self.addbtn.clicked.connect(self.trackLibrary)
                diodegrid.addWidget(self.addbtn,self.row,2)
                diodebox.setLayout(diodegrid)
                
                #CSS
                diodebox.setStyleSheet(" \
                QGroupBox { border: 1px solid gray; border-radius: 9px; margin-top: 0.5em; } \
                QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; } \
                ")
                
                self.grid.addWidget(diodebox)
                
                #Adding Device Details
                self.deviceDetail[self.count] = words[0]
                                
                #Increment row and widget count
                self.row = self.row+1
                self.count = self.count+1
                
            elif eachline[0] == 'j':
                print "Words",words[0]
                jfetbox=QtGui.QGroupBox()
                jfetgrid=QtGui.QGridLayout()
                jfetbox.setTitle("Add library for JFET "+words[0]+" : "+words[4])
                self.entry_var[self.count] = QtGui.QLineEdit()
                self.entry_var[self.count].setText("")
                jfetgrid.addWidget(self.entry_var[self.count],self.row,1)
                self.addbtn = QtGui.QPushButton("Add")
                self.addbtn.setObjectName("%d" %self.count)
                self.addbtn.clicked.connect(self.trackLibrary)
                jfetgrid.addWidget(self.addbtn,self.row,2)
                jfetbox.setLayout(jfetgrid)
                
                #CSS
                jfetbox.setStyleSheet(" \
                QGroupBox { border: 1px solid gray; border-radius: 9px; margin-top: 0.5em; } \
                QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; } \
                ")
                
                self.grid.addWidget(jfetbox)
                
                #Adding Device Details
                self.deviceDetail[self.count] = words[0]
                                
                #Increment row and widget count
                self.row = self.row+1
                self.count = self.count+1
                
                       
                
            elif eachline[0] == 'm':
                mosfetbox=QtGui.QGroupBox()
                mosfetgrid=QtGui.QGridLayout()
                mosfetbox.setTitle("Add library for MOSFET "+words[0]+" : "+words[5])
                self.entry_var[self.count] =QtGui.QLineEdit()
                self.entry_var[self.count].setText("")
                mosfetgrid.addWidget(self.entry_var[self.count],self.row,1)
                self.addbtn = QtGui.QPushButton("Add")
                self.addbtn.setObjectName("%d" %self.count)
                self.addbtn.clicked.connect(self.trackLibrary)
                mosfetgrid.addWidget(self.addbtn,self.row,2)
                
                #Adding Device Details
                self.deviceDetail[self.count] = words[0]
                                
                #Increment row and widget count
                self.row = self.row+1
                self.count = self.count+1
                
                #Adding to get MOSFET dimension                
                self.widthLabel[self.count] = QtGui.QLabel("Enter width of MOSFET "+words[0]+"(default=100u):")
                mosfetgrid.addWidget(self.widthLabel[self.count],self.row,0)
                self.entry_var[self.count] = QtGui.QLineEdit()
                self.entry_var[self.count].setText("")
                self.entry_var[self.count].setMaximumWidth(150)
                mosfetgrid.addWidget(self.entry_var[self.count],self.row,1)
                self.row = self.row + 1
                self.count = self.count+1
                
                self.lengthLabel[self.count] = QtGui.QLabel("Enter length of MOSFET "+words[0]+"(default=100u):")
                mosfetgrid.addWidget(self.lengthLabel[self.count],self.row,0)
                self.entry_var[self.count] = QtGui.QLineEdit()
                self.entry_var[self.count].setText("")
                self.entry_var[self.count].setMaximumWidth(150)
                mosfetgrid.addWidget(self.entry_var[self.count],self.row,1)
                self.row = self.row + 1
                self.count = self.count+1
                
                
                self.multifactorLable[self.count] = QtGui.QLabel("Enter multiplicative factor of MOSFET "+words[0]+"(default=1):")
                mosfetgrid.addWidget(self.multifactorLable[self.count],self.row,0)
                self.entry_var[self.count] = QtGui.QLineEdit()
                self.entry_var[self.count].setText("")
                self.entry_var[self.count].setMaximumWidth(150)
                mosfetgrid.addWidget(self.entry_var[self.count],self.row,1)
                self.row = self.row + 1
                self.count = self.count+1
                mosfetbox.setLayout(mosfetgrid)
                
                #CSS
                mosfetbox.setStyleSheet(" \
                QGroupBox { border: 1px solid gray; border-radius: 9px; margin-top: 0.5em; } \
                QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; } \
                ")
                
                self.grid.addWidget(mosfetbox)
                   
            self.show()
        
                  
    def trackLibrary(self):
        """
        This function is use to keep track of all Device Model widget
        """
        print "Calling Track Library funtion"
        sending_btn = self.sender()
        #print "Object Called is ",sending_btn.objectName()
        self.widgetObjCount = int(sending_btn.objectName())
        
        self.libfile = str(QtGui.QFileDialog.getOpenFileName(self,"Open Library Directory","../deviceModelLibrary","*.lib"))
        #print "Selected Library File :",self.libfile
        
        #Setting Library to Text Edit Line
        self.entry_var[self.widgetObjCount].setText(self.libfile)
        self.deviceName = self.deviceDetail[self.widgetObjCount]
        
        #Storing to track it during conversion
        
        
        if self.deviceName[0] == 'm':
            width = str(self.entry_var[self.widgetObjCount+1].text())
            length = str(self.entry_var[self.widgetObjCount+2].text())
            multifactor = str(self.entry_var[self.widgetObjCount+3].text())
            if width == "" : width="100u"
            if length == "": length="100u"
            if multifactor == "": multifactor="1"
                
            self.obj_trac.deviceModelTrack[self.deviceName] = self.libfile+":"+"W="+width+" L="+length+" M="+multifactor
            
        else:
            self.obj_trac.deviceModelTrack[self.deviceName] = self.libfile
        
        
        