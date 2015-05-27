
from PyQt4 import QtGui
from Processing import PrcocessNetlist
import TrackWidget


class Source(QtGui.QWidget):
    """
    This class create Source Tab of KicadtoNgSpice Window.
    """
        
    def __init__(self,sourcelist,sourcelisttrack):
        QtGui.QWidget.__init__(self)
        print "My Net List ",sourcelist
        self.obj_track = TrackWidget.TrackWidget()     
        #Variable
        self.count = 1
        self.start = 0
        self.end = 0
        self.row = 0
        self.entry_var = {}
        #self.font = QtGui.QFont("Times",20,QtGui.QFont.Bold,True)
        
        #Creating Source Widget
        self.createSourceWidget(sourcelist,sourcelisttrack)
        
           
        
    def createSourceWidget(self,sourcelist,sourcelisttrack):
        """
        This function dynamically create source widget in the Source tab of KicadtoNgSpice window
        """
                
        self.grid = QtGui.QGridLayout()
        self.setLayout(self.grid)
        
        if sourcelist:
            for line in sourcelist:
                #print "Voltage source line index: ",line[0]
                #print "SourceList line Test: ",line
                track_id=line[0]
                #print "track_id is ",track_id
                if line[2]=='ac':
                    acbox=QtGui.QGroupBox()
                    acbox.setTitle(line[3])
                    acgrid=QtGui.QGridLayout()
                    """
                    label=QtGui.QLabel(line[3])
                    self.grid.addWidget(label,self.row,1)
                    self.row=self.row+1
                    self.start=self.count
                    """
                    label=QtGui.QLabel(line[4])
                    acgrid.addWidget(label,self.row,0)
                    self.entry_var[self.count]=QtGui.QLineEdit()
                    self.entry_var[self.count].setMaximumWidth(150)
                    acgrid.addWidget(self.entry_var[self.count],self.row,1)
                    #Value Need to check previuouse value
                    self.entry_var[self.count].setText("")
                    self.row=self.row+1
                    self.end=self.count
                    self.count=self.count+1
                    
                    acbox.setLayout(acgrid)
                    
                    #CSS
                    acbox.setStyleSheet(" \
                    QGroupBox { border: 1px solid gray; border-radius: 9px; margin-top: 0.5em; } \
                    QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; } \
                    ")
                    
                    self.grid.addWidget(acbox)
                    sourcelisttrack.append([track_id,'ac',self.start,self.end])
                    
                elif line[2]=='dc':
                    dcbox=QtGui.QGroupBox()
                    dcbox.setTitle(line[3])
                    dcgrid=QtGui.QGridLayout()
                    """
                    label=QtGui.QLabel(line[3])
                    self.grid.addWidget(label,self.row,1)
                    self.row=self.row+1
                    self.start=self.count
                    """
                    label=QtGui.QLabel(line[4])
                    dcgrid.addWidget(label,self.row,0)
                    self.entry_var[self.count]=QtGui.QLineEdit()
                    self.entry_var[self.count].setMaximumWidth(150)
                    dcgrid.addWidget(self.entry_var[self.count],self.row,1)
                    self.entry_var[self.count].setText("")
                    self.row=self.row+1
                    self.end=self.count
                    self.count=self.count+1
                    
                    dcbox.setLayout(dcgrid)
                    
                    #CSS
                    dcbox.setStyleSheet(" \
                    QGroupBox { border: 1px solid gray; border-radius: 9px; margin-top: 0.5em; } \
                    QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; } \
                    ")
                    
                    self.grid.addWidget(dcbox)
                    sourcelisttrack.append([track_id,'dc',self.start,self.end])
                    
                elif line[2]=='sine':
                    sinebox=QtGui.QGroupBox()
                    sinebox.setTitle(line[3])
                    sinegrid=QtGui.QGridLayout()
                    """
                    label=QtGui.QLabel(line[3])
                    sinegrid.addWidget(label,self.row,1)
                    self.row=self.row+1
                    self.start=self.count
                    """
                    
                    for it in range(4,9):
                        label=QtGui.QLabel(line[it])
                        sinegrid.addWidget(label,self.row,0)
                        self.entry_var[self.count]=QtGui.QLineEdit()
                        self.entry_var[self.count].setMaximumWidth(150)
                        sinegrid.addWidget(self.entry_var[self.count],self.row,1)
                        self.entry_var[self.count].setText("")     
                        self.row=self.row+1
                        self.count=self.count+1  
                    self.end=self.count-1
                    
                    sinebox.setLayout(sinegrid)
                    
                    #CSS
                    sinebox.setStyleSheet(" \
                    QGroupBox { border: 1px solid gray; border-radius: 9px; margin-top: 0.5em; } \
                    QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; } \
                    ")
                    
                    self.grid.addWidget(sinebox)
                    sourcelisttrack.append([track_id,'sine',self.start,self.end])
                    
                elif line[2]=='pulse':
                    pulsebox=QtGui.QGroupBox()
                    pulsebox.setTitle(line[3])
                    pulsegrid=QtGui.QGridLayout()
                    """
                    label=QtGui.QLabel(line[3])
                    pulsegrid.addWidget(label,self.row,1)
                    self.row=self.row+1
                    self.start=self.count
                    """
                    for it in range(4,11):
                        label=QtGui.QLabel(line[it])
                        pulsegrid.addWidget(label,self.row,0)
                        self.entry_var[self.count]=QtGui.QLineEdit()
                        self.entry_var[self.count].setMaximumWidth(150)
                        pulsegrid.addWidget(self.entry_var[self.count],self.row,1)
                        self.entry_var[self.count].setText("")
                        self.row=self.row+1
                        self.count=self.count+1
                    self.end=self.count-1
                    
                    pulsebox.setLayout(pulsegrid)
                    
                    #CSS
                    pulsebox.setStyleSheet(" \
                    QGroupBox { border: 1px solid gray; border-radius: 9px; margin-top: 0.5em; } \
                    QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; } \
                    ")
                    
                    self.grid.addWidget(pulsebox)
                    sourcelisttrack.append([track_id,'pulse',self.start,self.end])
                
                elif line[2]=='pwl':
                    pwlbox=QtGui.QGroupBox()
                    pwlbox.setTitle(line[3])
                    pwlgrid=QtGui.QGridLayout()
                    """
                    label=QtGui.QLabel(line[3])
                    self.grid.addWidget(label,self.row,1)
                    self.row=self.row+1
                    self.start=self.count
                    """
                    label=QtGui.QLabel(line[4])
                    pwlgrid.addWidget(label,self.row,0)
                    self.entry_var[self.count]=QtGui.QLineEdit()
                    self.entry_var[self.count].setMaximumWidth(150)
                    pwlgrid.addWidget(self.entry_var[self.count],self.row,1)
                    self.entry_var[self.count].setText("");
                    self.row=self.row+1
                    self.end=self.count
                    self.count=self.count+1
                    
                    pwlbox.setLayout(pwlgrid)
                    
                    #CSS
                    pwlbox.setStyleSheet(" \
                    QGroupBox { border: 1px solid gray; border-radius: 9px; margin-top: 0.5em; } \
                    QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; } \
                    ")
                    
                    self.grid.addWidget(pwlbox)
                    sourcelisttrack.append([track_id,'pwl',self.start,self.end])
                    
                elif line[2]=='exp':
                    expbox=QtGui.QGroupBox()
                    expbox.setTitle(line[3])
                    expgrid=QtGui.QGridLayout()
                    """
                    label=QtGui.QLabel(line[3])
                    self.grid.addWidget(label,self.row,1)
                    self.row=self.row+1
                    self.start=self.count
                    """
                    for it in range(4,10):
                        label=QtGui.QLabel(line[it])
                        expgrid.addWidget(label,self.row,0)
                        self.entry_var[self.count]=QtGui.QLineEdit()
                        self.entry_var[self.count].setMaximumWidth(150)
                        expgrid.addWidget(self.entry_var[self.count],self.row,1)
                        self.entry_var[self.count].setText("")
                        self.row=self.row+1
                        self.count=self.count+1
                    self.end=self.count-1
                    print "End",self.end
                    expbox.setLayout(expgrid)
                    
                    #CSS
                    expbox.setStyleSheet(" \
                    QGroupBox { border: 1px solid gray; border-radius: 9px; margin-top: 0.5em; } \
                    QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; } \
                    ")
                    
                    self.grid.addWidget(expbox)
                    sourcelisttrack.append([track_id,'exp',self.start,self.end])
                    
                    
                self.count=self.count+1
                          
                
        else:
            print "No source is present in your circuit"
        
        
        #This is used to keep the track of dynamically created widget
        self.obj_track.sourcelisttrack["ITEMS"] = sourcelisttrack
        self.obj_track.source_entry_var["ITEMS"] = self.entry_var
        self.show()
        
        
        
        
        
      
        
