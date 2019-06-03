
from PyQt4 import QtGui
from . import TrackWidget
import os
# from xml.etree import ElementTree as ET
import json


class Analysis(QtGui.QWidget):
    """
    - This class create Analysis Tab in KicadtoNgspice Window. 4 sections -
    - - Select Analysis Type
    - - AC Analysis
    - - DC Analysis
    - - Transient Analysis
    - Set various track widget options here, for tracking purposes across\
    different functions and modules -
    - - AC_entry_var
    - - AC_Parameter
    - - DC_entry_var
    - - DC_Parameter
    - - TRAN_entry_var
    - - TRAN_Parameter
    - - set_Checkbox
    - - AC_type
    - - op_check
    """

    def __init__(self, clarg1):
        self.clarg1 = clarg1
        QtGui.QWidget.__init__(self)
        self.track_obj = TrackWidget.TrackWidget()
        self.count = 0
        self.parameter_cnt = 0
        self.ac_entry_var = {}
        self.dc_entry_var = {}
        self.tran_entry_var = {}
        self.ac_parameter = {}
        self.dc_parameter = {}
        self.tran_parameter = {}
        self.createAnalysisWidget()

    def createAnalysisWidget(self):
        """
        - Create the main anaylsis widget overwiew
        - - Checkbox for analysis type
        - - Place, `AC`, `DC` and `TRANSIENT` analysis tab
        - - `self.acbox`, `self.dcbox`,`self.trbox`...
        - Check for `analysis` file, if any in projDir, extract data from it
        - Else set the default checkbox to `TRAN`
        - Accordingly set state for track widget options, as `TRAN`, `AC` ...
        """
        self.grid = QtGui.QGridLayout()
        self.grid.addWidget(self.createCheckBox(), 0, 0)
        self.grid.addWidget(self.createACgroup(), 1, 0)
        self.grid.addWidget(self.createDCgroup(), 2, 0)
        self.grid.addWidget(self.createTRANgroup(), 3, 0)

        try:
            kicadFile = self.clarg1
            (projpath, filename) = os.path.split(kicadFile)
            if os.path.isfile(os.path.join(projpath, 'analysis')):
                print("Analysis file is present")

            analysisfile = open(os.path.join(projpath, 'analysis'))
            content = analysisfile.readline()
            print("=========================================================")
            print("Content of Analysis file :", content)
            print("=========================================================")
            contentlist = content.split()

            if contentlist[0] == '.ac':
                self.checkAC.setChecked(True)
                self.acbox.setDisabled(False)
                self.dcbox.setDisabled(True)
                self.trbox.setDisabled(True)
                self.track_obj.set_CheckBox["ITEMS"] = "AC"
                if contentlist[1] == 'lin':
                    self.Lin.setChecked(True)
                    self.track_obj.AC_type["ITEMS"] = "lin"
                elif contentlist[1] == 'dec':
                    self.Dec.setChecked(True)
                    self.track_obj.AC_type["ITEMS"] = "dec"
                elif contentlist[1] == 'oct':
                    self.Oct.setChecked(True)
                    self.track_obj.AC_type["ITEMS"] = "oct"

            elif contentlist[0] == '.dc':
                self.checkDC.setChecked(True)
                self.dcbox.setDisabled(False)
                self.acbox.setDisabled(True)
                self.trbox.setDisabled(True)
                self.track_obj.set_CheckBox["ITEMS"] = "DC"

            elif contentlist[0] == '.tran':
                self.checkTRAN.setChecked(True)
                self.trbox.setDisabled(False)
                self.acbox.setDisabled(True)
                self.dcbox.setDisabled(True)
                self.track_obj.set_CheckBox["ITEMS"] = "TRAN"

            elif contentlist[0] == '.op':
                self.checkDC.setChecked(True)
                self.dcbox.setDisabled(False)
                self.acbox.setDisabled(True)
                self.trbox.setDisabled(True)
                self.check.setChecked(True)
                self.track_obj.set_CheckBox["ITEMS"] = "DC"

        except BaseException:
            self.checkTRAN.setChecked(True)
            self.track_obj.set_CheckBox["ITEMS"] = "TRAN"

        self.setLayout(self.grid)
        self.show()

    def createCheckBox(self):
        """
        - Create the checkboxes for analysis type, under analysis tab
        - checkbox > checkgrid > checkgroupbtn > checkAC | checkDC | checkTRAN
        - Trigger enableBox on clicking
        """
        self.checkbox = QtGui.QGroupBox()
        self.checkbox.setTitle("Select Analysis Type")
        self.checkgrid = QtGui.QGridLayout()

        self.checkgroupbtn = QtGui.QButtonGroup()
        self.checkAC = QtGui.QCheckBox("AC")
        self.checkDC = QtGui.QCheckBox("DC")
        self.checkTRAN = QtGui.QCheckBox("TRANSIENT")

        self.checkgroupbtn.addButton(self.checkAC)
        self.checkgroupbtn.addButton(self.checkDC)
        self.checkgroupbtn.addButton(self.checkTRAN)
        self.checkgroupbtn.setExclusive(True)
        self.checkgroupbtn.buttonClicked.connect(self.enableBox)

        self.checkgrid.addWidget(self.checkAC, 0, 0)
        self.checkgrid.addWidget(self.checkDC, 0, 1)
        self.checkgrid.addWidget(self.checkTRAN, 0, 2)
        self.checkbox.setLayout(self.checkgrid)

        return self.checkbox

    def enableBox(self):
        """
        - Activate analysis areas according to checkBox marked
        - Add analysis data to track_obj from TrackWidget
        """
        if self.checkAC.isChecked():
            self.acbox.setDisabled(False)
            self.dcbox.setDisabled(True)
            self.trbox.setDisabled(True)
            self.track_obj.set_CheckBox["ITEMS"] = "AC"

        elif self.checkDC.isChecked():
            self.dcbox.setDisabled(False)
            self.acbox.setDisabled(True)
            self.trbox.setDisabled(True)
            self.track_obj.set_CheckBox["ITEMS"] = "DC"

        elif self.checkTRAN.isChecked():
            self.trbox.setDisabled(False)
            self.acbox.setDisabled(True)
            self.dcbox.setDisabled(True)
            self.track_obj.set_CheckBox["ITEMS"] = "TRAN"

    def createACgroup(self):
        """
        - Designing of AC group in analysis tab
        - 3 radio buttons - Lin | Dec | Oct
        - 3 input boxes, with top 2 combos\
        - If previous values exist then fill default values from
          previous value json file
        """
        kicadFile = self.clarg1
        (projpath, filename) = os.path.split(kicadFile)
        project_name = os.path.basename(projpath)
        check = 1

        try:
            f = open(
                os.path.join(
                    projpath,
                    project_name +
                    "_Previous_Values.json"),
                'r')
            data = f.read()
            json_data = json.loads(data)
        except BaseException:
            check = 0
            print("AC Previous Values JSON is Empty")

        self.acbox = QtGui.QGroupBox()
        self.acbox.setTitle("AC Analysis")
        self.acbox.setDisabled(True)
        self.acgrid = QtGui.QGridLayout()
        self.radiobuttongroup = QtGui.QButtonGroup()
        self.Lin = QtGui.QRadioButton("Lin")
        self.Dec = QtGui.QRadioButton("Dec")
        self.Oct = QtGui.QRadioButton("Oct")
        self.radiobuttongroup.addButton(self.Lin)
        self.radiobuttongroup.addButton(self.Dec)
        self.radiobuttongroup.addButton(self.Oct)
        self.radiobuttongroup.setExclusive(True)
        self.Lin.setChecked(True)
        self.track_obj.AC_type["ITEMS"] = "lin"
        self.radiobuttongroup.buttonClicked.connect(self.set_ac_type)
        self.acgrid.addWidget(self.Lin, 1, 1)
        self.acgrid.addWidget(self.Dec, 1, 2)
        self.acgrid.addWidget(self.Oct, 1, 3)
        self.acbox.setLayout(self.acgrid)

        self.scale = QtGui.QLabel("Scale")
        self.start_fre_lable = QtGui.QLabel("Start Frequency")
        self.stop_fre_lable = QtGui.QLabel("Stop Frequency")
        self.no_of_points = QtGui.QLabel("No.of Points")
        self.acgrid.addWidget(self.scale, 1, 0)
        self.acgrid.addWidget(self.start_fre_lable, 2, 0)
        self.acgrid.addWidget(self.stop_fre_lable, 3, 0)
        self.acgrid.addWidget(self.no_of_points, 4, 0)

        self.count = 0
        self.ac_entry_var[self.count] = QtGui.QLineEdit()  # start
        self.acgrid.addWidget(self.ac_entry_var[self.count], 2, 1)
        self.ac_entry_var[self.count].setMaximumWidth(150)
        self.count = self.count + 1
        self.ac_entry_var[self.count] = QtGui.QLineEdit()  # stop
        self.acgrid.addWidget(self.ac_entry_var[self.count], 3, 1)
        self.ac_entry_var[self.count].setMaximumWidth(150)
        self.count = self.count + 1
        self.ac_entry_var[self.count] = QtGui.QLineEdit()  # no of pts
        self.acgrid.addWidget(self.ac_entry_var[self.count], 4, 1)
        self.ac_entry_var[self.count].setMaximumWidth(150)

        self.parameter_cnt = 0
        self.start_fre_combo = QtGui.QComboBox()
        self.start_fre_combo.addItem("Hz",)
        self.start_fre_combo.addItem("KHz")
        self.start_fre_combo.addItem("Meg")
        self.start_fre_combo.addItem("GHz")
        self.start_fre_combo.addItem("THz")
        self.start_fre_combo.setMaximumWidth(150)
        self.acgrid.addWidget(self.start_fre_combo, 2, 2)
        self.ac_parameter[0] = "Hz"

        # Try setting to default value from anaylsis file
        try:
            self.ac_parameter[self.parameter_cnt] = str(
                json_data["analysis"]["ac"]["Start Fre Combo"])
        except BaseException:
            self.ac_parameter[self.parameter_cnt] = "Hz"

        # Event listener for combo action
        self.start_fre_combo.activated[str].connect(self.start_combovalue)

        self.parameter_cnt = self.parameter_cnt + 1
        self.stop_fre_combo = QtGui.QComboBox()
        self.stop_fre_combo.addItem("Hz")
        self.stop_fre_combo.addItem("KHz")
        self.stop_fre_combo.addItem("Meg")
        self.stop_fre_combo.addItem("GHz")
        self.stop_fre_combo.addItem("THz")
        self.stop_fre_combo.setMaximumWidth(150)
        self.acgrid.addWidget(self.stop_fre_combo, 3, 2)
        self.ac_parameter[1] = "Hz"

        try:
            self.ac_parameter[self.parameter_cnt] = str(
                json_data["analysis"]["ac"]["Stop Fre Combo"])
        except BaseException:
            self.ac_parameter[self.parameter_cnt] = "Hz"

        self.stop_fre_combo.activated[str].connect(self.stop_combovalue)

        self.track_obj.AC_entry_var["ITEMS"] = self.ac_entry_var
        self.track_obj.AC_Parameter["ITEMS"] = self.ac_parameter

        # CSS
        self.acbox.setStyleSheet(" \
        QGroupBox { border: 1px solid gray; border-radius: 9px; margin-top: \
        0.5em; } \
        QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: \
        0 3px 0 3px; } \
        ")
        if check:
            try:
                if json_data["analysis"]["ac"]["Lin"] == "true":
                    self.Lin.setChecked(True)
                    self.Dec.setChecked(False)
                    self.Oct.setChecked(False)
                elif json_data["analysis"]["ac"]["Dec"] == "true":
                    self.Lin.setChecked(False)
                    self.Dec.setChecked(True)
                    self.Oct.setChecked(False)
                elif json_data["analysis"]["ac"]["Oct"] == "true":
                    self.Lin.setChecked(False)
                    self.Dec.setChecked(False)
                    self.Oct.setChecked(True)
                else:
                    pass

                self.ac_entry_var[0].setText(
                    json_data["analysis"]["ac"]["Start Frequency"])
                self.ac_entry_var[1].setText(
                    json_data["analysis"]["ac"]["Stop Frequency"])
                self.ac_entry_var[2].setText(
                    json_data["analysis"]["ac"]["No. of points"])
                index = self.start_fre_combo.findText(
                    json_data["analysis"]["ac"]["Start Fre Combo"])
                self.start_fre_combo.setCurrentIndex(index)
                index = self.stop_fre_combo.findText(
                    json_data["analysis"]["ac"]["Stop Fre Combo"])
                self.stop_fre_combo.setCurrentIndex(index)

            except BaseException:
                print("AC Analysis JSON Parse Error")

        return self.acbox

    '''
    - Below 2 functions handle combo value event listeners for
    - - start frequency for ac
    - - stop frequency for ac
    - And accordingly set the ac_parameters
    '''

    def start_combovalue(self, text):
        """
        - Handle start_fre_combo box event
        - Check where it is Hz, MHz, etc.
        - Accordingly set ac_parameter
        """
        self.ac_parameter[0] = str(text)

    def stop_combovalue(self, text):
        """
        - Handle stop_fre_combo box event
        - Check where it is Hz, MHz, etc.
        - Accordingly set ac_parameter
        """
        self.ac_parameter[1] = str(text)

    def set_ac_type(self):
        """
        - Set track object for AC, according to the type of radio box selected
        """
        self.parameter_cnt = 0

        if self.Lin.isChecked():
            self.track_obj.AC_type["ITEMS"] = "lin"
        elif self.Dec.isChecked():
            self.track_obj.AC_type["ITEMS"] = "dec"
        elif self.Oct.isChecked():
            self.track_obj.AC_type["ITEMS"] = "oct"
        else:
            pass

    def createDCgroup(self):
        """
        - Create DC area under analysis tab
        - Source 1 and 2, each having 4 input boxes as follows
        - - Source
        - - Start
        - - Increment
        - - Stop
        - The last 3 have combo box pertaining to their unit as well
        - Also in the end a checkbox, for operating system point analysis
        """
        kicadFile = self.clarg1
        (projpath, filename) = os.path.split(kicadFile)
        project_name = os.path.basename(projpath)
        check = 1

        try:
            f = open(
                os.path.join(
                    projpath,
                    project_name +
                    "_Previous_Values.json"),
                'r')
            data = f.read()
            json_data = json.loads(data)
        except BaseException:
            check = 0
            print("DC Previous Values JSON is empty")

        self.dcbox = QtGui.QGroupBox()
        self.dcbox.setTitle("DC Analysis")
        self.dcbox.setDisabled(True)
        self.dcgrid = QtGui.QGridLayout()
        self.dcbox.setLayout(self.dcgrid)

        self.source_name = QtGui.QLabel('Enter Source 1', self)
        self.source_name.setMaximumWidth(150)
        self.start = QtGui.QLabel('Start', self)
        self.start.setMaximumWidth(150)
        self.increment = QtGui.QLabel('Increment', self)
        self.increment.setMaximumWidth(150)
        self.stop = QtGui.QLabel('Stop', self)
        self.stop.setMaximumWidth(150)

        self.source_name2 = QtGui.QLabel('Enter Source 2', self)
        self.source_name2.setMaximumWidth(150)
        self.start2 = QtGui.QLabel('Start', self)
        self.start2.setMaximumWidth(150)
        self.increment2 = QtGui.QLabel('Increment', self)
        self.increment2.setMaximumWidth(150)
        self.stop2 = QtGui.QLabel('Stop', self)
        self.stop2.setMaximumWidth(150)

        self.dcgrid.addWidget(self.source_name, 1, 0)
        self.dcgrid.addWidget(self.start, 2, 0)
        self.dcgrid.addWidget(self.increment, 3, 0)
        self.dcgrid.addWidget(self.stop, 4, 0)

        self.dcgrid.addWidget(self.source_name2, 5, 0)
        self.dcgrid.addWidget(self.start2, 6, 0)
        self.dcgrid.addWidget(self.increment2, 7, 0)
        self.dcgrid.addWidget(self.stop2, 8, 0)

        self.count = 0

        self.dc_entry_var[self.count] = QtGui.QLineEdit()  # source
        self.dcgrid.addWidget(self.dc_entry_var[self.count], 1, 1)
        self.dc_entry_var[self.count].setMaximumWidth(150)
        self.count += 1

        self.dc_entry_var[self.count] = QtGui.QLineEdit()  # start
        self.dcgrid.addWidget(self.dc_entry_var[self.count], 2, 1)
        self.dc_entry_var[self.count].setMaximumWidth(150)
        self.count += 1

        self.dc_entry_var[self.count] = QtGui.QLineEdit()  # increment
        self.dcgrid.addWidget(self.dc_entry_var[self.count], 3, 1)
        self.dc_entry_var[self.count].setMaximumWidth(150)
        self.count += 1

        self.dc_entry_var[self.count] = QtGui.QLineEdit()  # stop
        self.dcgrid.addWidget(self.dc_entry_var[self.count], 4, 1)
        self.dc_entry_var[self.count].setMaximumWidth(150)
        self.count += 1

        self.dc_entry_var[self.count] = QtGui.QLineEdit()  # source
        self.dcgrid.addWidget(self.dc_entry_var[self.count], 5, 1)
        self.dc_entry_var[self.count].setMaximumWidth(150)
        self.count += 1

        self.dc_entry_var[self.count] = QtGui.QLineEdit()  # start
        self.dcgrid.addWidget(self.dc_entry_var[self.count], 6, 1)
        self.dc_entry_var[self.count].setMaximumWidth(150)
        self.count += 1

        self.dc_entry_var[self.count] = QtGui.QLineEdit()  # increment
        self.dcgrid.addWidget(self.dc_entry_var[self.count], 7, 1)
        self.dc_entry_var[self.count].setMaximumWidth(150)
        self.count += 1

        self.dc_entry_var[self.count] = QtGui.QLineEdit()  # stop
        self.dcgrid.addWidget(self.dc_entry_var[self.count], 8, 1)
        self.dc_entry_var[self.count].setMaximumWidth(150)

        self.parameter_cnt = 0
        self.start_combo = QtGui.QComboBox(self)
        self.start_combo.setMaximumWidth(150)
        self.start_combo.addItem('Volts or Amperes')
        self.start_combo.addItem('mV or mA')
        self.start_combo.addItem('uV or uA')
        self.start_combo.addItem("nV or nA")
        self.start_combo.addItem("pV or pA")
        self.dcgrid.addWidget(self.start_combo, 2, 2)

        try:
            self.dc_parameter[self.parameter_cnt] = str(
                json_data["analysis"]["dc"]["Start Combo"])
        except BaseException:
            self.dc_parameter[self.parameter_cnt] = "Volts or Amperes"

        self.start_combo.activated[str].connect(self.start_changecombo)
        self.parameter_cnt += 1

        self.increment_combo = QtGui.QComboBox(self)
        self.increment_combo.setMaximumWidth(150)
        self.increment_combo.addItem("Volts or Amperes")
        self.increment_combo.addItem("mV or mA")
        self.increment_combo.addItem("uV or uA")
        self.increment_combo.addItem("nV or nA")
        self.increment_combo.addItem("pV or pA")
        self.dcgrid.addWidget(self.increment_combo, 3, 2)

        try:
            self.dc_parameter[self.parameter_cnt] = str(
                json_data["analysis"]["dc"]["Increment Combo"])
        except BaseException:
            self.dc_parameter[self.parameter_cnt] = "Volts or Amperes"

        self.increment_combo.activated[str].connect(self.increment_changecombo)
        self.parameter_cnt += 1

        self.stop_combo = QtGui.QComboBox(self)
        self.stop_combo.setMaximumWidth(150)
        self.stop_combo.addItem("Volts or Amperes")
        self.stop_combo.addItem("mV or mA")
        self.stop_combo.addItem("uV or uA")
        self.stop_combo.addItem("nV or nA")
        self.stop_combo.addItem("pV or pA")
        self.dcgrid.addWidget(self.stop_combo, 4, 2)

        try:
            self.dc_parameter[self.parameter_cnt] = str(
                json_data["analysis"]["dc"]["Stop Combo"])
        except BaseException:
            self.dc_parameter[self.parameter_cnt] = "Volts or Amperes"

        self.stop_combo.activated[str].connect(self.stop_changecombo)
        self.parameter_cnt += 1

        self.start_combo2 = QtGui.QComboBox(self)
        self.start_combo2.setMaximumWidth(150)
        self.start_combo2.addItem('Volts or Amperes')
        self.start_combo2.addItem('mV or mA')
        self.start_combo2.addItem('uV or uA')
        self.start_combo2.addItem("nV or nA")
        self.start_combo2.addItem("pV or pA")
        self.dcgrid.addWidget(self.start_combo2, 6, 2)

        try:
            self.dc_parameter[self.parameter_cnt] = str(
                json_data["analysis"]["dc"]["Start Combo2"])
        except BaseException:
            self.dc_parameter[self.parameter_cnt] = "Volts or Amperes"

        self.start_combo2.activated[str].connect(self.start_changecombo2)
        self.parameter_cnt += 1

        self.increment_combo2 = QtGui.QComboBox(self)
        self.increment_combo2.setMaximumWidth(150)
        self.increment_combo2.addItem("Volts or Amperes")
        self.increment_combo2.addItem("mV or mA")
        self.increment_combo2.addItem("uV or uA")
        self.increment_combo2.addItem("nV or nA")
        self.increment_combo2.addItem("pV or pA")
        self.dcgrid.addWidget(self.increment_combo2, 7, 2)

        try:
            self.dc_parameter[self.parameter_cnt] = str(
                json_data["analysis"]["dc"]["Increment Combo2"])
        except BaseException:
            self.dc_parameter[self.parameter_cnt] = "Volts or Amperes"

        self.increment_combo2.activated[str].connect(
            self.increment_changecombo2)
        self.parameter_cnt += 1

        self.stop_combo2 = QtGui.QComboBox(self)
        self.stop_combo2.setMaximumWidth(150)
        self.stop_combo2.addItem("Volts or Amperes")
        self.stop_combo2.addItem("mV or mA")
        self.stop_combo2.addItem("uV or uA")
        self.stop_combo2.addItem("nV or nA")
        self.stop_combo2.addItem("pV or pA")
        self.dcgrid.addWidget(self.stop_combo2, 8, 2)

        try:
            self.dc_parameter[self.parameter_cnt] = str(
                json_data["analysis"]["dc"]["Stop Combo2"])
        except BaseException:
            self.dc_parameter[self.parameter_cnt] = "Volts or Amperes"

        self.stop_combo2.activated[str].connect(self.stop_changecombo2)
        self.parameter_cnt += 1

        self.check = QtGui.QCheckBox('Operating Point Analysis', self)
        try:
            self.track_obj.op_check.append(
                str(json_data["analysis"]["dc"]["Operating Point"]))
        except BaseException:
            self.track_obj.op_check.append('0')

        # QtCore.QObject.connect(check,SIGNAL("stateChanged()"),check,SLOT("checkedSlot"))
        self.check.stateChanged.connect(self.setflag)
        # self.flagcheck = 1
        # self.flagcheck= 2
        self.dcgrid.addWidget(self.check, 9, 1, 9, 2)
        self.track_obj.DC_entry_var["ITEMS"] = self.dc_entry_var
        self.track_obj.DC_Parameter["ITEMS"] = self.dc_parameter

        # CSS
        self.dcbox.setStyleSheet(" \
        QGroupBox { border: 1px solid gray; border-radius: 9px; margin-top: \
        0.5em; } \
        QGroupBox::title { subcontrol-origin: margin; left: \
        10px; padding: 0 3px 0 3px; } \
        ")
        if check:
            try:
                self.dc_entry_var[0].setText(
                    json_data["analysis"]["dc"]["Source 1"])
                self.dc_entry_var[1].setText(
                    json_data["analysis"]["dc"]["Start"])
                self.dc_entry_var[2].setText(
                    json_data["analysis"]["dc"]["Increment"])
                self.dc_entry_var[3].setText(
                    json_data["analysis"]["dc"]["Stop"])
                index = self.start_combo.findText(
                    json_data["analysis"]["dc"]["Start Combo"])
                self.start_combo.setCurrentIndex(index)
                index = self.increment_combo.findText(
                    json_data["analysis"]["dc"]["Increment Combo"])
                self.increment_combo.setCurrentIndex(index)
                index = self.stop_combo.findText(
                    json_data["analysis"]["dc"]["Stop Combo"])
                self.stop_combo.setCurrentIndex(index)
                self.dc_entry_var[4].setText(
                    json_data["analysis"]["dc"]["Source 2"])
                self.dc_entry_var[5].setText(
                    json_data["analysis"]["dc"]["Start2"])
                self.dc_entry_var[6].setText(
                    json_data["analysis"]["dc"]["Increment2"])
                self.dc_entry_var[7].setText(
                    json_data["analysis"]["dc"]["Stop2"])
                index = self.start_combo2.findText(
                    json_data["analysis"]["dc"]["Start Combo2"])
                self.start_combo2.setCurrentIndex(index)
                index = self.increment_combo2.findText(
                    json_data["analysis"]["dc"]["Increment Combo2"])
                self.increment_combo2.setCurrentIndex(index)
                index = self.stop_combo2.findText(
                    json_data["analysis"]["dc"]["Stop Combo2"])
                self.stop_combo2.setCurrentIndex(index)

                if json_data["analysis"]["dc"]["Operating Point"] == 1:
                    self.check.setChecked(True)
                else:
                    self.check.setChecked(False)
            except BaseException:
                print("DC Analysis JSON Parse Error")

        return self.dcbox

    # Below 6 functions to handle combo boxes for the DC group
    def start_changecombo(self, text):
        """Handle start combo box, ie. units, as mV, V..."""
        self.dc_parameter[0] = str(text)

    def increment_changecombo(self, text):
        """Handle increment combo box, ie. units, as mV, V..."""
        self.dc_parameter[1] = str(text)

    def stop_changecombo(self, text):
        """Handle stop combo box, ie. units, as mV, V..."""
        self.dc_parameter[2] = str(text)

    def start_changecombo2(self, text):
        """Handle second start combo box, ie. units, as mV, V..."""
        self.dc_parameter[3] = str(text)

    def increment_changecombo2(self, text):
        """Handle second increment combo box, ie. units, as mV, V..."""
        self.dc_parameter[4] = str(text)

    def stop_changecombo2(self, text):
        """Handle second stop combo box, ie. units, as mV, V..."""
        self.dc_parameter[5] = str(text)

    def setflag(self):
        """
        - Handles the Operating point analysis checkbox
        """
        if self.check.isChecked():
            self.track_obj.op_check.append(1)
        else:
            self.track_obj.op_check.append(0)

    def createTRANgroup(self):
        """
        - Creating transient group under analysis and creating it's components
        - Contains 3 inout and combo boxes for -
        - - Start time
        - - Step time
        - - Stop time
        - Input boxes for values, combo boxes for unit
        - Accordingly also event handlers for combo boxes, creates 3 functions
        """
        kicadFile = self.clarg1
        (projpath, filename) = os.path.split(kicadFile)
        project_name = os.path .basename(projpath)
        check = 1

        try:
            f = open(
                os.path.join(
                    projpath,
                    project_name +
                    "_Previous_Values.json"),
                'r')
            data = f.read()
            json_data = json.loads(data)
        except BaseException:
            check = 0
            print("Transient Previous Values JSON is Empty")

        self.trbox = QtGui.QGroupBox()
        self.trbox.setTitle("Transient Analysis")
        # self.trbox.setDisabled(True)
        self.trgrid = QtGui.QGridLayout()
        self.trbox.setLayout(self.trgrid)

        self.start = QtGui.QLabel("Start Time")
        self.step = QtGui.QLabel("Step Time")
        self.stop = QtGui.QLabel("Stop Time")
        self.trgrid.addWidget(self.start, 1, 0)
        self.trgrid.addWidget(self.step, 2, 0)
        self.trgrid.addWidget(self.stop, 3, 0)
        self.count = 0

        self.tran_entry_var[self.count] = QtGui.QLineEdit()
        self.trgrid.addWidget(self.tran_entry_var[self.count], 1, 1)
        self.tran_entry_var[self.count].setMaximumWidth(150)
        self.count += 1

        self.tran_entry_var[self.count] = QtGui.QLineEdit()
        self.trgrid.addWidget(self.tran_entry_var[self.count], 2, 1)
        self.tran_entry_var[self.count].setMaximumWidth(150)
        self.count += 1

        self.tran_entry_var[self.count] = QtGui.QLineEdit()
        self.trgrid.addWidget(self.tran_entry_var[self.count], 3, 1)
        self.tran_entry_var[self.count].setMaximumWidth(150)
        self.count += 1

        self.parameter_cnt = 0
        self.start_combobox = QtGui.QComboBox()
        self.start_combobox.addItem("Sec")
        self.start_combobox.addItem("ms")
        self.start_combobox.addItem("us")
        self.start_combobox.addItem("ns")
        self.start_combobox.addItem("ps")
        self.trgrid.addWidget(self.start_combobox, 1, 3)

        try:
            self.tran_parameter[self.parameter_cnt] = str(
                json_data["analysis"]["tran"]["Start Combo"])
        except BaseException:
            self.tran_parameter[self.parameter_cnt] = "Sec"

        self.start_combobox.activated[str].connect(self.start_combo_change)
        self.parameter_cnt += 1

        self.step_combobox = QtGui.QComboBox()
        self.step_combobox.addItem("Sec")
        self.step_combobox.addItem("ms")
        self.step_combobox.addItem("us")
        self.step_combobox.addItem("ns")
        self.step_combobox.addItem("ps")
        self.trgrid.addWidget(self.step_combobox, 2, 3)
        try:
            self.tran_parameter[self.parameter_cnt] = str(
                json_data["analysis"]["tran"]["Step Combo"])
        except BaseException:
            self.tran_parameter[self.parameter_cnt] = "Sec"

        self.step_combobox.activated[str].connect(self.step_combo_change)
        self.parameter_cnt += 1

        self.stop_combobox = QtGui.QComboBox()
        self.stop_combobox.addItem("Sec")
        self.stop_combobox.addItem("ms")
        self.stop_combobox.addItem("us")
        self.stop_combobox.addItem("ns")
        self.stop_combobox.addItem("ps")
        self.trgrid.addWidget(self.stop_combobox, 3, 3)
        try:
            self.tran_parameter[self.parameter_cnt] = str(
                json_data["analysis"]["tran"]["Stop Combo"])
        except BaseException:
            self.tran_parameter[self.parameter_cnt] = "Sec"

        self.stop_combobox.activated[str].connect(self.stop_combo_change)
        self.parameter_cnt += 1

        self.track_obj.TRAN_entry_var["ITEMS"] = self.tran_entry_var
        self.track_obj.TRAN_Parameter["ITEMS"] = self.tran_parameter

        # CSS
        self.trbox.setStyleSheet(" \
        QGroupBox { border: 1px solid gray; border-radius: \
        9px; margin-top: 0.5em; } \
        QGroupBox::title { subcontrol-origin: margin; left: \
         10px; padding: 0 3px 0 3px; } \
        ")
        if check:
            try:
                self.tran_entry_var[0].setText(
                    json_data["analysis"]["tran"]["Start Time"])
                self.tran_entry_var[1].setText(
                    json_data["analysis"]["tran"]["Step Time"])
                self.tran_entry_var[2].setText(
                    json_data["analysis"]["tran"]["Stop Time"])
                index = self.start_combobox.findText(
                    json_data["analysis"]["tran"]["Start Combo"])
                self.start_combobox.setCurrentIndex(index)
                index = self.step_combobox.findText(
                    json_data["analysis"]["tran"]["Step Combo"])
                self.step_combobox.setCurrentIndex(index)
                index = self.stop_combobox.findText(
                    json_data["analysis"]["tran"]["Stop Combo"])
                self.stop_combobox.setCurrentIndex(index)
            except BaseException:
                print("Transient Analysis JSON Parse Error")

        return self.trbox
    '''
    - Below 3 functions handle event for the combo box in transient group
    '''

    def start_combo_change(self, text):
        """Handle start combo box, ie. units, as second, ms"""
        self.tran_parameter[0] = str(text)

    def step_combo_change(self, text):
        """Handle step combo box, ie. units, as second, ms..."""
        self.tran_parameter[1] = str(text)

    def stop_combo_change(self, text):
        """Handle stop combo box, ie. units, as second, ms..."""
        self.tran_parameter[2] = str(text)
