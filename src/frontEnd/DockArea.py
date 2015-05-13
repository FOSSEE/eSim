from PyQt4 import QtGui,QtCore
from ngspiceSimulation.pythonPlotting import plotWindow
#from configuration.Appconfig import Appconfig


dockList = ['Blank']
count = 1 
dock = {}

class DockArea(QtGui.QMainWindow):
    
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        for dockName in dockList:
            dock[dockName] = QtGui.QDockWidget(dockName)
            dock[dockName].setWidget(QtGui.QTextEdit())
                        
            self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dock[dockName])  
                    
        #self.tabifyDockWidget(dock['Notes'],dock['Blank'])
        self.show()
    
             
    def createTestEditor(self):
        """
        This function create widget for Library Editor
        """
        global count
                
        self.testWidget = QtGui.QWidget()
        self.testArea = QtGui.QTextEdit()
        self.testLayout = QtGui.QVBoxLayout()
        self.testLayout.addWidget(self.testArea)
        
        #Adding to main Layout
        self.testWidget.setLayout(self.testLayout)
        dock['Tips-'+str(count)] = QtGui.QDockWidget('Tips-'+str(count))
        dock['Tips-'+str(count)].setWidget(self.testWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dock['Tips-'+str(count)])  
        self.tabifyDockWidget(dock['Blank'],dock['Tips-'+str(count)])
        
        dock['Tips-'+str(count)].setVisible(True)
        dock['Tips-'+str(count)].setFocus()
        dock['Tips-'+str(count)].raise_()
        
        count = count + 1
        
    def plottingEditor(self):
        """
        This function create widget for Library Editor
        """
        global count
        self.plottingWidget = QtGui.QWidget()
        #self.plottingArea = QtGui.QTextEdit()
        
        
        self.plottingLayout = QtGui.QVBoxLayout()
        #self.plottingLayout.addWidget(self.plottingArea)
        self.plottingLayout.addWidget(plotWindow())
        
        #Adding to main Layout
        self.plottingWidget.setLayout(self.plottingLayout)
        dock['Plotting-'+str(count)] = QtGui.QDockWidget('Plotting-'+str(count))
        dock['Plotting-'+str(count)].setWidget(self.plottingWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dock['Plotting-'+str(count)])  
        self.tabifyDockWidget(dock['Blank'],dock['Plotting-'+str(count)])
        
        dock['Plotting-'+str(count)].setVisible(True)
        dock['Plotting-'+str(count)].setFocus()
        dock['Plotting-'+str(count)].raise_()
        
        count = count + 1
        
        
        
                
        
                     
        