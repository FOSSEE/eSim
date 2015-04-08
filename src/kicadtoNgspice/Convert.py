import os

class Convert:
    def __init__(self,sourcelisttrack,entry_var,schematicInfo):
        print "Start Conversion"
        self.sourcelisttrack = sourcelisttrack
        self.schematicInfo = schematicInfo
        self.entry_var = entry_var
        self.sourcelistvalue = []
        
        
    def addSourceParameter(self):
        print "Adding Source parameter"
        print "SourceListTrack : ",self.sourcelisttrack
        print "Schematic Info ",self.schematicInfo
        print "Entry Var",self.entry_var
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
        print ("HI THIS IS A ANALYSIS INSERTOR FUNCTION")
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
        self.direct="/home/fossee/workspace/FreeEDA/Examples/BJT_amplifier/"
        self.FileName = os.path.join(self.direct, "analysis")  
        self.writefile= open(self.FileName,"w")
       
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
        