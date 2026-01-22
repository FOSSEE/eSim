from PyQt5 import QtWidgets, QtCore
import os
from xml.etree import ElementTree as ET
from . import TrackWidget


class DeviceModel(QtWidgets.QWidget):
    """
    - This class creates Device Library Tab in KicadtoNgspice Window
      It dynamically creates the widget for device like diode,mosfet,
      transistor and jfet.
    - Same function as the subCircuit file, except for
      this takes different parameters in the if block
        - q   TRANSISTOR
        - d   DIODE
        - j   JFET
        - m   MOSFET
        - s   SWITCH
        - tx  single lossy transmission line
    - Other 2 functions same as the ones in subCircuit
        - trackLibrary
        - trackLibraryWithoutButton
    """

    def __init__(self, schematicInfo, clarg1):

        self.clarg1 = clarg1
        kicadFile = self.clarg1
        (projpath, filename) = os.path.split(kicadFile)
        project_name = os.path.basename(projpath)
        self.root = []
        try:
            f = open(
                os.path.join(
                    projpath,
                    project_name +
                    "_Previous_Values.xml"),
                'r')
            tree = ET.parse(f)
            parent_self = tree.getroot()
            for child in parent_self:
                if child.tag == "devicemodel":
                    self.root = child
        except BaseException:
            print("Device Model Previous XML is Empty")

        QtWidgets.QWidget.__init__(self)

        # Creating track widget object
        self.obj_trac = TrackWidget.TrackWidget()

        # Row and column count
        self.row = 0
        self.count = 1  # Entry count
        self.entry_var = {}

        # For MOSFET
        self.widthLabel = {}
        self.lengthLabel = {}
        self.parameterLabel = {}
        self.multifactorLable = {}
        self.devicemodel_dict_beg = {}
        self.devicemodel_dict_end = {}
        # List to hold information about device
        self.deviceDetail = {}

        # Set Layout
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)
        # print("Reading Device model details from Schematic")
        if "sky130" in " ".join(schematicInfo):
            self.eSim_sky130(schematicInfo)
        else:
            self.eSim_general_libs(schematicInfo)

    def eSim_sky130(self, schematicInfo):
        sky130box = QtWidgets.QGroupBox()
        sky130grid = QtWidgets.QGridLayout()
        self.count = self.count+1
        self.row = self.row + 1
        self.devicemodel_dict_beg["scmode1"] = self.count
        beg = self.count
        self.deviceDetail[self.count] = "scmode1"
        sky130box.setTitle("Add parameters of SKY130 library ")
        # +
        # " : " +
        # words[6])
        self.parameterLabel[self.count] = QtWidgets.QLabel("Enter the path ")
        self.row = self.row + 1
        sky130grid.addWidget(self.parameterLabel[self.count], self.row, 0)
        self.entry_var[self.count] = QtWidgets.QLineEdit()
        self.entry_var[self.count].setReadOnly(True)

        for child in self.root:
            if child.tag == "scmode1":
                if child[0].text \
                   and os.path.exists(child[0].text):
                    self.entry_var[self.count] \
                        .setText(child[0].text)
                    path_name = child[0].text
                else:
                    if os.name == 'nt':
                        path_name = os.path.abspath(
                            "library/" +
                            "sky130_fd_pr/models/sky130.lib.spice"
                        )
                    else:
                        path_name = os.path.abspath(
                            "/usr/share/local/" +
                            "sky130_fd_pr/models/sky130.lib.spice"
                        )
                    self.entry_var[self.count].setText(path_name)
        # self.trackLibraryWithoutButton(self.count, path_name)

        sky130grid.addWidget(self.entry_var[self.count], self.row, 1)
        self.addbtn = QtWidgets.QPushButton("Add")
        self.addbtn.setObjectName("%d" % beg)
        self.addbtn.clicked.connect(self.trackLibrary)
        sky130grid.addWidget(self.addbtn, self.row, 2)
        # self.count = self.count + 1
        self.adddefaultbtn = QtWidgets.QPushButton("Add Default")
        self.adddefaultbtn.setObjectName("%d" % beg)
        self.adddefaultbtn.clicked.connect(self.trackDefaultLib)
        sky130grid.addWidget(self.adddefaultbtn, self.row, 3)
        self.count = self.count + 1
        self.parameterLabel[self.count] = QtWidgets.QLabel(
            "Enter the corner e.g. tt")
        self.row = self.row + 1
        sky130grid.addWidget(self.parameterLabel[self.count], self.row, 0)
        self.entry_var[self.count] = QtWidgets.QLineEdit()
        self.entry_var[self.count].setText("")
        self.entry_var[self.count].setMaximumWidth(150)
        self.entry_var[self.count].setObjectName("%d" % beg)
        path_name = ''
        for child in self.root:
            if child.tag == "scmode1":
                if child[1].text:
                    self.entry_var[self.count] \
                        .setText(child[1].text)
                    path_name = child[0].text
                else:
                    self.entry_var[self.count].setText("")

        sky130grid.addWidget(self.entry_var[self.count], self.row, 1)
        self.entry_var[self.count].textChanged.connect(self.textChange)
        self.trackLibraryWithoutButton(beg, path_name)

        sky130box.setLayout(sky130grid)
        sky130box.setStyleSheet(" \
                QGroupBox { border: 1px solid gray; border-radius:\
                 9px; margin-top: 0.5em; } \
                QGroupBox::title { subcontrol-origin: margin; left:\
                 10px; padding: 0 3px 0 3px; } \
                ")
        self.grid.addWidget(sky130box)
        # if self.entry_var[self.count-3].text() == "":
        #    pass
        # else:
        #   self.trackLibraryWithoutButton(self.count-3, path_name)

        self.row = self.row + 1
        self.devicemodel_dict_end["scmode1"] = self.count
        self.count = self.count + 1

        for eachline in schematicInfo:
            print("=========================================")
            print(eachline)
            words = eachline.split()
            # supporteddesignator = ['sc', 'u', 'x', 'v', 'i', 'a']
            if eachline[0:2] != 'sc' and eachline[0] != 'u' \
                    and eachline[0] != 'x' and eachline[0] != '*'\
                    and eachline[0] != 'v' and eachline[0] != 'i'\
                    and eachline[0] != 'a':
                print("Only components with designators 'sc', 'u', \
'x', 'v', 'i', 'a'\
                     can be used with SKY130 mode")
                print("Please remove other components")
                self.msg = QtWidgets.QErrorMessage()
                self.msg.setModal(True)
                self.msg.setWindowTitle("Invalid components")
                self.content = "Only components with designators " + \
                               "'sc', 'u' and 'x' can be used \
                               with SKY130 mode. " + \
                               "Please edit the schematic and \
                               generate netlist again"
                self.msg.showMessage(self.content)
                self.msg.exec_()
                return

            elif eachline[0:2] == 'sc' and eachline[0:6] != 'scmode':
                self.devicemodel_dict_beg[words[0]] = self.count
                self.deviceDetail[self.count] = words[0]
                sky130box = QtWidgets.QGroupBox()
                sky130grid = QtWidgets.QGridLayout()
                beg = self.count
                sky130box.setTitle(
                    "Add parameters for " +
                    words[0] + " : " + words[-1])
                path_name = ''

                # Adding to get SKY130 dimension
                self.parameterLabel[self.count] = QtWidgets.QLabel(
                    "Enter the parameters of SKY130 component " + words[0])
                sky130grid.addWidget(
                    self.parameterLabel[self.count], self.row, 0)
                self.entry_var[self.count] = QtWidgets.QLineEdit()
                self.entry_var[self.count].setText("")
                self.entry_var[self.count].setMaximumWidth(1000)
                self.entry_var[self.count].setObjectName("%d" % beg)
                sky130grid.addWidget(self.entry_var[self.count], self.row, 1)
                self.entry_var[self.count].textChanged.connect(self.textChange)
                sky130box.setLayout(sky130grid)
                sky130box.setStyleSheet(" \
                QGroupBox { border: 1px solid gray; border-radius: \
                9px; margin-top: 0.5em; } \
                QGroupBox::title { subcontrol-origin: margin; left:\
                 10px; padding: 0 3px 0 3px; } \
                ")
                try:
                    for child in self.root:
                        if child.tag == words[0]:
                            # print("DEVICE MODEL MATCHING---", \
                            #       child.tag, words[0])
                            try:
                                if child[0].text:
                                    self.entry_var[self.count] \
                                        .setText(child[0].text)
                                    path_name = child[0].text
                                else:
                                    self.entry_var[self.count].setText("")
                                    path_name = ""
                            except BaseException as e:
                                print("Error when set text of Device " +
                                      "SKY130 Component :", str(e))
                except BaseException:
                    pass
                self.trackLibraryWithoutButton(self.count, path_name)
                self.grid.addWidget(sky130box)

                # Adding Device Details #

                # Increment row and widget count
                self.row = self.row + 1
                self.devicemodel_dict_end[words[0]] = self.count
                self.count = self.count + 1

            self.show()

    def eSim_general_libs(self, schematicInfo):
        for eachline in schematicInfo:
            print("=========================================")
            print(eachline)
            words = eachline.split()
            if eachline[0] == 'q':
                # print("Device Model Transistor: ", words[0])
                self.devicemodel_dict_beg[words[0]] = self.count
                transbox = QtWidgets.QGroupBox()
                transgrid = QtWidgets.QGridLayout()
                transbox.setTitle(
                    "Add library for Transistor " +
                    words[0] +
                    " : " +
                    words[4])
                self.entry_var[self.count] = QtWidgets.QLineEdit()
                self.entry_var[self.count].setText("")
                self.entry_var[self.count].setReadOnly(True)
                global path_name

                try:
                    for child in self.root:
                        if child.tag == words[0]:
                            # print("DEVICE MODEL MATCHING---", \
                            #       child.tag, words[0])
                            try:
                                if child[0].text \
                                   and os.path.exists(child[0].text):
                                    self.entry_var[self.count] \
                                        .setText(child[0].text)
                                    path_name = child[0].text
                                else:
                                    self.entry_var[self.count].setText("")
                            except BaseException as e:
                                print("Error when set text of device " +
                                      "model transistor :", str(e))
                except BaseException:
                    pass

                transgrid.addWidget(self.entry_var[self.count], self.row, 1)
                self.addbtn = QtWidgets.QPushButton("Add")
                self.addbtn.setObjectName("%d" % self.count)
                self.addbtn.clicked.connect(self.trackLibrary)
                self.deviceDetail[self.count] = words[0]

                if self.entry_var[self.count].text() == "":
                    pass
                else:
                    self.trackLibraryWithoutButton(self.count, path_name)

                transgrid.addWidget(self.addbtn, self.row, 2)
                transbox.setLayout(transgrid)

                # CSS
                transbox.setStyleSheet(" \
                QGroupBox { border: 1px solid gray; border-radius: \
                9px; margin-top: 0.5em; } \
                QGroupBox::title { subcontrol-origin: margin; left:\
                 10px; padding: 0 3px 0 3px; } \
                ")

                self.grid.addWidget(transbox)

                # Adding Device Details #

                # Increment row and widget count
                self.row = self.row + 1
                self.devicemodel_dict_end[words[0]] = self.count
                self.count = self.count + 1

            elif eachline[0] == 'd':
                # print("Device Model Diode:", words[0])
                self.devicemodel_dict_beg[words[0]] = self.count
                diodebox = QtWidgets.QGroupBox()
                diodegrid = QtWidgets.QGridLayout()
                diodebox.setTitle(
                    "Add library for Diode " +
                    words[0] +
                    " : " +
                    words[3])
                self.entry_var[self.count] = QtWidgets.QLineEdit()
                self.entry_var[self.count].setText("")
                self.entry_var[self.count].setReadOnly(True)
                # global path_name
                try:
                    for child in self.root:
                        if child.tag == words[0]:
                            # print("DEVICE MODEL MATCHING---", \
                            #       child.tag, words[0])
                            try:
                                if child[0].text \
                                   and os.path.exists(child[0].text):
                                    path_name = child[0].text
                                    self.entry_var[self.count] \
                                        .setText(child[0].text)
                                else:
                                    self.entry_var[self.count].setText("")
                            except BaseException as e:
                                print("Error when set text of device " +
                                      "model diode :", str(e))
                except BaseException:
                    pass

                diodegrid.addWidget(self.entry_var[self.count], self.row, 1)
                self.addbtn = QtWidgets.QPushButton("Add")
                self.addbtn.setObjectName("%d" % self.count)
                self.addbtn.clicked.connect(self.trackLibrary)
                self.deviceDetail[self.count] = words[0]

                if self.entry_var[self.count].text() == "":
                    pass
                else:
                    self.trackLibraryWithoutButton(self.count, path_name)

                diodegrid.addWidget(self.addbtn, self.row, 2)
                diodebox.setLayout(diodegrid)

                # CSS
                diodebox.setStyleSheet(" \
                QGroupBox { border: 1px solid gray; border-radius: \
                9px; margin-top: 0.5em; } \
                QGroupBox::title { subcontrol-origin: margin; left:\
                 10px; padding: 0 3px 0 3px; } \
                ")

                self.grid.addWidget(diodebox)

                # Adding Device Details #

                # Increment row and widget count
                self.row = self.row + 1
                self.devicemodel_dict_end[words[0]] = self.count
                self.count = self.count + 1

            elif eachline[0] == 'j':
                # print("Device Model JFET:", words[0])
                self.devicemodel_dict_beg[words[0]] = self.count
                jfetbox = QtWidgets.QGroupBox()
                jfetgrid = QtWidgets.QGridLayout()
                jfetbox.setTitle(
                    "Add library for JFET " +
                    words[0] +
                    " : " +
                    words[4])
                self.entry_var[self.count] = QtWidgets.QLineEdit()
                self.entry_var[self.count].setText("")
                self.entry_var[self.count].setReadOnly(True)
                # global path_name
                try:
                    for child in self.root:
                        if child.tag == words[0]:
                            # print("DEVICE MODEL MATCHING---", \
                            #       child.tag, words[0])
                            try:
                                if child[0].text \
                                   and os.path.exists(child[0].text):
                                    self.entry_var[self.count] \
                                        .setText(child[0].text)
                                    path_name = child[0].text
                                else:
                                    self.entry_var[self.count].setText("")
                            except BaseException as e:
                                print("Error when set text of Device " +
                                      "Model JFET :", str(e))
                except BaseException:
                    pass

                jfetgrid.addWidget(self.entry_var[self.count], self.row, 1)
                self.addbtn = QtWidgets.QPushButton("Add")
                self.addbtn.setObjectName("%d" % self.count)
                self.addbtn.clicked.connect(self.trackLibrary)
                self.deviceDetail[self.count] = words[0]

                if self.entry_var[self.count].text() == "":
                    pass
                else:
                    self.trackLibraryWithoutButton(self.count, path_name)

                jfetgrid.addWidget(self.addbtn, self.row, 2)
                jfetbox.setLayout(jfetgrid)

                # CSS
                jfetbox.setStyleSheet(" \
                QGroupBox { border: 1px solid gray; border-radius:\
                 9px; margin-top: 0.5em; } \
                QGroupBox::title { subcontrol-origin: margin; left:\
                 10px; padding: 0 3px 0 3px; } \
                ")

                self.grid.addWidget(jfetbox)

                # Adding Device Details #
                # Increment row and widget count
                self.row = self.row + 1
                self.devicemodel_dict_end[words[0]] = self.count
                self.count = self.count + 1

            elif eachline[0] == 's':
                # print("Device Model Switch:", words[0])
                self.devicemodel_dict_beg[words[0]] = self.count
                switchbox = QtWidgets.QGroupBox()
                switchgrid = QtWidgets.QGridLayout()
                switchbox.setTitle(
                    "Add library for Switch " +
                    words[0] +
                    " : " +
                    words[5])
                self.entry_var[self.count] = QtWidgets.QLineEdit()
                self.entry_var[self.count].setText("")
                # global path_name
                try:
                    for child in root:
                        if child.tag == words[0]:
                            # print("DEVICE MODEL MATCHING---", \
                            #       child.tag, words[0])
                            try:
                                if child[0].text \
                                   and os.path.exists(child[0].text):
                                    path_name = child[0].text
                                    self.entry_var[self.count] \
                                        .setText(child[0].text)
                                else:
                                    self.entry_var[self.count].setText("")
                            except BaseException as e:
                                print("Error when set text of device " +
                                      "model switch :", str(e))
                except BaseException:
                    pass

                switchgrid.addWidget(self.entry_var[self.count], self.row, 1)
                self.addbtn = QtWidgets.QPushButton("Add")
                self.addbtn.setObjectName("%d" % self.count)
                self.addbtn.clicked.connect(self.trackLibrary)
                self.deviceDetail[self.count] = words[0]

                if self.entry_var[self.count].text() == "":
                    pass
                else:
                    self.trackLibraryWithoutButton(self.count, path_name)

                switchgrid.addWidget(self.addbtn, self.row, 2)
                switchbox.setLayout(switchgrid)

                # CSS
                switchbox.setStyleSheet(" \
                QGroupBox { border: 1px solid gray; border-radius: \
                9px; margin-top: 0.5em; } \
                QGroupBox::title { subcontrol-origin: margin; left:\
                 10px; padding: 0 3px 0 3px; } \
                ")

                self.grid.addWidget(switchbox)

                # Adding Device Details #

                # Increment row and widget count
                self.row = self.row + 1
                self.devicemodel_dict_end[words[0]] = self.count
                self.count = self.count + 1

            elif eachline[0] == 'ytxl':
                # print("Device Model ymod:", words[0])
                self.devicemodel_dict_beg[words[0]] = self.count
                ymodbox = QtWidgets.QGroupBox()
                ymodgrid = QtWidgets.QGridLayout()
                ymodbox.setTitle(
                    "Add library for ymod " +
                    words[0] +
                    " : " +
                    words[4])
                self.entry_var[self.count] = QtWidgets.QLineEdit()
                self.entry_var[self.count].setText("")
                # global path_name
                try:
                    for child in root:
                        if child.tag == words[0]:
                            # print("DEVICE MODEL MATCHING---", \
                            #       child.tag, words[0])
                            try:
                                if child[0].text \
                                   and os.path.exists(child[0].text):
                                    path_name = child[0].text
                                    self.entry_var[self.count] \
                                        .setText(child[0].text)
                                else:
                                    self.entry_var[self.count].setText("")
                            except BaseException as e:
                                print("Error when set text of device " +
                                      "model ymod :", str(e))
                except BaseException:
                    pass

                ymodgrid.addWidget(self.entry_var[self.count], self.row, 1)
                self.addbtn = QtWidgets.QPushButton("Add")
                self.addbtn.setObjectName("%d" % self.count)
                self.addbtn.clicked.connect(self.trackLibrary)
                self.deviceDetail[self.count] = words[0]

                if self.entry_var[self.count].text() == "":
                    pass
                else:
                    self.trackLibraryWithoutButton(self.count, path_name)

                ymodgrid.addWidget(self.addbtn, self.row, 2)
                ymodbox.setLayout(ymodgrid)

                # CSS
                ymodbox.setStyleSheet(" \
                QGroupBox { border: 1px solid gray; border-radius: \
                9px; margin-top: 0.5em; } \
                QGroupBox::title { subcontrol-origin: margin; left:\
                 10px; padding: 0 3px 0 3px; } \
                ")

                self.grid.addWidget(ymodbox)

                # Adding Device Details #

                # Increment row and widget count
                self.row = self.row + 1
                self.devicemodel_dict_end[words[0]] = self.count
                self.count = self.count + 1

            elif eachline[0] == 'm':

                self.devicemodel_dict_beg[words[0]] = self.count
                mosfetbox = QtWidgets.QGroupBox()
                mosfetgrid = QtWidgets.QGridLayout()
                i = self.count
                beg = self.count
                mosfetbox.setTitle(
                    "Add library for MOSFET " +
                    words[0] +
                    " : " +
                    words[4])
                self.entry_var[self.count] = QtWidgets.QLineEdit()
                self.entry_var[self.count].setText("")
                self.entry_var[self.count].setReadOnly(True)
                mosfetgrid.addWidget(self.entry_var[self.count], self.row, 1)
                self.addbtn = QtWidgets.QPushButton("Add")
                self.addbtn.setObjectName("%d" % self.count)
                self.addbtn.clicked.connect(self.trackLibrary)
                mosfetgrid.addWidget(self.addbtn, self.row, 2)

                # Adding Device Details
                self.deviceDetail[self.count] = words[0]

                # Increment row and widget count
                self.row = self.row + 1
                self.count = self.count + 1

                # Adding to get MOSFET dimension
                self.widthLabel[self.count] = QtWidgets.QLabel(
                    "Enter width of MOSFET " + words[0] + "(default=100u):")
                mosfetgrid.addWidget(self.widthLabel[self.count], self.row, 0)
                self.entry_var[self.count] = QtWidgets.QLineEdit()
                self.entry_var[self.count].setText("")
                self.entry_var[self.count].setMaximumWidth(150)
                mosfetgrid.addWidget(self.entry_var[self.count], self.row, 1)
                self.row = self.row + 1
                self.count = self.count + 1

                self.lengthLabel[self.count] = QtWidgets.QLabel(
                    "Enter length of MOSFET " + words[0] + "(default=100u):")
                mosfetgrid.addWidget(self.lengthLabel[self.count], self.row, 0)
                self.entry_var[self.count] = QtWidgets.QLineEdit()
                self.entry_var[self.count].setText("")
                self.entry_var[self.count].setMaximumWidth(150)
                mosfetgrid.addWidget(self.entry_var[self.count], self.row, 1)
                self.row = self.row + 1
                self.count = self.count + 1

                self.multifactorLable[self.count] = QtWidgets.QLabel(
                    "Enter multiplicative factor of MOSFET " +
                    words[0] + "(default=1):")
                mosfetgrid.addWidget(
                    self.multifactorLable[self.count], self.row, 0)
                self.entry_var[self.count] = QtWidgets.QLineEdit()
                self.entry_var[self.count].setText("")
                end = self.count
                self.entry_var[self.count].setMaximumWidth(150)
                mosfetgrid.addWidget(self.entry_var[self.count], self.row, 1)
                self.row = self.row + 1
                self.devicemodel_dict_end[words[0]] = self.count
                self.count = self.count + 1
                mosfetbox.setLayout(mosfetgrid)

                # global path_name
                try:
                    for child in self.root:
                        if child.tag == words[0]:
                            # print("DEVICE MODEL MATCHING---", \
                            #       child.tag, words[0])
                            while i <= end:
                                self.entry_var[i].setText(child[i - beg].text)
                                if (i - beg) == 0:
                                    if os.path.exists(child[0].text):
                                        self.entry_var[i] \
                                            .setText(child[i - beg].text)
                                        path_name = child[i - beg].text
                                    else:
                                        self.entry_var[i].setText("")
                                i = i + 1
                except BaseException:
                    pass
                # CSS
                mosfetbox.setStyleSheet(" \
                QGroupBox { border: 1px solid gray; border-radius:\
                 9px; margin-top: 0.5em; } \
                QGroupBox::title { subcontrol-origin: margin; left: \
                10px; padding: 0 3px 0 3px; } \
                ")
                if self.entry_var[beg].text() == "":
                    pass
                else:
                    self.trackLibraryWithoutButton(beg, path_name)

                self.grid.addWidget(mosfetbox)

            self.show()

    def trackDefaultLib(self):
        sending_btn = self.sender()
        self.widgetObjCount = int(sending_btn.objectName())
        if os.name == 'nt':
            path_name = os.path.abspath(
                "library/" +
                "sky130_fd_pr/models/sky130.lib.spice"
            )
        else:
            path_name = os.path.abspath(
                "/usr/share/local/" +
                "sky130_fd_pr/models/sky130.lib.spice"
            )
        self.entry_var[self.widgetObjCount].setText(path_name)
        self.trackLibraryWithoutButton(self.widgetObjCount, path_name)

    def textChange(self):
        sending_btn = self.sender()
        self.widgetObjCount = int(sending_btn.objectName())
        self.deviceName = self.deviceDetail[self.widgetObjCount]
        # self.widgetObjCount = self.count_beg
        # if self.deviceName[0] == 'm':
        #     width = str(self.entry_var[self.widgetObjCount + 1].text())
        #     length = str(self.entry_var[self.widgetObjCount + 2].text())
        #     multifactor = str(self.entry_var[self.widgetObjCount + 3].text())
        #     if width == "":
        #         width = "100u"
        #     if length == "":
        #         length = "100u"
        #     if multifactor == "":
        #         multifactor = "1"

        #     self.obj_trac.deviceModelTrack[self.deviceName] =\
        # str(self.entry_var[self.widgetObjCount].text()) + \
        #         ":" + "W=" + width + " L=" + length + " M=" + multifactor

        if self.deviceName[0:6] == 'scmode':
            self.obj_trac.deviceModelTrack[self.deviceName] = \
                self.entry_var[self.widgetObjCount].text() + \
                ":" + str(self.entry_var[self.widgetObjCount + 1].text())
            print(self.obj_trac.deviceModelTrack[self.deviceName])
        elif self.deviceName[0:2] == 'sc':
            self.obj_trac.deviceModelTrack[self.deviceName] = str(
                self.entry_var[self.widgetObjCount].text())
            print(self.obj_trac.deviceModelTrack[self.deviceName])

        else:
            self.obj_trac.deviceModelTrack[self.deviceName] = self.libfile

    def trackLibrary(self):
        """
        This function is use to keep track of all Device Model widget
        """
        print("Calling Track Device Model Library funtion")
        sending_btn = self.sender()
        self.widgetObjCount = int(sending_btn.objectName())

        init_path = '../../'
        if os.name == 'nt':
            init_path = ''

        self.libfile = QtCore.QDir.toNativeSeparators(
            QtWidgets.QFileDialog.getOpenFileName(
                self, "Open Library Directory",
                init_path + "library/deviceModelLibrary", "*.lib"
            )[0]
        )

        if not self.libfile:
            return

        # Setting Library to Text Edit Line
        self.entry_var[self.widgetObjCount].setText(self.libfile)
        self.deviceName = self.deviceDetail[self.widgetObjCount]

        # Storing to track it during conversion
        if self.deviceName[0] == 'm':
            width = str(self.entry_var[self.widgetObjCount + 1].text())
            length = str(self.entry_var[self.widgetObjCount + 2].text())
            multifactor = str(self.entry_var[self.widgetObjCount + 3].text())
            if width == "":
                width = "100u"
            if length == "":
                length = "100u"
            if multifactor == "":
                multifactor = "1"

            self.obj_trac.deviceModelTrack[self.deviceName] = self.libfile + \
                ":" + "W=" + width + " L=" + length + " M=" + multifactor

        elif self.deviceName[0:6] == 'scmode':
            self.obj_trac.deviceModelTrack[self.deviceName] = self.libfile + \
                ":" + str(self.entry_var[self.widgetObjCount + 1].text())
            print(self.obj_trac.deviceModelTrack[self.deviceName])

        elif self.deviceName[0:2] == 'sc':
            self.obj_trac.deviceModelTrack[self.deviceName] = str(
                self.entry_var[self.widgetObjCount].text())
            print(self.obj_trac.deviceModelTrack[self.deviceName])

        else:
            self.obj_trac.deviceModelTrack[self.deviceName] = self.libfile

    def trackLibraryWithoutButton(self, iter_value, path_value):
        """
        This function is use to keep track of all Device Model widget
        """
        print("Calling Track Library function Without Button")
        self.widgetObjCount = iter_value
        print("self.widgetObjCount-----", self.widgetObjCount)
        self.libfile = path_value
        print("PATH VALUE", path_value)

        # Setting Library to Text Edit Line
        self.entry_var[self.widgetObjCount].setText(self.libfile)
        self.deviceName = self.deviceDetail[self.widgetObjCount]

        # Storing to track it during conversion
        if self.deviceName[0] == 'm':
            width = str(self.entry_var[self.widgetObjCount + 1].text())
            length = str(self.entry_var[self.widgetObjCount + 2].text())
            multifactor = str(self.entry_var[self.widgetObjCount + 3].text())
            if width == "":
                width = "100u"
            if length == "":
                length = "100u"
            if multifactor == "":
                multifactor = "1"
            self.obj_trac.deviceModelTrack[self.deviceName] = self.libfile + \
                ":" + "W=" + width + " L=" + length + " M=" + multifactor

        elif self.deviceName[0:6] == 'scmode':
            self.obj_trac.deviceModelTrack[self.deviceName] = self.libfile + \
                ":" + str(self.entry_var[self.widgetObjCount + 1].text())
            print(self.obj_trac.deviceModelTrack[self.deviceName])

        elif self.deviceName[0:2] == 'sc':
            self.obj_trac.deviceModelTrack[self.deviceName] = str(
                self.entry_var[self.widgetObjCount].text())
            print(self.obj_trac.deviceModelTrack[self.deviceName])

        else:
            self.obj_trac.deviceModelTrack[self.deviceName] = self.libfile

    def GenerateSOCbutton(self):
        #############################################################
        # ***************** SPICE to Verilog Converter **************

        # The development is under progress and may not be accurate

        # Developed by:
        #               Sumanto Kar, sumantokar@iitb.ac.in
        #               Nagesh Karmali, nags@cse.iitb.ac.in
        #               Firuza Karmali, firuza@cse.iitb.ac.in
        #               Rahul Paknikar, rahulp@iitb.ac.in
        # GUIDED BY:
        #               Kunal Ghosh, VLSI System Design Corp.Pvt.Ltd
        #               Anagha Ghosh, VLSI System Design Corp.Pvt.Ltd
        #               Philipp Gühring

        # ***********************************************************

        kicadFile = self.clarg1
        (projpath, filename) = os.path.split(kicadFile)
        analysisfile = open(os.path.join(projpath, filename))
        # analysisfile = open(os.path.join(projpath, 'analysis'))
        content = analysisfile.read()
        contentlines = content.split("\n")
        parsedfile = open(os.path.join(projpath, filename+'.parsed.v'), 'w')
        parsedfile.write("")
        # print("module "+filename)
        i = 1
        inputlist = []
        realinputlist = []
        outputlist = []
        realoutputlist = []
        wirelist = []
        realwirelist = []
        uutlist = []
        filelist = []
        parsedcontent = []
        for contentlist in contentlines:
            if "IPDD" in contentlist or "IPAD" in contentlist:
                # if len(contentlist)>1 and ( contentlist[0:1]=='U'\
                # or contentlist[0:1]=='X') and not 'plot_' in contentlist :
                # print(contentlist)
                netnames = contentlist.split()
                net = ' '.join(map(str, netnames[1:-1]))
                netnames[-1] = netnames[-1].replace("IPAD", '')
                netnames[-1] = netnames[-1].replace("IPDD", '')
                # net=net.replace(netnames[-1],'')
                # net=net.replace('BI_','')
                # net=net.replace('BO_','')
                net2 = []

                for j in net.split():
                    # print(j)
                    secondpart = j
                    if '_' in j:
                        secondpart = j.split('_')[1]
                    if secondpart in net2:
                        continue
                    if net.count(secondpart)-1 > 0:
                        k = "["+str(net.count(secondpart)-1) + \
                            ":0"+"] "+secondpart
                    else:
                        k = secondpart

                    net2.append(secondpart)
                    if '_I_' in str(j):
                        inputlist.append(k)
                    if '_IR_' in str(j):
                        inputlist.append(k)
                    if '_O_' in str(j):
                        outputlist.append(k)
                    if '_OR_' in str(j):
                        realoutputlist.append(k)
                    if '_W_' in str(j) and not (k in wirelist):
                        wirelist.append(k)
                    if '_WR_' in str(j) and not (k in realwirelist):
                        realwirelist.append(k)

                netnames[-1] = netnames[-1].replace("IPAD", '')
                netnames[-1] = netnames[-1].replace("IPDD", '')
                uutlist.append(netnames[-1]+" uut" +
                               str(i)+" ("+', '.join(net2)+');')
                filelist.append(netnames[-1])
                i = i+1
        # print(inputlist)
        # print(outputlist)
        # print(wirelist)
        parsedcontent.append(
            "\\\\Generated from SPICE to Verilog. \
Converter developed at FOSSEE, IIT Bombay\n")
        parsedcontent.append(
            "\\\\The development is under progress and may not be accurate.\n")

        for j in filelist:
            parsedcontent.append('''`include "'''+j+'''.v"''')
        parsedcontent.append(
            "module "+filename+"("+', '.join(inputlist  # noqa
            + realinputlist + outputlist + realoutputlist)+");")  # noqa
        if inputlist:
            parsedcontent.append("input "+', '.join(inputlist)+";")
        if realinputlist:
            parsedcontent.append("input real "+', '.join(inputlist)+";")
        if outputlist:
            parsedcontent.append("output "+', '.join(outputlist)+";")
        if realoutputlist:
            parsedcontent.append("output real "+', '.join(realoutputlist)+";")
        if wirelist:
            parsedcontent.append("wire "+', '.join(wirelist)+";")
        if realwirelist:
            parsedcontent.append("wire real"+', '.join(realwirelist)+";")
        for j in uutlist:
            parsedcontent.append(j)
        parsedcontent.append("endmodule;")

        print('\n**************Generated Verilog File: ' +
              filename + '.parsed.v***************\n')
        for j in parsedcontent:
            print(j)
            parsedfile.write(j+"\n")
        print(
            '\n*************************************\
************************************\n')
        self.msg = QtWidgets.QErrorMessage()
        self.msg.setModal(True)
        self.msg.setWindowTitle("Verilog File Generated")
        self.content = "The Verilog file has been successfully \
             generated from the SPICE netlist"
        self.msg.showMessage(self.content)
        self.msg.exec_()
        return
