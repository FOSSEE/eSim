import sys
import os
import re 
from string import maketrans

class NgMoConverter:
    def __init__(self):
        pass

    def readNetlist(self,filename):
        """
        Read Ngspice Netlist
        """
        if os.path.exists(filename):
            try:
                f = open(filename)
            except Exception as e:
                print("Error in opening file")
                print(str(e))
                sys.exit()
        else:
            print filename + " does not exist"
            sys.exit()

        data = f.read()
        #data = data.translate(maketrans('\n+', '  '))
        f.close()
        return data.splitlines()
    
    def separateNetlistInfo(self,data):
        """
        Separate schematic data and option data
        """
        optionInfo = []
        schematicInfo = []
        for eachline in data:
            if len(eachline) > 1:
                #if eachline[0] == '+':
                #    eachline=eachline.translate(maketrans('\n+','  '))
                if eachline[0]=='*':
                    continue
                elif eachline[0]=='.':
                    optionInfo.append(eachline.lower())
                else:
                    schematicInfo.append(eachline.lower())
        return optionInfo,schematicInfo
    
    def addModel(self,optionInfo):
        """
        Add model parameters in the modelica file and create dictionary of model parameters
        This function extract model and subckt information along with their parameters with the help of optionInfo
        """
        modelName = []
        modelInfo = {}
        subcktName = []
        paramInfo = []
        inbuiltmodelName = []
        inbuiltmodelInfo = {}
        #modelInfo['paramInfo'] = {}
        for eachline in optionInfo:
            words = eachline.split()
            if words[0] == '.include':
                name = words[1].split('.')
                if name[1] == 'lib':
                    modelName.append(name[0])
                if name[1] == 'sub':
                    subcktName.append(name[0])
            elif words[0] == '.param':
                paramInfo.append(eachline)
            elif words[0] == '.model':
                name = words[1]+':'+words[2].split('(')[0]  #model_ref_name:actual_model_name
                inbuiltmodelName.append(name)
                inbuiltmodelInfo[name] = {}
                #Get all the data with () of .model line
                paramData = re.compile("\((.*)\)" ).search(eachline).group(1)
                info = paramData.split()
                for eachitem in info:
                    eachitem =  eachitem.split('=')
                    inbuiltmodelInfo[name][eachitem[0]] = eachitem[1]
                 
        
        #Adding details of model(external) and subckt into modelInfo and subcktInfo
        for eachmodel in modelName:
            filename = eachmodel + '.lib'
            if os.path.exists(filename):
                try:
                    f = open(filename)
                except:
                    print("Error in opening file")
                    sys.exit()
            else:
                print filename + " does not exist"
                sys.exit()
            data = f.read()
            data = data.lower()
            newdata = data.split('(')
            newdata = newdata[1].split()
            modelInfo[eachmodel] = {}
            
            for eachline in newdata:
                if len(eachline) > 1:
                    info = eachline.split('=')
                    # modelInfo[eachmodel][info[0]] = {}
                    for eachitem in info:
                        modelInfo[eachmodel][info[0]] = info[1] #dic within a dic
            #modelInfo[eachmodel] = modelInfo[eachmodel].split()    
            # modelInfo[eachmodel] = modelInfo[eachmodel].lower()
            f.close()
                  
        
        return modelName, modelInfo, subcktName, paramInfo,inbuiltmodelName,inbuiltmodelInfo 
    
    def processParam(self,paramInfo):
        """
        Process parameter info and update in Modelica syntax
        """
        modelicaParam = []
        for eachline in paramInfo:
            eachline = eachline.split('.param')
            #Include ',' in between parameter
            #Removing leading and trailing space
            line = eachline[1].strip()
            line = line.split()
            final_line = ','.join(line)
            stat = 'parameter Real ' + final_line + ';'
            stat = stat.translate(maketrans('{}', '  '))
            modelicaParam.append(stat)
        print "Modelica Parameter----------->",modelicaParam
        return modelicaParam
    
    
    def separatePlot(self,schematicInfo):
        """
        separate print plot and component statements
        """
        compInfo = []
        plotInfo = []
        for eachline in schematicInfo:
            words = eachline.split()
            if words[0] == 'run':
                continue
            elif words[0] == 'plot' or words[0] == 'print':
                plotInfo.append(eachline)
            else:
                compInfo.append(eachline)
        return compInfo, plotInfo
    
    def separateSource(self,compInfo):
        """
        Find if dependent sources are present in the schematic and if so make a dictionary with source details
        """
        sourceInfo = {}
        source = []
        for eachline in compInfo:
            words = eachline.split()  ##This line need to be confirmed with Manas
            if eachline[0] in ['f', 'h']:
                source.append(words[3])
        if len(source) > 0:
            for eachline in compInfo:
                words_s = eachline.split()
                if words_s[0] in source:
                    sourceInfo[words_s[0]] = words_s[1:3]
        return sourceInfo
    
    def splitIntoVal(self,val):
        """
        Split the number k,u,p,t,g etc into powers e3,e-6 etc
        """
        print "Val------------->",val   
        for i in range(0,len(val),1):
            print "Val[i]----------------->",val[i]
            if val[i] in ['k','u','p','t','g','m','n','f']:
                newval = val.split(val[i])
                print "new Value------------>",newval
                if val[i] == 'k':
                    value = newval[0] + 'e3'
                if val[i] == 'u':
                    value = newval[0] + 'e-6'
                if val[i] == 'p':
                    value = newval[0] + 'e-12'
                if val[i] == 't':  
                    value = newval[0] + 'e12'
                if val[i] == 'g':
                    value = newval[0] + 'e9'
                if val[i] == 'm':
                    if i != len(val)-1:
                        if val[i+1] == 'e':
                            value = newval[0] + 'e6'
                    else:
                        value = newval[0] +'e-3'
                if val[i] == 'n':
                    value = newval[0] + 'e-9'       
                if val[i] == 'f':
                    value = newval[0] +'e-15'
                
            else:
                value = val
        return value
    
    def compInit(self,compInfo, node, modelInfo, subcktName):
        """
        For each component in the netlist initialise it acc to Modelica format
        """
        print "CompInfo inside compInit function : compInit",compInfo
        #### initial processing to check if MOs is present. If so, library to be used is BondLib
        modelicaCompInit = []
        numNodesSub = {} 
        IfMOS = '0'
        for eachline in compInfo:
            #words = eachline.split()
            if eachline[0] == 'm':
                IfMOS = '1'
                break
        if len(subcktName) > 0:
            subOptionInfo = []
            subSchemInfo = []
            for eachsub in subcktName:
                filename_tem = eachsub + '.sub'
                data = self.readNetlist(filename_tem)
                subOptionInfo, subSchemInfo = self.separateNetlistInfo(data)
                for eachline in subSchemInfo:
                    #words = eachline.split()
                    if eachline[0] == 'm':
                        IfMOS = '1'
                        break
        for eachline in compInfo:
            words = eachline.split()
            val = words[3]
            value = self.splitIntoVal(val)
            if eachline[0] == 'r':
                stat = 'Analog.Basic.Resistor ' + words[0] + '(R = ' + value + ');'
                modelicaCompInit.append(stat)
            elif eachline[0] == 'c':
                stat = 'Analog.Basic.Capacitor ' + words[0] + '(C = ' + value + ');'
                modelicaCompInit.append(stat)
            elif eachline[0] == 'l':
                stat = 'Analog.Basic.Inductor ' + words[0] + '(L = ' + value + ');'
                modelicaCompInit.append(stat) 
            elif eachline[0] == 'e':
                stat = 'Analog.Basic.VCV ' + words[0] + '(gain = ' + self.splitIntoVal(words[5]) + ');'
                modelicaCompInit.append(stat) 
            elif eachline[0] == 'g':
                stat = 'Analog.Basic.VCC ' + words[0] + '(transConductance = ' + self.splitIntoVal(words[5]) + ');'
                modelicaCompInit.append(stat) 
            elif eachline[0] == 'f':
                stat = 'Analog.Basic.CCC ' + words[0] + '(gain = ' + self.splitIntoVal(words[4]) + ');'
                modelicaCompInit.append(stat) 
            elif eachline[0] == 'h':
                stat = 'Analog.Basic.CCV ' + words[0] + '(transResistance = ' + self.splitIntoVal(words[4]) + ');'
                modelicaCompInit.append(stat)
            elif eachline[0] == 'd':
                if len(words) > 3:
                    n = float(modelInfo[words[3]]['n'])
                    vt_temp = 0.025*n
                    vt = str(vt_temp)
                    stat = 'Analog.Semiconductors.Diode ' + words[0] + '(Ids = ' + modelInfo[words[3]]['is'] + ', Vt = ' + vt + ', R = 1e12' +');'
                else:
                    stat = 'Analog.Semiconductors.Diode ' + words[0] +';'
                modelicaCompInit.append(stat)
            elif eachline[0] == 'm':
                line_l = words[7].split('=')
                line_w = words[8].split('=')
                line_pd = words[9].split('=')
                line_ps = words[10].split('=')
                line_ad = words[11].split('=')
                line_as = words[12].split('=')
                if words[5] == "mos_n" or words[5] == "mosfet_n":
                    start = 'BondLib.Electrical.Analog.Spice.Mn '
                if words[5] == "mos_p" or words[5] == "mosfet_p":
                    start = 'BondLib.Electrical.Analog.Spice.Mp '
                stat = start + words[0] + '(Tnom = 300, VT0 = ' + modelInfo[\
                       words[5]]['vto'] + ', GAMMA = ' + modelInfo[words[5]]['gamma'] +\
                       ', PHI = ' + modelInfo[words[5]]['phi'] + ', LD = ' + self.splitIntoVal(modelInfo[words[5]]['ld'])\
                        + ', U0 = ' + str(float(self.splitIntoVal(modelInfo[words[5]]['uo']))*0.0001) + ', LAMBDA = ' \
                        + modelInfo[words[5]]['lambda'] + ', TOX = ' + self.splitIntoVal(modelInfo[words[5]]['tox']) \
                        + ', PB = ' + modelInfo[words[5]]['pb'] + ', CJ = ' + self.splitIntoVal(modelInfo[words[5]]['cj']) \
                        + ', CJSW = ' + self.splitIntoVal(modelInfo[words[5]]['cjsw']) + ', MJ = ' + modelInfo[words[5]]['mj'] \
                        + ', MJSW = ' + modelInfo[words[5]]['mjsw'] + ', CGD0 = ' + self.splitIntoVal(modelInfo[words[5]]['cgdo']) \
                        + ', JS = ' + self.splitIntoVal(modelInfo[words[5]]['js']) + ', CGB0 = ' + self.splitIntoVal(modelInfo[words[5]]['cgbo']) \
                        + ', CGS0 = ' + self.splitIntoVal(modelInfo[words[5]]['cgso']) + ', L = ' + self.splitIntoVal(line_l[1]) + ', W = ' \
                        + line_w[1] + ', Level = 1' + ', AD = ' + line_ad[1] + ', AS = ' + line_as[1] + ', PD = ' \
                        + line_pd[1] + ', PS = ' + line_pd[1] + ');'
                stat = stat.translate(maketrans('{}', '  '))
                modelicaCompInit.append(stat)
            elif eachline[0] == 'v':
                typ = words[3].split('(')
                if typ[0] == "pulse":
                    per = words[9].split(')')
                    #if IfMOS == '0':
                        #stat = 'Spice3.Sources.V_pulse '+words[0]+'(TR = '+words[6]+', V2 = '+words[4]+', PW = '+words[8]+', PER = '+per[0]+', V1 = '+typ[1]+', TD = '+words[5]+', TF = '+words[7]+');'
                    #elif IfMOS == '1':
                    stat = 'Analog.Sources.TrapezoidVoltage '+words[0]+'(rising = '+words[6]+', V = '+words[4]\
                    +', width = '+words[8]+', period = '+per[0]+', offset = '+typ[1]+', startTime = '+words[5]+', falling = '+words[7]+');'                                                                                                                                                                             
                    modelicaCompInit.append(stat)
                if typ[0] == "sine":
                    theta = words[7].split(')')
                    #if IfMOS == '0':
                    #stat = 'Spice3.Sources.V_sin '+words[0]+'(VO = '+typ[1]+', VA = '+words[4]+', FREQ = '+words[5]+', TD = '+words[6]+', THETA = '+theta[0]+');'
                    #elif IfMOS == '1':
                    stat = 'Analog.Sources.SineVoltage '+words[0]+'(offset = '+typ[1]+', V = '+words[4]+', freqHz = '+words[5]+', startTime = '+words[6]+', phase = '+theta[0]+');'
                    modelicaCompInit.append(stat)
                if typ[0] == "pwl":
                    #if IfMOS == '0':
                    #keyw = 'Spice3.Sources.V_pwl '
                    #elif IfMOS == '1':
                    keyw = 'Analog.Sources.TableVoltage '
                    stat = keyw + words[0] + '(table = [' + typ[1] + ',' + words[4] + ';'
                    length = len(words);
                    for i in range(6,length,2):
                        if i == length-2:
                            w = words[i].split(')')
                            stat = stat + words[i-1] + ',' + w[0] 
                        else:
                            stat = stat + words[i-1] + ',' + words[i] + ';'
                    stat = stat + ']);'
                    modelicaCompInit.append(stat) 
                if typ[0] == words[3] and typ[0] != "dc":
                    val_temp = typ[0].split('v')
                    #if IfMOS  == '0':
                    stat = 'Analog.Sources.ConstantVoltage ' + words[0] + '(V = ' + val_temp[0] + ');'
                    #elif IfMOS == '1':
                    #stat = 'Analog.Sources.ConstantVoltage ' + words[0] + '(V = ' + val_temp[0] + ');'
                    modelicaCompInit.append(stat)
                elif typ[0] == words[3] and typ[0] == "dc":
                    #if IfMOS  == '0':
                        #stat = 'Spice3.Sources.V_constant ' + words[0] + '(V = ' + words[4] + ');'    ### check this
                    #elif IfMOS == '1':
                    stat = 'Analog.Sources.ConstantVoltage ' + words[0] + '(V = ' + words[4] + ');'    ### check this
                    modelicaCompInit.append(stat)
            
            elif eachline[0] == 'x':
                temp_line = eachline.split()
                temp = temp_line[0].split('x')
                index = temp[1]
                for i in range(0,len(temp_line),1):
                    if temp_line[i] in subcktName:
                        subname = temp_line[i]
                        numNodesSub[subname] = i - 1
                        point = i
                if len(temp_line) > point + 1:
                    rem = temp_line[point+1:len(temp_line)]
                    rem_new = ','.join(rem)
                    stat = subname + ' ' + subname +'_instance' + index + '(' +  rem_new + ');'
                else:
                    stat = subname + ' ' + subname +'_instance' + index + ';'
                modelicaCompInit.append(stat)
            else:
                continue
            
        if '0' in node:
            modelicaCompInit.append('Analog.Basic.Ground g;')
        return modelicaCompInit, numNodesSub
    
    def getSubInterface(self,subname,numNodesSub):
        """
        Get the list of nodes for subcircuit in .subckt line
        """
        subOptionInfo_p = []
        subSchemInfo_p = []
        filename_t = subname + '.sub'
        data_p = self.readNetlist(filename_t)
        subOptionInfo_p, subSchemInfo_p = self.separateNetlistInfo(data_p)
        if len(subOptionInfo_p) > 0:
            newline = subOptionInfo_p[0]
            newline = newline.split('.subckt '+ subname)       
            intLine = newline[1].split()
            newindex = numNodesSub[subname]
            nodesInfoLine = intLine[0:newindex]
        return nodesInfoLine
    
    def getSubParamLine(self,subname, numNodesSub, subParamInfo):
        """
        Take subcircuit name and give the info related to parameters in the first line and initislise it in
        """
        #nodeSubInterface = []
        subOptionInfo_p = []
        subSchemInfo_p = []
        filename_t = subname + '.sub'
        data_p = self.readNetlist(filename_t)
        subOptionInfo_p, subSchemInfo_p = self.separateNetlistInfo(data_p)
        print "subOptionInfo_p------------------------->",subOptionInfo_p
        print "subSchemInfo_p----------------------------->",subSchemInfo_p
        if len(subOptionInfo_p) > 0:
            newline = subOptionInfo_p[0]
            newline = newline.split('.subckt '+ subname)       
            intLine = newline[1].split()
            print "numNodesSub Index---------->",numNodesSub
            newindex = numNodesSub[subname]
            appen_line = intLine[newindex:len(intLine)]
            appen_param = ','.join(appen_line)
            paramLine = 'parameter Real ' + appen_param + ';'
            paramLine = paramLine.translate(maketrans('{}', '  '))
            subParamInfo.append(paramLine)
        return subParamInfo
    
    def nodeSeparate(self,compInfo, ifSub, subname, subcktName,numNodesSub):
        """
        separate the node numbers and create nodes in modelica file; 
        the nodes in the subckt line should not be inside protected keyword. pinInit is the one that goes under protected keyword.
        """
        node = []
        nodeTemp = []
        nodeDic = {}
        pinInit = 'Modelica.Electrical.Analog.Interfaces.Pin '
        pinProtectedInit = 'Modelica.Electrical.Analog.Interfaces.Pin '
        protectedNode = []
        print "CompInfo coming to nodeSeparate function: compInfo",compInfo
        
        #Removing '[' and ']' from compInfo for Digital node
        for i in range(0,len(compInfo),1):
            compInfo[i] = compInfo[i].replace("[","").replace("]","")
        
        
        
        for eachline in compInfo:
            words = eachline.split()
            if eachline[0] in ['m', 'e', 'g', 't']:
                nodeTemp.append(words[1])
                nodeTemp.append(words[2])
                nodeTemp.append(words[3])
                nodeTemp.append(words[4])
            elif eachline[0] in ['q', 'j']:
                nodeTemp.append(words[1])
                nodeTemp.append(words[2])
                nodeTemp.append(words[3])
            elif eachline[0] == 'x':
                templine = eachline.split()
                for i in range(0,len(templine),1):
                    if templine[i] in subcktName:
                        point = i   
                nodeTemp.extend(words[1:point])
            else:
                nodeTemp.append(words[1])
                nodeTemp.append(words[2])
        for i in nodeTemp:
            if i not in node:
                node.append(i)
      
        for i in range(0, len(node),1):
            nodeDic[node[i]] = 'n' + node[i]
            if ifSub == '0':
                if i != len(node)-1:
                    pinInit = pinInit + nodeDic[node[i]] + ', '
                else:
                    pinInit = pinInit + nodeDic[node[i]]
            else:
                nonprotectedNode = self.getSubInterface(subname, numNodesSub) 
                if node[i] in nonprotectedNode:
                    continue
                else:
                    protectedNode.append(node[i])
        if ifSub == '1':
            if len(nonprotectedNode) > 0:
                for i in range(0, len(nonprotectedNode),1):
                    if i != len(nonprotectedNode)-1:
                        pinProtectedInit = pinProtectedInit + nodeDic[nonprotectedNode[i]] + ','
                    else:
                        pinProtectedInit = pinProtectedInit + nodeDic[nonprotectedNode[i]]
            if len(protectedNode) > 0:
                for i in range(0, len(protectedNode),1):
                    if i != len(protectedNode)-1: 
                        pinInit = pinInit + nodeDic[protectedNode[i]] + ','
                    else:
                        pinInit = pinInit + nodeDic[protectedNode[i]]
        pinInit = pinInit + ';'
        pinProtectedInit = pinProtectedInit + ';'
        return node, nodeDic, pinInit, pinProtectedInit
    
    
    def connectInfo(self,compInfo, node, nodeDic, numNodesSub,subcktName):
        """
        Make node connections in the modelica netlist
        """
        connInfo = []
        sourcesInfo = self.separateSource(compInfo)
        for eachline in compInfo:
            words = eachline.split()
            if eachline[0] == 'r' or eachline[0] == 'c' or eachline[0] == 'd' or eachline[0] == 'l' or eachline[0] == 'v':
                conn = 'connect(' + words[0] + '.p,' + nodeDic[words[1]] + ');'
                connInfo.append(conn)
                conn = 'connect(' + words[0] + '.n,' + nodeDic[words[2]] + ');'
                connInfo.append(conn)
            elif eachline[0] == 'm':
                conn = 'connect(' + words[0] + '.D,' + nodeDic[words[1]] + ');'
                connInfo.append(conn)
                conn = 'connect(' + words[0] + '.G,' + nodeDic[words[2]] + ');'
                connInfo.append(conn)
                conn = 'connect(' + words[0] + '.S,' + nodeDic[words[3]] + ');'
                connInfo.append(conn)
                conn = 'connect(' + words[0] + '.B,' + nodeDic[words[4]] + ');'
                connInfo.append(conn)
            elif eachline[0] in ['f','h']:
                vsource = words[3]
                sourceNodes = sourcesInfo[vsource]
                sourceNodes = sourceNodes.split()
                conn = 'connect(' + words[0] + '.p1,'+ nodeDic[sourceNodes[0]] + ');'
                connInfo.append(conn)
                conn = 'connect(' + words[0] + '.n1,'+ nodeDic[sourceNodes[1]] + ');'
                connInfo.append(conn)
                conn = 'connect(' + words[0] + '.p2,'+ nodeDic[words[1]] + ');'
                connInfo.append(conn)
                conn = 'connect(' + words[0] + '.n2,'+ nodeDic[words[2]] + ');'
                connInfo.append(conn)
            elif eachline[0] in ['g','e']:
                conn = 'connect(' + words[0] + '.p1,'+ nodeDic[words[3]] + ');'
                connInfo.append(conn)
                conn = 'connect(' + words[0] + '.n1,'+ nodeDic[words[4]] + ');'
                connInfo.append(conn)
                conn = 'connect(' + words[0] + '.p2,'+ nodeDic[words[1]] + ');'
                connInfo.append(conn)
                conn = 'connect(' + words[0] + '.n2,'+ nodeDic[words[2]] + ');'
                connInfo.append(conn)
            elif eachline[0] == 'x':
                templine = eachline.split()
                temp = templine[0].split('x')
                index = temp[1]
                for i in range(0,len(templine),1):
                    print "Test------------------>"
                    if templine[i] in subcktName:   #Ask Manas Added subcktName in function Call
                        subname = templine[i]
                nodeNumInfo = self.getSubInterface(subname, numNodesSub)
                for i in range(0, numNodesSub[subname], 1):
                    #conn = 'connect(' + subname + '_instance' + index + '.' + nodeDic[nodeNumInfo[i]] + ',' + nodeDic[words[i+1]] + ');'
                    conn = 'connect(' + subname + '_instance' + index + '.' + 'n'+ nodeNumInfo[i] + ',' + nodeDic[words[i+1]] + ');'
                    connInfo.append(conn)
            else:
                continue
        if '0' in node:
            conn = 'connect(g.p,n0);'
            connInfo.append(conn)
         
        return connInfo
    
    
    def procesSubckt(self,subcktName,numNodesSub):
        
        #Process the subcircuit file .sub in the project folder
        
        #subcktDic = {}
        subOptionInfo = []
        subSchemInfo = []
        subModel = []
        subModelInfo = {}
        subsubName = [] 
        subParamInfo = []
        subinbuiltmodelName = []
        subinbuiltmodelInfo = {}
        nodeSubInterface = []
        nodeSub = []
        nodeDicSub = {}
        pinInitsub = []
        connSubInfo = []
        print "subcktName------------------>",subcktName
        if len(subcktName) > 0:
            for eachsub in subcktName:
                filename = eachsub + '.sub'
                data = self.readNetlist(filename)
                print "Data-------------------->",data
                subOptionInfo, subSchemInfo = self.separateNetlistInfo(data)
                print "SubOptionInfo------------------->",subOptionInfo
                print "SubSchemInfo-------------------->",subSchemInfo
                if len(subOptionInfo) > 0:
                    newline = subOptionInfo[0]
                    subInitLine = newline
                    newline = newline.split('.subckt')       
                    intLine = newline[1].split()
                    for i in range(0,len(intLine),1):
                        nodeSubInterface.append(intLine[i])
                    
                subModel, subModelInfo, subsubName, subParamInfo,subinbuiltmodelName, subinbuiltmodelInfo = self.addModel(subOptionInfo)
                print "Sub Model------------------------------------>",subModel
                print "SubModelInfo---------------------------------->",subModelInfo
                print "subsubName------------------------------------->",subsubName
                print "subParamInfo----------------------------------->",subParamInfo
                IfMOSsub = '0'
                for eachline in subSchemInfo:
                    #words = eachline.split()
                    if eachline[0] == 'm':
                        IfMOSsub = '1'
                        break
                subsubOptionInfo = []
                subsubSchemInfo = []
                if len(subsubName) > 0:
                    #subsubOptionInfo = []
                    #subsubSchemInfo = []
                    for eachsub in subsubName:
                        filename_stemp = eachsub + '.sub'
                        data = self.readNetlist(filename_stemp)
                        subsubOptionInfo, subsubSchemInfo = self.separateNetlistInfo(data)
                        for eachline in subsubSchemInfo:
                            #words = eachline.split()
                            if eachline[0] == 'm':
                                IfMOSsub = '1'
                                break
                print "subsubOptionInfo-------------------------->",subsubOptionInfo
                print "subsubSchemInfo-------------------------->",subsubSchemInfo
                
                modelicaSubParam =  self.processParam(subParamInfo)
                print "modelicaSubParam------------------->",modelicaSubParam
                nodeSub, nodeDicSub, pinInitSub, pinProtectedInitSub = self.nodeSeparate(subSchemInfo, '1', eachsub, subsubName,numNodesSub)
                print "NodeSub------------------------->",nodeSub
                print "NodeDicSub-------------------------->",nodeDicSub
                print "PinInitSub-------------------------->",pinInitSub
                print "PinProtectedInitSub------------------->",pinProtectedInitSub
                modelicaSubCompInit, numNodesSubsub = self.compInit(subSchemInfo, nodeSub, subModelInfo, subsubName)
                print "modelicaSubCompInit--------------------->",modelicaSubCompInit
                print "numNodesSubsub-------------------------->",numNodesSubsub
                modelicaSubParamNew = self.getSubParamLine(eachsub, numNodesSub, modelicaSubParam)     ###Ask Manas
                print "modelicaSubParamNew----------------->",modelicaSubParamNew
                connSubInfo = self.connectInfo(subSchemInfo, nodeSub, nodeDicSub, numNodesSubsub,subcktName)
                newname = filename.split('.')
                newfilename = newname[0]
                outfilename = newfilename+ ".mo"
                out = open(outfilename,"w")
                out.writelines('model ' + os.path.basename(newfilename))
                out.writelines('\n')
                if IfMOSsub == '0':
                    out.writelines('import Modelica.Electrical.*;')
                elif IfMOSsub == '1':
                    out.writelines('import BondLib.Electrical.*;')
                out.writelines('\n') 
                for eachline in modelicaSubParamNew:
                    if len(subParamInfo) == 0:
                        continue
                    else:
                        out.writelines(eachline) 
                        out.writelines('\n')
                for eachline in modelicaSubCompInit:
                    if len(subSchemInfo) == 0:
                        continue
                    else:
                        out.writelines(eachline)
                        out.writelines('\n')
                        
                out.writelines(pinProtectedInitSub)
                out.writelines('\n')
                if pinInitSub != 'Modelica.Electrical.Analog.Interfaces.Pin ;':
                    out.writelines('protected')
                    out.writelines('\n')
                    out.writelines(pinInitSub)
                    out.writelines('\n')
                out.writelines('equation')
                out.writelines('\n')
                for eachline in connSubInfo:
                    if len(connSubInfo) == 0:
                        continue
                    else:
                        out.writelines(eachline)
                        out.writelines('\n')
                out.writelines('end '+ os.path.basename(newfilename) + ';')
                out.writelines('\n')
                out.close()
            
        return data, subOptionInfo, subSchemInfo, subModel, subModelInfo, subsubName, \
            subParamInfo, modelicaSubCompInit, modelicaSubParam, nodeSubInterface, nodeSub, nodeDicSub, pinInitSub, connSubInfo         
                                 
    

