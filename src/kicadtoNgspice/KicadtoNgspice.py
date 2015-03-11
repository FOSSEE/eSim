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

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        print "Init Kicad to Ngspice"
        
        '''
        self.analysisTab = QtGui.QWidget()
        self.sourceTab = QtGui.QWidget()
        self.modelTab = QtGui.QWidget()
        '''
        self.analysisTab = Analysis.Analysis()
        self.sourceTab = QtGui.QWidget()
        self.modelTab = QtGui.QWidget()
        
        
        self.td = TabbedWidget.TabbedWidget()
        self.td.addTab(self.analysisTab, 'Analysis Inserter')
        self.td.addTab(self.sourceTab, 'Source Detail')
        self.td.addTab(self.modelTab, 'Model Detail')
        self.td.show()
        
        '''
        self.tabs = QtGui.QTabWidget()
        self.testpushBTN = QtGui.QPushButton("QPushButton 1")
           
        
        self.vbox = QtGui.QVBoxLayout()
        self.vbox.addWidget(self.testpushBTN)
        

        #Resize width and height
        self.tabs.resize(600, 600)
    
        #Move QTabWidget to x:300,y:300
        self.tabs.move(300, 300)
    
        #Set Layout for Third Tab Page
        self.modelTab.setLayout(self.vbox)   
    
        self.tabs.addTab(self.analysisTab,"Analysis Inserter")
        self.tabs.addTab(self.sourceTab,"Source Detail")
        self.tabs.addTab(self.modelTab,"Model Details")
    
        self.tabs.setWindowTitle('Kicad to Ngspice Conversion')
        self.tabs.show()
        '''
        
        



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
    
    
        
        