import os
import sys

import TrackWidget


class Convert:
    def __init__(self,sourcelisttrack,source_entry_var,schematicInfo):
        print "Start Conversion"
        self.sourcelisttrack = sourcelisttrack
        self.schematicInfo = schematicInfo
        self.entry_var = source_entry_var
        self.sourcelistvalue = []
        
              
    def addSourceParameter(self):
        print "Adding Source parameter"
        #print "SourceListTrack : ",self.sourcelisttrack
        #print "Schematic Info ",self.schematicInfo
        #print "Entry Var",self.entry_var
        self.start = 0
        self.end = 0
        
        for compline in self.sourcelisttrack:
            self.index = compline[0]
            self.addline = self.schematicInfo[self.index]
            if compline[1] == 'sine':
                try:
                    self.start = compline[2]
                    self.end = compline[3]
                    vo_val = str(self.entry_var[self.start].text()) if len(str(self.entry_var[self.start].text())) > 0 else '0'
                    va_val = str(self.entry_var[self.start+1].text()) if len(str(self.entry_var[self.start+1].text())) > 0 else '0'
                    freq_val = str(self.entry_var[self.start+2].text()) if len(str(self.entry_var[self.start+2].text())) > 0 else '0'
                    td_val = str(self.entry_var[self.start+3].text()) if len(str(self.entry_var[self.start+3].text())) > 0 else '0'
                    theta_val = str(self.entry_var[self.end].text()) if len(str(self.entry_var[self.end].text())) > 0 else '0'
                    self.addline = self.addline.partition('(')[0] + "("+vo_val+" "+va_val+" "+freq_val+" "+td_val+" "+theta_val+")"
                    self.sourcelistvalue.append([self.index,self.addline])
                except:
                    print "Caught an exception in sine voltage source ",self.addline
                    
            elif compline[1] == 'pulse':
                try:
                    self.start = compline[2]
                    self.end = compline[3]
                    v1_val = str(self.entry_var[self.start].text()) if len(str(self.entry_var[self.start].text())) > 0 else '0'
                    v2_val = str(self.entry_var[self.start+1].text()) if len(str(self.entry_var[self.start+1].text())) > 0 else '0'
                    td_val = str(self.entry_var[self.start+2].text()) if len(str(self.entry_var[self.start+2].text())) > 0 else '0'
                    tr_val = str(self.entry_var[self.start+3].text()) if len(str(self.entry_var[self.start+3].text())) > 0 else '0'
                    tf_val = str(self.entry_var[self.start+4].text()) if len(str(self.entry_var[self.start+4].text())) > 0 else '0'
                    pw_val = str(self.entry_var[self.start+5].text()) if len(str(self.entry_var[self.start+5].text())) > 0 else '0'
                    tp_val = str(self.entry_var[self.end].text()) if len(str(self.entry_var[self.end].text())) > 0 else '0'

                    self.addline = self.addline.partition('(')[0] + "("+v1_val+" "+v2_val+" "+td_val+" "+tr_val+" "+tf_val+" "+pw_val+" "+tp_val+")"
                    self.sourcelistvalue.append([self.index,self.addline])
                except:
                    print "Caught an exception in pulse voltage source ",self.addline 
                    
            elif compline[1] == 'pwl':
                try:
                    self.start = compline[2]
                    self.end = compline[3]
                    t_v_val = str(self.entry_var[self.start].text()) if len(str(self.entry_var[self.start].text())) > 0 else '0 0'
                    self.addline = self.addline.partition('(')[0] + "("+t_v_val+")"
                    self.sourcelistvalue.append([self.index,self.addline])
                except:
                    print "Caught an exception in pwl voltage source ",self.addline
                    
            elif compline[1] == 'ac':
                try:
                    self.start = compline[2]
                    self.end = compline[3]
                    va_val=str(self.entry_var[self.start].text()) if len(str(self.entry_var[self.start].text())) > 0 else '0'
                    self.addline = ' '.join(self.addline.split())
                    self.addline = self.addline.partition('ac')[0] +" "+'ac'+" "+ va_val
                    self.sourcelistvalue.append([self.index,self.addline]) 
                except:
                    print "Caught an exception in ac voltage source ",self.addline
                    
            elif compline[1] == 'dc':
                try:
                    self.start = compline[2]
                    self.end = compline[3]
                    v1_val = str(self.entry_var[self.start].text()) if len(str(self.entry_var[self.start].text())) > 0 else '0'
                    self.addline = ' '.join(self.addline.split())    
                    self.addline = self.addline.partition('dc')[0] + " " +'dc'+ " "+v1_val
                    self.sourcelistvalue.append([self.index,self.addline]) 
                except:
                    print "Caught an exception in dc voltage source",self.addline
                    
            elif compline[1] == 'exp':
                try:
                    self.start = compline[2]
                    self.end = compline[3]
                    v1_val = str(self.entry_var[self.start].text()) if len(str(self.entry_var[self.start].text())) > 0 else '0'
                    v2_val = str(self.entry_var[self.start+1].text()) if len(str(self.entry_var[self.start+1].text())) > 0 else '0'
                    td1_val = str(self.entry_var[self.start+2].text()) if len(str(self.entry_var[self.start+2].text())) > 0 else '0'
                    tau1_val = str(self.entry_var[self.start+3].text()) if len(str(self.entry_var[self.start+3].text())) > 0 else '0'
                    td2_val = str(self.entry_var[self.start+4].text()) if len(str(self.entry_var[self.start+4].text())) > 0 else '0'
                    tau2_val = str(self.entry_var[self.end].text()) if len(str(self.entry_var[self.end].text())) > 0 else '0'

                    self.addline = self.addline.partition('(')[0] + "("+v1_val+" "+v2_val+" "+td1_val+" "+tau1_val+" "+td2_val+" "+tau2_val+")"
                    self.sourcelistvalue.append([self.index,self.addline])
                except:
                    print "Caught an exception in exp voltage source ",self.addline 
                    
        #Updating Schematic with source value
        for item in self.sourcelistvalue:
            del self.schematicInfo[item[0]]
            self.schematicInfo.insert(item[0],item[1])   
            
        return self.schematicInfo
    
       
    def analysisInsertor(self,ac_entry_var,dc_entry_var, tran_entry_var,set_checkbox,ac_parameter,dc_parameter,tran_parameter,ac_type):
        self.ac_entry_var = ac_entry_var
        self.dc_entry_var = dc_entry_var
        self.tran_entry_var = tran_entry_var
        self.set_checkbox = set_checkbox
        self.ac_parameter= ac_parameter
        self.dc_parameter= dc_parameter
        self.trans_parameter = tran_parameter
        self.ac_type= ac_type
        self.no=0
        
        self.variable=self.set_checkbox
        self.direct= sys.argv[1]
        (filepath, filemname)= os.path.split(self.direct)
        self.Fileopen = os.path.join(filepath, "analysis")  
        self.writefile= open(self.Fileopen,"w")
       
        if self.variable== 'AC':
            self.no=0
            self.writefile.write(".ac " + self.ac_type + ' ' + str(self.ac_entry_var[self.no].text()) + ' ' + self.ac_parameter[self.no]+ ' ' + str(self.ac_entry_var[self.no+1].text()) + ' '+ self.ac_parameter[self.no+1] + ' ' + str(self.ac_entry_var[self.no+2].text()))        

        elif self.variable=='DC':
            self.no=0 
            self.writefile.write(".dc " + str(self.dc_entry_var[self.no+1].text())+ ' ' + self.converttosciform(self.dc_parameter[self.no]) + ' '+ str(self.dc_entry_var[self.no+2].text())+ ' ' + self.converttosciform(self.dc_parameter[self.no+1]) + ' '+ str(self.dc_entry_var[self.no+3].text())+ ' ' + self.converttosciform(self.dc_parameter[self.no+2]))

        elif self.variable == 'TRAN':
            self.no= 0
            self.writefile.write(".tran " + str(self.tran_entry_var[self.no].text())+ ' ' + self.converttosciform(self.trans_parameter[self.no]) + ' ' + str(self.tran_entry_var[self.no+1].text()) + ' ' + self.converttosciform(self.trans_parameter[self.no+1]) + ' ' + str(self.tran_entry_var[self.no+2].text()) + ' '+ self.converttosciform(self.trans_parameter[self.no+2]))

        else:
            pass
        self.writefile.close()
        
    def converttosciform(self, string_obj):
        self.string_obj = string_obj
        if self.string_obj[0] == 'm':
            return "e-03"
        elif self.string_obj[0] == 'u':
            return "e-06"
        elif self.string_obj[0] == 'n':
            return "e-09"
        elif self.string_obj[0] == 'p':
            return "e-12"
        else:
            return "e-00"
    
    
    def addModelParameter(self,schematicInfo):
        print "Schematic info after adding source detail",schematicInfo
        
        #Create object of TrackWidget
        self.obj_track = TrackWidget.TrackWidget()
        
        #List to store model line
        addmodelLine = []
        modelParamValue = []
        
        for line in self.obj_track.modelTrack:
            print "Model Track :",line
            if line[2] == 'transfo':
                try:
                    start=line[5]
                    end=line[6]
                    num_turns=str(self.obj_track.model_entry_var[start].text())
                    if num_turns=="": num_turns="310"    
                    h_array= "H_array = [ "
                    b_array = "B_array = [ "
                    h1=str(self.obj_track.model_entry_var[start+1].text())
                    b1=str(self.obj_track.model_entry_var[start+2].text())
                    if len(h1)!=0 and len(b1)!=0:
                        h_array=h_array+h1+" "
                        b_array=b_array+b1+" "
                        bh_array = h_array+" ] " + b_array+" ]"
                    else:
                        bh_array = "H_array = [-1000 -500 -375 -250 -188 -125 -63 0 63 125 188 250 375 500 1000] B_array = [-3.13e-3 -2.63e-3 -2.33e-3 -1.93e-3 -1.5e-3 -6.25e-4 -2.5e-4 0 2.5e-4 6.25e-4 1.5e-3 1.93e-3 2.33e-3 2.63e-3 3.13e-3]"
                    area=str(self.obj_track.model_entry_var[start+3].text())
                    length=str(self.obj_track.model_entry_var[start+4].text())
                    if area=="": area="1"
                    if length=="":length="0.01"
                    num_turns2=str(self.obj_track.model_entry_var[start+5].text())
                    if num_turns2=="": num_turns2="620"
                    addmodelLine=".model "+line[3]+"_primary lcouple (num_turns= "+num_turns+")"
                    modelParamValue.append([line[0],addmodelLine,line[4]])
                    addmodelLine=".model "+line[3]+"_iron_core core ("+bh_array+" area = "+area+" length ="+length +")"
                    modelParamValue.append([line[0],addmodelLine,line[4]])
                    addmodelLine=".model "+line[3]+"_secondary lcouple (num_turns ="+num_turns2+ ")"    
                    modelParamValue.append([line[0],addmodelLine,line[4]])    
                except:
                    print "Caught an exception in transfo model ",line[1]
            
            else:
                try:
                    start = line[5]
                    end = line[6]
                    addmodelLine=".model "+ line[3]+" "+line[2]+"("
                    for key,value in line[9].iteritems():
                        print "Tags: ",key
                        print "Value: ",value
                        #Checking for default value and accordingly assign param and default.
                        if ':' in key:
                            key = key.split(':')
                            param = key[0]
                            default = key[1]
                        else:
                            param = key
                            default = 0
                        #Cheking if value is iterable.its for vector
                        if hasattr(value, '__iter__'):
                            addmodelLine += param+"=["
                            for lineVar in value:
                                if  str(self.obj_track.model_entry_var[lineVar].text()) == "":
                                    paramVal = default
                                else:
                                    paramVal = str(self.obj_track.model_entry_var[lineVar].text())
                                addmodelLine += paramVal+" "
                            addmodelLine += "] "
                        else:
                            if  str(self.obj_track.model_entry_var[value].text()) == "":
                                paramVal = default
                            else:
                                paramVal = str(self.obj_track.model_entry_var[value].text())
                            
                            addmodelLine += param+"="+paramVal+" "
                                    
                        
                        
                                          
                    addmodelLine += ") "
                    modelParamValue.append([line[0],addmodelLine,line[4]]) 
                except:
                    print "Caught an exception in gain model ",line[1]        
        
        
        #Adding it to schematic
        for item in modelParamValue:
            schematicInfo.append(item[2]) #Adding Comment
            schematicInfo.append(item[1]) #Adding model line
            
            
        return schematicInfo
                