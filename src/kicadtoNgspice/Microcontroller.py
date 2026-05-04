#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import random
from configparser import ConfigParser
from xml.etree import ElementTree as ET

from PyQt6 import QtWidgets, QtCore

from . import TrackWidget


# Created By Vatsal Patel on 01/07/2022

class Microcontroller(QtWidgets.QWidget):
    """
    - This class creates Model Tab of KicadtoNgspice window.
      The widgets are created dynamically in the Model Tab.
    """

    def addHex(self):
        """
        This function is use to keep track of all Device Model widget
        """
        if os.name == 'nt':
            self.home = os.path.join('library', 'config')
        else:
            self.home = os.path.expanduser('~')

        self.parser = ConfigParser()
        self.parser.read(os.path.join(
            self.home, os.path.join('.nghdl', 'config.ini')))
        self.nghdl_home = self.parser.get('NGHDL', 'NGHDL_HOME')

        self.hexfile = QtCore.QDir.toNativeSeparators(
            QtWidgets.QFileDialog.getOpenFileName(
                self, "Open Hex Directory", os.path.expanduser('~'),
                "HEX files (*.hex);;Text files (*.txt)"
            )[0]
        )

        if not self.hexfile:
            """If no path is selected by user function returns"""
            return

        chosen_file_path = os.path.abspath(self.hexfile)
        btn = self.sender()

        # If path is selected the clicked button is stored in btn variable and
        # checked from list of buttons to add the file path to correct
        # QLineEdit

        if btn in self.hex_btns:
            if "Add Hex File" in self.sender().text():
                self.obj_trac.microcontroller_var[
                    4 + (5 * self.hex_btns.index(btn))].setText(
                    chosen_file_path)

    def __init__(
            self,
            schematicInfo,
            modelList,
            clarg1,
    ):

        QtWidgets.QWidget.__init__(self)

        # Processing for getting previous values

        kicadFile = clarg1
        (projpath, filename) = os.path.split(kicadFile)
        project_name = os.path.basename(projpath)
        check = 1
        try:
            f = open(
                os.path.join(projpath, project_name + "_Previous_Values.xml"),
                "r",
            )
            tree = ET.parse(f)
            parent_root = tree.getroot()
            for parent in parent_root:
                if parent.tag == "microcontroller":
                    self.root = parent
        except BaseException:

            check = 0
            print("Microcontroller Previous Values XML is Empty")

        # Creating track widget object

        self.obj_trac = TrackWidget.TrackWidget()

        # for increasing row and counting/tracking line edit widget

        self.nextrow = 0
        self.nextcount = 0

        # for storing line edit details position details

        self.start = 0
        self.end = 0
        self.entry_var = []
        self.hex_btns = []
        self.text = ""

        # Creating GUI dynamically for Model tab

        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        for line in modelList:
            # print "ModelList Item:",line
            # Adding title label for model
            # Key: Tag name,Value:Entry widget number

            tag_dict = {}
            modelbox = QtWidgets.QGroupBox()
            modelgrid = QtWidgets.QGridLayout()
            modelbox.setTitle(line[5])
            self.start = self.nextcount

            # line[7] is parameter dictionary holding parameter tags.

            i = 0
            for (key, value) in line[7].items():
                # Check if value is iterable

                if not isinstance(value, str) and hasattr(value, "__iter__"):

                    # For tag having vector value

                    temp_tag = []
                    for item in value:

                        paramLabel = QtWidgets.QLabel(item)
                        modelgrid.addWidget(paramLabel, self.nextrow, 0)
                        self.obj_trac.microcontroller_var[
                            self.nextcount
                        ] = QtWidgets.QLineEdit()
                        self.obj_trac.microcontroller_var[
                            self.nextcount] = QtWidgets.QLineEdit()
                        self.obj_trac.microcontroller_var[
                            self.nextcount].setText("")

                        if "Enter Instance ID (Between 0-99)" in value:
                            self.obj_trac.microcontroller_var[
                                self.nextcount].hide()
                            self.obj_trac.microcontroller_var[
                                self.nextcount].setText(
                                str(random.randint(0, 99)))
                        else:
                            modelgrid.addWidget(paramLabel, self.nextrow, 0)

                        if "Path of your .hex file" in value:
                            self.obj_trac.microcontroller_var[
                                self.nextcount].setReadOnly(True)
                            addbtn = QtWidgets.QPushButton("Add Hex File")
                            addbtn.setObjectName("%d" % self.nextcount)
                            addbtn.clicked.connect(self.addHex)
                            modelgrid.addWidget(addbtn, self.nextrow, 2)
                            modelbox.setLayout(modelgrid)
                            self.hex_btns.append(addbtn)
                        try:
                            for child in root:
                                if (
                                        child.text == line[2]
                                        and child.tag == line[3]
                                ):
                                    self.obj_trac.microcontroller_var[
                                        self.nextcount].setText(child[i].text)
                                    i = i + 1
                        except BaseException:
                            print("Passes previous values")

                        modelgrid.addWidget(
                            self.obj_trac.microcontroller_var[self.nextcount],
                            self.nextrow,
                            1, )

                        temp_tag.append(self.nextcount)
                        self.nextcount = self.nextcount + 1
                        self.nextrow = self.nextrow + 1

                    tag_dict[key] = temp_tag

                else:

                    paramLabel = QtWidgets.QLabel(value)
                    self.obj_trac.microcontroller_var[
                        self.nextcount
                    ] = QtWidgets.QLineEdit()
                    self.obj_trac.microcontroller_var[
                        self.nextcount] = QtWidgets.QLineEdit()
                    self.obj_trac.microcontroller_var[self.nextcount].setText(
                        "")

                    if "Enter Instance ID (Between 0-99)" in value:
                        self.obj_trac.microcontroller_var[
                            self.nextcount].hide()
                        self.obj_trac.microcontroller_var[
                            self.nextcount].setText(str(random.randint(0, 99)))
                    else:
                        modelgrid.addWidget(paramLabel, self.nextrow, 0)

                    if "Path of your .hex file" in value:
                        self.obj_trac.microcontroller_var[
                            self.nextcount].setReadOnly(True)
                        addbtn = QtWidgets.QPushButton("Add Hex File")
                        addbtn.setObjectName("%d" % self.nextcount)
                        addbtn.clicked.connect(self.addHex)
                        modelgrid.addWidget(addbtn, self.nextrow, 2)
                        modelbox.setLayout(modelgrid)
                        self.hex_btns.append(addbtn)

                        # CSS

                        modelbox.setStyleSheet(
                            " \
                        QGroupBox { border: 1px solid gray; border-radius:\
                        9px; margin-top: 0.5em; } \
                        QGroupBox::title { subcontrol-origin: margin; left:\
                        10px; padding: 0 3px 0 3px; } \
                        "
                        )
                        self.grid.addWidget(modelbox)

                    try:
                        for child in root:
                            if child.text == line[2] and child.tag == line[3]:
                                self.obj_trac.microcontroller_var[
                                    self.nextcount].setText(child[i].text)
                                i = i + 1

                    except BaseException:
                        print("Passes previous values")

                    modelgrid.addWidget(
                        self.obj_trac.microcontroller_var[self.nextcount],
                        self.nextrow,
                        1, )

                    tag_dict[key] = self.nextcount
                    self.nextcount = self.nextcount + 1
                    self.nextrow = self.nextrow + 1

            self.end = self.nextcount - 1
            modelbox.setLayout(modelgrid)

            # CSS

            modelbox.setStyleSheet(
                " \
            QGroupBox { border: 1px solid gray; border-radius: \
            9px; margin-top: 0.5em; } \
            QGroupBox::title { subcontrol-origin: margin; left:\
             10px; padding: 0 3px 0 3px; } \
            "
            )

            self.grid.addWidget(modelbox)

            # This keeps the track of Microcontroller Tab Widget

            lst = [
                line[0],
                line[1],
                line[2],
                line[3],
                line[4],
                line[5],
                line[6],
                self.start,
                self.end,
                tag_dict,
            ]
            check = 0
            for itr in self.obj_trac.microcontrollerTrack:
                if itr == lst:
                    check = 1
            if check == 0:
                self.obj_trac.microcontrollerTrack.append(lst)

        self.show()
