
class PrcocessNetlist:
    def __init__(self):
        pass
    
    def readNetlist(self,filename):
        f = open(filename)
        data=f.read()
        f.close()
        return data.splitlines()

    def readParamInfo(self,kicadNetlis):
        """Read Parameter information and store it into dictionary"""
        param={}
        for eachline in kicadNetlis:
            print eachline
            eachline=eachline.strip()
            if len(eachline)>1:
                words=eachline.split()
                option=words[0].lower()
                if option=='.param':
                    for i in range(1, len(words), 1):
                        paramList=words[i].split('=')
                        param[paramList[0]]=paramList[1]
        return param
    
    def preprocessNetlist(self,kicadNetlis,param):
        """Preprocess netlist (replace parameters)"""
        netlist=[]
        for eachline in kicadNetlis:
            # Remove leading and trailing blanks spaces from line 
            eachline=eachline.strip()
            # Remove special character $
            eachline=eachline.replace('$','')
            # Replace parameter with values
            for subParam in eachline.split():
                if '}' in subParam:
                    key=subParam.split()[0]
                    key=key.strip('{')
                    key=key.strip('}')
                    if key in param:
                        eachline=eachline.replace('{'+key+'}',param[key])
                    else:
                        print "Parameter " + key +" does not exists"
                        value=raw_input('Enter parameter value: ')
                        eachline=eachline.replace('{'+key+'}',value)
            #Convert netlist into lower case letter     
            eachline=eachline.lower()
            # Construct netlist
            if len(eachline)>1:
                if eachline[0]=='+':
                    netlist.append(netlist.pop()+eachline.replace('+',' '))
                else:
                    netlist.append(eachline)
        #Copy information line
        infoline=netlist[0]
        netlist.remove(netlist[0])
        return netlist,infoline
    
    def separateNetlistInfo(self,netlist):
        optionInfo=[]
        schematicInfo=[]
        for eachline in netlist:
            if eachline[0]=='*':
                continue
            elif eachline[0]=='.':
                optionInfo.append(eachline)
            else:
                schematicInfo.append(eachline)
        return optionInfo,schematicInfo
    
    def getModelSubcktList(self,schematicInfo,modelList,subcktList):
        #Processing Netlist for modellist and subcktlist details
        for eachline in schematicInfo:
            words = eachline.split()
            if eachline[0]=='d':
                modelName=words[3]
                if modelName in modelList:
                    continue
                else:
                    modelList.append(modelName)
            elif eachline[0]=='q':
                modelName=words[4]
                index=schematicInfo.index(eachline)
                schematicInfo.remove(eachline)
                schematicInfo.insert(index,words[0]+" "+words[3]+" "+words[2]+" "+words[1]+" "+words[4])
                if modelName in modelList:
                    continue
                else:
                    modelList.append(modelName)
            elif eachline[0]=='m':
                modelName=words[4]
                index=schematicInfo.index(eachline)
                schematicInfo.remove(eachline)
                width=raw_input('  Enter width of mosfet '+words[0]+'(default=100u):')
                length=raw_input('  Enter length of mosfet '+words[0]+'(default=100u):')
                multiplicative_factor=raw_input('  Enter multiplicative factor of mosfet '+words[0]+'(default=1):')
                if width=="": width="100u"
                if multiplicative_factor=="": multiplicative_factor="100u"
                if length=="": length="100u"
                schematicInfo.insert(index,words[0]+" "+words[1]+" "+words[2]+" "+words[3]+" "+words[3]+" "+words[4]+" "+'M='+multiplicative_factor+" "+'L='+length+" "+'W='+width)
                if modelName in modelList:
                    continue
                modelList.append(modelName)
            elif eachline[0]=='j':
                modelName=words[4]
                index=schematicInfo.index(eachline)
                schematicInfo.remove(eachline)
                schematicInfo.insert(index,words[0]+" "+words[1]+" "+words[2]+" "+words[3]+" "+words[4])
                if modelName in modelList:
                    continue
                else:
                    modelList.append(modelName)
            elif eachline[0]=='x':
                subcktName=words[len(words)-1]
                if subcktName in subcktList:
                    continue
                else:
                    subcktList.append(subcktName)
        
        return modelList,subcktList
    
    def insertSpecialSourceParam(self,schematicInfo,sourcelist):
        #Inser Special source parameter
        schematicInfo1=[]
        
        for compline in schematicInfo:
            words=compline.split()
            compName=words[0]
            # Ask for parameters of source
            if compName[0]=='v' or compName=='i':
                # Find the index component from circuit
                index=schematicInfo.index(compline)
                if words[3]=="pulse":
                    Title="Add parameters for pulse source "+compName
                    v1='  Enter initial value(Volts/Amps): '
                    v2='  Enter pulsed value(Volts/Amps): '
                    td='  Enter delay time (seconds): '
                    tr='  Enter rise time (seconds): '
                    tf='  Enter fall time (seconds): '
                    pw='  Enter pulse width (seconds): '
                    tp='  Enter period (seconds): '
                    sourcelist.append([index,compline,words[3],Title,v1,v2,td,tr,tf,pw,tp])
                    
                elif words[3]=="sine":
                    Title="Add parameters for sine source "+compName
                    vo='  Enter offset value (Volts/Amps): '
                    va='  Enter amplitude (Volts/Amps): '
                    freq='  Enter frequency (Hz): '
                    td='  Enter delay time (seconds): '
                    theta='  Enter damping factor (1/seconds): '
                    sourcelist.append([index,compline,words[3],Title,vo,va,freq,td,theta])

                elif words[3]=="pwl":
                    Title="Add parameters for pwl source "+compName
                    t_v=' Enter in pwl format without bracket i.e t1 v1 t2 v2.... '
                    sourcelist.append([index,compline,words[3],Title,t_v])

                elif words[3]=="ac":
                    Title="Add parameters for ac source "+compName
                    v_a='  Enter amplitude (Volts/Amps): '
                    sourcelist.append([index,compline,words[3],Title,v_a])

                elif words[3]=="exp":
                    Title="Add parameters for exponential source "+compName
                    v1='  Enter initial value(Volts/Amps): '
                    v2='  Enter pulsed value(Volts/Amps): '
                    td1='  Enter rise delay time (seconds): '
                    tau1='  Enter rise time constant (seconds):     '
                    td2='  Enter fall time (seconds): '
                    tau2='  Enter fall time constant (seconds): '
                    sourcelist.append([index,compline,words[3],Title,v1,v2,td1,tau1,td2,tau2])

                elif words[3]=="dc":
                    Title="Add parameters for DC source "+compName
                    v1='  Enter value(Volts/Amps): '
                    v2='  Enter zero frequency: '
                    sourcelist.append([index,compline,words[3],Title,v1,v2])
                
            elif compName[0]=='h' or compName[0]=='f':
                # Find the index component from the circuit
                index=schematicInfo.index(compline)
                schematicInfo.remove(compline)
                schematicInfo.insert(index,"* "+compName)
                schematicInfo1.append("V"+compName+" "+words[3]+" "+words[4]+" 0")
                schematicInfo1.append(compName+" "+words[1]+" "+words[2]+" "+"V"+compName+" "+words[5])
                
        schematicInfo=schematicInfo+schematicInfo1
        #print sourcelist
        #print schematicInfo
        return schematicInfo,sourcelist
    
    
            