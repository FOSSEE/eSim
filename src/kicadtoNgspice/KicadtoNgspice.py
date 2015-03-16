#===============================================================================
#
#          FILE: kicadtoNgspice.py
# 
#         USAGE: --- 
# 
#   DESCRIPTION: This define all configuration used in Application. 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Fahim Khan, fahim.elex@gmail.com
#  ORGANIZATION: eSim team at FOSSEE, IIT Bombay.
#       CREATED: Wednesday 04 March 2015 
#      REVISION:  ---
#===============================================================================
import sys
from PyQt4 import QtGui
import Analysis

class MainWindow(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        print "Init Kicad to Ngspice"
             
        self.grid = QtGui.QGridLayout(self)
        self.convertbtn = QtGui.QPushButton("Convert")
        self.cancelbtn = QtGui.QPushButton("Cancel")
        self.grid.addWidget(self.createcreateConvertWidget(),0,0)
        self.grid.addWidget(self.convertbtn,1,1)
        self.grid.addWidget(self.cancelbtn,1,2)
        self.setGeometry(500, 500, 600, 600)
        self.setLayout(self.grid)
        self.show()
          
    
    def createcreateConvertWidget(self):
        self.convertWindow = QtGui.QWidget()
                      
        self.analysisTab = QtGui.QScrollArea()
        self.analysisTab.setWidget(Analysis.Analysis())
        self.analysisTabLayout = QtGui.QVBoxLayout(self.analysisTab.widget())
        self.analysisTab.setWidgetResizable(True)
        
        self.sourceTab = QtGui.QScrollArea()
        self.sourceTab.setWidget(QtGui.QWidget())
        self.sourceTabLayout = QtGui.QVBoxLayout(self.sourceTab.widget())
        self.sourceTab.setWidgetResizable(True)
        
        self.modelTab = QtGui.QScrollArea()
        self.modelTab.setWidget(QtGui.QWidget())
        self.modelTabLayout = QtGui.QVBoxLayout(self.modelTab.widget())
        self.modelTab.setWidgetResizable(True)

        self.tabWidget = QtGui.QTabWidget()
        self.tabWidget.addTab(self.analysisTab,"Analysis Tab")
        self.tabWidget.addTab(self.sourceTab,"Source Tab")
        self.tabWidget.addTab(self.modelTab,"Model Tab")
        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.addWidget(self.tabWidget)
        #self.mainLayout.addStretch(1)
        self.convertWindow.setLayout(self.mainLayout)
        self.convertWindow.show()
    
        
        return self.convertWindow 
    
        
def main():
    print "=================================="
    print "Kicad to Ngspice netlist converter "
    print "=================================="
    
    #kicadNetlist = sys.argv[1]
    
  
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("KicadToNgspice")
    app.setQuitOnLastWindowClosed(True)
    window = MainWindow()
    main()
    sys.exit(app.exec_())
    
    
        
        