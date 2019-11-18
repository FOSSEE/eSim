from PyQt4 import QtGui

import TrackWidget
from xml.etree import ElementTree as ET
import os


class Model(QtGui.QWidget):
    """
    This class creates Model Tab of KicadtoNgspice window. 
    The widgets are created dynamically in the Model Tab.
    """
    
    def __init__(self,schematicInfo,modelList,clarg1):
        
        QtGui.QWidget.__init__(self)
        
        #Processing for getting previous values
        kicadFile = clarg1
        (projpath,filename)=os.path.split(kicadFile)
        project_name=os.path.basename(projpath)
        check=1
        try:
            f=open(os.path.join(projpath,project_name+"_Previous_Values.xml"),'r')
            tree=ET.parse(f)
            parent_root=tree.getroot()
            for child in parent_root:
                if child.tag=="model":
                    root=child
        except:
            check=0
            print "Model Previous Values XML is Empty"
        
        
        
        #Creating track widget object
        self.obj_trac = TrackWidget.TrackWidget()
        
        #for increasing row and counting/tracking line edit widget 
        self.nextrow = 0
        self.nextcount = 0
        
        #for storing line edit details position details
        self.start = 0
        self.end = 0
        
        #Creating GUI dynamically for Model tab    
        self.grid = QtGui.QGridLayout()
        self.setLayout(self.grid)
        
        for line in modelList:
            #print "ModelList Item:",line
            #Adding title label for model
            #Key: Tag name,Value:Entry widget number
            tag_dict = {} 
            modelbox=QtGui.QGroupBox()
            modelgrid=QtGui.QGridLayout()
            modelbox.setTitle(line[5])
            self.start=self.nextcount
            #line[7] is parameter dictionary holding parameter tags.
            i=0
            for key,value in line[7].iteritems():
                #print "Key : ",key
                #print "Value : ",value
                #Check if value is iterable
                if hasattr(value, '__iter__'):
                    #For tag having vector value
                    temp_tag = []
                    for item in value:
                        paramLabel = QtGui.QLabel(item)
                        modelgrid.addWidget(paramLabel,self.nextrow,0)
                        self.obj_trac.model_entry_var[self.nextcount]= QtGui.QLineEdit()
                        modelgrid.addWidget(self.obj_trac.model_entry_var[self.nextcount],self.nextrow,1)
                        try:
                            for child in root:
                                if child.text==line[2] and child.tag==line[3]:
                                    self.obj_trac.model_entry_var[self.nextcount].setText(child[i].text)
                                    i=i+1
                        except:
                            pass
                        temp_tag.append(self.nextcount)
                        self.nextcount = self.nextcount+1
                        self.nextrow = self.nextrow+1
                    tag_dict[key] = temp_tag
                else:
                    paramLabel = QtGui.QLabel(value)
                    modelgrid.addWidget(paramLabel,self.nextrow,0)
                    self.obj_trac.model_entry_var[self.nextcount]= QtGui.QLineEdit()
                    modelgrid.addWidget(self.obj_trac.model_entry_var[self.nextcount],self.nextrow,1)
                    try:
                        for child in root:
                            if child.text==line[2] and child.tag==line[3]:
                                self.obj_trac.model_entry_var[self.nextcount].setText(child[i].text)
                                i=i+1
                    except:
                            pass
                    tag_dict[key] = self.nextcount
                    self.nextcount = self.nextcount+1
                    self.nextrow = self.nextrow+1
            self.end= self.nextcount-1
            #print "End",self.end
            modelbox.setLayout(modelgrid)
            
            #CSS
            modelbox.setStyleSheet(" \
            QGroupBox { border: 1px solid gray; border-radius: 9px; margin-top: 0.5em; } \
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; } \
            ")
            
            self.grid.addWidget(modelbox)
            
            '''
            Listing all 
            line[0] = index
            line[1] = compLine
            line[2] = modelname  #Change from compType to modelname
            line[3] = compName
            line[4] = comment
            line[5] = title
            line[6] = type i.e analog or digital
            Now adding start,end and tag_dict which will be line[7],line[8] and line[9] respectively
            '''
            
            #This keeps the track of Model Tab Widget
            lst=[line[0],line[1],line[2],line[3],line[4],line[5],line[6],self.start,self.end,tag_dict]
            check=0
            for itr in self.obj_trac.modelTrack:
                if itr==lst:
                    check=1 
            
            if check==0: 
                self.obj_trac.modelTrack.append(lst)
                        
            #print "The tag dictionary : ",tag_dict
        
            
            
        self.show()
        
