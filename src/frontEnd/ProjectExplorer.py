from PyQt4 import QtGui, QtCore
import os
import json
from configuration.Appconfig import Appconfig


# This is main class for Project Explorer Area.
class ProjectExplorer(QtGui.QWidget):
    """
    This class contains function:

        - One work as a constructor(__init__).
        - For saving data.
        - for renaming project.
        - for refreshing project.
        - for removing project.
        - for saving data.
    """

    def __init__(self):
        """
        This method is doing following tasks:
            - Working as a constructor for class ProjectExplorer.
            - view of project explorer area.
        """
        QtGui.QWidget.__init__(self)
        self.obj_appconfig = Appconfig()
        self.treewidget = QtGui.QTreeWidget()
        self.window = QtGui.QVBoxLayout()
        header = QtGui.QTreeWidgetItem(["Projects", "path"])
        self.treewidget.setHeaderItem(header)
        self.treewidget.setColumnHidden(1, True)

        # CSS
        self.treewidget.setStyleSheet(" \
            QTreeView::branch:has-siblings:!adjoins-item { \
            border-image: url(../../images/vline.png) 0;} \
            QTreeView::branch:has-siblings:adjoins-item { \
            border-image: url(../../images/branch-more.png) 0; } \
            QTreeView::branch:!has-children:!has-siblings:adjoins-item { \
            border-image: url(../../images/branch-end.png) 0; } \
            QTreeView::branch:has-children:!has-siblings:closed, \
            QTreeView::branch:closed:has-children:has-siblings { \
            border-image: none; \
            image: url(../../images/branch-closed.png); } \
            QTreeView::branch:open:has-children:!has-siblings, \
            QTreeView::branch:open:has-children:has-siblings  { \
            border-image: none; \
            image: url(../../images/branch-open.png); } \
        ")

        for parents, children in list(
                self.obj_appconfig.project_explorer.items()):
            os.path.join(parents)
            if os.path.exists(parents):
                pathlist = parents.split(os.sep)
                parentnode = QtGui.QTreeWidgetItem(
                    self.treewidget, [pathlist[-1], parents]
                )
                for files in children:
                    QtGui.QTreeWidgetItem(
                        parentnode, [files, os.path.join(parents, files)])
        self.window.addWidget(self.treewidget)

        self.treewidget.doubleClicked.connect(self.openProject)
        self.treewidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treewidget.customContextMenuRequested.connect(self.openMenu)
        self.setLayout(self.window)
        self.show()

    def addTreeNode(self, parents, children):
        os.path.join(parents)
        pathlist = parents.split(os.sep)
        parentnode = QtGui.QTreeWidgetItem(
            self.treewidget, [pathlist[-1], parents])
        for files in children:
            QtGui.QTreeWidgetItem(
                parentnode, [files, os.path.join(parents, files)]
            )

        (
            self.obj_appconfig.
            proc_dict[self.obj_appconfig.current_project['ProjectName']]
        ) = []
        (
            self.obj_appconfig.
            dock_dict[self.obj_appconfig.current_project['ProjectName']]
        ) = []

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
            renameProject = menu.addAction(self.tr("Rename Project"))
            renameProject.triggered.connect(self.renameProject)
            deleteproject = menu.addAction(self.tr("Remove Project"))
            deleteproject.triggered.connect(self.removeProject)
            refreshproject = menu.addAction(self.tr("Refresh"))
            refreshproject.triggered.connect(self.refreshProject)
        elif level == 1:
            openfile = menu.addAction(self.tr("Open"))
            openfile.triggered.connect(self.openProject)

        menu.exec_(self.treewidget.viewport().mapToGlobal(position))

    def openProject(self):
        self.indexItem = self.treewidget.currentIndex()
        filename = str(self.indexItem.data())
        self.filePath = str(
            self.indexItem.sibling(
                self.indexItem.row(),
                1).data())
        self.obj_appconfig.print_info(
            'The current project is ' + self.filePath)

        self.textwindow = QtGui.QWidget()
        self.textwindow.setMinimumSize(600, 500)
        self.textwindow.setGeometry(QtCore.QRect(400, 150, 400, 400))
        self.textwindow.setWindowTitle(filename)

        self.text = QtGui.QTextEdit()
        self.save = QtGui.QPushButton('Save and Exit')
        self.save.setDisabled(True)
        self.windowgrid = QtGui.QGridLayout()
        # if (os.path.isfile(str(self.filePath))) == True:
        if (os.path.isfile(str(self.filePath))):
            self.fopen = open(str(self.filePath), 'r')
            lines = self.fopen.read()
            self.text.setText(lines)

            QtCore.QObject.connect(
                self.text,
                QtCore.SIGNAL("textChanged()"),
                self.enable_save)

            vbox_main = QtGui.QVBoxLayout(self.textwindow)
            vbox_main.addWidget(self.text)
            vbox_main.addWidget(self.save)
            self.save.clicked.connect(self.save_data)
            # self.connect(exit,QtCore.SIGNAL('close()'), self.onQuit)

            self.textwindow.show()
        else:
            self.obj_appconfig.current_project["ProjectName"] = str(
                self.filePath)
            (
                self.obj_appconfig.
                proc_dict[self.obj_appconfig.current_project['ProjectName']]
            ) = []
            if (
                self.obj_appconfig.current_project['ProjectName'] not in
                self.obj_appconfig.dock_dict
            ):
                (
                    self.obj_appconfig.
                    dock_dict[
                        self.obj_appconfig.current_project['ProjectName']]
                ) = []

    # This function is enabling save button option.
    def enable_save(self):
        self.save.setEnabled(True)

    # This function is saving data before it closes the given file.
    def save_data(self):
        """
        This function first opens file in write-mode, when write
        operation is performed it closes that file and then it closes window.
        """
        self.fopen = open(self.filePath, 'w')
        self.fopen.write(self.text.toPlainText())
        self.fopen.close()
        self.textwindow.close()

    # This function removes the project in explorer area by right
    # clicking on project and selecting remove option.
    def removeProject(self):
        """

        """
        self.indexItem = self.treewidget.currentIndex()
        self.filePath = str(
            self.indexItem.sibling(
                self.indexItem.row(),
                1).data())
        self.int = self.indexItem.row()
        self.treewidget.takeTopLevelItem(self.int)

        if self.obj_appconfig.current_project["ProjectName"] == self.filePath:
            self.obj_appconfig.current_project["ProjectName"] = None

        del self.obj_appconfig.project_explorer[str(self.filePath)]
        json.dump(self.obj_appconfig.project_explorer,
                  open(self.obj_appconfig.dictPath, 'w'))

    # This function refresh the project in explorer area by right
    # clicking on project and selecting refresh option.
    def refreshProject(self):
        """ """
        self.indexItem = self.treewidget.currentIndex()
        self.filePath = str(
            self.indexItem.sibling(
                self.indexItem.row(),
                1).data())
        filelistnew = os.listdir(os.path.join(self.filePath))
        parentnode = self.treewidget.currentItem()
        count = parentnode.childCount()
        for i in range(count):
            for items in self.treewidget.selectedItems():
                items.removeChild(items.child(0))
        for files in filelistnew:
            QtGui.QTreeWidgetItem(
                parentnode, [
                    files, os.path.join(
                        self.filePath, files)])

        self.obj_appconfig.project_explorer[self.filePath] = filelistnew
        json.dump(self.obj_appconfig.project_explorer,
                  open(self.obj_appconfig.dictPath, 'w'))

    '''def renameProject(self):
        indexItem = self.treewidget.currentIndex()
        baseFileName = str(indexItem.data())
        newBaseFileName, ok = QtGui.QInputDialog.getText(
            self, 'Rename Project', 'Project Name:',
            QtGui.QLineEdit.Normal, baseFileName
        )
        if ok and newBaseFileName:
            newBaseFileName = str(newBaseFileName)
            projectPath, projectFiles = list(
                self.obj_appconfig.project_explorer.items())[indexItem.row()]
            updatedProjectFiles = []

            # rename files matching project name
            for projectFile in projectFiles:
                if baseFileName in projectFile:
                    oldFilePath = os.path.join(projectPath, projectFile)
                    projectFile = projectFile.replace(
                        baseFileName, newBaseFileName, 1)
                    newFilePath = os.path.join(projectPath, projectFile)
                    print ("Renaming " + oldFilePath + " to " + newFilePath)
                    os.rename(oldFilePath, newFilePath)

                    updatedProjectFiles.append(projectFile)

            # rename project folder
            updatedProjectPath = newBaseFileName.join(
                projectPath.rsplit(baseFileName, 1))
            print ("Renaming " + projectPath + " to " + updatedProjectPath)
            os.rename(projectPath, updatedProjectPath)

            # update project_explorer dictionary
            del self.obj_appconfig.project_explorer[projectPath]
            self.obj_appconfig.project_explorer[updatedProjectPath] = (
                updatedProjectFiles
            )

            # save project_explorer dictionary on disk
            json.dump(self.obj_appconfig.project_explorer,
                      open(self.obj_appconfig.dictPath, 'w'))

            # recreate project explorer tree
            self.treewidget.clear()
            for parent, children in (
                self.obj_appconfig.project_explorer.items()
            ):
                self.addTreeNode(parent, children)
                '''
