from PyQt5 import QtCore, QtWidgets
import os
import json
from configuration.Appconfig import Appconfig
from projManagement.Validation import Validation


# This is main class for Project Explorer Area.
class ProjectExplorer(QtWidgets.QWidget):
    """
    This class contains function:

        - One work as a constructor(__init__).
        - For saving data.
        - for renaming project.
        - for refreshing project.
        - for removing project.
    """

    def __init__(self):
        """
        This method is doing following tasks:
            - Working as a constructor for class ProjectExplorer.
            - view of project explorer area.
        """
        QtWidgets.QWidget.__init__(self)
        self.obj_appconfig = Appconfig()
        self.obj_validation = Validation()
        self.treewidget = QtWidgets.QTreeWidget()
        self.window = QtWidgets.QVBoxLayout()
        header = QtWidgets.QTreeWidgetItem(["Projects", "path"])
        self.treewidget.setHeaderItem(header)
        self.treewidget.setColumnHidden(1, True)

        # CSS
        init_path = '../../'
        if os.name == 'nt':
            init_path = ''

        self.treewidget.setStyleSheet(" \
            QTreeView { border-radius: 15px; border: 1px \
            solid gray; padding: 5px; width: 200px; height: 150px;  }\
            QTreeView::branch:has-siblings:!adjoins-item { \
            border-image: url(" + init_path + "images/vline.png) 0;} \
            QTreeView::branch:has-siblings:adjoins-item { \
            border-image: url(" + init_path + "images/branch-more.png) 0; } \
            QTreeView::branch:!has-children:!has-siblings:adjoins-item { \
            border-image: url(" + init_path + "images/branch-end.png) 0; } \
            QTreeView::branch:has-children:!has-siblings:closed, \
            QTreeView::branch:closed:has-children:has-siblings { \
            border-image: none; \
            image: url(" + init_path + "images/branch-closed.png); } \
            QTreeView::branch:open:has-children:!has-siblings, \
            QTreeView::branch:open:has-children:has-siblings  { \
            border-image: none; \
            image: url(" + init_path + "images/branch-open.png); } \
        ")

        for parents, children in list(
                self.obj_appconfig.project_explorer.items()):
            os.path.join(parents)
            if os.path.exists(parents):
                pathlist = parents.split(os.sep)
                parentnode = QtWidgets.QTreeWidgetItem(
                    self.treewidget, [pathlist[-1], parents]
                )
                for files in children:
                    QtWidgets.QTreeWidgetItem(
                        parentnode, [files, os.path.join(parents, files)]
                    )
        self.window.addWidget(self.treewidget)
        self.treewidget.expanded.connect(self.refreshInstant)
        self.treewidget.doubleClicked.connect(self.openProject)
        self.treewidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treewidget.customContextMenuRequested.connect(self.openMenu)
        self.setLayout(self.window)
        self.show()

    def refreshInstant(self):
        for i in range(self.treewidget.topLevelItemCount()):
            if self.treewidget.topLevelItem(i).isExpanded():
                index = self.treewidget.indexFromItem(
                    self.treewidget.topLevelItem(i))
                self.refreshProject(indexItem=index)

    def addTreeNode(self, parents, children):
        os.path.join(parents)
        pathlist = parents.split(os.sep)
        parentnode = QtWidgets.QTreeWidgetItem(
            self.treewidget, [pathlist[-1], parents]
        )
        for files in children:
            QtWidgets.QTreeWidgetItem(
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

        menu = QtWidgets.QMenu()
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
            self.indexItem.sibling(self.indexItem.row(), 1).data()
        )

        if (os.path.isfile(str(self.filePath))):
            self.fopen = open(str(self.filePath), 'r')
            lines = self.fopen.read()

            self.textwindow = QtWidgets.QWidget()
            self.textwindow.setMinimumSize(600, 500)
            self.textwindow.setGeometry(QtCore.QRect(400, 150, 400, 400))
            self.textwindow.setWindowTitle(filename)

            self.text = QtWidgets.QTextEdit()
            self.save = QtWidgets.QPushButton('Save and Exit')
            self.save.setDisabled(True)

            self.text.setText(lines)
            self.text.textChanged.connect(self.enable_save)

            vbox_main = QtWidgets.QVBoxLayout(self.textwindow)
            vbox_main.addWidget(self.text)
            vbox_main.addWidget(self.save)
            self.save.clicked.connect(self.save_data)

            self.textwindow.show()
        else:
            self.refreshProject(self.filePath)

            self.obj_appconfig.print_info(
                'The current project is: ' + self.filePath
            )

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

    def enable_save(self):
        """This function enables save button option."""
        self.save.setEnabled(True)

    def save_data(self):
        """
        This function saves data before it closes the given file.
        It first opens file in write-mode, write operation is performed, \
        closes that file and then it closes window.
        """
        self.fopen = open(self.filePath, 'w')
        self.fopen.write(self.text.toPlainText())
        self.fopen.close()
        self.textwindow.close()

    def removeProject(self):
        """
        This function removes the project in explorer area by right \
        clicking on project and selecting remove option.
        """
        self.indexItem = self.treewidget.currentIndex()
        filePath = str(
            self.indexItem.sibling(self.indexItem.row(), 1).data()
        )
        self.int = self.indexItem.row()
        self.treewidget.takeTopLevelItem(self.int)

        if self.obj_appconfig.current_project["ProjectName"] == filePath:
            self.obj_appconfig.current_project["ProjectName"] = None

        del self.obj_appconfig.project_explorer[filePath]
        json.dump(self.obj_appconfig.project_explorer,
                  open(self.obj_appconfig.dictPath["path"], 'w'))

    def refreshProject(self, filePath=None, indexItem=None):
        """
        This function refresh the project in explorer area by right \
        clicking on project and selecting refresh option.
        """

        if not filePath or filePath is None:
            if indexItem is None:
                self.indexItem = self.treewidget.currentIndex()
            else:
                self.indexItem = indexItem

            filePath = str(
                self.indexItem.sibling(self.indexItem.row(), 1).data()
            )

        if os.path.exists(filePath):
            filelistnew = os.listdir(os.path.join(filePath))
            if indexItem is None:
                parentnode = self.treewidget.currentItem()
            else:
                parentnode = self.treewidget.itemFromIndex(self.indexItem)
            count = parentnode.childCount()
            for i in range(count):
                parentnode.removeChild(parentnode.child(0))
            for files in filelistnew:
                QtWidgets.QTreeWidgetItem(
                    parentnode, [files, os.path.join(filePath, files)]
                )

            self.obj_appconfig.project_explorer[filePath] = filelistnew
            json.dump(self.obj_appconfig.project_explorer,
                      open(self.obj_appconfig.dictPath["path"], 'w'))
            return True

        else:
            print("Selected project not found")
            print("==================")
            msg = QtWidgets.QErrorMessage(self)
            msg.setModal(True)
            msg.setWindowTitle("Error Message")
            msg.showMessage('Selected project does not exist.')
            msg.exec_()
            return False

    def renameProject(self):
        """
        This function renames the project present in project explorer area.
        It validates first:

            - If project names is not empty.
            - Project name does not contain spaces between them.
            - Project name is different between what it was earlier.
            - Project name should not exist.

        After project name is changed, it recreates the project explorer tree.
        """
        self.indexItem = self.treewidget.currentIndex()
        self.baseFileName = str(self.indexItem.data())
        filePath = str(
                    self.indexItem.sibling(self.indexItem.row(), 1).data()
                )

        newBaseFileName, ok = QtWidgets.QInputDialog.getText(
            self, 'Rename Project', 'Project Name:',
            QtWidgets.QLineEdit.Normal, self.baseFileName
        )

        if ok and newBaseFileName:
            newBaseFileName = str(newBaseFileName)

            if not newBaseFileName.strip():
                print("Project name cannot be empty")
                print("==================")
                msg = QtWidgets.QErrorMessage(self)
                msg.setModal(True)
                msg.setWindowTitle("Error Message")
                msg.showMessage('The project name cannot be empty')
                msg.exec_()

            elif self.baseFileName == newBaseFileName:
                print("Project name has to be different")
                print("==================")
                msg = QtWidgets.QErrorMessage(self)
                msg.setModal(True)
                msg.setWindowTitle("Error Message")
                msg.showMessage('The project name has to be different')
                msg.exec_()

            elif self.refreshProject(filePath):

                projectPath = None
                projectFiles = None

                for parents, children in list(
                        self.obj_appconfig.project_explorer.items()):
                    if filePath == parents:
                        if os.path.exists(parents):
                            projectPath, projectFiles = parents, children
                        break

                self.workspace = \
                    self.obj_appconfig.default_workspace['workspace']
                newBaseFileName = str(newBaseFileName).rstrip().lstrip()
                projDir = os.path.join(self.workspace, str(newBaseFileName))

                reply = self.obj_validation.validateNewproj(str(projDir))

                if not (projectPath and projectFiles):
                    print("Selected project not found")
                    print("Project Path :", projectPath)
                    print("Project Files :", projectFiles)
                    print("==================")
                    msg = QtWidgets.QErrorMessage(self)
                    msg.setModal(True)
                    msg.setWindowTitle("Error Message")
                    msg.showMessage('Selected project does not exist.')
                    msg.exec_()

                elif reply == "VALID":
                    # rename project folder
                    updatedProjectFiles = []

                    updatedProjectPath = newBaseFileName.join(
                        projectPath.rsplit(self.baseFileName, 1))
                    print("Renaming " + projectPath + " to " +
                          updatedProjectPath)

                    # rename project folder
                    try:
                        os.rename(projectPath, updatedProjectPath)
                    except BaseException as e:
                        msg = QtWidgets.QErrorMessage(self)
                        msg.setModal(True)
                        msg.setWindowTitle("Error Message")
                        msg.showMessage(str(e))
                        msg.exec_()
                        return

                    # rename files matching project name
                    try:
                        for projectFile in projectFiles:
                            if self.baseFileName in projectFile:
                                oldFilePath = os.path.join(updatedProjectPath,
                                                           projectFile)
                                projectFile = projectFile.replace(
                                    self.baseFileName, newBaseFileName, 1)
                                newFilePath = os.path.join(
                                    updatedProjectPath, projectFile)
                                print("Renaming " + oldFilePath + " to " +
                                      newFilePath)
                                os.rename(oldFilePath, newFilePath)
                                updatedProjectFiles.append(projectFile)

                    except BaseException as e:
                        print("==================")
                        print("Error! Revert renaming project")

                        # Revert updatedProjectFiles
                        for projectFile in updatedProjectFiles:
                            newFilePath = os.path.join(
                                            updatedProjectPath, projectFile)
                            projectFile = projectFile.replace(
                                    newBaseFileName, self.baseFileName, 1)
                            oldFilePath = os.path.join(
                                    updatedProjectPath, projectFile)
                            os.rename(newFilePath, oldFilePath)

                        # Revert project folder name
                        os.rename(updatedProjectPath, projectPath)
                        print("==================")
                        msg = QtWidgets.QErrorMessage(self)
                        msg.setModal(True)
                        msg.setWindowTitle("Error Message")
                        msg.showMessage(str(e))
                        msg.exec_()
                        return

                    # update project_explorer dictionary
                    del self.obj_appconfig.project_explorer[projectPath]
                    self.obj_appconfig.project_explorer[updatedProjectPath] = \
                        updatedProjectFiles

                    # save project_explorer dictionary on disk
                    json.dump(self.obj_appconfig.project_explorer, open(
                        self.obj_appconfig.dictPath["path"], 'w'))

                    # recreate project explorer tree
                    self.treewidget.clear()
                    for parent, children in \
                            self.obj_appconfig.project_explorer.items():
                        if os.path.exists(parent):
                            self.addTreeNode(parent, children)

                elif reply == "CHECKEXIST":
                    print("Project name already exists.")
                    print("==========================")
                    msg = QtWidgets.QErrorMessage(self)
                    msg.setModal(True)
                    msg.setWindowTitle("Error Message")
                    msg.showMessage(
                        'The project "' + newBaseFileName +
                        '" already exist. Please select a different name or' +
                        ' delete existing project'
                    )
                    msg.exec_()

                elif reply == "CHECKNAME":
                    print("Name can not contain space between them")
                    print("===========================")
                    msg = QtWidgets.QErrorMessage(self)
                    msg.setModal(True)
                    msg.setWindowTitle("Error Message")
                    msg.showMessage(
                        'The project name should not ' +
                        'contain space between them'
                    )
                    msg.exec_()