def main(args):
    """
    It is main function of module Ngspice to Modelica converter
    """
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        print "USAGE:"
        print "python NgspicetoModelica.py <filename>"
        sys.exit()
    
    obj_NgMoConverter = NgMoConverter()
    
    #Getting all the require information
    lines = obj_NgMoConverter.readNetlist(filename)
    #print "Complete Lines of Ngspice netlist :lines ---------------->",lines
    optionInfo, schematicInfo=obj_NgMoConverter.separateNetlistInfo(lines)
    #print "All option details like analysis,subckt,.ic,.model  : OptionInfo------------------->",optionInfo
    #print "Schematic connection info :schematicInfo",schematicInfo
    modelName, modelInfo, subcktName, paramInfo, inbuiltmodelName, inbuiltmodelInfo = obj_NgMoConverter.addModel(optionInfo)
    print "Name of Model : modelName-------------------->",modelName
    print "Model Information :modelInfo--------------------->",modelInfo
    print "Subcircuit Name :subcktName------------------------>",subcktName
    print "Parameter Information :paramInfo---------------------->",paramInfo
    print "Ngspice inbuiltmodelName :inbuiltmodelName---------------------->",inbuiltmodelName
    print "Ngspice inbuiltmodelInfo :inbuiltmodelInfo----------------------->",inbuiltmodelInfo
    
    
    modelicaParamInit = obj_NgMoConverter.processParam(paramInfo)
    #print "Make modelicaParamInit from paramInfo  :processParamInit------------->",modelicaParamInit 
    compInfo, plotInfo = obj_NgMoConverter.separatePlot(schematicInfo)
    #print "Info like run etc  : CompInfo----------------->",compInfo
    #print "Plot info like plot,print etc :plotInfo",plotInfo
    IfMOS = '0'
    
    for eachline in compInfo:
        words = eachline.split()
        if eachline[0] == 'm':
            IfMOS = '1'
            break
    subOptionInfo = []
    subSchemInfo = []
    if len(subcktName) > 0:
        #subOptionInfo = []
        #subSchemInfo = []
        for eachsub in subcktName:
            filename_temp = eachsub + '.sub'
            data = obj_NgMoConverter.readNetlist(filename_temp)
            subOptionInfo, subSchemInfo = obj_NgMoConverter.separateNetlistInfo(data)
            for eachline in subSchemInfo:
                words = eachline.split()
                if eachline[0] == 'm':
                    IfMOS = '1'
                    break
    #print "Subcircuit OptionInfo : subOptionInfo------------------->",subOptionInfo
    #print "Subcircuit Schematic Info :subSchemInfo-------------------->",subSchemInfo
                
    node, nodeDic, pinInit, pinProtectedInit = obj_NgMoConverter.nodeSeparate(compInfo, '0', [], subcktName,[])
    print "All nodes in the netlist :node---------------->",node
    print "NodeDic which will be used for modelica : nodeDic------------->",nodeDic
    print "PinInit-------------->",pinInit
    print "pinProtectedInit----------->",pinProtectedInit
    
    modelicaCompInit, numNodesSub  = obj_NgMoConverter.compInit(compInfo,node, modelInfo, subcktName)
    print "ModelicaComponents : modelicaCompInit----------->",modelicaCompInit
    print "SubcktNumNodes : numNodesSub---------------->",numNodesSub
    
    connInfo = obj_NgMoConverter.connectInfo(compInfo, node, nodeDic, numNodesSub,subcktName)
    
    print "ConnInfo------------------>",connInfo
    
    
    ###After Sub Ckt Func
    if len(subcktName) > 0:
        data, subOptionInfo, subSchemInfo, subModel, subModelInfo, subsubName,subParamInfo, modelicaSubCompInit, modelicaSubParam,\
        nodeSubInterface,nodeSub, nodeDicSub, pinInitSub, connSubInfo = obj_NgMoConverter.procesSubckt(subcktName,numNodesSub) #Adding 'numNodesSub' by Fahim
    
    #Creating Final Output file
    newfile = filename.split('.')
    newfilename = newfile[0]
    outfile = newfilename + ".mo"
    out = open(outfile,"w")
    out.writelines('model ' + os.path.basename(newfilename))
    out.writelines('\n')
    if IfMOS == '0':
        out.writelines('import Modelica.Electrical.*;')
    elif IfMOS == '1':
        out.writelines('import BondLib.Electrical.*;')
        #out.writelines('import Modelica.Electrical.*;')
    out.writelines('\n')
    
    for eachline in modelicaParamInit:
        if len(paramInfo) == 0:
            continue
        else:
            out.writelines(eachline)
            out.writelines('\n')
    for eachline in modelicaCompInit:
        if len(compInfo) == 0:
            continue
        else:
            out.writelines(eachline)
            out.writelines('\n')
    
    out.writelines('protected')
    out.writelines('\n')
    out.writelines(pinInit)
    out.writelines('\n')
    out.writelines('equation')
    out.writelines('\n')
    
    for eachline in connInfo:
        if len(connInfo) == 0:
            continue
        else:
            out.writelines(eachline)
            out.writelines('\n')
            
    out.writelines('end '+ os.path.basename(newfilename) + ';')
    out.writelines('\n')


    out.close()
    

# Call main function
if __name__ == '__main__':
    main(sys.argv)