import os
from PyQt4 import QtGui
from . import TrackWidget
# from xml.etree import ElementTree as ET
import json


class Source(QtGui.QWidget):
    """
    This class create Source Tab of KicadtoNgSpice Window.
    """

    def __init__(self, sourcelist, sourcelisttrack, clarg1):
        QtGui.QWidget.__init__(self)
        self.obj_track = TrackWidget.TrackWidget()
        # Variable
        self.count = 1
        self.clarg1 = clarg1
        self.start = 0
        self.end = 0
        self.row = 0
        self.entry_var = {}
        # self.font = QtGui.QFont("Times",20,QtGui.QFont.Bold,True)

        # Creating Source Widget
        self.createSourceWidget(sourcelist, sourcelisttrack)

    """
    - This function dynamically create source widget in the
      Source tab of KicadtoNgSpice window
    - Depending on the type of source, ac, dc, sine, pwl, etc...
      source tab is created
    - All the entry fields, are kept into the entry_var
      tracked by self.count
    - Finally after each of the sourcelist is mapped to its input component
      we move to adding these to the track widget
    - Also check if any default values present from previous analysis and add
      them by default
    """

    def createSourceWidget(self, sourcelist, sourcelisttrack):
        print("============================================================")
        print("SOURCELISTTRACK", sourcelisttrack)
        print("============================================================")
        kicadFile = self.clarg1
        (projpath, filename) = os.path.split(kicadFile)
        project_name = os.path.basename(projpath)

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
            print("Source Previous Values JSON is Empty")

        self.grid = QtGui.QGridLayout()
        self.setLayout(self.grid)

        if sourcelist:
            for line in sourcelist:
                # print "Voltage source line index: ",line[0]
                print("SourceList line: ", line)
                track_id = line[0]
                # print "track_id is ",track_id
                if line[2] == 'ac':
                    acbox = QtGui.QGroupBox()
                    acbox.setTitle(line[3])
                    acgrid = QtGui.QGridLayout()
                    self.start = self.count
                    label1 = QtGui.QLabel(line[4])
                    label2 = QtGui.QLabel(line[5])
                    acgrid.addWidget(label1, self.row, 0)
                    acgrid.addWidget(label2, self.row + 1, 0)

                    self.entry_var[self.count] = QtGui.QLineEdit()
                    self.entry_var[self.count].setMaximumWidth(150)
                    acgrid.addWidget(self.entry_var[self.count], self.row, 1)
                    self.entry_var[self.count].setText("")
                    self.count += 1

                    self.entry_var[self.count] = QtGui.QLineEdit()
                    self.entry_var[self.count].setMaximumWidth(150)
                    acgrid.addWidget(
                        self.entry_var[self.count], self.row + 1, 1)
                    self.entry_var[self.count].setText("")
                    self.count += 1

                    try:
                        for key in json_data["source"]:
                            templist1 = line[1]
                            templist2 = templist1.split(' ')

                            if key == templist2[0] and \
                                    json_data["source"][key]["type"]\
                                    == line[2]:
                                self.entry_var[self.count - 2].setText(
                                    str(
                                        json_data
                                        ["source"][key]["values"][0]
                                        ["Amplitude"]))
                                self.entry_var[self.count - 1].setText(
                                    str(
                                        json_data["source"][key]
                                        ["values"][1]["Phase"]))

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
                    dcbox = QtGui.QGroupBox()
                    dcbox.setTitle(line[3])
                    dcgrid = QtGui.QGridLayout()
                    self.start = self.count
                    label = QtGui.QLabel(line[4])
                    dcgrid.addWidget(label, self.row, 0)

                    self.entry_var[self.count] = QtGui.QLineEdit()
                    self.entry_var[self.count].setMaximumWidth(150)
                    dcgrid.addWidget(self.entry_var[self.count], self.row, 1)
                    self.entry_var[self.count].setText("")

                    try:
                        for key in json_data["source"]:
                            templist1 = line[1]
                            templist2 = templist1.split(' ')

                            if key == templist2[0] and \
                                    json_data["source"][key]["type"]\
                                    == line[2]:
                                self.entry_var[self.count].setText(
                                    str(
                                        json_data["source"][key]
                                        ["values"][0]["Value"]))

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
                    sinebox = QtGui.QGroupBox()
                    sinebox.setTitle(line[3])
                    sinegrid = QtGui.QGridLayout()
                    self.row = self.row + 1
                    self.start = self.count

                    for it in range(4, 9):
                        label = QtGui.QLabel(line[it])
                        sinegrid.addWidget(label, self.row, 0)
                        self.entry_var[self.count] = QtGui.QLineEdit()
                        self.entry_var[self.count].setMaximumWidth(150)
                        sinegrid.addWidget(
                            self.entry_var[self.count], self.row, 1)
                        self.entry_var[self.count].setText("")

                        try:
                            for key in json_data["source"]:
                                templist1 = line[1]
                                templist2 = templist1.split(' ')
                                if key == templist2[0] and \
                                        json_data["source"][key]["type"]\
                                        == line[2]:
                                    self.entry_var[self.count].setText(
                                        str(
                                            list(json_data["source"]
                                                 [key]["values"]
                                                 [it - 4].values())[0]))
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
                    pulsebox = QtGui.QGroupBox()
                    pulsebox.setTitle(line[3])
                    pulsegrid = QtGui.QGridLayout()
                    self.start = self.count

                    for it in range(4, 11):
                        label = QtGui.QLabel(line[it])
                        pulsegrid.addWidget(label, self.row, 0)
                        self.entry_var[self.count] = QtGui.QLineEdit()
                        self.entry_var[self.count].setMaximumWidth(150)
                        pulsegrid.addWidget(
                            self.entry_var[self.count], self.row, 1)
                        self.entry_var[self.count].setText("")

                        try:
                            for key in json_data["source"]:
                                templist1 = line[1]
                                templist2 = templist1.split(' ')

                                if key == templist2[0] and \
                                        json_data["source"][key]["type"]\
                                        == line[2]:
                                    self.entry_var[self.count].setText(
                                        str(list(
                                            json_data["source"][key]
                                            ["values"][it - 4].values())[0]))
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
                    pwlbox = QtGui.QGroupBox()
                    pwlbox.setTitle(line[3])
                    self.start = self.count
                    pwlgrid = QtGui.QGridLayout()
                    label = QtGui.QLabel(line[4])
                    pwlgrid.addWidget(label, self.row, 0)
                    self.entry_var[self.count] = QtGui.QLineEdit()
                    self.entry_var[self.count].setMaximumWidth(150)
                    pwlgrid.addWidget(self.entry_var[self.count], self.row, 1)
                    self.entry_var[self.count].setText("")

                    try:
                        for key in json_data["source"]:
                            templist1 = line[1]
                            templist2 = templist1.split(' ')
                            if key == templist2[0] and \
                                    json_data["source"][key]["type"] \
                                    == line[2]:
                                self.entry_var[self.count].setText(
                                    str(json_data["source"][key]
                                        ["values"][0]["Enter in pwl format"]))
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
                    expbox = QtGui.QGroupBox()
                    expbox.setTitle(line[3])
                    expgrid = QtGui.QGridLayout()
                    self.start = self.count

                    for it in range(4, 10):
                        label = QtGui.QLabel(line[it])
                        expgrid.addWidget(label, self.row, 0)
                        self.entry_var[self.count] = QtGui.QLineEdit()
                        self.entry_var[self.count].setMaximumWidth(150)
                        expgrid.addWidget(
                            self.entry_var[self.count], self.row, 1)
                        self.entry_var[self.count].setText("")

                        try:
                            for key in json_data["source"]:
                                templist1 = line[1]
                                templist2 = templist1.split(' ')
                                if key == templist2[0] and \
                                        json_data["source"][key]["type"]\
                                        == line[2]:
                                    self.entry_var[self.count].setText(
                                        str(
                                            list(
                                                json_data["source"][key]
                                                ["values"][it - 4].values())[0]
                                        )
                                    )
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

        else:
            print("No source is present in your circuit")

        print("============================================================")
        # This is used to keep the track of dynamically created widget
        self.obj_track.sourcelisttrack["ITEMS"] = sourcelisttrack
        self.obj_track.source_entry_var["ITEMS"] = self.entry_var
        self.show()
