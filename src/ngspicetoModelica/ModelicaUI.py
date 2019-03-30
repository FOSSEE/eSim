import os
import sys
from subprocess import Popen, PIPE, STDOUT
from PyQt4 import QtGui, QtCore
from configuration.Appconfig import Appconfig
from projManagement import Worker
from projManagement.Validation import Validation

BROWSE_LOCATION = '/home'

class OpenModelicaEditor(QtGui.QWidget):

    def __init__(self, dir=None):
        QtGui.QWidget.__init__(self)
        self.obj_validation = Validation()
        self.obj_appconfig = Appconfig()
        self.projDir = dir
        self.projName = os.path.basename(self.projDir)
        self.ngspiceNetlist = os.path.join(self.projDir,self.projName+".cir.out")
        self.modelicaNetlist = os.path.join(self.projDir,self.projName+".mo")
        self.map_json = Appconfig.modelica_map_json

        self.grid = QtGui.QGridLayout()
        self.FileEdit = QtGui.QLineEdit()
        self.FileEdit.setText(self.ngspiceNetlist)
        self.grid.addWidget(self.FileEdit, 0, 0)

        self.browsebtn = QtGui.QPushButton("Browse")
        self.browsebtn.clicked.connect(self.browseFile)
        self.grid.addWidget(self.browsebtn, 0, 1)

        self.convertbtn = QtGui.QPushButton("Convert")
        self.convertbtn.clicked.connect(self.callConverter)
        self.grid.addWidget(self.convertbtn, 2, 1)

        self.loadOMbtn = QtGui.QPushButton("Load OMEdit")
        self.loadOMbtn.clicked.connect(self.callOMEdit)
        self.grid.addWidget(self.loadOMbtn, 3, 1)

        #self.setGeometry(300, 300, 350, 300)
        self.setLayout(self.grid)
        self.show()

    def browseFile(self):

        self.ngspiceNetlist = QtGui.QFileDialog.getOpenFileName(self, 'Open Ngspice file', BROWSE_LOCATION)
        self.FileEdit.setText(self.ngspiceNetlist)

    def callConverter(self):

        try:
            self.cmd1 = "python ../ngspicetoModelica/NgspicetoModelica.py " + self.ngspiceNetlist + ' ' + self.map_json
            #self.obj_workThread1 = Worker.WorkerThread(self.cmd1)
            #self.obj_workThread1.start()
            convert_process = Popen(self.cmd1, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
            error_code = convert_process.stdout.read()
            if not error_code:
                self.msg = QtGui.QMessageBox()
                self.msg.setText("Ngspice netlist successfully converted to OpenModelica netlist")
                self.obj_appconfig.print_info("Ngspice netlist successfully converted to OpenModelica netlist")
                self.msg.exec_()

            else:
                self.err_msg = QtGui.QErrorMessage()
                self.err_msg.showMessage('Unable to convert NgSpice netlist to Modelica netlist. Check the netlist :'+ error_code)
                self.err_msg.setWindowTitle("Ngspice to Modelica conversion error")
                self.obj_appconfig.print_error(error_code)

        except Exception as e:
            self.msg = QtGui.QErrorMessage()
            self.msg.showMessage('Unable to convert NgSpice netlist to Modelica netlist. Check the netlist :'+str(e))
            self.msg.setWindowTitle("Ngspice to Modelica conversion error")


    def callOMEdit(self):

        if self.obj_validation.validateTool("OMEdit"):
            self.cmd2 = "OMEdit " + self.modelicaNetlist
            self.obj_workThread2 = Worker.WorkerThread(self.cmd2)
            self.obj_workThread2.start()
            print("OMEdit called")
            self.obj_appconfig.print_info("OMEdit called")

        else:
            self.msg = QtGui.QMessageBox()
            self.msgContent = "There was an error while opening OMEdit.<br/>\
                        Please make sure OpenModelica is installed in your system. <br/>\
                        To install it on Linux : Go to <a href=https://www.openmodelica.org/download/download-linux>OpenModelica Linux</a> and install nigthly build release.<br/>\
                        To install it on Windows : Go to <a href=https://www.openmodelica.org/download/download-windows>OpenModelica Windows</a> and install latest version.<br/>"
            self.msg.setTextFormat(QtCore.Qt.RichText)
            self.msg.setText(self.msgContent)
            self.msg.setWindowTitle("Missing OpenModelica")
            self.obj_appconfig.print_info(self.msgContent)
            self.msg.exec_()

