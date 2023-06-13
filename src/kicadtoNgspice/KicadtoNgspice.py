# =========================================================================
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
#      MODIFIED: Rahul Paknikar, rahulp@iitb.ac.in
#  ORGANIZATION: eSim Team at FOSSEE, IIT Bombay
#       CREATED: Wednesday 04 March 2015
#      REVISION: Tuesday 25 April 2023
# =========================================================================

import os
import sys
from xml.etree import ElementTree as ET

from PyQt5 import QtWidgets

from . import Analysis
from . import Convert
from . import DeviceModel
from . import Model
from . import Microcontroller
from . import Source
from . import SubcircuitTab
from . import TrackWidget
from .Processing import PrcocessNetlist


class MainWindow(QtWidgets.QWidget):
    """
    - This class create KicadtoNgspice window.
    - And Call Convert function if convert button is pressed.
    - The convert function takes all the value entered by user and create
      a final netlist "*.cir.out".
    - This final netlist is compatible with Ngspice.
    - clarg1 is the path to the .cir file
    - clarg2 is either None or "sub" depending on the analysis type
    """

    def __init__(self, clarg1, clarg2=None):
        QtWidgets.QWidget.__init__(self)
        print("==================================")
        print("Kicad to Ngspice netlist converter")
        print("==================================")
        global kicadNetlist, schematicInfo
        global infoline, optionInfo
        self.kicadFile = clarg1
        self.clarg1 = clarg1
        self.clarg2 = clarg2

        # Create object of track widget
        # Track the dynamically created widget of KicadtoNgspice Window
        self.obj_track = TrackWidget.TrackWidget()

        # Clear Dictionary/List item of sub circuit and Ngspice model
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
        # print("=============================================================")
        # print("Given Kicad Schematic Netlist Info :", kicadNetlist)

        # Construct parameter information
        param = obj_proc.readParamInfo(kicadNetlist)

        # Replace parameter with values
        netlist, infoline = obj_proc.preprocessNetlist(kicadNetlist, param)
        # print("=============================================================")
        # print("Schematic Info after processing Kicad Netlist: ", netlist)

        # Separate option and schematic information
        optionInfo, schematicInfo = obj_proc.separateNetlistInfo(netlist)
        # print("=============================================================")
        # print("OPTIONINFO in the Netlist", optionInfo)

        # List for storing source and its value
        global sourcelist, sourcelisttrack
        sourcelist = []
        sourcelisttrack = []
        schematicInfo, sourcelist = obj_proc.insertSpecialSourceParam(
            schematicInfo, sourcelist)

        # List storing model detail
        global modelList, outputOption, unknownModelList, multipleModelList, \
            plotText, microcontrollerList

        modelList = []
        microcontrollerList = []
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
        for line in modelList:
            if line[6] == "Nghdl":
                microcontrollerList.append(line)
                modelList.remove(line)

        """
        - Checking if any unknown model is used in schematic which is not
          recognized by Ngspice.
        - Also if the two model of same name is present under
          modelParamXML directory
        """
        if unknownModelList:
            print("Unknown Model List is : ", unknownModelList)
            self.msg = QtWidgets.QErrorMessage()
            self.msg.setModal(True)
            self.msg.setWindowTitle("Unknown Models")
            self.content = "Your schematic contain unknown model " + \
                           ', '.join(unknownModelList)
            self.msg.showMessage(self.content)
            self.msg.exec_()

        elif multipleModelList:
            self.msg = QtWidgets.QErrorMessage()
            self.msg.setModal(True)
            self.msg.setWindowTitle("Multiple Models")
            self.mcontent = "Look like you have duplicate model in \
            modelParamXML directory " + \
                            ', '.join(multipleModelList[0])
            self.msg.showMessage(self.mcontent)
            self.msg.exec_()

        else:
            self.createMainWindow()

    def createMainWindow(self):
        """
        - This function create main window of KiCad to Ngspice converter
        - Two components
            - createcreateConvertWidget
            - Convert button => callConvert
        """
        self.vbox = QtWidgets.QVBoxLayout()
        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addStretch(1)
        self.convertbtn = QtWidgets.QPushButton("Convert")
        self.convertbtn.clicked.connect(self.callConvert)
        self.hbox.addWidget(self.convertbtn)
        self.vbox.addWidget(self.createcreateConvertWidget())
        self.vbox.addLayout(self.hbox)

        self.setLayout(self.vbox)
        self.setWindowTitle("Kicad To NgSpice Converter")
        self.show()

    def createcreateConvertWidget(self):
        """
        - Contains the tabs for various convertor elements
            - Analysis            => obj_analysis
            => Analysis.Analysis(`path_to_projFile`)

            - Source Details      => obj_source
            => Source.Source(`sourcelist`,`sourcelisttrack`,`path_to_projFile`)

            - NgSpice Model       => obj_model
            => Model.Model(`schematicInfo`,`modelList`,`path_to_projFile`)

            - Device Modelling    => obj_devicemodel
            => DeviceModel.DeviceModel(`schematicInfo`,`path_to_projFile`)

            - Subcircuits         => obj_subcircuitTab
            => SubcircuitTab.SubcircuitTab(`schematicInfo`,`path_to_projFile`)

            - Microcontrollers         => obj_microcontroller
            => Model.Model(schematicInfo, microcontrollerList, self.clarg1)

        - Finally pass each of these objects, to widgets
        - convertWindow > mainLayout > tabWidgets > AnalysisTab, SourceTab ...
        """
        global obj_analysis
        self.convertWindow = QtWidgets.QWidget()
        self.analysisTab = QtWidgets.QScrollArea()
        obj_analysis = Analysis.Analysis(self.clarg1)
        self.analysisTab.setWidget(obj_analysis)
        # self.analysisTabLayout = \
        #       QtWidgets.QVBoxLayout(self.analysisTab.widget())
        self.analysisTab.setWidgetResizable(True)
        global obj_source
        self.sourceTab = QtWidgets.QScrollArea()
        obj_source = Source.Source(sourcelist, sourcelisttrack, self.clarg1)
        self.sourceTab.setWidget(obj_source)
        # self.sourceTabLayout = QtWidgets.QVBoxLayout(self.sourceTab.widget())
        self.sourceTab.setWidgetResizable(True)
        global obj_model
        self.modelTab = QtWidgets.QScrollArea()
        obj_model = Model.Model(schematicInfo, modelList, self.clarg1)
        self.modelTab.setWidget(obj_model)
        # self.modelTabLayout = QtWidgets.QVBoxLayout(self.modelTab.widget())
        self.modelTab.setWidgetResizable(True)
        global obj_devicemodel
        self.deviceModelTab = QtWidgets.QScrollArea()
        obj_devicemodel = DeviceModel.DeviceModel(schematicInfo, self.clarg1)
        self.deviceModelTab.setWidget(obj_devicemodel)
        self.deviceModelTab.setWidgetResizable(True)
        global obj_subcircuitTab
        self.subcircuitTab = QtWidgets.QScrollArea()
        obj_subcircuitTab = SubcircuitTab.SubcircuitTab(
            schematicInfo, self.clarg1)
        self.subcircuitTab.setWidget(obj_subcircuitTab)
        self.subcircuitTab.setWidgetResizable(True)
        global obj_microcontroller
        self.microcontrollerTab = QtWidgets.QScrollArea()
        obj_microcontroller = Microcontroller.\
            Microcontroller(schematicInfo, microcontrollerList, self.clarg1)
        self.microcontrollerTab.setWidget(obj_microcontroller)
        self.microcontrollerTab.setWidgetResizable(True)

        self.tabWidget = QtWidgets.QTabWidget()
        # self.tabWidget.TabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.addTab(self.analysisTab, "Analysis")
        self.tabWidget.addTab(self.sourceTab, "Source Details")
        self.tabWidget.addTab(self.modelTab, "Ngspice Model")
        self.tabWidget.addTab(self.deviceModelTab, "Device Modeling")
        self.tabWidget.addTab(self.subcircuitTab, "Subcircuits")
        self.tabWidget.addTab(self.microcontrollerTab, "Microcontroller")
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addWidget(self.tabWidget)
        # self.mainLayout.addStretch(1)
        self.convertWindow.setLayout(self.mainLayout)
        self.convertWindow.show()

        return self.convertWindow

    def callConvert(self):
        """
        - This function called when convert button clicked
        - Extracting data from the objs created above
        - Pushing this data to xml, and writing it finally
        - Written to a ..._Previous_Values.xml file in the projDirectory
        - Finally, call createNetListFile, with the converted schematic
        """
        global schematicInfo
        global analysisoutput
        global kicad
        store_schematicInfo = list(schematicInfo)
        (projpath, filename) = os.path.split(self.kicadFile)
        project_name = os.path.basename(projpath)
        check = 1

        try:
            fr = open(
                os.path.join(
                    projpath, project_name + "_Previous_Values.xml"), 'r'
            )
            temp_tree = ET.parse(fr)
            temp_root = temp_tree.getroot()
        except BaseException:
            check = 0

        # Opening previous value file pertaining to the selected project
        fw = os.path.join(projpath, project_name + "_Previous_Values.xml")

        if check == 0:
            attr_parent = ET.Element("KicadtoNgspice")
        if check == 1:
            attr_parent = temp_root

        for child in attr_parent:
            if child.tag == "analysis":
                attr_parent.remove(child)

        attr_analysis = ET.SubElement(attr_parent, "analysis")
        attr_ac = ET.SubElement(attr_analysis, "ac")

        if obj_analysis.Lin.isChecked():
            ET.SubElement(attr_ac, "field1", name="Lin").text = "true"
            ET.SubElement(attr_ac, "field2", name="Dec").text = "false"
            ET.SubElement(attr_ac, "field3", name="Oct").text = "false"
        elif obj_analysis.Dec.isChecked():
            ET.SubElement(attr_ac, "field1", name="Lin").text = "false"
            ET.SubElement(attr_ac, "field2", name="Dec").text = "true"
            ET.SubElement(attr_ac, "field3", name="Oct").text = "false"
        if obj_analysis.Oct.isChecked():
            ET.SubElement(attr_ac, "field1", name="Lin").text = "false"
            ET.SubElement(attr_ac, "field2", name="Dec").text = "false"
            ET.SubElement(attr_ac, "field3", name="Oct").text = "true"

        ET.SubElement(
            attr_ac, "field4", name="Start Frequency"
        ).text = str(obj_analysis.ac_entry_var[0].text())
        ET.SubElement(
            attr_ac, "field5", name="Stop Frequency"
        ).text = str(obj_analysis.ac_entry_var[1].text())
        ET.SubElement(
            attr_ac, "field6", name="No. of points"
        ).text = str(obj_analysis.ac_entry_var[2].text())
        ET.SubElement(
            attr_ac, "field7", name="Start Fre Combo"
        ).text = obj_analysis.ac_parameter[0]
        ET.SubElement(
            attr_ac, "field8", name="Stop Fre Combo"
        ).text = obj_analysis.ac_parameter[1]

        attr_dc = ET.SubElement(attr_analysis, "dc")

        ET.SubElement(
            attr_dc, "field1", name="Source 1"
        ).text = str(obj_analysis.dc_entry_var[0].text())
        ET.SubElement(
            attr_dc, "field2", name="Start"
        ).text = str(obj_analysis.dc_entry_var[1].text())
        ET.SubElement(
            attr_dc, "field3", name="Increment"
        ).text = str(obj_analysis.dc_entry_var[2].text())
        ET.SubElement(
            attr_dc, "field4", name="Stop"
        ).text = str(obj_analysis.dc_entry_var[3].text())
        # print("OBJ_ANALYSIS.CHECK -----", self.obj_track.op_check[-1])
        ET.SubElement(
            attr_dc, "field5", name="Operating Point"
        ).text = str(self.obj_track.op_check[-1])
        ET.SubElement(
            attr_dc, "field6", name="Start Combo"
        ).text = obj_analysis.dc_parameter[0]
        ET.SubElement(
            attr_dc, "field7", name="Increment Combo"
        ).text = obj_analysis.dc_parameter[1]
        ET.SubElement(
            attr_dc, "field8", name="Stop Combo"
        ).text = obj_analysis.dc_parameter[2]
        ET.SubElement(
            attr_dc, "field9", name="Source 2"
        ).text = str(obj_analysis.dc_entry_var[4].text())
        ET.SubElement(
            attr_dc, "field10", name="Start"
        ).text = str(obj_analysis.dc_entry_var[5].text())
        ET.SubElement(
            attr_dc, "field11", name="Increment"
        ).text = str(obj_analysis.dc_entry_var[6].text())
        ET.SubElement(
            attr_dc, "field12", name="Stop"
        ).text = str(obj_analysis.dc_entry_var[7].text())
        ET.SubElement(
            attr_dc, "field13", name="Start Combo"
        ).text = obj_analysis.dc_parameter[3]
        ET.SubElement(
            attr_dc, "field14", name="Increment Combo"
        ).text = obj_analysis.dc_parameter[4]
        ET.SubElement(
            attr_dc, "field15", name="Stop Combo"
        ).text = obj_analysis.dc_parameter[5]

        attr_tran = ET.SubElement(attr_analysis, "tran")
        ET.SubElement(
            attr_tran, "field1", name="Start Time"
        ).text = str(obj_analysis.tran_entry_var[0].text())
        ET.SubElement(
            attr_tran, "field2", name="Step Time"
        ).text = str(obj_analysis.tran_entry_var[1].text())
        ET.SubElement(
            attr_tran, "field3", name="Stop Time"
        ).text = str(obj_analysis.tran_entry_var[2].text())
        ET.SubElement(
            attr_tran, "field4", name="Start Combo"
        ).text = obj_analysis.tran_parameter[0]
        ET.SubElement(
            attr_tran, "field5", name="Step Combo"
        ).text = obj_analysis.tran_parameter[1]
        ET.SubElement(
            attr_tran, "field6", name="Stop Combo"
        ).text = obj_analysis.tran_parameter[2]
        # print("TRAN PARAMETER 2-----",obj_analysis.tran_parameter[2])

        if check == 0:
            attr_source = ET.SubElement(attr_parent, "source")
        if check == 1:
            for child in attr_parent:
                if child.tag == "source":
                    attr_source = child

        count = 0
        grand_child_count = 0
        entry_var_keys = list(obj_source.entry_var.keys())

        for i in store_schematicInfo:
            tmp_check = 0
            words = i.split(' ')
            wordv = words[0]
            for child in attr_source:
                if child.tag == wordv and child.text == words[len(words) - 1]:
                    tmp_check = 1
                    for grand_child in child:
                        grand_child.text = \
                            str(obj_source.entry_var
                                [entry_var_keys[grand_child_count]].text())
                        grand_child_count += 1
            if tmp_check == 0:
                words = i.split(' ')
                wordv = words[0]
                if wordv[0] == "v" or wordv[0] == "i":
                    attr_var = ET.SubElement(
                        attr_source, words[0], name="Source type"
                    )
                    attr_var.text = words[len(words) - 1]
                    # ET.SubElement(
                    #     attr_ac, "field1", name="Lin").text = "true"
                if words[len(words) - 1] == "ac":
                    # attr_ac = ET.SubElement(attr_var, "ac")
                    ET.SubElement(
                        attr_var, "field1", name="Amplitude"
                    ).text = str(obj_source.entry_var
                                 [entry_var_keys[count]].text())
                    count += 1
                    ET.SubElement(
                        attr_var, "field2", name="Phase"
                    ).text = str(obj_source.entry_var
                                 [entry_var_keys[count]].text())
                    count += 1
                elif words[len(words) - 1] == "dc":
                    # attr_dc = ET.SubElement(attr_var, "dc")
                    ET.SubElement(
                        attr_var, "field1", name="Value"
                    ).text = str(obj_source.entry_var
                                 [entry_var_keys[count]].text())
                    count += 1
                elif words[len(words) - 1] == "sine":
                    # attr_sine = ET.SubElement(attr_var, "sine")
                    ET.SubElement(
                        attr_var, "field1", name="Offset Value"
                    ).text = str(obj_source.entry_var
                                 [entry_var_keys[count]].text())
                    count += 1
                    ET.SubElement(
                        attr_var, "field2", name="Amplitude"
                    ).text = str(obj_source.entry_var
                                 [entry_var_keys[count]].text())
                    count += 1
                    ET.SubElement(
                        attr_var, "field3", name="Frequency"
                    ).text = str(obj_source.entry_var
                                 [entry_var_keys[count]].text())
                    count += 1
                    ET.SubElement(
                        attr_var, "field4", name="Delay Time"
                    ).text = str(obj_source.entry_var
                                 [entry_var_keys[count]].text())
                    count += 1
                    ET.SubElement(
                        attr_var, "field5", name="Damping Factor"
                    ).text = str(obj_source.entry_var
                                 [entry_var_keys[count]].text())
                    count += 1
                elif words[len(words) - 1] == "pulse":
                    # attr_pulse=ET.SubElement(attr_var,"pulse")
                    ET.SubElement(
                        attr_var, "field1", name="Initial Value"
                    ).text = str(obj_source.entry_var
                                 [entry_var_keys[count]].text())
                    count += 1
                    ET.SubElement(
                        attr_var, "field2", name="Pulse Value"
                    ).text = str(obj_source.entry_var
                                 [entry_var_keys[count]].text())
                    count += 1
                    ET.SubElement(
                        attr_var, "field3", name="Delay Time"
                    ).text = str(obj_source.entry_var
                                 [entry_var_keys[count]].text())
                    count += 1
                    ET.SubElement(
                        attr_var, "field4", name="Rise Time"
                    ).text = str(obj_source.entry_var
                                 [entry_var_keys[count]].text())
                    count += 1
                    ET.SubElement(
                        attr_var, "field5", name="Fall Time"
                    ).text = str(obj_source.entry_var
                                 [entry_var_keys[count]].text())
                    count += 1
                    ET.SubElement(
                        attr_var, "field5", name="Pulse width"
                    ).text = str(obj_source.entry_var
                                 [entry_var_keys[count]].text())
                    count += 1
                    ET.SubElement(
                        attr_var, "field5", name="Period"
                    ).text = str(obj_source.entry_var
                                 [entry_var_keys[count]].text())
                    count += 1
                elif words[len(words) - 1] == "pwl":
                    # attr_pwl=ET.SubElement(attr_var,"pwl")
                    ET.SubElement(
                        attr_var, "field1", name="Enter in pwl format"
                    ).text = str(obj_source.entry_var
                                 [entry_var_keys[count]].text())
                    count += 1
                elif words[len(words) - 1] == "exp":
                    # attr_exp=ET.SubElement(attr_var,"exp")
                    ET.SubElement(
                        attr_var, "field1", name="Initial Value"
                    ).text = str(obj_source.entry_var
                                 [entry_var_keys[count]].text())
                    count += 1
                    ET.SubElement(
                        attr_var, "field2", name="Pulsed Value"
                    ).text = str(obj_source.entry_var
                                 [entry_var_keys[count]].text())
                    count += 1
                    ET.SubElement(
                        attr_var, "field3", name="Rise Delay Time"
                    ).text = str(obj_source.entry_var
                                 [entry_var_keys[count]].text())
                    count += 1
                    ET.SubElement(
                        attr_var, "field4", name="Rise Time Constant"
                    ).text = str(obj_source.entry_var
                                 [entry_var_keys[count]].text())
                    count += 1
                    ET.SubElement(
                        attr_var, "field5", name="Fall Time"
                    ).text = str(obj_source.entry_var
                                 [entry_var_keys[count]].text())
                    count += 1
                    ET.SubElement(
                        attr_var, "field6", name="Fall Time Constant"
                    ).text = str(obj_source.entry_var
                                 [entry_var_keys[count]].text())
                    count += 1

        if check == 0:
            attr_model = ET.SubElement(attr_parent, "model")
        if check == 1:
            for child in attr_parent:
                if child.tag == "model":
                    attr_model = child
        i = 0

        # tmp_check is a variable to check for duplicates in the xml file
        tmp_check = 0
        # tmp_i is the iterator in case duplicates are there;
        # then in that case we need to replace only the child node and
        # not create a new parent node

        for line in modelList:
            tmp_check = 0
            for rand_itr in obj_model.obj_trac.modelTrack:
                if rand_itr[2] == line[2] and rand_itr[3] == line[3]:
                    start = rand_itr[7]
                    end = rand_itr[8]

            i = start
            for child in attr_model:
                if child.text == line[2] and child.tag == line[3]:
                    for grand_child in child:
                        if i <= end:
                            grand_child.text = \
                                str(obj_model.obj_trac.model_entry_var[
                                        i].text())
                            i = i + 1
                    tmp_check = 1

            if tmp_check == 0:
                attr_ui = ET.SubElement(attr_model, line[3], name="type")
                attr_ui.text = line[2]
                for key, value in line[7].items():
                    if (
                        hasattr(value, '__iter__') and
                        i <= end and not isinstance(value, str)
                    ):
                        for item in value:
                            ET.SubElement(
                                attr_ui, "field" + str(i + 1), name=item
                            ).text = str(
                                obj_model.obj_trac.model_entry_var[i].text()
                            )
                            i = i + 1

                    else:
                        ET.SubElement(
                            attr_ui, "field" + str(i + 1), name=value
                        ).text = str(
                            obj_model.obj_trac.model_entry_var[i].text()
                        )
                        i = i + 1

        # Writing Device Model values
        if check == 0:
            attr_devicemodel = ET.SubElement(attr_parent, "devicemodel")
        if check == 1:
            for child in attr_parent:
                if child.tag == "devicemodel":
                    del child[:]
                    attr_devicemodel = child

        for device in obj_devicemodel.devicemodel_dict_beg:
            attr_var = ET.SubElement(attr_devicemodel, device)
            it = obj_devicemodel.devicemodel_dict_beg[device]
            end = obj_devicemodel.devicemodel_dict_end[device]

            while it <= end:
                ET.SubElement(attr_var, "field").text = \
                    str(obj_devicemodel.entry_var[it].text())
                it = it + 1

        # Writing Subcircuit values
        if check == 0:
            attr_subcircuit = ET.SubElement(attr_parent, "subcircuit")
        if check == 1:
            for child in attr_parent:
                if child.tag == "subcircuit":
                    del child[:]
                    attr_subcircuit = child

        for subckt in obj_subcircuitTab.subcircuit_dict_beg:
            attr_var = ET.SubElement(attr_subcircuit, subckt)
            it = obj_subcircuitTab.subcircuit_dict_beg[subckt]
            end = obj_subcircuitTab.subcircuit_dict_end[subckt]

            while it <= end:
                ET.SubElement(attr_var, "field").text = \
                    str(obj_subcircuitTab.entry_var[it].text())
                it = it + 1

        # Writing for Microcontroller
        if check == 0:
            attr_microcontroller = ET.SubElement(attr_parent,
                                                 "microcontroller")
        if check == 1:
            for child in attr_parent:
                if child.tag == "microcontroller":
                    attr_microcontroller = child
        i = 0

        # tmp_check is a variable to check for duplicates in the xml file
        tmp_check = 0
        # tmp_i is the iterator in case duplicates are there;
        # then in that case we need to replace only the child node and
        # not create a new parent node

        for line in microcontrollerList:
            tmp_check = 0
            for rand_itr in obj_microcontroller.obj_trac.microcontrollerTrack:
                if rand_itr[2] == line[2] and rand_itr[3] == line[3]:
                    start = rand_itr[7]
                    end = rand_itr[8]

            i = start
            for child in attr_microcontroller:
                if child.text == line[2] and child.tag == line[3]:
                    for grand_child in child:
                        if i <= end:
                            grand_child.text = \
                                str(
                                    obj_microcontroller.
                                    obj_trac.microcontroller_var[i].text())
                            i = i + 1
                    tmp_check = 1

            if tmp_check == 0:
                attr_ui = ET.SubElement(attr_microcontroller, line[3],
                                        name="type")
                attr_ui.text = line[2]
                for key, value in line[7].items():
                    if (
                            hasattr(value, '__iter__') and
                            i <= end and not isinstance(value, str)
                    ):
                        for item in value:
                            ET.SubElement(
                                attr_ui, "field" + str(i + 1), name=item
                            ).text = str(
                                obj_microcontroller.
                                obj_trac.microcontroller_var[i].text()
                            )
                            i = i + 1
                    else:
                        ET.SubElement(
                            attr_ui, "field" + str(i + 1), name=value
                        ).text = str(
                            obj_microcontroller.obj_trac.microcontroller_var[
                                i].text()
                        )
                        i = i + 1

        # xml written to previous value file for the project
        tree = ET.ElementTree(attr_parent)
        tree.write(fw)

        # print("=============================================================")
        # print("SOURCE LIST TRACK")
        # print(self.obj_track.sourcelisttrack["ITEMS"])
        # print("SOURCE ENTRY VAR")
        # print(self.obj_track.source_entry_var["ITEMS"])
        # print("SCHEMATIC INFO")
        # print(store_schematicInfo)
        # print("=============================================================")

        # Create Convert object with the source details & the schematic details
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

            store_schematicInfo = self.obj_convert.addMicrocontrollerParameter(
                store_schematicInfo)
            print("=========================================================")
            print("Netlist After Adding Microcontroller Model :",
                  store_schematicInfo)

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
            print("=========================================================")
            print("STORE SCHEMATIC INFO")
            print(store_schematicInfo)
            print("=========================================================")
            self.createNetlistFile(store_schematicInfo, plotText)

            self.msg = "The KiCad to Ngspice conversion completed "
            self.msg += "successfully!"
            QtWidgets.QMessageBox.information(
                self, "Information", self.msg, QtWidgets.QMessageBox.Ok
            )
        except Exception as e:
            print("Exception Message: ", e)
            print("There was error while converting kicad to ngspice")
            self.close()

        # Generate .sub file from .cir.out file if it is a subcircuit
        subPath = os.path.splitext(self.kicadFile)[0]

        # If sub argument passed, create subCircuit file as well
        if self.clarg2 == "sub":
            self.createSubFile(subPath)

    def createNetlistFile(self, store_schematicInfo, plotText):
        """
        - Creating .cir.out file
        - If analysis file present uses that and extract
            - Simulator
            - Initial
            - Analysis
        - Finally add the following components to .cir.out file
            - SimulatorOption
            - InitialCondOption
            - Store_SchematicInfo
            - AnalysisOption
        - In the end add control statements and allv, alli, end statements
        """
        print("=============================================================")
        print("Creating Final netlist")

        # To avoid writing optionInfo twice in final netlist
        store_optionInfo = list(optionInfo)

        # checking if analysis files is present
        (projpath, filename) = os.path.split(self.kicadFile)
        analysisFileLoc = os.path.join(projpath, "analysis")

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
            # print("========================================================")
            print(analysisFileLoc + " does not exist")
            sys.exit()

        # Adding analysis file info to optionInfo
        analysisData = data.splitlines()
        for eachline in analysisData:
            eachline = eachline.strip()
            if len(eachline) > 1:
                if eachline[0] == '.':
                    store_optionInfo.append(eachline)

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
        """
        - To create subcircuit file
        - Extract data from .cir.out file
        """
        self.project = subPath
        self.projName = os.path.basename(self.project)
        if os.path.exists(self.project + ".cir.out"):
            try:
                f = open(self.project + ".cir.out")
            except BaseException:
                print("Error in opening .cir.out file.")
        else:
            # print("=========================================================")
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
            if (
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
        # print("=============================================================")
        print("The subcircuit has been written in " + self.projName + ".sub")
