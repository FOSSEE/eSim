import os
from PyQt6 import QtWidgets
from . import TrackWidget
from xml.etree import ElementTree as ET


class Source(QtWidgets.QWidget):
    """
    This class create Source Tab of KicadtoNgSpice Window.
    """

    def __init__(self, sourcelist, sourcelisttrack, clarg1):
        QtWidgets.QWidget.__init__(self)
        self.obj_track = TrackWidget.TrackWidget()
        # Variables
        self.count = 1
        self.clarg1 = clarg1
        self.start = 0
        self.end = 0
        self.row = 0
        self.entry_var = {}
        # self.font = QtGui.QFont("Times",20,QtGui.QFont.Bold,True)

        # Creating Source Widget
        self.createSourceWidget(sourcelist, sourcelisttrack)

    def createSourceWidget(self, sourcelist, sourcelisttrack):
        """
        - This function dynamically create source widget in the \
        Source tab of KicadtoNgSpice window
        - Depending on the type of source, sourcetab is created
        - - ac
        - - dc
        - - sine
        - - pulse
        - - pwl
        - - exp
        - All the entry fields, are kept into the entry_var \
        tracked by self.count
        - Finally after each of the sourcelist is mapped to its input \
        component we move to adding these to the track widget
        - Also check if any default values present from previous analysis \
        & add them by default
        - Each line in sourcelist corresponds to a source
        - According to the source type modify the source and add it to the tab
        """
        """print("============================================================")
        print("SOURCE LIST TRACK", sourcelisttrack)
        print("SOURCE LIST", sourcelist)
        print("===========================================================")"""
        kicadFile = self.clarg1
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
                if child.tag == "source":
                    root = child
        except BaseException:
            print("Source Previous Values XML is Empty")

        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)
        xml_num = 0

        if sourcelist:
            for line in sourcelist:
                print("SourceList line: ", line)
                track_id = line[0]
                if line[2] == 'ac':
                    acbox = QtWidgets.QGroupBox()
                    acbox.setTitle(line[3])
                    acgrid = QtWidgets.QGridLayout()
                    self.start = self.count
                    label1 = QtWidgets.QLabel(line[4])
                    label2 = QtWidgets.QLabel(line[5])
                    acgrid.addWidget(label1, self.row, 0)
                    acgrid.addWidget(label2, self.row + 1, 0)

                    self.entry_var[self.count] = QtWidgets.QLineEdit()
                    self.entry_var[self.count].setMaximumWidth(150)
                    acgrid.addWidget(self.entry_var[self.count], self.row, 1)
                    self.entry_var[self.count + 1] = QtWidgets.QLineEdit()
                    self.entry_var[self.count + 1].setMaximumWidth(150)
                    acgrid.addWidget(
                        self.entry_var[self.count+1], self.row + 1, 1)
                    self.entry_var[self.count].setText("")
                    self.entry_var[self.count+1].setText("")
                    try:
                        for child in root:
                            templist1 = line[1]
                            templist2 = templist1.split(' ')

                            if child.tag == templist2[0] and \
                                    child.text == line[2]:
                                self.entry_var[self.count] \
                                    .setText(child[0].text)
                                self.entry_var[self.count + 1] \
                                    .setText(child[1].text)
                    except BaseException:
                        pass
                    # Value Need to check previuouse value
                    # self.entry_var[self.count].setText("")
                    self.row = self.row + 1
                    self.end = self.count + 1
                    self.count = self.count + 1
                    acbox.setLayout(acgrid)

                    # CSS
                    acbox.setStyleSheet(" \
                    QGroupBox { border: 1px solid gray; border-radius:\
                     9px; margin-top: 0.5em; } \
                    QGroupBox::title { subcontrol-origin: margin; left:\
                     10px; padding: 0 3px 0 3px; } \
                    ")

                    self.grid.addWidget(acbox)
                    sourcelisttrack.append(
                        [track_id, 'ac', self.start, self.end])

                elif line[2] == 'dc':
                    dcbox = QtWidgets.QGroupBox()
                    dcbox.setTitle(line[3])
                    dcgrid = QtWidgets.QGridLayout()
                    self.row = self.row + 1
                    self.start = self.count
                    label = QtWidgets.QLabel(line[4])
                    dcgrid.addWidget(label, self.row, 0)

                    self.entry_var[self.count] = QtWidgets.QLineEdit()
                    self.entry_var[self.count].setMaximumWidth(150)
                    dcgrid.addWidget(self.entry_var[self.count], self.row, 1)
                    self.entry_var[self.count].setText("")

                    try:
                        for child in root:
                            templist1 = line[1]
                            templist2 = templist1.split(' ')

                            if child.tag == templist2[0] \
                                    and child.text == line[2]:
                                self.entry_var[self.count] \
                                    .setText(child[0].text)
                    except BaseException:
                        pass

                    self.row = self.row + 1
                    self.end = self.count
                    self.count = self.count + 1
                    dcbox.setLayout(dcgrid)

                    # CSS
                    dcbox.setStyleSheet(" \
                    QGroupBox { border: 1px solid gray; border-radius:\
                     9px; margin-top: 0.5em; } \
                    QGroupBox::title { subcontrol-origin: margin; left:\
                     10px; padding: 0 3px 0 3px; } \
                    ")

                    self.grid.addWidget(dcbox)
                    sourcelisttrack.append(
                        [track_id, 'dc', self.start, self.end])

                elif line[2] == 'sine':
                    sinebox = QtWidgets.QGroupBox()
                    sinebox.setTitle(line[3])
                    sinegrid = QtWidgets.QGridLayout()
                    self.row = self.row + 1
                    self.start = self.count

                    for it in range(4, 9):
                        label = QtWidgets.QLabel(line[it])
                        sinegrid.addWidget(label, self.row, 0)
                        self.entry_var[self.count] = QtWidgets.QLineEdit()
                        self.entry_var[self.count].setMaximumWidth(150)
                        sinegrid.addWidget(
                            self.entry_var[self.count], self.row, 1)
                        self.entry_var[self.count].setText("")

                        try:
                            for child in root:
                                templist1 = line[1]
                                templist2 = templist1.split(' ')
                                if child.tag == templist2[0] \
                                        and child.text == line[2]:
                                    self.entry_var[self.count] \
                                        .setText(child[it-4].text)
                        except BaseException:
                            pass

                        self.row = self.row + 1
                        self.count = self.count + 1
                    self.end = self.count - 1
                    sinebox.setLayout(sinegrid)

                    # CSS
                    sinebox.setStyleSheet(" \
                    QGroupBox { border: 1px solid gray; border-radius: \
                    9px; margin-top: 0.5em; } \
                    QGroupBox::title { subcontrol-origin: margin; left: \
                    10px; padding: 0 3px 0 3px; } \
                    ")

                    self.grid.addWidget(sinebox)
                    sourcelisttrack.append(
                        [track_id, 'sine', self.start, self.end])

                elif line[2] == 'pulse':
                    pulsebox = QtWidgets.QGroupBox()
                    pulsebox.setTitle(line[3])
                    pulsegrid = QtWidgets.QGridLayout()
                    self.start = self.count

                    for it in range(4, 11):
                        label = QtWidgets.QLabel(line[it])
                        pulsegrid.addWidget(label, self.row, 0)
                        self.entry_var[self.count] = QtWidgets.QLineEdit()
                        self.entry_var[self.count].setMaximumWidth(150)
                        pulsegrid.addWidget(
                            self.entry_var[self.count], self.row, 1)
                        self.entry_var[self.count].setText("")

                        try:
                            for child in root:
                                templist1 = line[1]
                                templist2 = templist1.split(' ')
                                if child.tag == templist2[0] \
                                        and child.text == line[2]:
                                    self.entry_var[self.count] \
                                        .setText(child[it-4].text)
                        except BaseException:
                            pass

                        self.row = self.row + 1
                        self.count = self.count + 1
                    self.end = self.count - 1
                    pulsebox.setLayout(pulsegrid)

                    # CSS
                    pulsebox.setStyleSheet(" \
                    QGroupBox { border: 1px solid gray; border-radius: \
                    9px; margin-top: 0.5em; } \
                    QGroupBox::title { subcontrol-origin: margin; left: \
                    10px; padding: 0 3px 0 3px; } \
                    ")

                    self.grid.addWidget(pulsebox)
                    sourcelisttrack.append(
                        [track_id, 'pulse', self.start, self.end])

                elif line[2] == 'pwl':
                    pwlbox = QtWidgets.QGroupBox()
                    pwlbox.setTitle(line[3])
                    self.start = self.count
                    pwlgrid = QtWidgets.QGridLayout()
                    label = QtWidgets.QLabel(line[4])
                    pwlgrid.addWidget(label, self.row, 0)
                    self.entry_var[self.count] = QtWidgets.QLineEdit()
                    self.entry_var[self.count].setMaximumWidth(150)
                    pwlgrid.addWidget(self.entry_var[self.count], self.row, 1)
                    self.entry_var[self.count].setText("")

                    try:
                        for child in root:
                            templist1 = line[1]
                            templist2 = templist1.split(' ')
                            if child.tag == templist2[0] \
                                    and child.text == line[2]:
                                self.entry_var[self.count] \
                                    .setText(child[0].text)
                    except BaseException:
                        pass

                    self.row = self.row + 1
                    self.end = self.count
                    self.count = self.count + 1
                    pwlbox.setLayout(pwlgrid)

                    # CSS
                    pwlbox.setStyleSheet(" \
                    QGroupBox { border: 1px solid gray; border-radius: \
                    9px; margin-top: 0.5em; } \
                    QGroupBox::title { subcontrol-origin: margin; left: \
                    10px; padding: 0 3px 0 3px; } \
                    ")

                    self.grid.addWidget(pwlbox)
                    sourcelisttrack.append(
                        [track_id, 'pwl', self.start, self.end])

                elif line[2] == 'exp':
                    expbox = QtWidgets.QGroupBox()
                    expbox.setTitle(line[3])
                    expgrid = QtWidgets.QGridLayout()
                    self.start = self.count

                    for it in range(4, 10):
                        label = QtWidgets.QLabel(line[it])
                        expgrid.addWidget(label, self.row, 0)
                        self.entry_var[self.count] = QtWidgets.QLineEdit()
                        self.entry_var[self.count].setMaximumWidth(150)
                        expgrid.addWidget(
                            self.entry_var[self.count], self.row, 1)
                        self.entry_var[self.count].setText("")

                        try:
                            for child in root:
                                templist1 = line[1]
                                templist2 = templist1.split(' ')
                                if child.tag == templist2[0] \
                                        and child.text == line[2]:
                                    self.entry_var[self.count] \
                                        .setText(child[it-4].text)
                        except BaseException:
                            pass

                        self.row = self.row + 1
                        self.count = self.count + 1
                    self.end = self.count - 1
                    expbox.setLayout(expgrid)

                    # CSS
                    expbox.setStyleSheet(" \
                    QGroupBox { border: 1px solid gray; border-radius:\
                     9px; margin-top: 0.5em; } \
                    QGroupBox::title { subcontrol-origin: margin; left: \
                    10px; padding: 0 3px 0 3px; } \
                    ")

                    self.grid.addWidget(expbox)
                    sourcelisttrack.append(
                        [track_id, 'exp', self.start, self.end])

                self.count = self.count + 1
                xml_num = xml_num + 1

        else:
            print("No source is present in your circuit")

        # print("============================================================")
        # This is used to keep the track of dynamically created widget
        self.obj_track.sourcelisttrack["ITEMS"] = sourcelisttrack
        self.obj_track.source_entry_var["ITEMS"] = self.entry_var
        self.show()
