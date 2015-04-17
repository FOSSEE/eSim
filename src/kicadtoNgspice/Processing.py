import sys
import os
from xml.etree import ElementTree as ET



class PrcocessNetlist:
    modelxmlDIR = '../modelParamXML'
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
                '''
                width=raw_input('  Enter width of mosfet '+words[0]+'(default=100u):')
                length=raw_input('  Enter length of mosfet '+words[0]+'(default=100u):')
                multiplicative_factor=raw_input('  Enter multiplicative factor of mosfet '+words[0]+'(default=1):')
              
                if width=="": width="100u"
                if multiplicative_factor=="": multiplicative_factor="100u"
                if length=="": length="100u"
                schematicInfo.insert(index,words[0]+" "+words[1]+" "+words[2]+" "+words[3]+" "+words[3]+" "+words[4]+" "+'M='+multiplicative_factor+" "+'L='+length+" "+'W='+width)
                '''
                
                schematicInfo.insert(index,words[0]+" "+words[1]+" "+words[2]+" "+words[3]+" "+words[3]+" "+words[4])
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
    
    
    def convertICintoBasicBlocks(self,schematicInfo,outputOption,modelList):
        #Insert details of Ngspice model
        unknownModelList = []
        multipleModelList = []
        k = 1
        for compline in schematicInfo:
            words = compline.split()
            compName = words[0]
            # Find the IC from schematic 
            if compName[0]=='u':
                # Find the component from the circuit
                index=schematicInfo.index(compline)
                compType=words[len(words)-1];
                schematicInfo.remove(compline)
                paramDict = {}
                print "Compline",compline 
                print "CompType",compType
                print "Words",words
                print "compName",compName
                #Looking if model file is present
                xmlfile = compType+".xml"   #XML Model File
                count = 0 #Check if model of same name is present
                modelPath = []
                all_dir = [x[0] for x in os.walk(PrcocessNetlist.modelxmlDIR)]
                for each_dir in all_dir:
                    all_file = os.listdir(each_dir)
                    if xmlfile in all_file:
                        count += 1
                        modelPath.append(os.path.join(each_dir,xmlfile))
                      
                if count > 1:
                    multipleModelList.append(modelPath)
                elif count == 0:
                    unknownModelList.append(compType)
                elif count == 1:
                    try:
                        print "Start Parsing :",modelPath  
                        tree = ET.parse(modelPath[0])
                        
                        root = tree.getroot()
                        #Getting number of nodes for model and title
                        for child in tree.iter():
                            if child.tag == 'node_number':
                                num_of_nodes = int(child.text)
                            elif child.tag == 'title':
                                title = child.text+" "+compName
                            elif child.tag == 'name':
                                modelname = child.text
                            elif child.tag == 'type':
                                #Checking for Analog and Digital
                                type = child.text
                            elif child.tag == 'split':
                                splitDetail = child.text
                                
                            #print "Child Item",child
                            #print "Tag",child.tag
                            #print "Tag Value",child.text
                            
                        for param in tree.findall('param'):
                            for item in param:
                                #print "Tags ",item.tag
                                #print "Value",item.text
                                if 'vector'in item.attrib:
                                    print "Tag having vector attribute",item.tag,item.attrib['vector']
                                    temp_count = 1
                                    temp_list = []
                                    for i in range(0,int(item.attrib['vector'])):
                                        temp_list.append(item.text+" "+str(temp_count))
                                        temp_count += 1
                                    if 'default' in item.attrib:
                                        paramDict[item.tag+":"+item.attrib['default']] = temp_list
                                    else:
                                        paramDict[item.tag] = item.text
                                                                    
                                else:
                                    if 'default' in item.attrib:
                                        paramDict[item.tag+":"+item.attrib['default']] = item.text
                                    else:
                                        paramDict[item.tag] = item.text
                                
                            
                        print "Number of Nodes : ",num_of_nodes
                        print "Title : ",title
                        print "Parameters",paramDict
                        #Creating line for adding model line in schematic
                        if splitDetail == 'None':
                            modelLine = "a"+str(k)+" "
                            for i in range(1,num_of_nodes+1):
                                modelLine += words[i]+" "
                            modelLine += compName
                            
                        else:
                            print "Split Details :",splitDetail
                            modelLine = "a"+str(k)+" "
                            vectorDetail = splitDetail.split(':')
                            print "Vector Details",vectorDetail
                            pos = 1 #Node position
                            for item in vectorDetail:
                                try:
                                    if item.split("-")[1] == 'V':
                                        print "Vector"
                                        modelLine += "["
                                        for i in range(0,int(item.split("-")[0])):
                                            modelLine += words[pos]+" "
                                            pos += 1
                                        modelLine += "] "
                                    elif item.split("-")[1] == 'NV':
                                        print "Non Vector"  
                                        for i in range(0,int(item.split("-")[0])):
                                            modelLine += words[pos]+" "
                                            pos += 1
                                
                                except:
                                    print  "There is error while processing Vector Details"
                                    sys.exit(2)
                            modelLine += compName        
                            
                        print "Final Model Line :",modelLine
                        try:
                            schematicInfo.append(modelLine)
                            k=k+1
                        except Exception as e:
                            print "Error while appending ModelLine ",modelLine
                            print "Excpetion Message : ",str(e)
                        #Insert comment at remove line
                        schematicInfo.insert(index,"* "+compline)
                        comment = "* "+modelname+" "+compType
                        modelList.append([index,compline,compType,compName,comment,title,type,paramDict])
                    except:
                        print  "Unable to parse the model, Please check your your xml file"
                        sys.exit(2)
                        
                #print "Count",count
                #print "UnknownModelList",unknownModelList
                #print "MultipleModelList",multipleModelList  
                '''
                if compType=="gain":
                    schematicInfo.append("a"+str(k)+" "+words[1]+" "+words[2]+" "+compName)
                    k=k+1
                    #Insert comment at remove line
                    schematicInfo.insert(index,"* "+compline)
                    print "-----------------------------------------------------------\n"
                    print "Adding Gain"
                    Comment='* Gain '+compType
                    Title='Add parameters for Gain '+compName
                    in_offset='  Enter offset for input (default=0.0): '
                    gain='  Enter gain (default=1.0): '
                    out_offset='  Enter offset for output (default=0.0): '
                    print "-----------------------------------------------------------"
                    modelList.append([index,compline,compType,compName,Comment,Title,in_offset,gain,out_offset])
                elif compType=="summer":
                    schematicInfo.append("a"+str(k)+" ["+words[1]+" "+words[2]+"] "+words[3]+" "+compName)
                    k=k+1
                    #Insert comment at remove line
                    schematicInfo.insert(index,"* "+compline)
                    print "-----------------------------------------------------------\n"
                    print "Adding summer"
                    Comment='* Summer '+compType
                    Title='Add parameters for Summer '+compName
                    in1_offset='  Enter offset for input 1 (default=0.0): '
                    in2_offset='  Enter offset for input 2 (default=0.0): '
                    in1_gain='  Enter gain for input 1 (default=1.0): '
                    in2_gain='  Enter gain for input 2 (default=1.0): '
                    out_gain='  Enter gain for output (default=1.0): '
                    out_offset='  Enter offset for output (default=0.0): '
                    print "-----------------------------------------------------------"
                    modelList.append([index,compline,compType,compName,Comment,Title,in1_offset,in2_offset,in1_gain,in2_gain,out_gain,out_offset])
                '''
        return schematicInfo,outputOption,modelList,unknownModelList,multipleModelList
        
        
            