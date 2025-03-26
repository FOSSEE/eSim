import sys
import subprocess
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QMessageBox
from PyQt5.QtCore import Qt

class KiCadUpdaterGUI(QWidget):
    def __init__(self, main_gui):
        super().__init__()
        self.main_gui = main_gui
        self.package_name = "KiCad"
        self.versions = ["7.0.11", "8.0.9"]
        self.script_path = "./update-kicad-final.sh"
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()

        self.title_label = QLabel("KiCad Updater", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; padding: 10px 0;")
        layout.addWidget(self.title_label)

        self.installed_version = self.main_gui.package_versions.get("kicad", "Unknown")
        self.installedLabel = QLabel(f"Installed Version: {self.installed_version}", self)
        self.installedLabel.setStyleSheet("font-size: 14px; padding: 5px 0;")
        layout.addWidget(self.installedLabel)
        
        self.statusLabel = QLabel(self.get_version_status(), self)
        self.statusLabel.setAlignment(Qt.AlignCenter)
        self.statusLabel.setStyleSheet("font-size: 14px; padding: 5px 0;")
        layout.addWidget(self.statusLabel)
        
        self.label = QLabel("Select the KiCad version to update: ", self)
        self.label.setStyleSheet("font-size: 14px; padding: 5px 0;")
        layout.addWidget(self.label)
        
        self.versionCombo = QComboBox(self)
        self.versionCombo.addItems(self.versions)
        self.versionCombo.setStyleSheet("font-size: 14px; padding: 5px 0;")
        layout.addWidget(self.versionCombo)
        
        self.updateButton = QPushButton("Update KiCad", self)
        self.updateButton.clicked.connect(self.runUpdater)
        self.updateButton.setStyleSheet("font-size: 14px; padding: 5px 0;")
        layout.addWidget(self.updateButton)
        
        self.setLayout(layout)
        self.setWindowTitle("KiCad Updater")
        self.setGeometry(100, 100, 400, 300)
    
    def get_version_status(self):
        latest_version = "8.0.8"
        if self.installed_version == "8.0.9-0~ubuntu20.04.1":
            color = "green"
            text = "You are using the latest version."
        else:
            color = "red"
            text = "Please Update. Your Package is out of date."
        
        return f'<span style="color:{color}; font-size:14px;">{text}</span>'
    
    def runUpdater(self):
        if self.installed_version == "8.0.8-0~ubuntu20.04.1":
            QMessageBox.information(self, "Info", "You are using the latest version.")
            return
        
        selected_version = self.versionCombo.currentText()
        try:
            subprocess.run(["bash", self.script_path, selected_version], check=True, text=True)
            QMessageBox.information(self, "Success", f"KiCad {selected_version} installation started.")
            self.main_gui.reload_versions()
            self.installed_version = self.main_gui.package_versions.get("kicad", "Unknown")
            self.installedLabel.setText(f"Installed Version: {self.installed_version}")
            self.statusLabel.setText(self.get_version_status())
        except subprocess.CalledProcessError:
            QMessageBox.critical(self, "Error", "Failed to execute the installation script.")

class GHDLUpdaterGUI(QWidget):
    def __init__(self, main_gui):
        super().__init__()
        self.main_gui = main_gui
        self.package_name = "GHDL"
        self.versions = ["3.0.0", "4.0.0", "4.1.0", "nightly"]
        self.script_path = "./nghdl/update-ghdl-with-dependency.sh"
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()

        self.title_label = QLabel("GHDL Updater", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; padding: 10px 0;")
        layout.addWidget(self.title_label)

        self.installed_version = self.main_gui.package_versions.get("ghdl", "Unknown")
        self.installedLabel = QLabel(f"Installed Version: {self.installed_version}", self)
        self.installedLabel.setStyleSheet("font-size: 14px; padding: 5px 0;")
        layout.addWidget(self.installedLabel)
        
        self.statusLabel = QLabel(self.get_version_status(), self)
        self.statusLabel.setAlignment(Qt.AlignCenter)
        self.statusLabel.setStyleSheet("font-size: 14px; padding: 5px 0;")
        layout.addWidget(self.statusLabel)
        
        self.label = QLabel("Select the GHDL version to update: ", self)
        self.label.setStyleSheet("font-size: 14px; padding: 5px 0;")
        layout.addWidget(self.label)
        
        self.versionCombo = QComboBox(self)
        self.versionCombo.addItems(self.versions)
        self.versionCombo.setStyleSheet("font-size: 14px; padding: 5px 0;")
        layout.addWidget(self.versionCombo)
        
        self.updateButton = QPushButton("Update GHDL", self)
        self.updateButton.clicked.connect(self.runUpdater)
        self.updateButton.setStyleSheet("font-size: 14px; padding: 5px 0;")
        layout.addWidget(self.updateButton)
        
        self.setLayout(layout)
        self.setWindowTitle("GHDL Updater")
        self.setGeometry(100, 100, 400, 300)
    
    def get_version_status(self):
        latest_version = self.versions[-1]
        if self.installed_version == "Unknown" or self.installed_version != latest_version:
            color = "red"
            text = "Please Update. Your Package is out of date."
        else:
            color = "green"
            text = "You are using the latest version."
        
        return f'<span style="color:{color}; font-size:14px;">{text}</span>'
    
    def runUpdater(self):
        if self.installed_version == "5.0.0-dev":
            QMessageBox.information(self, "Info", "You are using the latest version.")
            return

        selected_version = self.versionCombo.currentText()
        try:
            subprocess.run(["bash", self.script_path, selected_version], check=True, text=True)
            QMessageBox.information(self, "Success", f"GHDL {selected_version} installation started.")
            self.main_gui.reload_versions()
            self.installed_version = self.main_gui.package_versions.get("ghdl", "Unknown")
            self.installedLabel.setText(f"Installed Version: {self.installed_version}")
            self.statusLabel.setText(self.get_version_status())
        except subprocess.CalledProcessError:
            QMessageBox.critical(self, "Error", "Failed to execute the installation script.")

class VerilatorUpdaterGUI(QWidget):
    def __init__(self, main_gui):
        super().__init__()
        self.main_gui = main_gui
        self.package_name = "Verilator"
        self.versions = ["4.228", "5.020", "5.026", "5.030"]
        self.script_path = "./nghdl/update-verilator-final.sh"
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()

        self.title_label = QLabel("Verilator Updater", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; padding: 10px 0;")
        layout.addWidget(self.title_label)

        self.installed_version = self.main_gui.package_versions.get("verilator", "Unknown")
        self.installedLabel = QLabel(f"Installed Version: {self.installed_version}", self)
        self.installedLabel.setStyleSheet("font-size: 14px; padding: 5px 0;")
        layout.addWidget(self.installedLabel)
        
        self.statusLabel = QLabel(self.get_version_status(), self)
        self.statusLabel.setAlignment(Qt.AlignCenter)
        self.statusLabel.setStyleSheet("font-size: 14px; padding: 5px 0;")
        layout.addWidget(self.statusLabel)
        
        self.label = QLabel("Select the Verilator version to update: ", self)
        self.label.setStyleSheet("font-size: 14px; padding: 5px 0;")
        layout.addWidget(self.label)
        
        self.versionCombo = QComboBox(self)
        self.versionCombo.addItems(self.versions)
        self.versionCombo.setStyleSheet("font-size: 14px; padding: 5px 0;")
        layout.addWidget(self.versionCombo)
        
        self.updateButton = QPushButton("Update Verilator", self)
        self.updateButton.clicked.connect(self.runUpdater)
        self.updateButton.setStyleSheet("font-size: 14px; padding: 5px 0;")
        layout.addWidget(self.updateButton)
        
        self.setLayout(layout)
        self.setWindowTitle("Verilator Updater")
        self.setGeometry(100, 100, 400, 300)
    
    def get_version_status(self):
        latest_version = "verilator-5.030"
        if self.installed_version == "Unknown" or self.installed_version != latest_version:
            color = "red"
            text = "Please Update. Your Package is out of date."
        else:
            color = "green"
            text = "You are using the latest version."
        
        return f'<span style="color:{color}; font-size:14px;">{text}</span>'
    
    def runUpdater(self):
        if self.installed_version == "verilator-5.030":
            QMessageBox.information(self, "Info", "You are using the latest version.")
            return

        selected_version = self.versionCombo.currentText()
        try:
            subprocess.run(["bash", self.script_path, selected_version], check=True, text=True)
            QMessageBox.information(self, "Success", f"Verilator {selected_version} installation started.")
            self.main_gui.reload_versions()
            self.installed_version = self.main_gui.package_versions.get("verilator", "Unknown")
            self.installedLabel.setText(f"Installed Version: {self.installed_version}")
            self.statusLabel.setText(self.get_version_status())
        except subprocess.CalledProcessError:
            QMessageBox.critical(self, "Error", "Failed to execute the installation script.")

class NGSpiceUpdaterGUI(QWidget):
    def __init__(self, main_gui):
        super().__init__()
        self.main_gui = main_gui
        self.package_name = "NGSPICE"
        self.versions = ["38", "40", "43"]
        self.script_path = "./nghdl/update-ngspice-final.sh"
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()

        self.title_label = QLabel("NGSPICE Updater", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; padding: 10px 0;")
        layout.addWidget(self.title_label)

        self.installed_version = self.main_gui.package_versions.get("ngspice", "Unknown")
        self.installedLabel = QLabel(f"Installed Version: {self.installed_version}", self)
        self.installedLabel.setStyleSheet("font-size: 14px; padding: 5px 0;")
        layout.addWidget(self.installedLabel)
        
        self.statusLabel = QLabel(self.get_version_status(), self)
        self.statusLabel.setAlignment(Qt.AlignCenter)
        self.statusLabel.setStyleSheet("font-size: 14px; padding: 5px 0;")
        layout.addWidget(self.statusLabel)
        
        self.label = QLabel("Select the NGSPICE version to update: ", self)
        self.label.setStyleSheet("font-size: 14px; padding: 5px 0;")
        layout.addWidget(self.label)
        
        self.versionCombo = QComboBox(self)
        self.versionCombo.addItems(self.versions)
        self.versionCombo.setStyleSheet("font-size: 14px; padding: 5px 0;")
        layout.addWidget(self.versionCombo)
        
        self.updateButton = QPushButton("Update NGSPICE", self)
        self.updateButton.clicked.connect(self.runUpdater)
        self.updateButton.setStyleSheet("font-size: 14px; padding: 5px 0;")
        layout.addWidget(self.updateButton)
        
        self.setLayout(layout)
        self.setWindowTitle("NGSPICE Updater")
        self.setGeometry(100, 100, 400, 300)
    
    def get_version_status(self):
        latest_version = "ngspice-43"
        if self.installed_version == "Unknown" or self.installed_version != latest_version:
            color = "red"
            text = "Please Update. Your Package is out of date."
        else:
            color = "green"
            text = "You are using the latest version."
        
        return f'<span style="color:{color}; font-size:14px;">{text}</span>'
    
    def runUpdater(self):
        if self.installed_version == "43":
            QMessageBox.information(self, "Info", "You are using the latest version.")
            return
        
        selected_version = self.versionCombo.currentText()
        try:
            subprocess.run(["bash", self.script_path, selected_version], check=True, text=True)
            QMessageBox.information(self, "Success", f"NGSPICE {selected_version} installation started.")
            self.main_gui.reload_versions()
            self.installed_version = self.main_gui.package_versions.get("ngspice", "Unknown")
            self.installedLabel.setText(f"Installed Version: {self.installed_version}")
            self.statusLabel.setText(self.get_version_status())
        except subprocess.CalledProcessError:
            QMessageBox.critical(self, "Error", "Failed to execute the installation script.")

class MainGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.files = {
            "Check Packages": "./check-packages-final.sh",
            "Update Dependencies": "./update-dependency-final.sh",
        }
        self.package_versions = self.load_versions()
        self.initUI()
    
    def load_versions(self):
        try:
            with open("information.json", "r") as file:
                data = json.load(file)
                versions = {pkg["package_name"]: pkg["version"] for pkg in data["important_packages"]}
                return versions
        except Exception as e:
            print(f"Error loading versions: {e}")
            return {}
    
    def initUI(self):
        layout = QVBoxLayout()

        self.setWindowTitle("eSim Tool Manager (Updater)")
        # self.setGeometry(-200, -200, 400, 300)
        self.adjust_position()
        
        self.title_label = QLabel("eSim Updater", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px 0;")
        layout.addWidget(self.title_label)

        self.version_label = QLabel("Installed Version", self)
        self.version_label.setStyleSheet("font-size: 16px; padding: 5px 0;")
        layout.addWidget(self.version_label)

        self.version_text_label = QLabel(self.get_version_text(), self)
        self.version_text_label.setStyleSheet("font-size: 16px; padding: 5px 0;")
        layout.addWidget(self.version_text_label)

        self.download_label = QLabel("Please download the packages first.", self)
        self.download_label.setAlignment(Qt.AlignCenter)
        self.download_label.setStyleSheet("font-size: 14px; padding: 15px 0 5px 0;")
        layout.addWidget(self.download_label)

        self.download_button = QPushButton("Download Packages", self)
        self.download_button.setStyleSheet("font-size: 14px; padding: 5px 0;")
        self.download_button.clicked.connect(self.runDownloadPackages)
        layout.addWidget(self.download_button)

        self.update_label = QLabel("Please update the dependencies first.", self)
        self.update_label.setAlignment(Qt.AlignCenter)
        self.update_label.setStyleSheet("font-size: 14px; padding: 15px 0 5px 0;")
        layout.addWidget(self.update_label)

        self.update_button = QPushButton("Update Dependencies", self)
        self.update_button.setStyleSheet("font-size: 14px; padding: 5px 0;")
        self.update_button.clicked.connect(lambda: self.runUpdate(self.files["Update Dependencies"]))
        layout.addWidget(self.update_button)

        self.Updater_label = QLabel("You can update each package from the respective updater.", self)
        self.Updater_label.setAlignment(Qt.AlignCenter)
        self.Updater_label.setStyleSheet("font-size: 14px; padding: 15px 0 5px 0;")
        layout.addWidget(self.Updater_label)

        self.kicad_button = QPushButton("Open KiCad Updater", self)
        self.kicad_button.setStyleSheet("font-size: 14px; padding: 5px 0;")
        self.kicad_button.clicked.connect(self.openKiCad)
        layout.addWidget(self.kicad_button)

        self.ghdl_button = QPushButton("Open GHDL Updater", self)
        self.ghdl_button.setStyleSheet("font-size: 14px; padding: 5px 0;")
        self.ghdl_button.clicked.connect(self.openGHDL)
        layout.addWidget(self.ghdl_button)

        self.verilator_button = QPushButton("Open Verilator Updater", self)
        self.verilator_button.setStyleSheet("font-size: 14px; padding: 5px 0;")
        self.verilator_button.clicked.connect(self.openVerilator)
        layout.addWidget(self.verilator_button)

        self.ngspice_button = QPushButton("Open NGSPICE Updater", self)
        self.ngspice_button.setStyleSheet("font-size: 14px; padding: 5px 0;")
        self.ngspice_button.clicked.connect(self.openNGSpice)
        layout.addWidget(self.ngspice_button)

        self.check_label = QLabel("You can check the packages updated or not alongside with the version in the json file.", self)
        self.check_label.setAlignment(Qt.AlignCenter)
        self.check_label.setStyleSheet("font-size: 14px; padding: 15px 0 5px 0;")
        layout.addWidget(self.check_label)

        self.check_button = QPushButton("Check Packages", self)
        self.check_button.setStyleSheet("font-size: 14px; padding: 5px 0;")
        self.check_button.clicked.connect(lambda: self.runUpdate(self.files["Check Packages"]))
        layout.addWidget(self.check_button)

        self.remove_label = QLabel("Please remove the packages for the storage usage.", self)
        self.remove_label.setAlignment(Qt.AlignCenter)
        self.remove_label.setStyleSheet("font-size: 14px; padding: 15px 0 5px 0;")
        layout.addWidget(self.remove_label)

        self.remove_button = QPushButton("Remove Packages", self)
        self.remove_button.setStyleSheet("font-size: 14px; padding: 5px 0;")
        self.remove_button.clicked.connect(self.runRemovePackages)
        layout.addWidget(self.remove_button)
        
        self.setLayout(layout)
    
    def get_version_text(self):
        return f"KiCad: {self.package_versions.get('kicad', 'Unknown')}\n" \
               f"NGSPICE: {self.package_versions.get('ngspice', 'Unknown')}\n" \
               f"GHDL: {self.package_versions.get('ghdl', 'Unknown')}\n" \
               f"Verilator: {self.package_versions.get('verilator', 'Unknown')}"
    
    def reload_versions(self):
        self.package_versions = self.load_versions()
        self.version_text_label.setText(self.get_version_text())
    
    def runUpdate(self, script):
        subprocess.run(["bash", script], check=True)
    
    def runDownloadPackages(self):
        result = subprocess.run(["bash", "./nghdl/download_packages.sh", "download"], text=True)
        if result.returncode == 0:
            QMessageBox.information(self, "Success", "Downloaded Packages successfully in the nghdl/packages folder.")
        else:
            QMessageBox.critical(self, "Error", "There is some error in downloading packages. You can check in the log.")
    
    def runRemovePackages(self):
        result = subprocess.run(["bash", "./nghdl/download_packages.sh", "remove"], text=True)
        if result.returncode == 0:
            QMessageBox.information(self, "Success", "Removed Packages successfully from the nghdl/packages folder.")
        else:
            QMessageBox.critical(self, "Error", "There is some error in removing packages. You can check in the log.")
    
    def openGHDL(self):
        self.ghdl_window = GHDLUpdaterGUI(self)
        self.ghdl_window.show()
    
    def openKiCad(self):
        self.kicad_window = KiCadUpdaterGUI(self)
        self.kicad_window.show()
    
    def openNGSpice(self):
        self.ngspice_window = NGSpiceUpdaterGUI(self)
        self.ngspice_window.show()
    
    def openVerilator(self):
        self.verilator_window = VerilatorUpdaterGUI(self)
        self.verilator_window.show()

    def center(self):
        screen = QApplication.primaryScreen().availableGeometry().center()
        frame = self.frameGeometry()
        frame.moveCenter(screen)
        self.move(frame.topLeft())

    def adjust_position(self):
        screen = QApplication.desktop().screenGeometry()
        widget = self.geometry()
        x = (screen.width() - widget.width()) // 2
        y = (screen.height() - widget.height()) // 3  # Move up slightly
        self.move(x, y)    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainGUI()
    main_window.show()
    sys.exit(app.exec_())
