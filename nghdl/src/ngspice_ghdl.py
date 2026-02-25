#! /Users/thethtarshwesin/Desktop/eSim-2.5/esim-venv/bin/python3

# This file create the GUI to install code model in the Ngspice.

import os
import sys
import shutil
import subprocess
from PyQt5 import QtGui, QtCore, QtWidgets
from configparser import ConfigParser
from Appconfig import Appconfig
from createKicadLibrary import AutoSchematic
from model_generation import ModelGeneration


class Mainwindow(QtWidgets.QWidget):

    def __init__(self):
        # super(Mainwindow, self).__init__()
        QtWidgets.QMainWindow.__init__(self)
        print("Initializing..........")

        if os.name == 'nt':
            self.home = os.path.join('library', 'config')
        else:
            self.home = os.path.expanduser('~')

        # Reading all variables from config.ini
        self.parser = ConfigParser()
        self.parser.read(
            os.path.join(self.home, os.path.join('.nghdl', 'config.ini'))
        )
        self.nghdl_home = self.parser.get('NGHDL', 'NGHDL_HOME')
        self.release_dir = self.parser.get('NGHDL', 'RELEASE')
        self.src_home = self.parser.get('SRC', 'SRC_HOME')
        self.licensefile = self.parser.get('SRC', 'LICENSE')
        # Printing LICENCE file on terminal
        fileopen = open(self.licensefile, 'r')
        print(fileopen.read())
        fileopen.close()
        self.file_list = []       # to keep the supporting files
        self.errorFlag = False    # to keep the check of "make install" errors
        self.initUI()

    def initUI(self):
        self.uploadbtn = QtWidgets.QPushButton('Upload')
        self.uploadbtn.clicked.connect(self.uploadModel)
        self.exitbtn = QtWidgets.QPushButton('Exit')
        self.exitbtn.clicked.connect(self.closeWindow)
        self.browsebtn = QtWidgets.QPushButton('Browse')
        self.browsebtn.clicked.connect(self.browseFile)
        self.addbtn = QtWidgets.QPushButton('Add Files')
        self.addbtn.clicked.connect(self.addFiles)
        self.removebtn = QtWidgets.QPushButton('Remove Files')
        self.removebtn.clicked.connect(self.removeFiles)
        self.ledit = QtWidgets.QLineEdit(self)
        self.sedit = QtWidgets.QTextEdit(self)
        self.process = QtCore.QProcess(self)
        self.termedit = QtWidgets.QTextEdit(self)
        self.termedit.setReadOnly(1)
        pal = QtGui.QPalette()
        bgc = QtGui.QColor(0, 0, 0)
        pal.setColor(QtGui.QPalette.Base, bgc)
        self.termedit.setPalette(pal)
        self.termedit.setStyleSheet("QTextEdit {color:white}")

        # Creating gridlayout
        grid = QtWidgets.QGridLayout()
        grid.setSpacing(5)
        grid.addWidget(self.ledit, 1, 0)
        grid.addWidget(self.browsebtn, 1, 1)
        grid.addWidget(self.sedit, 2, 0, 4, 1)
        grid.addWidget(self.addbtn, 2, 1)
        grid.addWidget(self.removebtn, 3, 1)
        grid.addWidget(self.termedit, 6, 0, 10, 1)
        grid.addWidget(self.uploadbtn, 17, 0)
        grid.addWidget(self.exitbtn, 17, 1)

        self.setLayout(grid)
        self.setGeometry(300, 300, 600, 600)
        self.setWindowTitle("Ngspice Digital Model Creator (from VHDL)")
        # self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.show()

    def closeWindow(self):
        try:
            self.process.close()
        except BaseException:
            pass
        print("Close button clicked")
        sys.exit()

    def browseFile(self):
        print("Browse button clicked")
        self.filename = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Open File', '.')[0]
        self.ledit.setText(self.filename)
        print("Vhdl file uploaded to process :", self.filename)

    def addFiles(self):
        print("Starts adding supporting files")
        title = self.addbtn.text()
        for file in QtWidgets.QFileDialog.getOpenFileNames(self, title)[0]:
            self.sedit.append(str(file))
            self.file_list.append(file)
        print("Supporting Files are :", self.file_list)

    def removeFiles(self):
        self.fileRemover = FileRemover(self)

    # Check extensions of all supporting files
    def checkSupportFiles(self):
        nonvhdl_count = 0
        for file in self.file_list:
            extension = os.path.splitext(str(file))[1]
            if extension != ".vhdl":
                nonvhdl_count += 1
                self.file_list.remove(file)

        if nonvhdl_count > 0:
            QtWidgets.QMessageBox.critical(
                self, 'Critical', '''<b>Important Message.</b>
                <br/><br/>Supporting files should be <b>.vhdl</b> file '''
            )

    def createModelDirectory(self):
        print("Create Model Directory Called")
        self.digital_home = self.parser.get('NGHDL', 'DIGITAL_MODEL')
        self.digital_home = os.path.join(self.digital_home, "ghdl")
        os.chdir(self.digital_home)
        print("Current Working Directory Changed to", os.getcwd())
        self.modelname = os.path.basename(str(self.filename)).split('.')[0]
        print("Model to be created :", self.modelname)
        # Looking if model directory is present or not
        if os.path.isdir(self.modelname):
            print("Model Already present")
            ret = QtWidgets.QMessageBox.warning(
                self, "Warning",
                "<b>This model already exist. Do you want to " +
                "overwrite it?</b><br/> If yes press ok, else cancel it and " +
                "change the name of your vhdl file.",
                QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Cancel
            )
            if ret == QtWidgets.QMessageBox.Ok:
                print("Overwriting existing model " + self.modelname)
                if os.name == 'nt':
                    cmd = "rmdir " + self.modelname + "/s /q"
                else:
                    cmd = "rm -rf " + self.modelname
                # process = subprocess.Popen(
                #     cmd, stdout=subprocess.PIPE,
                #     stderr=subprocess.PIPE, shell=True
                # )
                subprocess.call(cmd, shell=True)
                os.mkdir(self.modelname)
            else:
                print("Exiting application")
                sys.exit()
        else:
            print("Creating model " + self.modelname + " directory")
            os.mkdir(self.modelname)

    def addingModelInModpath(self):
        print("Adding Model " + self.modelname +
              " in Modpath file " + self.digital_home)
        # Adding name of model in the modpath file
        # Check if the string is already in the file
        with open(self.digital_home + "/modpath.lst", 'r+') as f:
            flag = 0
            for line in f:
                if line.strip() == self.modelname:
                    print("Found model "+self.modelname+" in the modpath.lst")
                    flag = 1
                    break

            if flag == 0:
                print("Adding model name "+self.modelname+" into modpath.lst")
                f.write(self.modelname + "\n")
            else:
                print("Model name is already into modpath.lst")

    def createModelFiles(self):
        print("Create Model Files Called")
        os.chdir(self.cur_dir)
        print("Current Working directory changed to " + self.cur_dir)

        # Generate model corresponding to the uploaded VHDL file
        model = ModelGeneration(str(self.ledit.text()))
        model.readPortInfo()
        model.createCfuncModFile()
        model.createIfSpecFile()
        model.createTestbench()
        model.createServerScript()
        model.createSockScript()

        # Moving file to model directory
        path = os.path.join(self.digital_home, self.modelname)
        shutil.move("cfunc.mod", path)
        shutil.move("ifspec.ifs", path)

        # Creating directory inside model directoy
        print("Creating DUT directory at " + os.path.join(path, "DUTghdl"))
        os.mkdir(path + "/DUTghdl/")
        print("Copying required file to DUTghdl directory")
        shutil.move("connection_info.txt", path + "/DUTghdl/")
        shutil.move("start_server.sh", path + "/DUTghdl/")
        shutil.move("sock_pkg_create.sh", path + "/DUTghdl/")
        shutil.move(self.modelname + "_tb.vhdl", path + "/DUTghdl/")

        shutil.copy(str(self.filename), path + "/DUTghdl/")
        shutil.copy(os.path.join(self.home, self.src_home) +
                    "/src/ghdlserver/compile.sh", path + "/DUTghdl/")
        shutil.copy(os.path.join(self.home, self.src_home) +
                    "/src/ghdlserver/uthash.h", path + "/DUTghdl/")
        shutil.copy(os.path.join(self.home, self.src_home) +
                    "/src/ghdlserver/ghdlserver.c", path + "/DUTghdl/")
        shutil.copy(os.path.join(self.home, self.src_home) +
                    "/src/ghdlserver/ghdlserver.h", path + "/DUTghdl/")
        shutil.copy(os.path.join(self.home, self.src_home) +
                    "/src/ghdlserver/Utility_Package.vhdl", path + "/DUTghdl/")
        shutil.copy(os.path.join(self.home, self.src_home) +
                    "/src/ghdlserver/Vhpi_Package.vhdl", path + "/DUTghdl/")

        if os.name == 'nt':
            shutil.copy(os.path.join(self.home, self.src_home) +
                        "/src/ghdlserver/libws2_32.a", path + "/DUTghdl/")

        for file in self.file_list:
            shutil.copy(str(file), path + "/DUTghdl/")

        os.chdir(path + "/DUTghdl")
        if os.name == 'nt':
            # path to msys bin directory where bash is located
            self.msys_home = self.parser.get('COMPILER', 'MSYS_HOME')
            subprocess.call(self.msys_home + "/usr/bin/bash.exe " +
                            path + "/DUTghdl/compile.sh", shell=True)
            subprocess.call(self.msys_hoscme + "/usr/bin/bash.exe -c " +
                            "'chmod a+x start_server.sh'", shell=True)
            subprocess.call(self.msys_home + "/usr/bin/bash.exe -c " +
                            "'chmod a+x sock_pkg_create.sh'", shell=True)
        else:
            subprocess.call("bash " + path + "/DUTghdl/compile.sh", shell=True)
            subprocess.call("chmod a+x start_server.sh", shell=True)
            subprocess.call("chmod a+x sock_pkg_create.sh", shell=True)

        os.remove("compile.sh")
        # os.remove("ghdlserver.c")

    # Slot to redirect stdout and stderr to window console
    @QtCore.pyqtSlot()
    def readAllStandard(self):
        self.termedit.append(
            str(self.process.readAllStandardOutput().data(), encoding='utf-8')
        )
        stderror = self.process.readAllStandardError()
        if stderror.toUpper().contains(b"ERROR"):
            self.errorFlag = True
        self.termedit.append(str(stderror.data(), encoding='utf-8'))

    def runMake(self):
        print("run Make Called")
        self.release_home = self.parser.get('NGHDL', 'RELEASE')
        path_icm = os.path.join(self.release_home, "src/xspice/icm")
        os.chdir(path_icm)

        try:
            if os.name == 'nt':
                # path to msys bin directory where make is located
                self.msys_home = self.parser.get('COMPILER', 'MSYS_HOME')
                cmd = self.msys_home + "/mingw64/bin/mingw32-make.exe"
            else:
                cmd = " make"

            print("Running Make command in " + path_icm)
            path = os.getcwd()  # noqa
            self.process = QtCore.QProcess(self)
            self.process.start(cmd)
            print("make command process pid ---------- >", self.process.pid())

            if os.name == "nt":
                self.process.finished.connect(self.createSchematicLib)
                self.process \
                    .readyReadStandardOutput.connect(self.readAllStandard)

        except BaseException:
            print("There is error in 'make' ")
            sys.exit()

    def runMakeInstall(self):
        print("run Make Install Called")
        try:
            if os.name == 'nt':
                self.msys_home = self.parser.get('COMPILER', 'MSYS_HOME')
                cmd = self.msys_home + "/mingw64/bin/mingw32-make.exe install"
            else:
                cmd = " make install"
            print("Running Make Install")
            path = os.getcwd()  # noqa
            try:
                self.process.close()
            except BaseException:
                pass

            self.process = QtCore.QProcess(self)
            self.process.start(cmd)
            self.process.finished.connect(self.createSchematicLib)
            self.process.readyReadStandardOutput.connect(self.readAllStandard)
            os.chdir(self.cur_dir)

        except BaseException:
            print("There is error in 'make install' ")
            sys.exit()

    def createSchematicLib(self):
        if os.name == "nt":
            shutil.copy("ghdl/ghdl.cm", "../../../../lib/ngspice/")

        os.chdir(self.cur_dir)
        if Appconfig.esimFlag == 1:
            if not self.errorFlag:
                print('Creating library files................................')
                schematicLib = AutoSchematic(self, self.modelname)
                schematicLib.createKicadSymbol()
            else:
                QtWidgets.QMessageBox.critical(
                    self, 'Error', '''Cannot create Schematic Library of ''' +
                    '''your model. Resolve the <b>errors</b> shown on ''' +
                    '''console of NGHDL window. '''
                )
        else:
            QtWidgets.QMessageBox.information(
                self, 'Message', '''<b>Important Message</b><br/><br/>''' +
                '''To create Schematic Library of your model, ''' +
                '''use NGHDL through <b>eSim</b> '''
            )

    def uploadModel(self):
        print("Upload button clicked")
        try:
            self.process.close()
        except BaseException:
            pass
        try:
            self.file_extension = os.path.splitext(str(self.filename))[1]
            print("Uploaded File extension :" + self.file_extension)
            self.cur_dir = os.getcwd()
            print("Current Working Directory :" + self.cur_dir)
            self.checkSupportFiles()
            if self.file_extension == ".vhdl":
                self.errorFlag = False
                self.createModelDirectory()
                self.addingModelInModpath()
                self.createModelFiles()
                self.runMake()
                if os.name != 'nt':
                    self.runMakeInstall()
            else:
                QtWidgets.QMessageBox.information(
                    self, 'Message', '''<b>Important Message.</b><br/>''' +
                    '''<br/>This accepts only <b>.vhdl</b> file '''
                )
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Error', str(e))


