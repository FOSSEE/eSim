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

    projectOpened = QtCore.pyqtSignal(str, str, list)

    def __init__(self, is_dark_theme=False):
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
        
        # Initialize with the correct theme
        self.set_theme(is_dark_theme)
        
        for parents, children in list(
                self.obj_appconfig.project_explorer.items()):
            os.path.join(parents)
            if os.path.exists(parents):
                pathlist = parents.split(os.sep)
                QtWidgets.QTreeWidgetItem(
                    self.treewidget, [pathlist[-1], parents]
                )

        self.window.addWidget(self.treewidget)
        self.treewidget.expanded.connect(self.refreshInstant)
        self.treewidget.itemClicked.connect(self.handleItemClicked)
        self.treewidget.itemDoubleClicked.connect(self.handleItemDoubleClicked)
        self.treewidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treewidget.customContextMenuRequested.connect(self.openMenu)
        self.setLayout(self.window)
        self.show()

    def set_theme(self, is_dark):
        """Sets the theme for the widget."""
        if is_dark:
            self.apply_dark_theme()
        else:
            self.apply_light_theme()

    def apply_dark_theme(self):
        """Apply dark theme to the project explorer"""
        # Set the main widget background to match Application.py
        self.setStyleSheet('''
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #23273a, stop:1 #181b24);
                color: #e8eaed;
            }
        ''')
        # Set the tree widget styles to match Application.py
        self.treewidget.setStyleSheet('''
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #23273a, stop:1 #181b24);
                color: #40c4ff;
                font-weight: 700;
                font-size: 12px;
                border: none;
                border-radius: 0;
                padding: 8px 0px 8px 12px;
                letter-spacing: 0.5px;
            }
            QTreeWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #23273a, stop:1 #181b24);
                color: #e8eaed;
                border: 1px solid #23273a;
                border-radius: 12px;
                selection-background-color: #40c4ff;
                selection-color: #181b24;
                font-weight: 500;
                font-size: 10px;
                padding: 6px;
            }
            QTreeWidget::item {
                padding: 4px;
                border-radius: 4px;
                margin: 1px 0px;
                background: transparent;
                font-size: 10px;
            }
            QTreeWidget::item:hover {
                background: #2d3348;
                color: #40c4ff;
            }
            QTreeWidget::item:selected {
                background: #40c4ff;
                color: #181b24;
                font-weight: 600;
            }
            QTreeView::branch {
                background: transparent;
                width: 12px;
            }
            QTreeView::branch:has-children:!has-siblings:closed,
            QTreeView::branch:closed:has-children:has-siblings {
                image: url(images/branch-closed.png);
            }
            QTreeView::branch:open:has-children:!has-siblings,
            QTreeView::branch:open:has-children:has-siblings {
                image: url(images/branch-open.png);
            }
            QScrollBar:vertical {
                background: #23273a;
                width: 10px;
                margin: 0;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #40c4ff;
                min-height: 20px;
                border-radius: 5px;
                margin: 1px;
            }
            QScrollBar::handle:vertical:hover {
                background: #1976d2;
            }
            QScrollBar::add-line, QScrollBar::sub-line {
                background: none;
                border: none;
            }
        ''')

    def apply_light_theme(self):
        """Apply light theme to the project explorer"""
        # Set the main widget background
        self.setStyleSheet('''
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f8f9fa);
                color: #2c3e50;
            }
        ''')
        
        # Set the tree widget styles
        self.treewidget.setStyleSheet('''
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ffffff, stop:1 #f8f9fa);
                color: #1976d2;
                font-weight: 700;
                font-size: 12px;
                border: none;
                border-radius: 0;
                padding: 8px 0px 8px 12px;
                letter-spacing: 0.5px;
            }
            QTreeWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f8f9fa);
                color: #2c3e50;
                border: 1px solid #e1e4e8;
                border-radius: 12px;
                selection-background-color: #1976d2;
                selection-color: #ffffff;
                font-weight: 500;
                font-size: 10px;
                padding: 6px;
            }
            QTreeWidget::item {
                padding: 4px;
                border-radius: 4px;
                margin: 1px 0px;
                background: transparent;
                font-size: 10px;
            }
            QTreeWidget::item:hover {
                background: #f1f4f9;
                color: #1976d2;
            }
            QTreeWidget::item:selected {
                background: #1976d2;
                color: #ffffff;
                font-weight: 600;
            }
            QTreeView::branch {
                background: transparent;
                width: 12px;
            }
            QTreeView::branch:has-children:!has-siblings:closed,
            QTreeView::branch:closed:has-children:has-siblings {
                image: url(images/branch-closed.png);
            }
            QTreeView::branch:open:has-children:!has-siblings,
            QTreeView::branch:open:has-children:has-siblings {
                image: url(images/branch-open.png);
            }
            QScrollBar:vertical {
                background: #f1f4f9;
                width: 10px;
                margin: 0;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #1976d2;
                min-height: 20px;
                border-radius: 5px;
                margin: 1px;
            }
            QScrollBar::handle:vertical:hover {
                background: #1565c0;
            }
            QScrollBar::add-line, QScrollBar::sub-line {
                background: none;
                border: none;
            }
        ''')

    def refreshInstant(self):
        # Disabled: Do not repopulate file nodes under projects
        pass

    def addTreeNode(self, parents, children):
        os.path.join(parents)
        pathlist = parents.split(os.sep)
        QtWidgets.QTreeWidgetItem(
            self.treewidget, [pathlist[-1], parents]
        )
        # Do NOT add file children

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

            # Apply dark theme and custom scrollbar
            premium_dark_stylesheet = """
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0a0e1a, stop:0.3 #1a1d29, stop:0.7 #1e2124, stop:1 #0f1419);
                color: #e8eaed;
                font-family: 'Fira Sans', 'Inter', 'Segoe UI', 'Roboto', 'Arial', sans-serif;
                font-size: 15px;
                font-weight: 500;
            }
            QTextEdit {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #23273a, stop:1 #181b24);
                color: #e8eaed;
                border: 1px solid #23273a;
                border-radius: 10px;
                padding: 16px 20px;
                font-weight: 500;
                font-size: 15px;
                selection-background-color: #40c4ff;
                selection-color: #181b24;
            }
            QScrollBar:vertical, QScrollBar:horizontal {
                background: #23273a;
                border-radius: 6px;
                margin: 0;
            }
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background: #40c4ff;
                border-radius: 6px;
                min-height: 30px;
                min-width: 30px;
                margin: 2px;
            }
            QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {
                background: #1976d2;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #40c4ff, stop:1 #1976d2);
                color: #181b24;
                border: 1px solid #40c4ff;
                padding: 12px 24px;
                border-radius: 10px;
                font-weight: 700;
                font-size: 15px;
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background: #1976d2;
                color: #fff;
                border: 1.5px solid #1976d2;
            }
            QPushButton:pressed {
                background: #23273a;
                color: #40c4ff;
                border: 1.5px solid #40c4ff;
            }
            """
            self.textwindow.setStyleSheet(premium_dark_stylesheet)

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
            projectName = os.path.basename(self.filePath)
            files = [f for f in os.listdir(self.filePath) if os.path.isfile(os.path.join(self.filePath, f))]
            self.projectOpened.emit(projectName, self.filePath, files)
            self.obj_appconfig.print_info(
                'The current project is: ' + self.filePath
            )

            self.obj_appconfig.current_project["ProjectName"] = self.filePath
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
            # Disabled: Do not add file nodes under project
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

    def handleItemClicked(self, item, column):
        # If the clicked item is a project (has children), open in tabs
        if item.childCount() > 0:
            projectName = item.text(0)
            projectPath = item.text(1)
            files = [item.child(i).text(0) for i in range(item.childCount())]
            self.projectOpened.emit(projectName, projectPath, files)
        else:
            # If it's a file, use the old behavior
            self.openProject()

    def handleItemDoubleClicked(self, item, column):
        # Only open a new window for editing if it's a file (no children)
        if item.childCount() == 0:
            filePath = item.text(1)
            if os.path.isfile(filePath):
                try:
                    with open(filePath, 'r', errors='ignore') as f:
                        content = f.read()
                except Exception as e:
                    QtWidgets.QMessageBox.warning(self, "Error", f"Could not open file: {e}")
                    return

                editorWindow = QtWidgets.QWidget()
                editorWindow.setWindowTitle(os.path.basename(filePath))
                editorWindow.setMinimumSize(600, 500)
                layout = QtWidgets.QVBoxLayout(editorWindow)
                textEdit = QtWidgets.QTextEdit()
                textEdit.setText(content)
                saveButton = QtWidgets.QPushButton('Save and Exit')
                layout.addWidget(textEdit)
                layout.addWidget(saveButton)

                def save_and_exit():
                    try:
                        with open(filePath, 'w') as f:
                            f.write(textEdit.toPlainText())
                        editorWindow.close()
                    except Exception as e:
                        QtWidgets.QMessageBox.warning(editorWindow, "Error", f"Could not save file: {e}")

                saveButton.clicked.connect(save_and_exit)
                editorWindow.show()

    def selectProjectNode(self, projectName):
        for i in range(self.treewidget.topLevelItemCount()):
            item = self.treewidget.topLevelItem(i)
            if item.text(0) == projectName:
                self.treewidget.setCurrentItem(item)
                self.treewidget.scrollToItem(item)
                break
