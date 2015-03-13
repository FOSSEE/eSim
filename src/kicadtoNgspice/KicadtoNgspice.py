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
import TabbedWidget
import Analysis

class MainWindow(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        print "Init Kicad to Ngspice"
             
        self.grid = QtGui.QGridLayout(self)
        self.grid.addWidget(self.createConvertWidget(),0,0)
        self.setGeometry(500, 500, 600, 600)
        self.setLayout(self.grid)
        self.show()
          
    def createConvertWidget(self):
        self.convertbox = QtGui.QGroupBox()
        self.convertgrid = QtGui.QGridLayout()
        
        self.convertbtn = QtGui.QPushButton("Convert")
        self.cancelbtn = QtGui.QPushButton("Cancel")
        
        self.analysisTab = Analysis.Analysis()
        self.sourceTab = QtGui.QWidget()
        self.modelTab = QtGui.QWidget()
        
        self.td = TabbedWidget.TabbedWidget()
        self.td.addTab(self.analysisTab, 'Analysis Inserter')
        self.td.addTab(self.sourceTab, 'Source Detail')
        self.td.addTab(self.modelTab, 'Model Detail')
      
        
        
        #self.td.show()
        
        self.convertgrid.addWidget(self.td,0,0)
        self.convertgrid.addWidget(self.convertbtn,1,1)
        self.convertgrid.addWidget(self.cancelbtn,1,2)
        
        self.convertbox.setLayout(self.convertgrid)
                    
        return self.convertbox
        
        
        
        
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
    
    
        
        