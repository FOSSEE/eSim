import sys
from PyQt4 import QtGui,QtCore
from configuration.Appconfig import Appconfig

class ProjectExplorer(QtGui.QWidget):
    """
    This Class create the project explorer windows of eSim-Workspace
    """
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self)
        #Creating object of AppConfig
        self.obj_appconfig = Appconfig()
        
        self.startpath = self.obj_appconfig.default_workspace["workspace"]
        
        self.view = QtGui.QTreeView()
              
        self.grid= QtGui.QGridLayout()
        self.model = QtGui.QFileSystemModel()
        
        self.view.setModel(self.model)
        self.view.setRootIndex(self.model.setRootPath(self.startpath))
        self.view.setHeaderHidden(True)
        self.view.hideColumn(1)
        self.view.hideColumn(2)
        self.view.hideColumn(3)

        self.view.doubleClicked.connect(self.on_clicked)
        self.grid.addWidget(self.view)
        
        
        self.setLayout(self.grid)
        self.show()
        
    def on_clicked(self,index):
               
        self.indexItem = self.model.index(index.row(), 0, index.parent())
        
        self.textwindow = QtGui.QWidget()
        self.text = QtGui.QTextEdit()
        self.save = QtGui.QPushButton('Save and Exit')
        self.save.setDisabled(True)
        self.windowgrid = QtGui.QGridLayout()
                
        self.filePath = self.model.filePath(self.indexItem)
        
             
        self.fopen = open(self.filePath, 'r')
        lines = self.fopen.readlines()
        for line in lines:
            self.text.append(line)
    
        QtCore.QObject.connect(self.text,QtCore.SIGNAL("textChanged()"), self.enable_save)        
        splitter_filelist = QtGui.QSplitter()
        splitter_filelist.setOrientation(QtCore.Qt.Vertical)
        
        vbox_main = QtGui.QVBoxLayout(self.textwindow)
        vbox_main.addWidget(splitter_filelist)
        vbox_main.addWidget(self.text)
        vbox_main.addWidget(self.save)
        self.save.clicked.connect(self.save_data)
        #self.connect(exit,QtCore.SIGNAL('close()'), self.onQuit)
        
        self.textwindow.show()
    
    def enable_save(self):
        self.save.setEnabled(True)
        
    def save_data(self):
        self.fopen=open(self.filePath, 'w')
        self.fopen.write(self.text.toPlainText())
        self.fopen.close()
        self.textwindow.close()