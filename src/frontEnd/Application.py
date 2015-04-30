
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
#  ORGANIZATION: eSim team at FOSSEE, IIT Bombay.
#       CREATED: Wednesday 21 January 2015 
#      REVISION:  ---
#===============================================================================


from PyQt4 import QtGui, QtCore
from configuration.Appconfig import Appconfig
from projManagement.openProject import OpenProjectInfo
from projManagement.newProject import NewProjectInfo
from projManagement.Kicad import Kicad
import os
import ViewManagement
import Workspace
import sys 
import time
import subprocess
import TestView


class Application(QtGui.QMainWindow):
    """
    Its our main window of application
    """
    def __init__(self,*args):
        """
        Initialize main Application window
        """
        #Calling __init__ of super class
        QtGui.QMainWindow.__init__(self,*args)
        
        #Init Workspace
        self.obj_workspace = Workspace.Workspace()
        
        #Creating object of Kicad.py
        self.obj_kicad = Kicad()
        
        #Creating Application configuration object
        self.obj_appconfig = Appconfig() 
        self.setGeometry(self.obj_appconfig._app_xpos,
                         self.obj_appconfig._app_ypos,
                         self.obj_appconfig._app_width,
                         self.obj_appconfig._app_heigth)
        self.setWindowTitle(self.obj_appconfig._APPLICATION) 
        
           
        #Init necessary components in sequence
        self.initToolBar()
        #self.initView()
        self.setCentralWidget(self.initMainView())
        
    
      
    def initMainView(self):
        
        self.mainWidget = QtGui.QWidget()
        
        self.leftSplit = QtGui.QSplitter()
        self.middleSplit = QtGui.QSplitter()
        self.rightSplit = QtGui.QSplitter()  #Will be use in future for Browser
        
        self.projectExplorer = QtGui.QTextEdit()
        self.mainArea = QtGui.QTextEdit()
        self.noteArea = QtGui.QTextEdit()
        self.browserArea = QtGui.QTextEdit()
        
        self.mainLayout = QtGui.QVBoxLayout()
        
        #Intermediate Widget
        self.middleContainer = QtGui.QWidget()
        self.middleContainerLayout = QtGui.QVBoxLayout()
        
        #Adding content to middle Split whichis vertical
        self.middleSplit.setOrientation(QtCore.Qt.Vertical)
        self.middleSplit.addWidget(self.mainArea)
        self.middleSplit.addWidget(self.noteArea)
        #Adding middle split to Middle Container Widget
        self.middleContainerLayout.addWidget(self.middleSplit)
        self.middleContainer.setLayout(self.middleContainerLayout)
        
        #Adding content ot left split
        self.leftSplit.addWidget(self.projectExplorer)
        self.leftSplit.addWidget(self.middleContainer)
        
        
        #Adding to main Layout
        self.mainLayout.addWidget(self.leftSplit)
        self.mainWidget.setLayout(self.mainLayout)
                
        return self.mainWidget
    
        
        
    def initToolBar(self):
        
        #Top Tool bar
        self.newproj = QtGui.QAction(QtGui.QIcon('../images/newProject.png'),'<b>New Project</b>',self)
        self.newproj.setShortcut('Ctrl+N')
        self.newproj.triggered.connect(self.new_project)
               
        self.openproj = QtGui.QAction(QtGui.QIcon('../images/openProject.png'),'<b>Open Project</b>',self)
        self.openproj.setShortcut('Ctrl+O')
        self.openproj.triggered.connect(self.open_project)
        
        self.exitproj = QtGui.QAction(QtGui.QIcon('../images/closeProject.png'),'<b>Exit</b>',self)
        self.exitproj.setShortcut('Ctrl+X')
        self.exitproj.triggered.connect(self.exit_project)
        
        self.helpfile = QtGui.QAction(QtGui.QIcon('../images/helpProject.png'),'<b>Help</b>',self)
        self.helpfile.setShortcut('Ctrl+H')
        self.helpfile.triggered.connect(self.help_project)
        
        self.topToolbar = self.addToolBar('Top Tool Bar')
        self.topToolbar.addAction(self.newproj)
        self.topToolbar.addAction(self.openproj)
        self.topToolbar.addAction(self.exitproj)
        self.topToolbar.addAction(self.helpfile)
                
        #Left Tool bar Start
        self.kicad = QtGui.QAction(QtGui.QIcon('../images/default.png'),'<b>Open Schematic</b>',self)
        self.kicad.triggered.connect(self.obj_kicad.openSchematic)
        
        self.conversion = QtGui.QAction(QtGui.QIcon('../images/default.png'),'<b>Convert Kicad to Ngspice</b>',self)
        self.conversion.triggered.connect(self.obj_kicad.openKicadToNgspice)
               
        self.ngspice = QtGui.QAction(QtGui.QIcon('../images/default.png'), '<b>Simulation</b>', self)
        
        self.footprint = QtGui.QAction(QtGui.QIcon('../images/default.png'),'<b>Footprint Editor</b>',self)
        self.footprint.triggered.connect(self.obj_kicad.openFootprint)
        
        self.pcb = QtGui.QAction(QtGui.QIcon('../images/default.png'),'<b>PCB Layout</b>',self)
        self.pcb.triggered.connect(self.obj_kicad.openLayout)
              
        
        self.lefttoolbar = QtGui.QToolBar('Left ToolBar')
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.lefttoolbar)
        self.lefttoolbar.addAction(self.kicad)
        self.lefttoolbar.addAction(self.conversion)
        self.lefttoolbar.addAction(self.ngspice)
        self.lefttoolbar.addAction(self.footprint)
        self.lefttoolbar.addAction(self.pcb)
        self.lefttoolbar.setOrientation(QtCore.Qt.Vertical)
        
    def initView(self):
        """
        Create GUI from the class Views and initialize it
        """
        self.view = ViewManagement.ViewManagement()
        self.setCentralWidget(self.view)
        
    def new_project(self):
        """
        This function call New Project Info class.
        """
        print "New Project called"
        self.project = NewProjectInfo()
        self.project.body()
                  
    
    def open_project(self):
        """
        This project call Open Project Info class
        """
        print "Open Project called"
        self.project = OpenProjectInfo()
        self.project.body()
        
    def exit_project(self):
        print "Exit Project called"
        for proc in self.obj_appconfig.procThread_list:
                try:
                        proc.terminate()
                except:
                        pass
        ##Just checking if open and New window is open. If yes just close it when application is closed
        try:
            self.project.close()
        except:
            pass
        
        self.close()
        
    def help_project(self):
        print "Help is called"
        print "Current Project : ",self.obj_appconfig.current_project
                
        
    def testing(self):
        print "Success hit kicad button"
              

def main(args):
    """
    It is main function of the module.It starts the application
    """
    print "Starting eSim......"
    app = QtGui.QApplication(args)
   
    """
    splash_pix = QtGui.QPixmap('../images/FreeEDAlogo.jpg')
    splash = QtGui.QSplashScreen(splash_pix,QtCore.Qt.WindowStaysOnTopHint)
    progressBar = QtGui.QProgressBar(splash)
    splash.setMask(splash_pix.mask())
    splash.show()
    
    for i in range(0, 100):
        progressBar.setValue(i)
        t = time.time()
        while time.time() < t + 0.1:
            app.processEvents()    
    
    time.sleep(2)
    
    appView = Application()
    appView.show()
    splash.finish(appView)
    sys.exit(app.exec_())
    """
    appView = Application()
    #QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Cleanlooks"))
    appView.show()
    sys.exit(app.exec_())
    
    


# Call main function
if __name__ == '__main__':
    # Create and display the splash screen
    main(sys.argv)
    


