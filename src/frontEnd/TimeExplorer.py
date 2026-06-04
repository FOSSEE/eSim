import os
import re
import shutil
import json
from PyQt5 import QtWidgets

class TimeExplorer(QtWidgets.QWidget):

    if os.name == 'nt':
        user_home = os.path.join('library', 'config')
    else:
        user_home = os.path.expanduser('~')

    current_project = {"ProjectName": None}
    current_project_path = {"ProjectPath": None}

    def __init__(self):
        super(TimeExplorer, self).__init__()

        self.setFixedHeight(200)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.treewidget = QtWidgets.QTreeWidget()
        self.treewidget.setHeaderLabels(["Timeline", ""])
        self.treewidget.setColumnWidth(0, 150)

        self.treewidget.setStyleSheet(" \
            QTreeView { border-radius: 15px; border: 1px \
            solid gray; padding: 5px; width: 200px; height: 150px;  }\
        ")

        self.layout.addWidget(self.treewidget)

        self.button_layout = QtWidgets.QHBoxLayout()
        self.restore = QtWidgets.QPushButton("Restore")
        self.clear = QtWidgets.QPushButton("Clear")
        self.button_layout.addWidget(self.restore)
        self.button_layout.addWidget(self.clear)

        self.layout.addLayout(self.button_layout)

        self.restore.clicked.connect(self.restore_snapshots)
        self.clear.clicked.connect(self.clear_snapshots)

    def add_snapshot(self, file_name, timestamp):
        item = QtWidgets.QTreeWidgetItem([file_name, timestamp])
        self.treewidget.addTopLevelItem(item)

    def load_snapshots(self, project_name):
        self.treewidget.clear()
        snapshot_dir = os.path.join(self.user_home, ".esim", "history", project_name)
        self.current_project["ProjectName"] = project_name
        if not os.path.exists(snapshot_dir):
            return
        pattern = re.compile(r"(.+)\((\d{1,2}\.\d{2} [APM]{2} \d{2}-\d{2}-\d{4})\)$")
        for filename in os.listdir(snapshot_dir):
            match = pattern.match(filename)
            if match:
                file_name = match.group(1)
                timestamp = match.group(2)
                self.add_snapshot(file_name, timestamp)
            else:
                print(f"Skipping unmatched snapshot file: {filename}")

    def load_last_snapshots(self):
        try:
            path = os.path.join(self.user_home, ".esim", "last_project.json")
            with open(path, "r") as f:
                data = json.load(f)
                project_path = data.get("ProjectName", None)
                self.current_project_path["ProjectPath"] = project_path
                if project_path and os.path.exists(project_path):
                    project_name = os.path.basename(project_path)
                    self.current_project["ProjectName"] = project_name
                    self.load_snapshots(project_name)
        except Exception as e:
            print(f"Error loading last snapshots: {e}")

    def clear_snapshots(self):
        selected = self.treewidget.selectedItems()
        project_name = self.current_project["ProjectName"]
        snapshot_dir = os.path.join(self.user_home, ".esim", "history", project_name)

        if selected:
            item = selected[0]
            file_name = item.text(0)
            timestamp = item.text(1)

            snapshot_filename = f"{file_name}({timestamp})"
            snapshot_path = os.path.join(snapshot_dir, snapshot_filename)

            confirm = QtWidgets.QMessageBox.question(
                self, "Confirm Deletion",
                f"Are you sure you want to delete this snapshot?\n\n{file_name}",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )

            if confirm == QtWidgets.QMessageBox.Yes:
                try:
                    os.remove(snapshot_path)
                    self.treewidget.takeTopLevelItem(self.treewidget.indexOfTopLevelItem(item))
                except Exception as e:
                    QtWidgets.QMessageBox.warning(self, "Error", f"Could not delete snapshot:\n{e}")
        else:
            confirm = QtWidgets.QMessageBox.question(
                self, "Clear All Snapshots",
                f"No file selected.\nDo you want to delete ALL snapshots for '{project_name}'?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            if confirm == QtWidgets.QMessageBox.Yes:
                deleted = 0
                for filename in os.listdir(snapshot_dir):
                    path = os.path.join(snapshot_dir, filename)
                    try:
                        os.remove(path)
                        deleted += 1
                    except Exception as e:
                        print(f"Error deleting {filename}: {e}")
                self.treewidget.clear()
                QtWidgets.QMessageBox.information(self, "Deleted", f"{deleted} snapshots deleted.")

    def restore_snapshots(self):
        selected_items = self.treewidget.selectedItems()

        project_name = self.current_project["ProjectName"]
        snapshot_dir = os.path.join(self.user_home, ".esim", "history", project_name)

        if not os.path.exists(snapshot_dir):
            QtWidgets.QMessageBox.warning(self, "No Snapshots", "No snapshots found for this project.")
            return

        if selected_items:
            item = selected_items[0]
            file_name = item.text(0)  
            timestamp = item.text(1)  

            snapshot_filename = f"{file_name}({timestamp})"
            snapshot_path = os.path.join(snapshot_dir, snapshot_filename)
            destination_path = os.path.join(self.current_project_path["ProjectPath"], file_name)

            confirm = QtWidgets.QMessageBox.question(
                self, "Confirm Restore",
                f"Do you want to restore this snapshot?\n\n{file_name}",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )

            if confirm == QtWidgets.QMessageBox.Yes:
                try:
                    if os.path.exists(destination_path):
                        os.remove(destination_path)
                    shutil.copy2(snapshot_path, destination_path)
                    if os.path.exists(snapshot_path):
                        os.remove(snapshot_path)
                    self.treewidget.takeTopLevelItem(self.treewidget.indexOfTopLevelItem(item))
                    QtWidgets.QMessageBox.information(self, "Restored", f"{file_name} has been restored.")
                except Exception as e:
                    QtWidgets.QMessageBox.warning(self, "Error", f"Could not restore:\n{e}")

        else:
            confirm = QtWidgets.QMessageBox.question(
                self, "Restore All Snapshots",
                "No file selected.\nDo you want to restore ALL snapshot files?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            if confirm == QtWidgets.QMessageBox.Yes:
                restored = 0
                for filename in os.listdir(snapshot_dir):
                    match = re.match(r"(.+)\((\d{1,2}\.\d{2} [APM]{2} \d{2}-\d{2}-\d{4})\)$", filename)
                    if match:
                        file_base = match.group(1)
                        snapshot_path = os.path.join(snapshot_dir, filename)
                        destination_path = os.path.join(self.current_project_path["ProjectPath"], file_base)

                        try:
                            if os.path.exists(destination_path):
                                os.remove(destination_path)
                            shutil.copy2(snapshot_path, destination_path)
                            if os.path.exists(snapshot_path):
                                os.remove(snapshot_path)
                            restored += 1
                        except Exception as e:
                            print(f"Could not restore {file_base}: {e}")

                self.treewidget.clear()

                QtWidgets.QMessageBox.information(self, "Restored", f"{restored} snapshot(s) restored.")