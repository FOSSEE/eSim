from PyQt4 import QtGui,QtCore
import os
import json
from configuration.Appconfig import Appconfig
from lxml.etree import tostring

class ProjectExplorer(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.obj_appconfig = Appconfig()
        self.treewidget = QtGui.QTreeWidget()
        self.window= QtGui.QVBoxLayout()
        header = QtGui.QTreeWidgetItem(["Projects","path"])
        self.treewidget.setHeaderItem(header)
        self.treewidget.setColumnHidden(1,True)
        
        #CSS
        self.treewidget.setStyleSheet(" \
        QTreeView { border-radius: 15px; border: 1px solid gray; padding: 5px; width: 200px; height: 150px;  } \
        QTreeView::branch:has-siblings:!adjoins-item { border-image: url(../images/vline.png) 0; } \
        QTreeView::branch:has-siblings:adjoins-item { border-image: url(../images/branch-more.png) 0; } \
        QTreeView::branch:!has-children:!has-siblings:adjoins-item { border-image: url(../images/branch-end.png) 0; } \
        QTreeView::branch:has-children:!has-siblings:closed, \
        QTreeView::branch:closed:has-children:has-siblings { border-image: none; image: url(../images/branch-closed.png); } \
        QTreeView::branch:open:has-children:!has-siblings, \
        QTreeView::branch:open:has-children:has-siblings { border-image: none; image: url(../images/branch-open.png); } \
        ")
        
        for parents, children in self.obj_appconfig.project_explorer.items():
            os.path.join(parents)
            if os.path.exists(parents):
                pathlist= parents.split(os.sep)
                parentnode = QtGui.QTreeWidgetItem(self.treewidget, [pathlist[-1],parents])
                for files in children:
                    childnode = QtGui.QTreeWidgetItem(parentnode, [files, parents+ '/'+ files])
        self.window.addWidget(self.treewidget)
        
        self.treewidget.doubleClicked.connect(self.openProject)
        self.treewidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treewidget.customContextMenuRequested.connect(self.openMenu)
        self.setLayout(self.window)
        self.show()
        
    def addTreeNode(self, parents, children):
        os.path.join(parents)
        pathlist= parents.split(os.sep)
        parentnode = QtGui.QTreeWidgetItem(self.treewidget, [pathlist[-1], parents])
        for files in children:
            childnode= QtGui.QTreeWidgetItem(parentnode, [files, parents+ '/'+ files])
            
    def openMenu(self, position):
    
        indexes = self.treewidget.selectedIndexes()
        if len(indexes) > 0:
        
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1
        
        menu = QtGui.QMenu()
        if level == 0:
            deleteproject = menu.addAction(self.tr("Remove Project"))
            deleteproject.triggered.connect(self.removeProject)
            refreshproject= menu.addAction(self.tr("Refresh"))
            refreshproject.triggered.connect(self.refreshProject)
        elif level == 1:
            openfile = menu.addAction(self.tr("Open"))
            openfile.triggered.connect(self.openProject)
        
        menu.exec_(self.treewidget.viewport().mapToGlobal(position))  
        
    def openProject(self):
        self.indexItem =self.treewidget.currentIndex()
        filename= self.indexItem.data().toString()
        self.filePath= self.indexItem.sibling(self.indexItem.row(), 1).data().toString()
        
        self.textwindow = QtGui.QWidget()
        self.textwindow.setMinimumSize(600, 500)
        self.textwindow.setGeometry(QtCore.QRect(400,150,400,400))
        self.textwindow.setWindowTitle(filename)
        
        self.text = QtGui.QTextEdit()
        self.save = QtGui.QPushButton('Save and Exit')
        self.save.setDisabled(True)
        self.windowgrid = QtGui.QGridLayout()
        if (os.path.isfile(str(self.filePath)))== True:
            self.fopen = open(str(self.filePath), 'r')
            lines = self.fopen.readlines()
            for line in lines:
                self.text.append(line)
    
            QtCore.QObject.connect(self.text,QtCore.SIGNAL("textChanged()"), self.enable_save)        
            
            vbox_main = QtGui.QVBoxLayout(self.textwindow)
            vbox_main.addWidget(self.text)
            vbox_main.addWidget(self.save)
            self.save.clicked.connect(self.save_data)
            #self.connect(exit,QtCore.SIGNAL('close()'), self.onQuit)
            
            self.textwindow.show()
        else:
            self.obj_appconfig.current_project["ProjectName"]= str(self.filePath)
        
    def enable_save(self):
        self.save.setEnabled(True)
        
    def save_data(self):
        self.fopen=open(self.filePath, 'w')
        lines = str(self.text.toPlainText()).split('\n')
        lines=[i+'\r' if i in lines[:-1] else i for i in lines]
        self.fopen.writelines(lines)
        self.fopen.close()
        self.textwindow.close()
        
    def removeProject(self):
        self.indexItem =self.treewidget.currentIndex()
        filename= self.indexItem.data().toString()
        self.filePath= self.indexItem.sibling(self.indexItem.row(), 1).data().toString()
        self.int = self.indexItem.row()
        self.treewidget.takeTopLevelItem(self.int)
        
        if self.obj_appconfig.current_project["ProjectName"] == self.filePath:
            self.obj_appconfig.current_project["ProjectName"] = None 
            
        del self.obj_appconfig.project_explorer[str(self.filePath)]
        json.dump(self.obj_appconfig.project_explorer, open(self.obj_appconfig.dictPath,'w'))
        
    def refreshProject(self):
        self.indexItem =self.treewidget.currentIndex()
        filename= self.indexItem.data().toString()
        self.filePath= str(self.indexItem.sibling(self.indexItem.row(), 1).data().toString())
        filelistnew= os.listdir(os.path.join(self.filePath))
        print filelistnew
        parentnode = self.treewidget.currentItem()
        count = parentnode.childCount()
        for i in range(count):
            for items in self.treewidget.selectedItems():
                items.removeChild(items.child(0))
        for files in filelistnew:
            childnode= QtGui.QTreeWidgetItem(parentnode, [files, self.filePath+ '/'+ files])
        
        self.obj_appconfig.project_explorer[self.filePath]= filelistnew
        json.dump(self.obj_appconfig.project_explorer, open(self.obj_appconfig.dictPath,'w'))