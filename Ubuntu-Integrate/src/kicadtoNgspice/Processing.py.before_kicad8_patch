import sys
import os
from xml.etree import ElementTree as ET


class PrcocessNetlist:
    """
    - This class include all the function required for pre-proccessing of
      netlist before converting to Ngspice Netlist.
    """
    init_path = '../../'
    if os.name == 'nt':
        init_path = ''

    modelxmlDIR = init_path + 'library/modelParamXML'

    def __init__(self):
        pass

    def readNetlist(self, filename):
        """
        - Read the circuit file and return splitted lines
        """
        f = open(filename)
        data = f.read()
        f.close()
        # print("=============================================================")
        # print("readNetList called, from Processing")
        # print("=============================================================")
        # print("NETLIST", data.splitlines())
        # print("=============================================================")
        return data.splitlines()

    def readParamInfo(self, kicadNetlist):
        """
        - Read Parameter information and store it into dictionary
        - kicadNetlist is the .cir file content
        """
        param = {}
        # print("=========================KICADNETLIST========================")
        for eachline in kicadNetlist:
            print(eachline)
            eachline = eachline.strip()
            if len(eachline) > 1:
                words = eachline.split()
                option = words[0].lower()
                if option == '.param':
                    for i in range(1, len(words), 1):
                        paramList = words[i].split('=')
                        param[paramList[0]] = paramList[1]
        # print("=============================================================")
        # print("readParamInfo called, from Processing")
        # print("=============================================================")
        # print("PARAM", param)
        # print("=============================================================")
        return param

    def preprocessNetlist(self, kicadNetlist, param):
        """
        - Preprocess netlist (replace parameters)
        - Separate infoline (first line) from the rest of netlist
        """
        netlist = []
        for eachline in kicadNetlist:
            # Remove leading and trailing blanks spaces from line
            eachline = eachline.strip()
            # Remove special character $
            eachline = eachline.replace('$', '')
            # Replace parameter with values
            for subParam in eachline.split():
                if '}' in subParam:
                    key = subParam.split()[0]
                    key = key.strip('{')
                    key = key.strip('}')
                    if key in param:
                        eachline = eachline.replace(
                            '{' + key + '}', param[key])
                    else:
                        print("Parameter " + key + " does not exists")
                        value = input('Enter parameter value: ')
                        eachline = eachline.replace('{' + key + '}', value)
            # Convert netlist into lower case letter
            eachline = eachline.lower()
            # Construct netlist
            if len(eachline) > 1:
                if eachline[0] == '+':
                    netlist.append(netlist.pop() + eachline.replace('+', ' '))
                else:
                    netlist.append(eachline)
        # Copy information line
        infoline = netlist[0]
        netlist.remove(netlist[0])
        """print("=============================================================")
        print("preprocessNetList called, from Processing")
        print("=============================================================")
        print("NETLIST", netlist)
        print("INFOLINE", infoline)
        print("===========================================================")"""
        return netlist, infoline

    def separateNetlistInfo(self, netlist):
        """
        - Remove the options such as .end, .param, starting wtih "."
          from the netlist file
        - This is stored as option info, whereas rest is stored as
          schematicInfo
        - Rest from the `* Sheet Name:` line stored as schematicInfo
        """
        optionInfo = []
        schematicInfo = []
        for eachline in netlist:
            if eachline[0] == '*':
                continue
            elif eachline[0] == '.':
                optionInfo.append(eachline)
            else:
                schematicInfo.append(eachline)
        """print("=============================================================")
        print("separateNetlistInfo called, from Processing")
        print("=============================================================")
        print("OPTIONINFO", optionInfo)
        print("SCHEMATICINFO", schematicInfo)
        print("===========================================================")"""
        return optionInfo, schematicInfo

    def insertSpecialSourceParam(self, schematicInfo, sourcelist):
        """
        - Insert Special source parameter
        - As per the parameters passed create source list, start with v or i
        - Then check for type whether ac, dc, sine, etc...
        - Handle starting with h and f as well
        """
        schematicInfo1 = []
        # print("=============================================================")
        # print("Reading schematic info for source details")
        # print("=============================================================")
        for compline in schematicInfo:
            words = compline.split()
            compName = words[0]
            # Ask for parameters of source
            if compName[0] == 'v' or compName[0] == 'i':
                # Find the index component from circuit
                index = schematicInfo.index(compline)
                if words[3] == "pulse":
                    Title = "Add parameters for pulse source " + compName
                    v1 = '  Enter initial value (Volts/Amps): '
                    v2 = '  Enter pulsed value (Volts/Amps): '
                    td = '  Enter delay time (seconds): '
                    tr = '  Enter rise time (seconds): '
                    tf = '  Enter fall time (seconds): '
                    pw = '  Enter pulse width (seconds): '
                    tp = '  Enter period (seconds): '
                    sourcelist.append(
                        [index, compline, words[3],
                         Title, v1, v2, td, tr, tf, pw, tp])

                elif words[3] == "sine":
                    Title = "Add parameters for sine source " + compName
                    vo = '  Enter offset value (Volts/Amps): '
                    va = '  Enter amplitude (Volts/Amps): '
                    freq = '  Enter frequency (Hz): '
                    td = '  Enter delay time (seconds): '
                    theta = '  Enter damping factor (1/seconds): '
                    sourcelist.append(
                        [index, compline, words[3],
                         Title, vo, va, freq, td, theta])

                elif words[3] == "pwl":
                    Title = "Add parameters for pwl source " + compName
                    t_v = ' Enter in pwl format without bracket\
                     i.e t1 v1 t2 v2.... '
                    sourcelist.append([index, compline, words[3], Title, t_v])

                elif words[3] == "ac":
                    Title = "Add parameters for ac source " + compName
                    v_a = '  Enter amplitude (Volts/Amps): '
                    p_a = '  Enter Phase Shift: '
                    sourcelist.append(
                        [index, compline, words[3], Title, v_a, p_a])

                elif words[3] == "exp":
                    Title = "Add parameters for exponential source " + compName
                    v1 = '  Enter initial value (Volts/Amps): '
                    v2 = '  Enter pulsed value (Volts/Amps): '
                    td1 = '  Enter rise delay time (seconds): '
                    tau1 = '  Enter rise time constant (seconds):     '
                    td2 = '  Enter fall time (seconds): '
                    tau2 = '  Enter fall time constant (seconds): '
                    sourcelist.append(
                        [index, compline, words[3],
                         Title, v1, v2, td1, tau1, td2, tau2])

                elif words[3] == "dc":
                    Title = "Add parameters for DC source " + compName
                    v1 = '  Enter value (Volts/Amps): '
                    v2 = '  Enter zero frequency: '
                    sourcelist.append(
                        [index, compline, words[3], Title, v1, v2])

            elif compName[0] == 'h' or compName[0] == 'f':
                # Find the index component from the circuit
                index = schematicInfo.index(compline)
                schematicInfo.remove(compline)
                schematicInfo.insert(index, "* " + compName)
                schematicInfo1.append(
                    "V" + compName + " " + words[3] + " " + words[4] + " 0")
                schematicInfo1.append(
                    compName +
                    " " +
                    words[1] +
                    " " +
                    words[2] +
                    " " +
                    "V" +
                    compName +
                    " " +
                    words[5])

        schematicInfo = schematicInfo + schematicInfo1
        # print("Source List : ", sourcelist)

        """print("=============================================================")
        print("insertSpecialSourceParam called, from Processing")
        print("=============================================================")
        print("SCHEMATICINFO", schematicInfo)
        print("SOURCELIST", sourcelist)
        print("===========================================================")"""
        return schematicInfo, sourcelist

    def convertICintoBasicBlocks(
            self, schematicInfo, outputOption, modelList, plotText):
        """
        - Parses the schematicInfo and returns
        - - SchematicInfo
        - - Output Option
        - - Model List
        - - Unkown Model List
        - - Multiple Model List
        - - Plot text
        - Parsing info is provided below
        """
        # print("=============================================================")
        # print("Reading Schematic info for Model")
        # Insert details of Ngspice model
        unknownModelList = []
        multipleModelList = []
        plotList = [
            'plot_v1',
            'plot_v2',
            'plot_i2',
            'plot_log',
            'plot_db',
            'plot_phase']
        interMediateNodeCount = 1
        k = 1
        for compline in schematicInfo:
            words = compline.split()
            compName = words[0]
            # print "Compline----------------->",compline
            # print "compName-------------->",compName
            # Find the IC from schematic
            if compName[0] == 'u' or compName[0] == 'U':
                # Find the component from the circuit
                index = schematicInfo.index(compline)
                compType = words[len(words) - 1]
                schematicInfo.remove(compline)
                paramDict = {}
                # e.g compLine : u1 1 2 gain
                # compType : gain
                # compName : u1
                # print "Compline",compline
                # print "CompType",compType
                # print "Words",words
                # print "compName",compName
                # Looking if model file is present
                if compType != "port" and compType != "ic" and \
                        compType not in plotList and \
                        compType != 'transfo':
                    xmlfile = compType + ".xml"  # XML Model File
                    count = 0  # Check if model of same name is present
                    modelPath = []
                    all_dir = [x[0]
                               for x in os.walk(PrcocessNetlist.modelxmlDIR)]
                    for each_dir in all_dir:
                        all_file = os.listdir(each_dir)
                        if xmlfile in all_file:
                            count += 1
                            modelPath.append(os.path.join(each_dir, xmlfile))

                    if count > 1:
                        multipleModelList.append(modelPath)
                    elif count == 0:
                        unknownModelList.append(compType)
                    elif count == 1:
                        try:
                            # print("==========================================\
                            #     ===========================")
                            print(
                                "Start Parsing Previous Values XML\
                                 for ngspice model :", modelPath)
                            tree = ET.parse(modelPath[0])

                            # Getting number of nodes for model and title
                            for child in tree.iter():
                                if child.tag == 'node_number':
                                    num_of_nodes = int(child.text)
                                elif child.tag == 'title':
                                    title = child.text + " " + compName
                                elif child.tag == 'name':
                                    modelname = child.text
                                elif child.tag == 'type':
                                    # Checking for Analog and Digital
                                    type = child.text
                                elif child.tag == 'split':
                                    splitDetail = child.text

                            for param in tree.findall('param'):
                                for item in param:
                                    # print "Tags ",item.tag
                                    # print "Value",item.text
                                    if 'vector' in item.attrib:
                                        # print "Tag having vector attribute",\
                                        # item.tag,item.attrib['vector']
                                        temp_count = 1
                                        temp_list = []
                                        for i in range(0, int(
                                                item.attrib['vector'])):
                                            temp_list.append(
                                                item.text + " " + str(
                                                    temp_count))
                                            temp_count += 1
                                        if 'default' in item.attrib:
                                            paramDict[item.tag + ":" +
                                                      item.attrib['default']] \
                                                = temp_list
                                        else:
                                            paramDict[item.tag] = item.text

                                    else:
                                        if 'default' in item.attrib:
                                            paramDict[item.tag + ":" +
                                                      item.attrib['default']]\
                                                = item.text
                                        else:
                                            paramDict[item.tag] = item.text

                            # print "Number of Nodes : ",num_of_nodes
                            # print "Title : ",title
                            # print "Parameters",paramDict
                            # Creating line for adding model line in schematic
                            if splitDetail == 'None':
                                modelLine = "a" + str(k) + " "
                                for i in range(1, num_of_nodes + 1):
                                    modelLine += words[i] + " "
                                modelLine += compName

                            else:
                                # print("=====================================\
                                #     ================================")
                                # print("Split Details :", splitDetail)
                                modelLine = "a" + str(k) + " "
                                vectorDetail = splitDetail.split(':')
                                # print "Vector Details",vectorDetail
                                pos = 1  # Node position
                                for item in vectorDetail:
                                    try:
                                        if item.split("-")[1] == 'V':
                                            # print "Vector"
                                            if compType == "aswitch":
                                                modelLine += "("
                                                for i in range(0, int(
                                                        item.split("-")[0])):
                                                    modelLine += words[pos] +\
                                                        " "
                                                    pos += 1
                                                modelLine += ") "
                                            else:
                                                modelLine += "["
                                                for i in range(0, int(
                                                        item.split("-")[0])):
                                                    modelLine += words[pos] + \
                                                        " "
                                                    pos += 1
                                                modelLine += "] "
                                        elif item.split("-")[1] == 'NV':
                                            # print "Non Vector"
                                            for i in range(0, int(
                                                    item.split("-")[0])):
                                                modelLine += words[pos] + " "
                                                pos += 1

                                    except BaseException:
                                        print(
                                            "There is error while processing\
                                             Vector Details")
                                        sys.exit(2)
                                modelLine += compName

                            # print "Final Model Line :",modelLine
                            try:
                                schematicInfo.append(modelLine)
                                k = k + 1
                            except Exception as e:
                                print(
                                    "Error while appending \
                                    ModelLine ", modelLine)
                                print("Exception Message : ", str(e))
                            # Insert comment at remove line
                            schematicInfo.insert(index, "* " + compline)
                            comment = "* Schematic Name:\
                             " + compType + ", Ngspice Name: " + modelname
                            # Here instead of adding compType(use for XML),
                            # added modelName(Unique Model Name)
                            modelList.append(
                                [index, compline, modelname, compName,
                                 comment, title, type, paramDict])
                        except Exception as e:
                            print(
                                "Unable to parse the model, \
                                Please check your your XML file")
                            print("Exception Message : ", str(e))
                            sys.exit(2)
                elif compType == "ic":
                    schematicInfo.insert(index, "* " + compline)
                    modelname = "ic"
                    comment = "* " + compline
                    title = "Initial Condition for " + compName
                    type = "NA"  # Its is not model
                    text = "Enter initial voltage at node for " + compline
                    paramDict[title] = text
                    modelList.append(
                        [index, compline, modelname, compName,
                         comment, title, type, paramDict])

                elif compType in plotList:
                    schematicInfo.insert(index, "* " + compline)
                    if compType == 'plot_v1':
                        words = compline.split()
                        plotText.append("plot v(" + words[1] + ")")
                    elif compType == 'plot_v2':
                        words = compline.split()
                        plotText.append(
                            "plot v(" + words[1] + "," + words[2] + ")")
                    elif compType == 'plot_i2':
                        words = compline.split()
                        # Adding zero voltage source to netlist
                        schematicInfo.append(
                            "v_" + words[0] + " " +
                            words[1] + " " + words[2] + " " + "0")
                        plotText.append("plot i(v_" + words[0] + ")")
                    elif compType == 'plot_log':
                        words = compline.split()
                        plotText.append("plot log(" + words[1] + ")")
                    elif compType == 'plot_db':
                        words = compline.split()
                        plotText.append("plot db(" + words[1] + ")")
                    elif compType == 'plot_phase':
                        words = compline.split()
                        plotText.append("plot phase(" + words[1] + ")")

                elif compType == 'transfo':
                    schematicInfo.insert(index, "* " + compline)

                    # For Primary Couple
                    modelLine = (
                        "a" + str(k) + " (" + words[1] + " " +
                        words[2] + ") (interNode_" +
                        str(interMediateNodeCount) + " " + words[3] + ") "
                    )
                    modelLine += compName + "_primary"
                    schematicInfo.append(modelLine)
                    k = k + 1
                    # For iron core
                    modelLine = "a" + str(k) + " (" + words[4] + " " + \
                        words[2] + ") (interNode_" + \
                        str(interMediateNodeCount + 1) + " " + words[3] + ") "
                    modelLine += compName + "_secondary"
                    schematicInfo.append(modelLine)
                    k = k + 1
                    # For Secondary Couple
                    modelLine = "a" + str(k) + " (interNode_" + str(
                        interMediateNodeCount) + " interNode_" + \
                        str(interMediateNodeCount + 1) + ") "
                    modelLine += compName + "_iron_core"
                    schematicInfo.append(modelLine)
                    k = k + 1
                    interMediateNodeCount += 2

                    modelname = "transfo"
                    comment = "* " + compline
                    title = "Transformer details for model " + compName
                    type = "NA"
                    # It is model but do not load from xml and lib file
                    paramDict['h1_array'] = "Enter the H1 array "
                    paramDict['primary_turns'] = "Enter the primary number \
                    of turns (default=310) "
                    paramDict['area'] = "Enter iron core area (default=1)"
                    paramDict['secondar_turns'] = "Enter the secondary number\
                     of turns (default=620)"
                    paramDict['length'] = "Enter iron core length \
                    (default=0.01)"
                    paramDict['b1_array'] = "Enter the B1 array "

                    modelList.append(
                        [index, compline, modelname, compName,
                         comment, title, type, paramDict])

                else:
                    schematicInfo.insert(index, "* " + compline)
                # print("=====================================================")
                print(
                    "UnknownModelList Used in the Schematic",
                    unknownModelList)
                print("=====================================================")
                print(
                    "Multiple Model XML file with same name ",
                    multipleModelList)
                print("=====================================================")
                # print("Model List Details : ", modelList)
        print("=============================================================")
        print("convertICIntoBasicBlocks called, from Processing")
        print("=============================================================")
        print("SCHEMATICINFO", schematicInfo)
        print("OUTPUTOPTION", outputOption)
        print("MODELLIST", modelList)
        print("UNKOWNMODELLIST", unknownModelList)
        print("MULTIPLEMODELLIST", multipleModelList)
        print("PLOTTEST", plotText)
        print("=============================================================")
        return (
            schematicInfo, outputOption, modelList, unknownModelList,
            multipleModelList, plotText
        )
