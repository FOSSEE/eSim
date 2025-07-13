from PyQt5 import QtCore, QtWidgets
import os
import json
import shutil
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
            deletepermanent = menu.addAction(self.tr("Delete Project"))
            deletepermanent.triggered.connect(self.deleteProject)
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





    def deleteProject(self):
        """
        This function deletes the project folder from disk (either to trash or permanently) and updates the explorer.
        """
        print("=" * 60)
        print("DEBUG: deleteProject method called")
        print("=" * 60)
        
        from PyQt5.QtWidgets import QMessageBox
        try:
            import send2trash
            has_send2trash = True
            print("DEBUG: send2trash import successful")
        except ImportError as e:
            has_send2trash = False
            print(f"DEBUG: send2trash import failed: {e}")
        
        self.indexItem = self.treewidget.currentIndex()
        filePath = str(
            self.indexItem.sibling(self.indexItem.row(), 1).data()
        )
        projectName = str(self.indexItem.data())
        
        print(f"DEBUG: Project name: {projectName}")
        print(f"DEBUG: Project path: {filePath}")
        print(f"DEBUG: Project exists: {os.path.exists(filePath)}")
        print(f"DEBUG: Project is directory: {os.path.isdir(filePath)}")
        if os.path.exists(filePath):
            print(f"DEBUG: Project permissions: {oct(os.stat(filePath).st_mode)[-3:]}")
            print(f"DEBUG: Project absolute path: {os.path.abspath(filePath)}")
        else:
            print("DEBUG: Project does not exist!")
        
        if not os.path.exists(filePath):
            print("DEBUG: ERROR - Project does not exist, showing error message")
            msg = QtWidgets.QErrorMessage(self)
            msg.setModal(True)
            msg.setWindowTitle("Error Message")
            msg.showMessage('Selected project does not exist.')
            msg.exec_()
            return
        
        # Ask user for confirmation and method
        print("DEBUG: Showing delete confirmation dialog")
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Delete Project")
        msgBox.setText(f"Do you want to delete the project '{projectName}'?\nThis will remove the project folder from disk.")
        trashBtn = msgBox.addButton("Send to Trash", QMessageBox.AcceptRole)
        permBtn = msgBox.addButton("Delete Permanently", QMessageBox.DestructiveRole)
        cancelBtn = msgBox.addButton(QMessageBox.Cancel)
        msgBox.setDefaultButton(cancelBtn)
        msgBox.exec_()
        
        clicked_button = msgBox.clickedButton()
        print(f"DEBUG: User clicked: {clicked_button.text() if clicked_button else 'None'}")
        
        if clicked_button == cancelBtn:
            print("DEBUG: User cancelled deletion")
            return
        
        try:
            if clicked_button == trashBtn and has_send2trash:
                print(f"DEBUG: Attempting to send to trash: {filePath}")
                print(f"DEBUG: Project exists before send2trash: {os.path.exists(filePath)}")
                
                # Check trash before
                trash_path = os.path.expanduser("~/.local/share/Trash/files/")
                if os.path.exists(trash_path):
                    trash_before = os.listdir(trash_path)
                    print(f"DEBUG: Trash contents before: {trash_before}")
                
                send2trash.send2trash(filePath)
                print(f"DEBUG: send2trash completed successfully")
                print(f"DEBUG: Project exists after send2trash: {os.path.exists(filePath)}")
                
                # Check trash after
                if os.path.exists(trash_path):
                    trash_after = os.listdir(trash_path)
                    print(f"DEBUG: Trash contents after: {trash_after}")
                    
                    # Find what was added
                    new_items = [item for item in trash_after if item not in trash_before]
                    print(f"DEBUG: New items in trash: {new_items}")
                
            elif clicked_button == permBtn or not has_send2trash:
                print(f"DEBUG: Attempting permanent delete: {filePath}")
                shutil.rmtree(filePath)
                print(f"DEBUG: Permanent delete completed")
            else:
                print("DEBUG: No valid delete option selected")
                return
                
        except Exception as e:
            print(f"DEBUG: ERROR during deletion: {e}")
            print(f"DEBUG: Exception type: {type(e)}")
            import traceback
            print(f"DEBUG: Traceback: {traceback.format_exc()}")
            
            err = QtWidgets.QErrorMessage(self)
            err.setModal(True)
            err.setWindowTitle("Error Message")
            err.showMessage(f"Failed to delete project: {e}")
            err.exec_()
            return
        
        # Remove from explorer and config
        print("DEBUG: Removing project from UI and config")
        self.int = self.indexItem.row()
        self.treewidget.takeTopLevelItem(self.int)
        if self.obj_appconfig.current_project["ProjectName"] == filePath:
            self.obj_appconfig.current_project["ProjectName"] = None
        if filePath in self.obj_appconfig.project_explorer:
            del self.obj_appconfig.project_explorer[filePath]
            json.dump(self.obj_appconfig.project_explorer,
                      open(self.obj_appconfig.dictPath["path"], 'w'))
        
        # Info message
        print("DEBUG: Showing success message")
        info = QMessageBox(self)
        info.setWindowTitle("Project Deleted")
        info.setText(f"Project '{projectName}' has been deleted.")
        info.exec_()
        
        # Final debug: Check if project is in trash
        if clicked_button == trashBtn and has_send2trash:
            print("DEBUG: Final verification - checking trash")
            trash_path = os.path.expanduser("~/.local/share/Trash/files/")
            if os.path.exists(trash_path):
                trash_files = os.listdir(trash_path)
                project_name = os.path.basename(filePath)
                print(f"DEBUG: Looking for project in trash: {project_name}")
                print(f"DEBUG: All files in trash: {trash_files}")
                if project_name in trash_files:
                    print(f"DEBUG: ✓ SUCCESS - Project found in trash")
                    
                    # Check project contents in trash
                    trash_project_path = os.path.join(trash_path, project_name)
                    if os.path.exists(trash_project_path):
                        trash_contents = os.listdir(trash_project_path)
                        print(f"DEBUG: Project contents in trash: {trash_contents}")
                    else:
                        print(f"DEBUG: ✗ Project directory not accessible in trash")
                else:
                    print(f"DEBUG: ✗ FAILURE - Project NOT found in trash")
                    print(f"DEBUG: Available in trash: {trash_files}")
            else:
                print(f"DEBUG: ✗ Trash directory does not exist: {trash_path}")
        
        print("DEBUG: deleteProject method completed")
        print("=" * 60)

    def apply_dark_theme(self):
        """Apply dark theme to the project explorer"""
        pass
    
    def apply_light_theme(self):
        """Apply light theme to the project explorer"""
        pass
    
    def set_theme(self, is_dark):
        """Set the theme for the project explorer"""
        pass

    def selectProjectNode(self, projectName):
        """Select a project node in the tree widget"""
        for i in range(self.treewidget.topLevelItemCount()):
            item = self.treewidget.topLevelItem(i)
            if item.text(0) == projectName:
                self.treewidget.setCurrentItem(item)
                self.treewidget.scrollToItem(item)
                break
