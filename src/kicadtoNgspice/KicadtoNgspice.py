# =========================================================================
#
#          FILE: kicadtoNgspice.py
#
#         USAGE: ---
#
#   DESCRIPTION: This define all configuration used in Application.
#
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Fahim Khan, fahim.elex@gmail.com
#  ORGANIZATION: eSim team at FOSSEE, IIT Bombay.
#       CREATED: Wednesday 04 March 2015
#      REVISION:  ---
# =========================================================================
import sys
import os
from PyQt4 import QtGui
from .Processing import PrcocessNetlist
from . import Analysis
from . import Source
from . import Model
from . import DeviceModel
from . import SubcircuitTab
from . import Convert
from . import TrackWidget
import json

# from xml.etree import ElementTree as ET


class MainWindow(QtGui.QWidget):
    """
    - This class create KicadtoNgspice window.
    - And Call Convert function if convert button is pressed.
    - The convert function takes all the value entered by user and create
      a final netlist "*.cir.out".
    - This final netlist is compatible with NgSpice.
    - clarg1 is the path to the .cir file
    - clarg2 is either None or "sub" depending on the analysis type
    """

    def __init__(self, clarg1, clarg2=None):
        QtGui.QWidget.__init__(self)
        print("==================================")
        print("Kicad to Ngspice netlist converter ")
        print("==================================")
        global kicadNetlist, schematicInfo
        global infoline, optionInfo
        self.kicadFile = clarg1
        self.clarg1 = clarg1
        self.clarg2 = clarg2

        # Create object of track widget
        # Track the dynamically created widget of KicadtoNgSpice Window
        self.obj_track = TrackWidget.TrackWidget()

        # Clear Dictionary/List item of sub circuit and ngspice model
        # Dictionary
        self.obj_track.subcircuitList.clear()
        self.obj_track.subcircuitTrack.clear()
        self.obj_track.model_entry_var.clear()
        # List
        self.obj_track.modelTrack[:] = []

        # Object of Processing
        obj_proc = PrcocessNetlist()

        # Read the netlist, ie the .cir file
        kicadNetlist = obj_proc.readNetlist(self.kicadFile)
        print("=============================================================")
        print("Given Kicad Schematic Netlist Info :", kicadNetlist)

        # Construct parameter information
        param = obj_proc.readParamInfo(kicadNetlist)

        # Replace parameter with values
        netlist, infoline = obj_proc.preprocessNetlist(kicadNetlist, param)
        print("=============================================================")
        print("Schematic Info after processing Kicad Netlist: ", netlist)
        # print "INFOLINE",infoline

        # Separate option and schematic information
        optionInfo, schematicInfo = obj_proc.separateNetlistInfo(netlist)
        print("=============================================================")
        print("OPTIONINFO in the Netlist", optionInfo)

        # List for storing source and its value
        global sourcelist, sourcelisttrack
        sourcelist = []
        sourcelisttrack = []
        schematicInfo, sourcelist = obj_proc.insertSpecialSourceParam(
            schematicInfo, sourcelist)

        # List storing model detail
        global modelList, outputOption,\
            unknownModelList, multipleModelList, plotText

        modelList = []
        outputOption = []
        plotText = []
        (
            schematicInfo,
            outputOption,
            modelList,
            unknownModelList,
            multipleModelList,
            plotText
            ) = obj_proc.convertICintoBasicBlocks(
            schematicInfo, outputOption, modelList, plotText
        )
        print("=======================================")
        print("Model available in the Schematic :", modelList)

        """
        Checking if any unknown model is used in schematic which is not
        recognized by NgSpice.
        Also if the two model of same name is present under
        modelParamXML directory
        """
        if unknownModelList:
            print("Unknown Model List is : ", unknownModelList)
            self.msg = QtGui.QErrorMessage()
            self.content = "Your schematic contain unknown model " + \
                ', '.join(unknownModelList)
            self.msg.showMessage(self.content)
            self.msg.setWindowTitle("Unknown Models")

        elif multipleModelList:
            self.msg = QtGui.QErrorMessage()
            self.mcontent = "Look like you have duplicate model in \
            modelParamXML directory " + \
                ', '.join(multipleModelList[0])
            self.msg.showMessage(self.mcontent)
            self.msg.setWindowTitle("Multiple Models")

        else:
            self.createMainWindow()

    """
    This function create main window of Kicad to Ngspice converter
    """

    def createMainWindow(self):
        self.vbox = QtGui.QVBoxLayout(self)
        self.hbox = QtGui.QHBoxLayout(self)
        self.hbox.addStretch(1)
        self.convertbtn = QtGui.QPushButton("Convert")
        self.convertbtn.clicked.connect(self.callConvert)
        self.hbox.addWidget(self.convertbtn)
        self.vbox.addWidget(self.createcreateConvertWidget())
        self.vbox.addLayout(self.hbox)

        self.setLayout(self.vbox)
        self.setWindowTitle("Kicad To NgSpice Converter")
        self.show()

    def createcreateConvertWidget(self):
        global obj_analysis
        self.convertWindow = QtGui.QWidget()
        self.analysisTab = QtGui.QScrollArea()
        obj_analysis = Analysis.Analysis(self.clarg1)
        self.analysisTab.setWidget(obj_analysis)
        # self.analysisTabLayout = QtGui.QVBoxLayout(self.analysisTab.widget())
        self.analysisTab.setWidgetResizable(True)
        global obj_source
        self.sourceTab = QtGui.QScrollArea()
        obj_source = Source.Source(sourcelist, sourcelisttrack, self.clarg1)
        self.sourceTab.setWidget(obj_source)
        # self.sourceTabLayout = QtGui.QVBoxLayout(self.sourceTab.widget())
        self.sourceTab.setWidgetResizable(True)
        global obj_model
        self.modelTab = QtGui.QScrollArea()
        obj_model = Model.Model(schematicInfo, modelList, self.clarg1)
        self.modelTab.setWidget(obj_model)
        # self.modelTabLayout = QtGui.QVBoxLayout(self.modelTab.widget())
        self.modelTab.setWidgetResizable(True)
        global obj_devicemodel
        self.deviceModelTab = QtGui.QScrollArea()
        obj_devicemodel = DeviceModel.DeviceModel(schematicInfo, self.clarg1)
        self.deviceModelTab.setWidget(obj_devicemodel)
        self.deviceModelTab.setWidgetResizable(True)
        global obj_subcircuitTab
        self.subcircuitTab = QtGui.QScrollArea()
        obj_subcircuitTab = SubcircuitTab.SubcircuitTab(
            schematicInfo, self.clarg1)
        self.subcircuitTab.setWidget(obj_subcircuitTab)
        self.subcircuitTab.setWidgetResizable(True)

        self.tabWidget = QtGui.QTabWidget()
        # self.tabWidget.TabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.addTab(self.analysisTab, "Analysis")
        self.tabWidget.addTab(self.sourceTab, "Source Details")
        self.tabWidget.addTab(self.modelTab, "NgSpice Model")
        self.tabWidget.addTab(self.deviceModelTab, "Device Modeling")
        self.tabWidget.addTab(self.subcircuitTab, "Subcircuits")
        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.addWidget(self.tabWidget)
        # self.mainLayout.addStretch(1)
        self.convertWindow.setLayout(self.mainLayout)
        self.convertWindow.show()

        return self.convertWindow

    def callConvert(self):
        """
        Calling Convert Class Constructor
        """
        global schematicInfo
        global analysisoutput
        global kicad
        store_schematicInfo = list(schematicInfo)
        (projpath, filename) = os.path.split(self.kicadFile)
        project_name = os.path.basename(projpath)

        fw = open(
            os.path.join(
                projpath,
                project_name +
                "_Previous_Values.json"),
            'w')
        json_data = {}

        """
        Writing Analysis values
        """

        json_data["analysis"] = {}

        json_data["analysis"]["ac"] = {}
        if obj_analysis.Lin.isChecked():
            json_data["analysis"]["ac"]["Lin"] = "true"
            json_data["analysis"]["ac"]["Dec"] = "false"
            json_data["analysis"]["ac"]["Oct"] = "false"
        elif obj_analysis.Dec.isChecked():
            json_data["analysis"]["ac"]["Lin"] = "false"
            json_data["analysis"]["ac"]["Dec"] = "true"
            json_data["analysis"]["ac"]["Oct"] = "false"
        if obj_analysis.Oct.isChecked():
            json_data["analysis"]["ac"]["Lin"] = "false"
            json_data["analysis"]["ac"]["Dec"] = "false"
            json_data["analysis"]["ac"]["Oct"] = "true"
        else:
            pass

        json_data["analysis"]["ac"]["Start Frequency"] = str(
            obj_analysis.ac_entry_var[0].text())
        json_data["analysis"]["ac"]["Stop Frequency"] = str(
            obj_analysis.ac_entry_var[1].text())
        json_data["analysis"]["ac"]["No. of points"] = str(
            obj_analysis.ac_entry_var[2].text())
        json_data["analysis"]["ac"]["Start Fre Combo"] = (
            obj_analysis.ac_parameter[0]
        )
        json_data["analysis"]["ac"]["Stop Fre Combo"] = (
            obj_analysis.ac_parameter[1]
        )

        json_data["analysis"]["dc"] = {}
        json_data["analysis"]["dc"]["Source 1"] = str(
            obj_analysis.dc_entry_var[0].text())
        json_data["analysis"]["dc"]["Start"] = str(
            obj_analysis.dc_entry_var[1].text())
        json_data["analysis"]["dc"]["Increment"] = str(
            obj_analysis.dc_entry_var[2].text())
        json_data["analysis"]["dc"]["Stop"] = str(
            obj_analysis.dc_entry_var[3].text())
        json_data["analysis"]["dc"]["Operating Point"] = str(
            self.obj_track.op_check[-1])
        json_data["analysis"]["dc"]["Start Combo"] = (
            obj_analysis.dc_parameter[0]
        )
        json_data["analysis"]["dc"]["Increment Combo"] = (
            obj_analysis.dc_parameter[1]
        )
        json_data["analysis"]["dc"]["Stop Combo"] = (
            obj_analysis.dc_parameter[2]
        )
        json_data["analysis"]["dc"]["Source 2"] = str(
            obj_analysis.dc_entry_var[4].text())
        json_data["analysis"]["dc"]["Start2"] = str(
            obj_analysis.dc_entry_var[5].text())
        json_data["analysis"]["dc"]["Increment2"] = str(
            obj_analysis.dc_entry_var[6].text())
        json_data["analysis"]["dc"]["Stop2"] = str(
            obj_analysis.dc_entry_var[7].text())
        json_data["analysis"]["dc"]["Start Combo2"] = (
            obj_analysis.dc_parameter[3]
        )
        json_data["analysis"]["dc"]["Increment Combo2"] = (
            obj_analysis.dc_parameter[4]
        )
        json_data["analysis"]["dc"]["Stop Combo2"] = (
            obj_analysis.dc_parameter[5]
        )

        json_data["analysis"]["tran"] = {}
        json_data["analysis"]["tran"]["Start Time"] = str(
            obj_analysis.tran_entry_var[0].text())
        json_data["analysis"]["tran"]["Step Time"] = str(
            obj_analysis.tran_entry_var[1].text())
        json_data["analysis"]["tran"]["Stop Time"] = str(
            obj_analysis.tran_entry_var[2].text())
        json_data["analysis"]["tran"]["Start Combo"] = (
            obj_analysis.tran_parameter[0]
        )
        json_data["analysis"]["tran"]["Step Combo"] = (
            obj_analysis.tran_parameter[1]
        )
        json_data["analysis"]["tran"]["Stop Combo"] = (
            obj_analysis.tran_parameter[2]
        )

        """
        Writing Source values
        """

        json_data["source"] = {}
        count = 1

        for line in store_schematicInfo:
            words = line.split(' ')
            wordv = words[0]

            if wordv[0] == "v" or wordv[0] == "i":
                json_data["source"][wordv] = {}
                json_data["source"][wordv]["type"] = words[len(words) - 1]
                json_data["source"][wordv]["values"] = []

            if words[len(words) - 1] == "ac":
                amp = {"Amplitude": str(obj_source.entry_var[count].text())}
                count += 1
                json_data["source"][wordv]["values"].append(amp)

                phase = {"Phase": str(obj_source.entry_var[count].text())}
                count += 1
                json_data["source"][wordv]["values"].append(phase)

            elif words[len(words) - 1] == "dc":
                value = {"Value": str(obj_source.entry_var[count].text())}
                count += 1
                json_data["source"][wordv]["values"].append(value)

            elif words[len(words) - 1] == "sine":
                offset = {
                    "Offset Value": str(
                        obj_source.entry_var[count].text())}
                count += 1
                json_data["source"][wordv]["values"].append(offset)

                amp = {"Amplitude": str(obj_source.entry_var[count].text())}
                count += 1
                json_data["source"][wordv]["values"].append(amp)

                freq = {"Freuency": str(obj_source.entry_var[count].text())}
                count += 1
                json_data["source"][wordv]["values"].append(freq)

                delay = {"Delay Time": str(obj_source.entry_var[count].text())}
                count += 1
                json_data["source"][wordv]["values"].append(delay)

                damp = {
                    "Damping Factor": str(
                        obj_source.entry_var[count].text())}
                count += 1
                json_data["source"][wordv]["values"].append(damp)

            elif words[len(words) - 1] == "pulse":
                initial = {
                    "Initial Value": str(
                        obj_source.entry_var[count].text())}
                count += 1
                json_data["source"][wordv]["values"].append(initial)

                pulse = {
                    "Pulse Value": str(
                        obj_source.entry_var[count].text())}
                count += 1
                json_data["source"][wordv]["values"].append(pulse)

                delay = {"Delay Time": str(obj_source.entry_var[count].text())}
                count += 1
                json_data["source"][wordv]["values"].append(delay)

                rise = {"Rise Time": str(obj_source.entry_var[count].text())}
                count += 1
                json_data["source"][wordv]["values"].append(rise)

                fall = {"Fall Time": str(obj_source.entry_var[count].text())}
                count += 1
                json_data["source"][wordv]["values"].append(fall)

                width = {
                    "Pulse width": str(
                        obj_source.entry_var[count].text())}
                count += 1
                json_data["source"][wordv]["values"].append(width)

                period = {"Period": str(obj_source.entry_var[count].text())}
                count += 1
                json_data["source"][wordv]["values"].append(period)

            elif words[len(words) - 1] == "pwl":
                pwl = {
                    "Enter in pwl format": str(
                        obj_source.entry_var[count].text())}
                count += 1
                json_data["source"][wordv]["values"].append(pwl)

            elif words[len(words) - 1] == "exp":
                initial = {
                    "Initial Value": str(
                        obj_source.entry_var[count].text())}
                count += 1
                json_data["source"][wordv]["values"].append(initial)

                pulsed = {
                    "Pulsed Value": str(
                        obj_source.entry_var[count].text())}
                count += 1
                json_data["source"][wordv]["values"].append(pulsed)

                rise = {
                    "Rise Delay Time": str(
                        obj_source.entry_var[count].text())}
                count += 1
                json_data["source"][wordv]["values"].append(rise)

                fall = {"Fall Time": str(obj_source.entry_var[count].text())}
                count += 1
                json_data["source"][wordv]["values"].append(fall)

                fallConstant = {
                    "Fall Time Constant": str(
                        obj_source.entry_var[count].text())}
                count += 1
                json_data["source"][wordv]["values"].append(fallConstant)

            else:
                pass

        """
        Writing Model values
        """

        i = 0
        json_data["model"] = {}

        for line in modelList:
            for rand_itr in obj_model.obj_trac.modelTrack:
                if rand_itr[2] == line[2] and rand_itr[3] == line[3]:
                    start = rand_itr[7]
                    end = rand_itr[8]
            i = start

            json_data["model"][line[3]] = {}
            json_data["model"][line[3]]["type"] = line[2]
            json_data["model"][line[3]]["values"] = []

            for key, value in line[7].items():
                if(
                    hasattr(value, '__iter__') and
                    i <= end and type(value) is not
                    str
                ):
                    for item in value:
                        fields = {
                            item: str(
                                obj_model.obj_trac.model_entry_var[i].text())}
                        json_data["model"][line[3]]["values"].append(fields)
                        i = i + 1

                else:
                    fields = {
                        value: str(
                            obj_model.obj_trac.model_entry_var[i].text())}
                    json_data["model"][line[3]]["values"].append(fields)
                    i = i + 1

        """
        Writing Device Model values
        """

        json_data["deviceModel"] = {}

        for device in obj_devicemodel.devicemodel_dict_beg:
            json_data["deviceModel"][device] = []
            it = obj_devicemodel.devicemodel_dict_beg[device]
            end = obj_devicemodel.devicemodel_dict_end[device]

            while it <= end:
                json_data["deviceModel"][device].append(
                    str(obj_devicemodel.entry_var[it].text()))
                it = it + 1

        """
        Writing Subcircuit values
        """

        json_data["subcircuit"] = {}
        for subckt in obj_subcircuitTab.subcircuit_dict_beg:
            json_data["subcircuit"][subckt] = []
            it = obj_subcircuitTab.subcircuit_dict_beg[subckt]
            end = obj_subcircuitTab.subcircuit_dict_end[subckt]

            while it <= end:
                json_data["subcircuit"][subckt].append(
                    str(obj_subcircuitTab.entry_var[it].text()))
                it = it + 1

        write_data = json.dumps(json_data)
        fw.write(write_data)

        self.obj_convert = Convert.Convert(
            self.obj_track.sourcelisttrack["ITEMS"],
            self.obj_track.source_entry_var["ITEMS"],
            store_schematicInfo, self.clarg1
        )

        try:
            # Adding Source Value to Schematic Info
            store_schematicInfo = self.obj_convert.addSourceParameter()
            print("=========================================================")
            print("Netlist After Adding Source details :", store_schematicInfo)

            # Adding Model Value to store_schematicInfo
            store_schematicInfo = self.obj_convert.addModelParameter(
                store_schematicInfo)
            print("=========================================================")
            print("Netlist After Adding Ngspice Model :", store_schematicInfo)

            # Adding Device Library to SchematicInfo
            store_schematicInfo = self.obj_convert.addDeviceLibrary(
                store_schematicInfo, self.kicadFile)
            print("=========================================================")
            print(
                "Netlist After Adding Device Model Library :",
                store_schematicInfo)

            # Adding Subcircuit Library to SchematicInfo
            store_schematicInfo = self.obj_convert.addSubcircuit(
                store_schematicInfo, self.kicadFile)
            print("=========================================================")
            print("Netlist After Adding subcircuits :", store_schematicInfo)

            analysisoutput = self.obj_convert.analysisInsertor(
                self.obj_track.AC_entry_var["ITEMS"],
                self.obj_track.DC_entry_var["ITEMS"],
                self.obj_track.TRAN_entry_var["ITEMS"],
                self.obj_track.set_CheckBox["ITEMS"],
                self.obj_track.AC_Parameter["ITEMS"],
                self.obj_track.DC_Parameter["ITEMS"],
                self.obj_track.TRAN_Parameter["ITEMS"],
                self.obj_track.AC_type["ITEMS"],
                self.obj_track.op_check
            )
            print("=========================================================")
            print("Analysis OutPut ", analysisoutput)

            # Calling netlist file generation function
            self.createNetlistFile(store_schematicInfo, plotText)

            self.msg = "The Kicad to Ngspice Conversion completed\
            successfully!"
            QtGui.QMessageBox.information(
                self, "Information", self.msg, QtGui.QMessageBox.Ok)

        except Exception as e:
            print("Exception Message: ", e)
            print("There was error while converting kicad to ngspice")
            self.close()

        # Generate .sub file from .cir.out file if it is a subcircuit
        subPath = os.path.splitext(self.kicadFile)[0]

        if self.clarg2 == "sub":
            self.createSubFile(subPath)

    def createNetlistFile(self, store_schematicInfo, plotText):
        print("=============================================================")
        print("Creating Final netlist")
        # print "INFOLINE",infoline
        # print "OPTIONINFO",optionInfo
        # print "Device MODEL LIST ",devicemodelList
        # print "SUBCKT ",subcktList
        # print "OUTPUTOPTION",outputOption
        # print "KicadfIle",kicadFile
        # To avoid writing optionInfo twice in final netlist
        store_optionInfo = list(optionInfo)

        # checking if analysis files is present
        (projpath, filename) = os.path.split(self.kicadFile)
        analysisFileLoc = os.path.join(projpath, "analysis")
        # print "Analysis File Location",analysisFileLoc
        if os.path.exists(analysisFileLoc):
            try:
                f = open(analysisFileLoc)
                # Read data
                data = f.read()
                # Close the file
                f.close()

            except BaseException:
                print("Error While opening Project Analysis file.\
                 Please check it")
                sys.exit()
        else:
            print("========================================================")
            print(analysisFileLoc + " does not exist")
            sys.exit()

        # Adding analysis file info to optionInfo
        analysisData = data.splitlines()
        for eachline in analysisData:
            eachline = eachline.strip()
            if len(eachline) > 1:
                if eachline[0] == '.':
                    store_optionInfo.append(eachline)
                else:
                    pass

        # print "Option Info",optionInfo
        analysisOption = []
        initialCondOption = []
        simulatorOption = []
        # includeOption=[]  # Don't know why to use it
        # model = []      # Don't know why to use it

        for eachline in store_optionInfo:
            words = eachline.split()
            option = words[0]
            if (option == '.ac' or option == '.dc' or option ==
                '.disto' or option == '.noise' or
                option == '.op' or option == '.pz' or option ==
                '.sens' or option == '.tf' or
                    option == '.tran'):
                analysisOption.append(eachline + '\n')

            elif (option == '.save' or option == '.print' or option ==
                    '.plot' or option == '.four'):
                eachline = eachline.strip('.')
                outputOption.append(eachline + '\n')
            elif (option == '.nodeset' or option == '.ic'):
                initialCondOption.append(eachline + '\n')
            elif option == '.option':
                simulatorOption.append(eachline + '\n')
            # elif (option=='.include' or option=='.lib'):
            #    includeOption.append(eachline+'\n')
            # elif (option=='.model'):
            #    model.append(eachline+'\n')
            elif option == '.end':
                continue

        # Start creating final netlist cir.out file
        outfile = self.kicadFile + ".out"
        out = open(outfile, "w")
        out.writelines(infoline)
        out.writelines('\n')
        sections = [
            simulatorOption,
            initialCondOption,
            store_schematicInfo,
            analysisOption]

        for section in sections:
            if len(section) == 0:
                continue
            else:
                for line in section:
                    out.writelines('\n')
                    out.writelines(line)

        out.writelines('\n* Control Statements \n')
        out.writelines('.control\n')
        out.writelines('run\n')
        # out.writelines(outputOption)
        out.writelines('print allv > plot_data_v.txt\n')
        out.writelines('print alli > plot_data_i.txt\n')
        for item in plotText:
            out.writelines(item + '\n')
        out.writelines('.endc\n')
        out.writelines('.end\n')
        out.close()

    def createSubFile(self, subPath):
        self.project = subPath
        self.projName = os.path.basename(self.project)
        if os.path.exists(self.project + ".cir.out"):
            try:
                f = open(self.project + ".cir.out")
            except BaseException:
                print("Error in opening .cir.out file.")
        else:
            print("=========================================================")
            print(
                self.projName +
                ".cir.out does not exist. Please create a spice netlist.")

        # Read the data from file
        data = f.read()
        # Close the file

        f.close()
        newNetlist = []
        netlist = iter(data.splitlines())
        for eachline in netlist:
            eachline = eachline.strip()
            if len(eachline) < 1:
                continue
            words = eachline.split()
            if eachline[2] == 'u':
                if words[len(words) - 1] == "port":
                    subcktInfo = ".subckt " + self.projName + " "
                    for i in range(2, len(words) - 1):
                        subcktInfo += words[i] + " "
                    continue
            if(
                words[0] == ".end" or
                words[0] == ".ac" or
                words[0] == ".dc" or
                words[0] == ".tran" or
                words[0] == '.disto' or
                words[0] == '.noise' or
                words[0] == '.op' or
                words[0] == '.pz' or
                words[0] == '.sens' or
                words[0] == '.tf'
            ):
                continue
            elif words[0] == ".control":
                while words[0] != ".endc":
                    eachline = next(netlist)
                    eachline = eachline.strip()
                    if len(eachline) < 1:
                        continue
                    words = eachline.split()
            else:
                newNetlist.append(eachline)

        outfile = self.project + ".sub"
        out = open(outfile, "w")
        out.writelines("* Subcircuit " + self.projName)
        out.writelines('\n')
        out.writelines(subcktInfo)
        out.writelines('\n')

        for i in range(len(newNetlist), 0, -1):
            newNetlist.insert(i, '\n')

        out.writelines(newNetlist)
        out.writelines('\n')

        out.writelines('.ends ' + self.projName)
        print("=============================================================")
        print("The subcircuit has been written in " + self.projName + ".sub")
