
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
#  ORGANIZATION: ecSim team at FOSSEE, IIT Bombay.
#       CREATED: Wednesday 21 January 2015 
#      REVISION:  ---
#===============================================================================


from PyQt4 import QtGui
from configuration.Appconfig import Appconfig
import ViewManagement
import Workspace
import sys 


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
        
        
        #Creating Application configuration object
        
        self.confObj = Appconfig() 
        
        self.setGeometry(self.confObj.app_xpos,
                         self.confObj.app_ypos,
                         self.confObj.app_width,
                         self.confObj.app_heigth)
        self.setWindowTitle(self.confObj._APPLICATION) 
        
        #Init Workspace
        self.work_space = Workspace.Workspace()
                
        
        
                
        #Init necessary components in sequence
        self.initActions()
        self.initView()
        
        
    def initActions(self):
     
        self.newproj = QtGui.QAction(QtGui.QIcon('../images/default.png'),'New Project',self)
        self.newproj.setShortcut('Ctrl+N')
        self.newproj.triggered.connect(self.testfn)
        
        self.openproj = QtGui.QAction(QtGui.QIcon('../images/default.png'),'Open Project',self)
        self.openproj.setShortcut('Ctrl+O')
        self.openproj.triggered.connect(self.testfn)
        
        self.exitproj = QtGui.QAction(QtGui.QIcon('../images/default.png'),'Exit',self)
        self.exitproj.setShortcut('Ctrl+X')
        self.exitproj.triggered.connect(self.testfn)
        
        self.helpfile = QtGui.QAction(QtGui.QIcon('../images/default.png'),'Help',self)
        self.helpfile.setShortcut('Ctrl+H')
        self.helpfile.triggered.connect(self.testfn)
        
        self.mainToolbar = self.addToolBar('Top Navigation')
        self.mainToolbar.addAction(self.newproj)
        self.mainToolbar.addAction(self.openproj)
        self.mainToolbar.addAction(self.exitproj)
        self.mainToolbar.addAction(self.helpfile)
              
      
    def initView(self):
        """
        Create gui from the class Views and initialize it
        """
        self.view = ViewManagement.ViewManagement()
        self.setCentralWidget(self.view)
   
    
    def testfn(self):
        print "Success hit :"
        
    def new_project(self):
        print "New Project called"
        
      

def main(args):
    """
    It is main function of the module.It starts the application
    """
    app = QtGui.QApplication(args)
       
    appView = Application()
    appView.show()
    sys.exit(app.exec_())        
    
    


# Call main function
if __name__ == '__main__':
    main(sys.argv)
    


