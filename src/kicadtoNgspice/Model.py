#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QObject, pyqtSlot
from  import TrackWidget
from xml.etree import ElementTree as ET
import os
import sys


class Model(QtWidgets.QWidget):

    """
    - This class creates Model Tab of KicadtoNgspice window.
      The widgets are created dynamically in the Model Tab.
    """

    # by Sumanto and Jay

    def addHex(self):
        """
        This function is use to keep track of all Device Model widget
        """

        # print("Calling Track Device Model Library funtion")

        init_path = '../../../'
        if os.name == 'nt':
            init_path = ''

        self.hexfile = \
            QtCore.QDir.toNativeSeparators(QtWidgets.QFileDialog.getOpenFileName(self,
                'Open Hex Directory', init_path + 'home', '*.hex')[0])
        self.text = open(self.hexfile).read()
        chosen_file_path = os.path.abspath(self.hexfile)
        print os.path.abspath(self.hexfile)

    # By Sumanto and Jay

    def uploadHex(self):
        """
        This function is use to keep track of all Device Model widget
        """

        # print("Calling Track Device Model Library funtion")

        path1 = os.path.expanduser('~')
        path2 = '/ngspice-nghdl/src/xspice/icm/ghdl'
        init_path = path1 + path2
        if os.name == 'nt':
            init_path = ''

        self.hexloc = QtWidgets.QFileDialog.getExistingDirectory(self,
                'Open Hex Directory', init_path)
        print self.hexloc
        self.file = open(self.hexloc + '/hex.txt', 'w')
        self.file.write(self.text)
        self.file.close()

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
            f = open(os.path.join(projpath, project_name
                     + '_Previous_Values.xml'), 'r')
            tree = ET.parse(f)
            parent_root = tree.getroot()
            for child in parent_root:
                if child.tag == 'model':
                    root = child
        except BaseException:

            check = 0
            print 'Model Previous Values XML is Empty'

        # Creating track widget object

        self.obj_trac = TrackWidget.TrackWidget()

        # for increasing row and counting/tracking line edit widget

        self.nextrow = 0
        self.nextcount = 0

        # for storing line edit details position details

        self.start = 0
        self.end = 0
        self.entry_var = {}
        self.text = ''

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

                if not isinstance(value, str) and hasattr(value,
                        '__iter__'):

                    # For tag having vector value

                    temp_tag = []
                    for item in value:
                        paramLabel = QtWidgets.QLabel(item)
                        modelgrid.addWidget(paramLabel, self.nextrow, 0)
                        self.obj_trac.model_entry_var[self.nextcount] = \
                            QtWidgets.QLineEdit()
                        modelgrid.addWidget(self.obj_trac.model_entry_var[self.nextcount],
                                self.nextrow, 1)

                        try:
                            for child in root:
                                if child.text == line[2] and child.tag \
                                    == line[3]:
                                    self.obj_trac.model_entry_var
                                    [self.nextcount].setText(child[i].text)
                                    i = i + 1
                        except BaseException:
                            pass

                        temp_tag.append(self.nextcount)
                        self.nextcount = self.nextcount + 1
                        self.nextrow = self.nextrow + 1
                        if 'upload_hex_file:1' in tag_dict:
                            self.addbtn = \
                                QtWidgets.QPushButton('Add Hex File')
                            self.addbtn.setObjectName('%d'
                                    % self.nextcount)
                            self.addbtn.clicked.connect(self.addHex)
                            modelgrid.addWidget(self.addbtn,
                                    self.nextrow, 2)
                            modelbox.setLayout(modelgrid)

                            # CSS

                            modelbox.setStyleSheet(" \
                            QGroupBox { border: 1px solid gray; border-radius:\
                            9px; margin-top: 0.5em; } \
                            QGroupBox::title { subcontrol-origin: margin; left:\
                            10px; padding: 0 3px 0 3px; } \
                            "
                                    )

                            self.grid.addWidget(modelbox)
                            self.addbtn = \
                                QtWidgets.QPushButton('Upload Hex File')
                            self.addbtn.setObjectName('%d'
                                    % self.nextcount)
                            self.addbtn.clicked.connect(self.uploadHex)
                            modelgrid.addWidget(self.addbtn,
                                    self.nextrow, 3)
                            modelbox.setLayout(modelgrid)

                            # CSS

                            modelbox.setStyleSheet(" \
                            QGroupBox { border: 1px solid gray; border-radius:\
                            9px; margin-top: 0.5em; } \
                            QGroupBox::title { subcontrol-origin: margin; left:\
                            10px; padding: 0 3px 0 3px; } \
                            "
                                    )

                            self.grid.addWidget(modelbox)

                    tag_dict[key] = temp_tag
                else:

                    paramLabel = QtWidgets.QLabel(value)
                    modelgrid.addWidget(paramLabel, self.nextrow, 0)
                    self.obj_trac.model_entry_var[self.nextcount] = \
                        QtWidgets.QLineEdit()
                    modelgrid.addWidget(self.obj_trac.model_entry_var[self.nextcount],
                            self.nextrow, 1)

                    try:
                        for child in root:
                            if child.text == line[2] and child.tag \
                                == line[3]:
                                self.obj_trac.model_entry_var[self.nextcount].setText(child[i].text)
                                i = i + 1
                    except BaseException:
                        pass

                    tag_dict[key] = self.nextcount
                    self.nextcount = self.nextcount + 1
                    self.nextrow = self.nextrow + 1
                    if 'upload_hex_file:1' in tag_dict:
                        self.addbtn = \
                            QtWidgets.QPushButton('Add Hex File')
                        self.addbtn.setObjectName('%d' % self.nextcount)
                        self.addbtn.clicked.connect(self.addHex)
                        modelgrid.addWidget(self.addbtn, self.nextrow,
                                2)
                        modelbox.setLayout(modelgrid)

                        # CSS

                        modelbox.setStyleSheet(" \
                        QGroupBox { border: 1px solid gray; border-radius:\
                        9px; margin-top: 0.5em; } \
                        QGroupBox::title { subcontrol-origin: margin; left:\
                        10px; padding: 0 3px 0 3px; } \
                        "
                                )

                        self.grid.addWidget(modelbox)
                        self.addbtn = \
                            QtWidgets.QPushButton('Upload Hex File')
                        self.addbtn.setObjectName('%d' % self.nextcount)
                        self.addbtn.clicked.connect(self.uploadHex)
                        modelgrid.addWidget(self.addbtn, self.nextrow,
                                3)
                        modelbox.setLayout(modelgrid)

                        # CSS

                        modelbox.setStyleSheet(" \
                        QGroupBox { border: 1px solid gray; border-radius:\
                        9px; margin-top: 0.5em; } \
                        QGroupBox::title { subcontrol-origin: margin; left:\
                        10px; padding: 0 3px 0 3px; } \
                        "
                                )

                        self.grid.addWidget(modelbox)

            self.end = self.nextcount - 1
            modelbox.setLayout(modelgrid)

            # CSS

            modelbox.setStyleSheet(" \
            QGroupBox { border: 1px solid gray; border-radius: \
            9px; margin-top: 0.5em; } \
            QGroupBox::title { subcontrol-origin: margin; left:\
             10px; padding: 0 3px 0 3px; } \
            "
                                   )

            self.grid.addWidget(modelbox)

            # This keeps the track of Model Tab Widget

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
            for itr in self.obj_trac.modelTrack:
                if itr == lst:
                    check = 1
            if check == 0:
                self.obj_trac.modelTrack.append(lst)

        self.show()
