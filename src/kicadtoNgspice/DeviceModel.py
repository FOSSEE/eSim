from PyQt4 import QtGui
import os
from xml.etree import ElementTree as ET

import TrackWidget


class DeviceModel(QtGui.QWidget):
    """
    This class creates Device Library  Tab in KicadtoNgspice Window
    It dynamically creates the widget for device like diode,mosfet,transistor and jfet.
    """
    
    def __init__(self,schematicInfo,clarg1):
        
        self.clarg1=clarg1
        kicadFile = self.clarg1
        (projpath,filename)=os.path.split(kicadFile)
        project_name=os.path.basename(projpath)
        check=1
        try:
            f=open(os.path.join(projpath,project_name+"_Previous_Values.xml"),'r')
            tree=ET.parse(f)
            parent_root=tree.getroot()
            for child in parent_root:
                if child.tag=="devicemodel":
                    root=child
        except:
            check=0
            print "Device Model Previous XML is Empty"
        
        
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
        self.devicemodel_dict_beg={}   
        self.devicemodel_dict_end={}           
        #List to hold information about device
        self.deviceDetail = {}
                
        #Set Layout
        self.grid = QtGui.QGridLayout()
        self.setLayout(self.grid)
        print "Reading Device model details from Schematic"
        
        for eachline in schematicInfo:
            words = eachline.split()
            if eachline[0] == 'q':
                print "Device Model Transistor: ",words[0]
                self.devicemodel_dict_beg[words[0]]=self.count
                transbox=QtGui.QGroupBox()
                transgrid=QtGui.QGridLayout()
                transbox.setTitle("Add library for Transistor "+words[0]+" : "+words[4])
                self.entry_var[self.count] = QtGui.QLineEdit()
                self.entry_var[self.count].setText("")
                global path_name
                try:
                    for child in root:
                        if child.tag[0]==eachline[0] and child.tag[1]==eachline[1]:
                            #print "DEVICE MODEL MATCHING---",child.tag[0],child.tag[1],eachline[0],eachline[1]
                            try:
                                if os.path.exists(child[0].text):
                                    self.entry_var[self.count].setText(child[0].text)
                                    path_name=child[0].text
                                else:
                                    self.entry_var[self.count].setText("")
                            except:
                                print "Error when set text of device model transistor"
                except:
                    pass
                transgrid.addWidget(self.entry_var[self.count],self.row,1)
                self.addbtn = QtGui.QPushButton("Add")
                self.addbtn.setObjectName("%d" %self.count)
                self.addbtn.clicked.connect(self.trackLibrary)
                self.deviceDetail[self.count] = words[0]
                if self.entry_var[self.count].text()=="":
                    pass
                else:
                    self.trackLibraryWithoutButton(self.count,path_name)
                transgrid.addWidget(self.addbtn,self.row,2)
                transbox.setLayout(transgrid)
                
                #CSS
                transbox.setStyleSheet(" \
                QGroupBox { border: 1px solid gray; border-radius: 9px; margin-top: 0.5em; } \
                QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; } \
                ")
                
                self.grid.addWidget(transbox)
                
                #Adding Device Details
                
                                
                #Increment row and widget count
                self.row = self.row+1
                self.devicemodel_dict_end[words[0]]=self.count
                self.count = self.count+1
                
            elif eachline[0] == 'd':
                print "Device Model Diode:",words[0]
                self.devicemodel_dict_beg[words[0]]=self.count
                diodebox=QtGui.QGroupBox()
                diodegrid=QtGui.QGridLayout()
                diodebox.setTitle("Add library for Diode "+words[0]+" : "+words[3])
                self.entry_var[self.count] = QtGui.QLineEdit()
                self.entry_var[self.count].setText("")
                #global path_name
                try:
                    for child in root:
                        if child.tag[0]==eachline[0] and child.tag[1]==eachline[1]:
                            #print "DEVICE MODEL MATCHING---",child.tag[0],child.tag[1],eachline[0],eachline[1]
                            try:
                                if os.path.exists(child[0].text):
                                    path_name=child[0].text
                                    self.entry_var[self.count].setText(child[0].text)
                                else:
                                    self.entry_var[self.count].setText("")
                            except:
                                print "Error when set text of device model diode"
                except:
                    pass
                diodegrid.addWidget(self.entry_var[self.count],self.row,1)
                self.addbtn = QtGui.QPushButton("Add")
                self.addbtn.setObjectName("%d" %self.count)
                self.addbtn.clicked.connect(self.trackLibrary)
                self.deviceDetail[self.count] = words[0]
                if self.entry_var[self.count].text()=="":
                    pass
                else:
                    self.trackLibraryWithoutButton(self.count,path_name)
                diodegrid.addWidget(self.addbtn,self.row,2)
                diodebox.setLayout(diodegrid)
                
                #CSS
                diodebox.setStyleSheet(" \
                QGroupBox { border: 1px solid gray; border-radius: 9px; margin-top: 0.5em; } \
                QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; } \
                ")
                
                self.grid.addWidget(diodebox)
                
                #Adding Device Details
                
                                
                #Increment row and widget count
                self.row = self.row+1
                self.devicemodel_dict_end[words[0]]=self.count
                self.count = self.count+1
                
            elif eachline[0] == 'j':
                print "Device Model JFET:",words[0]
                self.devicemodel_dict_beg[words[0]]=self.count
                jfetbox=QtGui.QGroupBox()
                jfetgrid=QtGui.QGridLayout()
                jfetbox.setTitle("Add library for JFET "+words[0]+" : "+words[4])
                self.entry_var[self.count] = QtGui.QLineEdit()
                self.entry_var[self.count].setText("")
                #global path_name
                try:
                    for child in root:
                        if child.tag[0]==eachline[0] and child.tag[1]==eachline[1]:
                            #print "DEVICE MODEL MATCHING---",child.tag[0],child.tag[1],eachline[0],eachline[1]
                            try:
                                if os.path.exists(child[0].text):
                                    self.entry_var[self.count].setText(child[0].text)
                                    path_name=child[0].text
                                else:
                                    self.entry_var[self.count].setText("")
                            except:
                                print "Error when set text of Device Model JFET "
                except:
                    pass
                jfetgrid.addWidget(self.entry_var[self.count],self.row,1)
                self.addbtn = QtGui.QPushButton("Add")
                self.addbtn.setObjectName("%d" %self.count)
                self.addbtn.clicked.connect(self.trackLibrary)
                self.deviceDetail[self.count] = words[0]
                if self.entry_var[self.count].text()=="":
                    pass
                else:
                    self.trackLibraryWithoutButton(self.count,path_name)
                jfetgrid.addWidget(self.addbtn,self.row,2)
                jfetbox.setLayout(jfetgrid)
                
                #CSS
                jfetbox.setStyleSheet(" \
                QGroupBox { border: 1px solid gray; border-radius: 9px; margin-top: 0.5em; } \
                QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; } \
                ")
                
                self.grid.addWidget(jfetbox)
                
                #Adding Device Details
                
                                
                #Increment row and widget count
                self.row = self.row+1
                self.devicemodel_dict_end[words[0]]=self.count
                self.count = self.count+1
                
                       
                
            elif eachline[0] == 'm':
                self.devicemodel_dict_beg[words[0]]=self.count
                mosfetbox=QtGui.QGroupBox()
                mosfetgrid=QtGui.QGridLayout()
                i=self.count
                beg=self.count
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
                end=self.count
                self.entry_var[self.count].setMaximumWidth(150)
                mosfetgrid.addWidget(self.entry_var[self.count],self.row,1)
                self.row = self.row + 1
                self.devicemodel_dict_end[words[0]]=self.count
                self.count = self.count+1
                mosfetbox.setLayout(mosfetgrid)
                #global path_name
                try:
                    for child in root:
                        if child.tag[0]==eachline[0] and child.tag[1]==eachline[1]:
                            #print "DEVICE MODEL MATCHING---",child.tag[0],child.tag[1],eachline[0],eachline[1]
                            while i<=end:
                                self.entry_var[i].setText(child[i-beg].text)
                                if (i-beg)==0:
                                    if os.path.exists(child[0].text):
                                        self.entry_var[i].setText(child[i-beg].text)
                                        path_name=child[i-beg].text
                                    else:
                                        self.entry_var[i].setText("")
                                i=i+1
                except:
                    pass
                #CSS
                mosfetbox.setStyleSheet(" \
                QGroupBox { border: 1px solid gray; border-radius: 9px; margin-top: 0.5em; } \
                QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; } \
                ")
                if self.entry_var[beg].text()=="":
                    pass
                else:
                    self.trackLibraryWithoutButton(beg,path_name)
                self.grid.addWidget(mosfetbox)
                
                   
            self.show()
        
                  
    def trackLibrary(self):
        """
        This function is use to keep track of all Device Model widget
        """
        print "Calling Track Device Model Library funtion"
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
    def trackLibraryWithoutButton(self,iter_value,path_value):
        """
        This function is use to keep track of all Device Model widget
        """
        print "Calling Track Library function Without Button"
        #print "Object Called is ",sending_btn.objectName()
        self.widgetObjCount = iter_value
        print "self.widgetObjCount-----",self.widgetObjCount
        self.libfile = path_value
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
    
