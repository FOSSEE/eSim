from PyQt5 import QtWidgets, QtCore
from . import TrackWidget
from projManagement import Validation
import os
from xml.etree import ElementTree as ET


class SubcircuitTab(QtWidgets.QWidget):
    """
    - This class creates Subcircuit Tab in KicadtoNgspice Window
    - It dynamically creates the widget for subcircuits,
      according to the .cir file
    - Creates `lineEdit` and `Add` button, which triggers `fileSelector`
    - Also, checks `Previous_value.xml` for previous subcircuit value
      to autofill, the `lineEdit`
    - Add button is bind to `trackSubcircuit`
    - Also `trackSubcircuit` without button is triggered if `lineEdit` filled
    """

    def __init__(self, schematicInfo, clarg1):
        kicadFile = clarg1
        (projpath, filename) = os.path.split(kicadFile)
        project_name = os.path.basename(projpath)

        try:
            f = open(
                os.path.join(
                    projpath,
                    project_name +
                    "_Previous_Values.xml"),
                'r')
            tree = ET.parse(f)
            parent_root = tree.getroot()
            for child in parent_root:
                if child.tag == "subcircuit":
                    root = child
        except BaseException:
            print("Subcircuit Previous values XML is Empty")

        QtWidgets.QWidget.__init__(self)

        # Creating track widget object
        self.obj_trac = TrackWidget.TrackWidget()

        # Creating validation object
        self.obj_validation = Validation.Validation()
        # Row and column count
        self.row = 0
        self.count = 1  # Entry count
        self.entry_var = {}
        self.subcircuit_dict_beg = {}
        self.subcircuit_dict_end = {}
        # List to hold information about subcircuit
        self.subDetail = {}

        # Stores the number of ports in each subcircuit
        self.numPorts = []

        # Set Layout
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        for eachline in schematicInfo:
            words = eachline.split()
            if eachline[0] == 'x':
                # print("Subcircuit : Words", words[0])
                self.obj_trac.subcircuitList[project_name + words[0]] = words
                self.subcircuit_dict_beg[words[0]] = self.count
                subbox = QtWidgets.QGroupBox()
                subgrid = QtWidgets.QGridLayout()
                subbox.setTitle("Add subcircuit for " + words[len(words) - 1])
                self.entry_var[self.count] = QtWidgets.QLineEdit()
                self.entry_var[self.count].setText("")
                self.entry_var[self.count].setReadOnly(True)
                global path_name
                try:
                    for child in root:
                        if child.tag[0] == eachline[0] \
                                and child.tag[1] == eachline[1]:
                            # print("Subcircuit MATCHING---", child.tag[0], \
                            #       child.tag[1], eachline[0],eachline[1])
                            try:
                                if child[0].text \
                                   and os.path.exists(child[0].text):
                                    self.entry_var[self.count] \
                                        .setText(child[0].text)
                                    path_name = child[0].text
                                else:
                                    self.entry_var[self.count].setText("")
                            except BaseException as e:
                                print("Error when set text of " +
                                      "subcircuit :", str(e))
                except BaseException as e:
                    print("Error before subcircuit :", str(e))

                subgrid.addWidget(self.entry_var[self.count], self.row, 1)
                self.addbtn = QtWidgets.QPushButton("Add")
                self.addbtn.setObjectName("%d" % self.count)
                # Send the number of ports specified with the given\
                # subcircuit for verification.
                # eg. If the line is 'x1 4 0 3 ua741', there are 3 ports(4, 0
                # and 3).
                self.numPorts.append(len(words) - 2)
                # print("Number of ports of sub circuit : ", self.numPorts)
                self.addbtn.clicked.connect(self.trackSubcircuit)
                subgrid.addWidget(self.addbtn, self.row, 2)
                subbox.setLayout(subgrid)

                # CSS
                subbox.setStyleSheet(" \
                QGroupBox { border: 1px solid gray; border-radius:\
                 9px; margin-top: 0.5em; } \
                QGroupBox::title { subcontrol-origin: margin; left:\
                 10px; padding: 0 3px 0 3px; } \
                ")

                self.grid.addWidget(subbox)

                # Adding Subcircuit Details
                self.subDetail[self.count] = words[0]

                # Increment row and widget count

                if self.entry_var[self.count].text() == "":
                    pass
                else:
                    self.trackSubcircuitWithoutButton(self.count, path_name)

                self.subcircuit_dict_end[words[0]] = self.count
                self.row = self.row + 1
                self.count = self.count + 1

            self.show()

    def trackSubcircuit(self):
        """
        - This function is use to keep track of all Subcircuit widget
        - Here the number of ports is tracked using the numPorts
          and `Add` button objectName property, which is refered using `sender`
        - Once a file is selected using the `QFileDialog` validate it
        - Pass the path of subciruit and the number of ports
        - According to validation state take further steps
        - If validated correctly, add to TrackWidget
        """
        sending_btn = self.sender()
        # print "Object Called is ",sending_btn.objectName()
        self.widgetObjCount = int(sending_btn.objectName())

        init_path = '../../'
        if os.name == 'nt':
            init_path = ''

        self.subfile = str(
            QtCore.QDir.toNativeSeparators(
                QtWidgets.QFileDialog.getExistingDirectory(
                    self, "Open Subcircuit",
                    init_path + "library/SubcircuitLibrary"
                )
            )
        )

        if not self.subfile:
            return

        self.reply = self.obj_validation.validateSub(
            self.subfile, self.numPorts[self.widgetObjCount - 1]
        )

        if self.reply == "True":
            # Setting Library to Text Edit Line
            self.entry_var[self.widgetObjCount].setText(self.subfile)
            self.subName = self.subDetail[self.widgetObjCount]

            # Storing to track it during conversion
            self.obj_trac.subcircuitTrack[self.subName] = self.subfile

        elif self.reply == "PORT":
            self.msg = QtWidgets.QErrorMessage(self)
            self.msg.setModal(True)
            self.msg.setWindowTitle("Error Message")
            self.msg.showMessage(
                "Please select a Subcircuit with correct number of ports."
            )
            self.msg.exec_()
        elif self.reply == "DIREC":
            self.msg = QtWidgets.QErrorMessage(self)
            self.msg.setModal(True)
            self.msg.setWindowTitle("Error Message")
            self.msg.showMessage(
                "Please select a valid Subcircuit directory "
                "(Containing '.sub' file)."
            )
            self.msg.exec_()

    def trackSubcircuitWithoutButton(self, iter_value, path_value):
        """
        - Same as trackSubcircuit, but here the count value is passed directly
          without using any button as in `Add`
        - This is triggered only once, initally
        """

        self.widgetObjCount = iter_value

        self.subfile = path_value
        self.reply = self.obj_validation.validateSub(
            self.subfile, self.numPorts[self.widgetObjCount - 1])
        if self.reply == "True":
            # Setting Library to Text Edit Line
            self.entry_var[self.widgetObjCount].setText(self.subfile)
            self.subName = self.subDetail[self.widgetObjCount]

            # Storing to track it during conversion
            self.obj_trac.subcircuitTrack[self.subName] = self.subfile
        elif self.reply == "PORT":
            self.msg = QtWidgets.QErrorMessage(self)
            self.msg.setModal(True)
            self.msg.setWindowTitle("Error Message")
            self.msg.showMessage(
                "Please select a Subcircuit with correct number of ports.")
            self.msg.exec_()
        elif self.reply == "DIREC":
            self.msg = QtWidgets.QErrorMessage(self)
            self.msg.setModal(True)
            self.msg.setWindowTitle("Error Message")
            self.msg.showMessage(
                "Please select a valid Subcircuit directory "
                "(Containing '.sub' file).")
            self.msg.exec_()
