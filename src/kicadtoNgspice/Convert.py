

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