class FileRemover(QtWidgets.QWidget):

    def __init__(self, main_obj):
        super(FileRemover, self).__init__()
        self.row = 0
        self.col = 0
        self.cb_dict = {}
        self.marked_list = []
        self.files = main_obj.file_list
        self.sedit = main_obj.sedit

        print(self.files)

        self.grid = QtWidgets.QGridLayout()
        removebtn = QtWidgets.QPushButton('Remove', self)
        removebtn.clicked.connect(self.removeFiles)

        self.grid.addWidget(self.createCheckBox(), 0, 0)
        self.grid.addWidget(removebtn, 1, 1)

        self.setLayout(self.grid)
        self.show()

    def createCheckBox(self):
        self.checkbox = QtWidgets.QGroupBox()
        self.checkbox.setTitle('Remove Files')
        self.checkgrid = QtWidgets.QGridLayout()

        self.checkgroupbtn = QtWidgets.QButtonGroup()

        for path in self.files:
            print(path)
            self.cb_dict[path] = QtWidgets.QCheckBox(path)
            self.checkgroupbtn.addButton(self.cb_dict[path])
            self.checkgrid.addWidget(self.cb_dict[path], self.row, self.col)
            self.row += 1

        self.checkgroupbtn.setExclusive(False)
        self.checkgroupbtn.buttonClicked.connect(self.mark_file)
        self.checkbox.setLayout(self.checkgrid)

        return self.checkbox

    def mark_file(self):
        for path in self.cb_dict:
            if self.cb_dict[path].isChecked():
                if path not in self.marked_list:
                    self.marked_list.append(path)
            else:
                if path in self.marked_list:
                    self.marked_list.remove(path)

    def removeFiles(self):
        for path in self.marked_list:
            print(path + " is removed")
            self.sedit.append(path + " removed")
            self.files.remove(path)

        self.sedit.clear()
        for path in self.files:
            self.sedit.append(path)

        self.marked_list[:] = []
        self.files[:] = []
        self.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    if len(sys.argv) > 1:
        if sys.argv[1] == '-e':
            Appconfig.esimFlag = 1

    # Mainwindow() object must be assigned to a variable.
    # Otherwise, it is destroyed as soon as it gets created.
    w = Mainwindow()    # noqa
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
