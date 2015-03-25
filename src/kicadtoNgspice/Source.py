
from PyQt4 import QtGui
from Processing import PrcocessNetlist
import TrackWidget


class Source(QtGui.QWidget):
        
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
        
        #Creating Source Widget
        self.createSourceWidget(sourcelist,sourcelisttrack)
        
           
        
    def createSourceWidget(self,sourcelist,sourcelisttrack):
                
        self.grid = QtGui.QGridLayout()
        self.setLayout(self.grid)
        
        if sourcelist:
            for line in sourcelist:
                #print "Voltage source line index: ",line[0]
                #print "SourceList line Test: ",line
                track_id=line[0]
                print "track_id is ",track_id
                if line[2]=='ac':
                    label=QtGui.QLabel(line[3])
                    self.grid.addWidget(label,self.row,1)
                    self.row=self.row+1
                    self.start=self.count
                    label=QtGui.QLabel(line[4])
                    self.grid.addWidget(label,self.row,0)
                    self.entry_var[self.count]=QtGui.QLineEdit()
                    self.grid.addWidget(self.entry_var[self.count],self.row,1)
                    #Value Need to check previuouse value
                    self.entry_var[self.count].setText("")
                    self.row=self.row+1
                    self.end=self.count
                    self.count=self.count+1
                    sourcelisttrack.append([track_id,'ac',self.start,self.end])
                    
                elif line[2]=='dc':
                    label=QtGui.QLabel(line[3])
                    self.grid.addWidget(label,self.row,1)
                    self.row=self.row+1
                    self.start=self.count
                    label=QtGui.QLabel(line[4])
                    self.grid.addWidget(label,self.row,0)
                    self.entry_var[self.count]=QtGui.QLineEdit()
                    self.grid.addWidget(self.entry_var[self.count],self.row,1)
                    self.entry_var[self.count].setText("")
                    self.row=self.row+1
                    self.end=self.count
                    self.count=self.count+1
                    sourcelisttrack.append([track_id,'dc',self.start,self.end])
                    
                elif line[2]=='sine':
                    label=QtGui.QLabel(line[3])
                    self.grid.addWidget(label,self.row,1)
                    self.row=self.row+1
                    self.start=self.count
                    
                    for it in range(4,9):
                        label=QtGui.QLabel(line[it])
                        self.grid.addWidget(label,self.row,0)
                        self.entry_var[self.count]=QtGui.QLineEdit()
                        self.grid.addWidget(self.entry_var[self.count],self.row,1)
                        self.entry_var[self.count].setText("")     
                        self.row=self.row+1
                        self.count=self.count+1  
                    self.end=self.count-1
                    sourcelisttrack.append([track_id,'sine',self.start,self.end])
                    
                elif line[2]=='pulse':
                    label=QtGui.QLabel(line[3])
                    self.grid.addWidget(label,self.row,1)
                    self.row=self.row+1
                    self.start=self.count
                    for it in range(4,11):
                        label=QtGui.QLabel(line[it])
                        self.grid.addWidget(label,self.row,0)
                        self.entry_var[self.count]=QtGui.QLineEdit()
                        self.grid.addWidget(self.entry_var[self.count],self.row,1)
                        self.entry_var[self.count].setText("")
                        self.row=self.row+1
                        self.count=self.count+1
                    self.end=self.count-1
                    sourcelisttrack.append([track_id,'pulse',self.start,self.end])
                
                elif line[2]=='pwl':
                    label=QtGui.QLabel(line[3])
                    self.grid.addWidget(label,self.row,1)
                    self.row=self.row+1
                    self.start=self.count
                    label=QtGui.QLabel(line[4])
                    self.grid.addWidget(label,self.row,0)
                    self.entry_var[self.count]=QtGui.QLineEdit()
                    self.grid.addWidget(self.entry_var[self.count],self.row,1)
                    self.entry_var[self.count].setText("");
                    self.row=self.row+1
                    self.end=self.count
                    self.count=self.count+1
                    sourcelisttrack.append([track_id,'pwl',self.start,self.end])
                    
                elif line[2]=='exp':
                    label=QtGui.QLabel(line[3])
                    self.grid.addWidget(label,self.row,1)
                    self.row=self.row+1
                    self.start=self.count
                    for it in range(4,10):
                        label=QtGui.QLabel(line[it])
                        self.grid.addWidget(label,self.row,0)
                        self.entry_var[self.count]=QtGui.QLineEdit()
                        self.grid.addWidget(self.entry_var[self.count],self.row,1)
                        self.entry_var[self.count].setText("")
                        self.row=self.row+1
                        self.count=self.count+1
                    self.end=self.count-1
                    sourcelisttrack.append([track_id,'exp',self.start,self.end])
                    
                    
                self.count=self.count+1
                          
                
        else:
            print "No source is present in your circuit"
        
    
        
        self.obj_track.sourcelisttrack["ITEMS"] = sourcelisttrack
        self.obj_track.entry_var["ITEMS"] = self.entry_var
        self.show()
        
        
        
        
        
      
        
