#===============================================================================
#
#          FILE: Application.py
# 
#         USAGE: --- 
# 
#   DESCRIPTION: This main file use to start the Application
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Fahim Khan, fahim.elex@gmail.com
#      MODIFIED: Rahul Paknikar, rahulp@iitb.ac.in    
#  ORGANIZATION: eSim team at FOSSEE, IIT Bombay.
#       CREATED: Tuesday 24 Feb 2015 
#      REVISION: Thursday 3 Oct 2019
#===============================================================================
import os
import sys
#Setting PYTHONPATH
cwd = os.getcwd()
(setPath,fronEnd) = os.path.split(cwd) 
sys.path.append(setPath)

from PyQt4 import QtGui, QtCore
from configuration.Appconfig import Appconfig
from projManagement.openProject import OpenProjectInfo
from projManagement.newProject import NewProjectInfo
from projManagement.Kicad import Kicad
from projManagement.Validation import Validation
from projManagement import Worker
from frontEnd import ProjectExplorer
from frontEnd import Workspace
from frontEnd import DockArea
import time
from PyQt4.Qt import QSize


class Application(QtGui.QMainWindow):
    global project_name	
    """
    Its our main window of application
    """
    def __init__(self,*args):
        """
        Initialize main Application window
        """
        #Calling __init__ of super class
        QtGui.QMainWindow.__init__(self,*args)


        #Flag for online-offline mode. Default is set offline mode.
        #Mode gets updated dynamically from the previous eSim session.
        self.online_flag = False

        
        #Creating require Object
        self.obj_workspace = Workspace.Workspace()
        self.obj_Mainview = MainView()
        self.obj_kicad = Kicad(self.obj_Mainview.obj_dockarea)
        self.obj_appconfig = Appconfig() 
        self.obj_validation = Validation()
        #Initialize all widget
        self.setCentralWidget(self.obj_Mainview)
        self.initToolBar()
        
        self.setGeometry(self.obj_appconfig._app_xpos,
                         self.obj_appconfig._app_ypos,
                         self.obj_appconfig._app_width,
                         self.obj_appconfig._app_heigth)
        self.setWindowTitle(self.obj_appconfig._APPLICATION) 
        self.showMaximized()
        self.setWindowIcon(QtGui.QIcon('../../images/logo.png'))
        #self.show()
        self.systemTrayIcon = QtGui.QSystemTrayIcon(self)
        self.systemTrayIcon.setIcon(QtGui.QIcon('../../images/logo.png'))
        self.systemTrayIcon.setVisible(True)
    
           
    def initToolBar(self):
        """
        This function initialize Tool Bar
        """
        #Top Tool bar
        self.newproj = QtGui.QAction(QtGui.QIcon('../../images/newProject.png'),'<b>New Project</b>',self)
        self.newproj.setShortcut('Ctrl+N')
        self.newproj.triggered.connect(self.new_project)
        #self.newproj.connect(self.newproj,QtCore.SIGNAL('triggered()'),self,QtCore.SLOT(self.new_project()))
               
        self.openproj = QtGui.QAction(QtGui.QIcon('../../images/openProject.png'),'<b>Open Project</b>',self)
        self.openproj.setShortcut('Ctrl+O')
        self.openproj.triggered.connect(self.open_project)
        
        self.closeproj = QtGui.QAction(QtGui.QIcon('../../images/closeProject.png'),'<b>Close Project</b>',self)
        self.closeproj.setShortcut('Ctrl+X')
        self.closeproj.triggered.connect(self.close_project)
        


        for file in os.listdir("../../../../.config/kicad"):
            if file.startswith("fp-lib-table"):
                if file.endswith("offline"):
                    self.webConnect = QtGui.QAction(QtGui.QIcon('../../images/online.png'),'<b>Go Offline</b>',self)
                    self.online_flag = True
                    break
                elif file.endswith("online"):
                    self.webConnect = QtGui.QAction(QtGui.QIcon('../../images/offline.png'),'<b>Go Online</b>',self)
                    self.online_flag = False
            	    break

        self.webConnect.setShortcut('Ctrl+G')
        self.webConnect.triggered.connect(self.go_online_offline)
                

        self.helpfile = QtGui.QAction(QtGui.QIcon('../../images/helpProject.png'),'<b>Help</b>',self)
        self.helpfile.setShortcut('Ctrl+H')
        self.helpfile.triggered.connect(self.help_project)
        
        self.topToolbar = self.addToolBar('Top Tool Bar')
        self.topToolbar.addAction(self.newproj)
        self.topToolbar.addAction(self.openproj)
        
        self.topToolbar.addAction(self.closeproj)
        self.topToolbar.addAction(self.webConnect)
        self.topToolbar.addAction(self.helpfile)
        
        self.spacer = QtGui.QWidget()
        self.spacer.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        self.topToolbar.addWidget(self.spacer)
        self.logo = QtGui.QLabel()
        self.logopic = QtGui.QPixmap(os.path.join(os.path.abspath('../..'),'images','fosseeLogo.png'))
        self.logopic = self.logopic.scaled(QSize(150,150),QtCore.Qt.KeepAspectRatio)
        self.logo.setPixmap(self.logopic)
        self.logo.setStyleSheet("padding:0 15px 0 0;")
        self.topToolbar.addWidget(self.logo)
             
        #Left Tool bar Action Widget 
        self.kicad = QtGui.QAction(QtGui.QIcon('../../images/kicad.png'),'<b>Open Schematic</b>',self)
        self.kicad.triggered.connect(self.obj_kicad.openSchematic)
        
        self.conversion = QtGui.QAction(QtGui.QIcon('../../images/ki-ng.png'),'<b>Convert Kicad to Ngspice</b>',self)
        self.conversion.triggered.connect(self.obj_kicad.openKicadToNgspice)
               
        self.ngspice = QtGui.QAction(QtGui.QIcon('../../images/ngspice.png'), '<b>Simulation</b>', self)
        self.ngspice.triggered.connect(self.open_ngspice)
        
        self.model = QtGui.QAction(QtGui.QIcon('../../images/model.png'),'<b>Model Editor</b>',self)
        self.model.triggered.connect(self.open_modelEditor) 
        
        self.subcircuit=QtGui.QAction(QtGui.QIcon('../../images/subckt.png'),'<b>Subcircuit</b>',self)
        self.subcircuit.triggered.connect(self.open_subcircuit)

        self.nghdl = QtGui.QAction(QtGui.QIcon('../../images/nghdl.png'), '<b>Nghdl</b>', self)
        self.nghdl.triggered.connect(self.open_nghdl)
        
        self.omedit = QtGui.QAction(QtGui.QIcon('../../images/omedit.png'),'<b>Modelica Converter</b>',self)
        self.omedit.triggered.connect(self.open_OMedit) 
        
        self.omoptim=QtGui.QAction(QtGui.QIcon('../../images/omoptim.png'),'<b>OM Optimisation</b>',self)
        self.omoptim.triggered.connect(self.open_OMoptim)
        
        #Adding Action Widget to tool bar   
        self.lefttoolbar = QtGui.QToolBar('Left ToolBar')
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.lefttoolbar)
        self.lefttoolbar.addAction(self.kicad)
        self.lefttoolbar.addAction(self.conversion)
        self.lefttoolbar.addAction(self.ngspice)
        self.lefttoolbar.addAction(self.model)
        self.lefttoolbar.addAction(self.subcircuit)
        self.lefttoolbar.addAction(self.nghdl)
        self.lefttoolbar.addAction(self.omedit)
        self.lefttoolbar.addAction(self.omoptim)
        self.lefttoolbar.setOrientation(QtCore.Qt.Vertical)
        self.lefttoolbar.setIconSize(QSize(40,40))
    
    def closeEvent(self, event):
        exit_msg = "Are you sure you want to exit the program ? All unsaved data will be lost."
        reply = QtGui.QMessageBox.question(self, 'Message',
                                           exit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        
        if reply == QtGui.QMessageBox.Yes:   
            for proc in self.obj_appconfig.procThread_list:
                    try:
                            proc.terminate()
                    except:
                            pass
            try:       
                for process_object in self.obj_appconfig.process_obj:
                    try:
                        process_object.close()
                    except:
                            pass
            except:
                pass
            ##Just checking if open project and New project window is open. If yes just close it when application is closed
            try:
                self.project.close()
            except:
                pass
            event.accept()
            self.systemTrayIcon.showMessage('Exit', 'eSim is Closed.')
        
        elif reply == QtGui.QMessageBox.No:
            event.ignore()
    
     
    def close_project(self):
        print "Function : Close Project"
        current_project = self.obj_appconfig.current_project['ProjectName']
        if current_project==None:
            pass
        else:
            for pid in self.obj_appconfig.proc_dict[self.obj_appconfig.current_project['ProjectName']]:
                try:
                    os.kill(pid, 9)
                except:
                    pass
            self.obj_Mainview.obj_dockarea.closeDock()
            self.obj_appconfig.current_project['ProjectName'] = None
            self.systemTrayIcon.showMessage('Close', 'Current project '+os.path.basename(current_project)+' is Closed.')
    
    def new_project(self):
        """
        This function call New Project Info class.
        """
        text, ok = QtGui.QInputDialog.getText(self, 'New Project Info','Enter Project Name:')
        if ok:
            self.projname = (str(text))
            self.project = NewProjectInfo()
            directory, filelist =self.project.createProject(self.projname)
    
            self.obj_Mainview.obj_projectExplorer.addTreeNode(directory, filelist)
            
        else:
            print "No new project created"
            self.obj_appconfig.print_info('No new project created')
            try:
                self.obj_appconfig.print_info('Current project is : ' + self.obj_appconfig.current_project["ProjectName"])
            except:
                pass
        
    def open_project(self):
        """
        This project call Open Project Info class
        """
        print "Function : Open Project"
        self.project = OpenProjectInfo()
        
        try:
            directory, filelist = self.project.body()
            self.obj_Mainview.obj_projectExplorer.addTreeNode(directory, filelist)
        except:
            pass
                
    def help_project(self):
        print "Function : Help"
        self.obj_appconfig.print_info('Help is called')
        print "Current Project is : ",self.obj_appconfig.current_project
        self.obj_Mainview.obj_dockarea.usermanual()    
    
    

    def go_online_offline(self):
        if not self.obj_kicad.check_open_schematic():
            if self.online_flag:
                os.rename("../../../../.config/kicad/fp-lib-table", "../../../../.config/kicad/fp-lib-table-online")
                os.rename("../../../../.config/kicad/fp-lib-table-offline", "../../../../.config/kicad/fp-lib-table")
                self.webConnect.setIcon(QtGui.QIcon('../../images/offline.png'))
                self.webConnect.setText('<b>Go Online</b>')
                self.online_flag = False
            else:
                os.rename("../../../../.config/kicad/fp-lib-table", "../../../../.config/kicad/fp-lib-table-offline")
                os.rename("../../../../.config/kicad/fp-lib-table-online", "../../../../.config/kicad/fp-lib-table")
                self.webConnect.setIcon(QtGui.QIcon('../../images/online.png'))
                self.webConnect.setText('<b>Go Offline</b>')
                self.online_flag = True
        else:
            self.msg = QtGui.QErrorMessage()
            self.msg.showMessage('Please save and close all the Kicad Windows first, and then change the online-offline mode')
            self.msg.setWindowTitle("Error Message")


    def open_ngspice(self):
        """
        This Function execute ngspice on current project
        """
        
        self.projDir = self.obj_appconfig.current_project["ProjectName"]
        
        if self.projDir != None:
            self.obj_Mainview.obj_dockarea.ngspiceEditor(self.projDir)
            time.sleep(2)  #Need permanent solution 
            #Calling Python Plotting
                
            try:
                self.obj_Mainview.obj_dockarea.plottingEditor()
            except Exception as e:
                self.msg = QtGui.QErrorMessage(None)
                self.msg.showMessage('Error while opening python plotting Editor. Please look at console for more details ')
                print "Exception Message:",str(e)
                self.obj_appconfig.print_error('Exception Message : ' + str(e))
                self.msg.setWindowTitle("Error Message")
                        
        else:
            self.msg = QtGui.QErrorMessage()
            self.msg.showMessage('Please select the project first. You can either create new project or open existing project')
            self.msg.setWindowTitle("Error Message")
            
    def open_subcircuit(self):
        print "Function : Subcircuit editor"
        self.obj_appconfig.print_info('Subcircuit editor is called')
        self.obj_Mainview.obj_dockarea.subcircuiteditor()

    def open_nghdl(self):
        print "Function : Nghdl"
        self.obj_appconfig.print_info('Nghdl is called')

        if self.obj_validation.validateTool('nghdl'):
            self.cmd = 'nghdl -e'
            self.obj_workThread = Worker.WorkerThread(self.cmd)
            self.obj_workThread.start()

        else:
            self.msg = QtGui.QErrorMessage(None)
            self.msg.showMessage('Error while opening nghdl. Please make sure nghdl is installed')
            self.obj_appconfig.print_error('Error while opening nghdl. Please make sure nghdl is installed')
            self.msg.setWindowTitle('nghdl Error Message')
            
      
    def open_modelEditor(self):
        print "Function : Model editor"
        self.obj_appconfig.print_info('Model editor is called')
        self.obj_Mainview.obj_dockarea.modelEditor()

    
    def open_OMedit(self):
        """
        This function call ngspice to OM edit converter and then launch OM edit.
        """
        self.obj_appconfig.print_info('OM edit is called')
        self.projDir = self.obj_appconfig.current_project["ProjectName"]
        
        if self.projDir != None:
            if self.obj_validation.validateCirOut(self.projDir):
                self.projName = os.path.basename(self.projDir)
                self.ngspiceNetlist = os.path.join(self.projDir,self.projName+".cir.out")
                self.modelicaNetlist = os.path.join(self.projDir,self.projName+".mo")
                
                """
                try:
                    #Creating a command for Ngspice to Modelica converter
                    self.cmd1 = "python ../ngspicetoModelica/NgspicetoModelica.py "+self.ngspiceNetlist
                    self.obj_workThread1 = Worker.WorkerThread(self.cmd1)
                    self.obj_workThread1.start()
                    
                    
                    if self.obj_validation.validateTool("OMEdit"):
                        #Creating command to run OMEdit
                        self.cmd2 = "OMEdit "+self.modelicaNetlist
                        self.obj_workThread2 = Worker.WorkerThread(self.cmd2)
                        self.obj_workThread2.start()
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
                                  
                except Exception as e:
                    self.msg = QtGui.QErrorMessage()
                    self.msg.showMessage('Unable to convert NgSpice netlist to Modelica netlist :'+str(e))
                    self.msg.setWindowTitle("Ngspice to Modelica conversion error")
                    self.obj_appconfig.print_error(str(e))
                """

                self.obj_Mainview.obj_dockarea.modelicaEditor(self.projDir)
                    
            else:
                self.msg = QtGui.QErrorMessage()
                self.msg.showMessage('Current project does not contain any ngspice file. Please create ngspice file with extension .cir.out')
                self.msg.setWindowTitle("Missing Ngspice netlist")
        else:
            self.msg = QtGui.QErrorMessage()
            self.msg.showMessage('Please select the project first. You can either create new project or open existing project')
            self.msg.setWindowTitle("Error Message")
        
    
    def open_OMoptim(self):
        print "Function : OM Optim"    
        self.obj_appconfig.print_info('OM Optim is called')
        #Check if OMOptim is installed 
        if self.obj_validation.validateTool("OMOptim"):
            #Creating a command to run
            self.cmd = "OMOptim"
            self.obj_workThread = Worker.WorkerThread(self.cmd)
            self.obj_workThread.start()
        else:
            self.msg = QtGui.QMessageBox()
            self.msgContent = "There was an error while opening OMOptim.<br/>\
            Please make sure OpenModelica is installed in your system. <br/>\
            To install it on Linux : Go to <a href=https://www.openmodelica.org/download/download-linux>OpenModelica Linux</a> and install nigthly build release.<br/>\
            To install it on Windows : Go to <a href=https://www.openmodelica.org/download/download-windows>OpenModelica Windows</a> and install latest version.<br/>"
            self.msg.setTextFormat(QtCore.Qt.RichText)
            self.msg.setText(self.msgContent)
            self.msg.setWindowTitle("Error Message")
            self.obj_appconfig.print_info(self.msgContent)
            self.msg.exec_()



class MainView(QtGui.QWidget):
    """
    This class initialize the Main View of Application
    """
    def __init__(self, *args):
        # call init method of superclass
        QtGui.QWidget.__init__(self, *args)
        
        self.obj_appconfig = Appconfig()
        
        self.leftSplit = QtGui.QSplitter()
        self.middleSplit = QtGui.QSplitter()
        
        self.mainLayout = QtGui.QVBoxLayout()
        #Intermediate Widget
        self.middleContainer = QtGui.QWidget()
        self.middleContainerLayout = QtGui.QVBoxLayout()
        
        #Area to be included in MainView
        self.noteArea = QtGui.QTextEdit()
        self.noteArea.setReadOnly(True)
        self.obj_appconfig.noteArea['Note'] = self.noteArea
        self.obj_appconfig.noteArea['Note'].append('        eSim Started......')
        self.obj_appconfig.noteArea['Note'].append('Project Selected : None')
        self.obj_appconfig.noteArea['Note'].append('\n')
        
        #CSS
        self.noteArea.setStyleSheet(" \
        QWidget { border-radius: 15px; border: 1px solid gray; padding: 5px; } \
        ")
        
        self.obj_dockarea = DockArea.DockArea()
        self.obj_projectExplorer = ProjectExplorer.ProjectExplorer()
               
        #Adding content to vertical middle Split. 
        self.middleSplit.setOrientation(QtCore.Qt.Vertical)
        self.middleSplit.addWidget(self.obj_dockarea)
        self.middleSplit.addWidget(self.noteArea)
                
        #Adding middle split to Middle Container Widget
        self.middleContainerLayout.addWidget(self.middleSplit)
        self.middleContainer.setLayout(self.middleContainerLayout)
        
        #Adding content of left split
        self.leftSplit.addWidget(self.obj_projectExplorer)
        self.leftSplit.addWidget(self.middleContainer)
    
        #Adding to main Layout
        self.mainLayout.addWidget(self.leftSplit)
        self.leftSplit.setSizes([self.width()/4.5,self.height()])
        self.middleSplit.setSizes([self.width(),self.height()/2])
        self.setLayout(self.mainLayout)
     

def main(args):
    """
    It is main function of the module. It starts the application
    """
    print "Starting eSim......"
    app = QtGui.QApplication(args)
    
    splash_pix = QtGui.QPixmap('../../images/splash_screen_esim.png')
    splash = QtGui.QSplashScreen(splash_pix,QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    appView = Application()
    appView.splash=splash
    appView.obj_workspace.returnWhetherClickedOrNot(appView)
    appView.hide()
    appView.obj_workspace.show() 
    sys.exit(app.exec_())
        
        
# Call main function
if __name__ == '__main__':
    # Create and display the splash screen
    main(sys.argv)
    


