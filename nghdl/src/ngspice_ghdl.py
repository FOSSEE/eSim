#!/usr/bin/env python


"""#!/usr/bin/python"""

#This file create the gui to install code model in the ngspice.

import os
import sys
import shutil
import subprocess
from PyQt4 import QtGui
from PyQt4 import QtCore
from ConfigParser import SafeConfigParser
from Appconfig import Appconfig
from createKicadLibrary import AutoSchematic

class Mainwindow(QtGui.QWidget):
    def __init__(self):
        #super(Mainwindow, self).__init__()
        QtGui.QMainWindow.__init__(self)
        print "Initializing.........."
        self.home = os.path.expanduser("~")
        #Reading all varibale from config.ini
        self.parser = SafeConfigParser()
        self.parser.read(os.path.join(self.home, os.path.join('.nghdl','config.ini')))
        self.ngspice_home = self.parser.get('NGSPICE','NGSPICE_HOME')
        self.release_dir = self.parser.get('NGSPICE','RELEASE')
        self.src_home = self.parser.get('SRC','SRC_HOME')
        self.licensefile = self.parser.get('SRC','LICENSE')
        #Printing LICENCE file on terminal
        fileopen = open(self.licensefile, 'r')
        print fileopen.read()
        self.file_list = []             #to keep the supporting files
        self.initUI()

    def initUI(self):
        self.uploadbtn = QtGui.QPushButton('Upload')
        self.uploadbtn.clicked.connect(self.uploadModle)
        self.exitbtn = QtGui.QPushButton('Exit')
        self.exitbtn.clicked.connect(self.closeWindow)
        self.browsebtn = QtGui.QPushButton('Browse')
        self.browsebtn.clicked.connect(self.browseFile)
        self.addbtn = QtGui.QPushButton('Add Files')
        self.addbtn.clicked.connect(self.addFiles)
        self.removebtn = QtGui.QPushButton('Remove Files')
        self.removebtn.clicked.connect(self.removeFiles)
        self.ledit = QtGui.QLineEdit(self)
        self.sedit = QtGui.QTextEdit(self)
        self.process = QtCore.QProcess(self)
        self.termedit = QtGui.QTextEdit(self)
        self.termedit.setReadOnly(1)
        pal = QtGui.QPalette()
        bgc = QtGui.QColor(0, 0, 0)
        pal.setColor(QtGui.QPalette.Base, bgc)
        self.termedit.setPalette(pal)
        self.termedit.setStyleSheet("QTextEdit {color:white}")

        #Creating gridlayout
        grid = QtGui.QGridLayout()
        grid.setSpacing(5)
        grid.addWidget(self.ledit, 1, 0)
        grid.addWidget(self.browsebtn, 1, 1)
        grid.addWidget(self.sedit, 2, 0, 4, 1)
        grid.addWidget(self.addbtn, 2, 1)
        grid.addWidget(self.removebtn, 3, 1)
        grid.addWidget(self.termedit, 6, 0, 10, 1)
        grid.addWidget(self.uploadbtn, 17, 0)
        grid.addWidget(self.exitbtn,17, 1)

        self.setLayout(grid)
        self.setGeometry(300, 300, 600,600)
        self.setWindowTitle("Ngspice Digital Model Creator")
        #self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.show()
	


    def closeWindow(self):
        try:
            self.process.close()
        except:
                pass
        print "Close button clicked"
        quit()

    def browseFile(self):
        print "Browse button clicked"
        self.filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '.')
        self.ledit.setText(self.filename)
        print "Vhdl file uploaded to process :", self.filename

    def addFiles(self):
        print "Starts adding supporting files"
        title = self.addbtn.text()
        for file in QtGui.QFileDialog.getOpenFileNames(self, title):
                self.sedit.append(str(file))
                self.file_list.append(file)
        print "Supporting Files are :",self.file_list


    def removeFiles(self):
            self.fileRemover = FileRemover(self)


    #check extensions of all supporting files
    def checkSupportFiles(self):
        nonvhdl_count = 0
        for file in self.file_list:
            extension = os.path.splitext(str(file))[1]
            if extension != ".vhdl":
                nonvhdl_count += 1
                self.file_list.remove(file)

        if nonvhdl_count > 0:
             QtGui.QMessageBox.about(self,'Message','''<b>Important Message.</b><br/><br/>Supporting files should be <b>.vhdl</b> file ''')


    def createModelDirectory(self):
        print "Create Model Directory Called"
        self.digital_home=self.parser.get('NGSPICE','DIGITAL_MODEL')
        os.chdir(self.digital_home)
        print "Current Working Directory Changed to",os.getcwd()
        self.modelname = os.path.basename(str(self.filename)).split('.')[0]
        print "Model to be created :",self.modelname
        # Looking if model directory is present or not
        if os.path.isdir(self.modelname):
            print "Model Already present"
            ret = QtGui.QMessageBox.critical(self, "Critical",'''<b>The Model already exist.Do you want to overwrite it?</b><br/>
                    <b>If yes press ok else cancel it and change the name of you vhdl file</b>''', QtGui.QMessageBox.Ok, QtGui.QMessageBox.Cancel)
            if ret == QtGui.QMessageBox.Ok:
                print "Overwriting existing model "+self.modelname
                cmd="rm -rf "+self.modelname
                #process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                subprocess.call(cmd, shell=True)
                os.mkdir(self.modelname)
            else:
                print "Exiting application"
                quit()
                


        else:
            print "Creating model "+self.modelname+" directory"
            os.mkdir(self.modelname)
    
    def addingModelInModpath(self):
        print "Adding Model "+self.modelname+" in Modpath file "+self.digital_home
        #Adding name of model in the modpath file
        #Check if the string is already in the file
        with open(self.digital_home+"/modpath.lst",'a+') as f:
            flag = 0
            for line in f:
                if line.strip() == self.modelname:
                    print "Found model "+self.modelname+" in the modpath.lst"
                    flag = 1
                    break
                else:
                    pass

            if flag == 0:
                print "Adding model name "+self.modelname+" into modpath.lst"
                f.write(self.modelname+"\n")
            else:
                print "Model name is already into modpath.lst"


    def createModelFiles(self):
        print "Create Model Files Called"
        os.chdir(self.cur_dir)
        print "Current Working directory changed to "+self.cur_dir
        cmd = "python "+self.src_home+"/src/model_generation.py "+str(self.ledit.text())
        stdouterr = os.popen4(cmd)[1].read()
        print stdouterr
        #Moving file to model directory
        path=os.path.join(self.digital_home,self.modelname)
        shutil.move("cfunc.mod",path)
        shutil.move("ifspec.ifs",path)

        #Creating directory inside model directoy
        print "Creating DUT directory at "+os.path.join(path,"DUTghdl")
        os.mkdir(path+"/DUTghdl/")
        print "Copying required file to DUTghdl directory"
        shutil.move("connection_info.txt",path+"/DUTghdl/")
        shutil.move("start_server.sh",path+"/DUTghdl/")
        shutil.move("sock_pkg_create.sh",path+"/DUTghdl/")
        shutil.move(self.modelname+"_tb.vhdl",path+"/DUTghdl/")
        
        shutil.copy(str(self.filename),path+"/DUTghdl/")
        shutil.copy(os.path.join(self.home, self.src_home)+"/src/ghdlserver/compile.sh",path+"/DUTghdl/")
        shutil.copy(os.path.join(self.home, self.src_home)+"/src/ghdlserver/uthash.h",path+"/DUTghdl/")
        shutil.copy(os.path.join(self.home, self.src_home)+"/src/ghdlserver/ghdlserver.c",path+"/DUTghdl/")
        shutil.copy(os.path.join(self.home, self.src_home)+"/src/ghdlserver/ghdlserver.h",path+"/DUTghdl/")
        shutil.copy(os.path.join(self.home, self.src_home)+"/src/ghdlserver/Utility_Package.vhdl",path+"/DUTghdl/")
        shutil.copy(os.path.join(self.home, self.src_home)+"/src/ghdlserver/Vhpi_Package.vhdl",path+"/DUTghdl/")

        for file in self.file_list:
                shutil.copy(str(file), path+"/DUTghdl/")
        
        os.chdir(path+"/DUTghdl")
        subprocess.call("bash "+path+"/DUTghdl/compile.sh", shell=True)
        subprocess.call("chmod a+x start_server.sh",shell=True)
        subprocess.call("chmod a+x sock_pkg_create.sh",shell=True)
        os.remove("compile.sh")
        os.remove("ghdlserver.c")
        #os.remove("ghdlserver.h")
        #os.remove("Utility_Package.vhdl")
        #os.remove("Vhpi_Package.vhdl")
        
    
    #slot to redirect stdout to window console
    @QtCore.pyqtSlot()
    def readStdOutput(self):
        self.termedit.append(QtCore.QString(self.process.readAllStandardOutput()))
        

    def runMake(self):
        print "run Make Called"
        self.release_home=self.parser.get('NGSPICE','RELEASE')
        os.chdir(self.release_home)
        try:
            cmd = " make"
            print "Running Make command in "+self.release_home
            path = os.getcwd()
            self.process.start(cmd)
            self.process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
            QtCore.QObject.connect(self.process, QtCore.SIGNAL("readyReadStandardOutput()"), self, QtCore.SLOT("readStdOutput()"))
            print "make command process pid ---------- >",self.process.pid()
            
        except:
            print "There is error in 'make' "
            quit()

    def runMakeInstall(self):
        print "run Make Install Called"
        try:
            cmd = " make install"
            print "Running Make Install"
            path = os.getcwd()
            try:
                self.process.close()
            except:
                pass
            self.process.finished.connect(self.createSchematicLib)
            self.process.start(cmd)
            self.process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
            QtCore.QObject.connect(self.process, QtCore.SIGNAL("readyReadStandardOutput()"), self, QtCore.SLOT("readStdOutput()"))
            os.chdir(self.cur_dir)

        except:
            print "There is error during in 'make install' "
            quit()

    def createSchematicLib(self):
        if Appconfig.esimFlag == 1:
            print 'Creating library files.................................'
            self.schematicLib = AutoSchematic(self.modelname)
            self.schematicLib.createKicadLibrary()

    def uploadModle(self):
        print "Upload button clicked"
        try:
            self.process.close()
        except:
                pass
        try:
            self.file_extension = os.path.splitext(str(self.filename))[1]
            print "Uploaded File extension :"+self.file_extension
            self.cur_dir = os.getcwd()
            print "Current Working Directory :"+self.cur_dir
            self.checkSupportFiles()
            if self.file_extension == ".vhdl":
                self.createModelDirectory()
                self.addingModelInModpath()
                self.createModelFiles()
                self.runMake()
                self.runMakeInstall()
            else:
                QtGui.QMessageBox.about(self,'Message','''<b>Important Message.</b><br/><br/>This accepts only <b>.vhdl</b> file ''')
        except:
            QtGui.QMessageBox.about(self, 'Message','''<b>Error</b><br/><br/> select a <b>.vhdl</b> file ''')

class FileRemover(QtGui.QWidget):

        def __init__(self, main_obj):
                super(FileRemover, self).__init__()
                self.row = 0
                self.col = 0
                self.cb_dict = {}
                self.marked_list = []
                self.files = main_obj.file_list
                self.sedit = main_obj.sedit

                print self.files

                self.grid = QtGui.QGridLayout()
                removebtn = QtGui.QPushButton('Remove', self)
                removebtn.clicked.connect(self.removeFiles)

                self.grid.addWidget(self.createCheckBox(), 0, 0)
                self.grid.addWidget(removebtn, 1, 1)

                self.setLayout(self.grid)
                self.show()

        def createCheckBox(self):

                self.checkbox = QtGui.QGroupBox()
                self.checkbox.setTitle('Remove Files')
                self.checkgrid = QtGui.QGridLayout()

                self.checkgroupbtn = QtGui.QButtonGroup()

                for path in self.files:

                        print path

                        self.cb_dict[path] = QtGui.QCheckBox(path)
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
                        print path +" is removed"
                        self.sedit.append(path + " removed")
                        self.files.remove(path)

                self.sedit.clear()
                for path in self.files:
                        self.sedit.append(path)

                self.marked_list[:] = []
                self.files[:] = []
                self.close()



def main():
    app = QtGui.QApplication(sys.argv)
    if len(sys.argv) > 1:
        if sys.argv[1] == '-e':
            Appconfig.esimFlag = 1
    w = Mainwindow()
    sys.exit(app.exec_())

if __name__=='__main__':
    main()
