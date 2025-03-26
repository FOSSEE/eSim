import os
import sys
import json
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

# Path to the information.json file
INFO_JSON = r"C:\FOSSEE\Tool-Manager\information.json"

def get_version(package_name):
    """Get the installed version of a package from the JSON file."""
    if os.path.exists(INFO_JSON):
        with open(INFO_JSON, "r") as f:
            data = json.load(f)
            for package in data["important_packages"]:
                if package["package_name"] == package_name:
                    return package["version"]
    return "Unknown"

class ToolManagerUpdater(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("eSim Tool Manager (Updater)")

        self.resize(400, 300)
        self.adjust_position()

        layout = QVBoxLayout()

        self.title_label = QLabel("eSim Tool Manager (Updater)", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; padding: 10px 0;")
        layout.addWidget(self.title_label)

        # Fetch versions from the JSON file
        kicad_version = get_version("kicad")
        ngspice_version = get_version("ngspice")
        ghdl_version = get_version("ghdl")
        verilator_version = get_version("verilator")

        # Display installed versions
        self.kicad_version_label = QLabel(f"KiCad Version: {kicad_version}")
        self.kicad_version_label.setStyleSheet("font-size: 14px;")
        self.ngspice_version_label = QLabel(f"Ngspice Version: {ngspice_version}")
        self.ngspice_version_label.setStyleSheet("font-size: 14px;")
        self.ghdl_version_label = QLabel(f"GHDL Version: {ghdl_version}")
        self.ghdl_version_label.setStyleSheet("font-size: 14px;")
        self.verilator_version_label = QLabel(f"Verilator Version: {verilator_version}")
        self.verilator_version_label.setStyleSheet("font-size: 14px;")

        layout.addWidget(self.kicad_version_label)
        layout.addWidget(self.ngspice_version_label)
        layout.addWidget(self.ghdl_version_label)
        layout.addWidget(self.verilator_version_label)

        # Button for updating KiCad
        self.update_kicad_button = QPushButton("Update KiCad")
        self.update_kicad_button.clicked.connect(self.run_kicad_gui)
        self.update_kicad_button.setStyleSheet("font-size: 14px; padding: 10px 0;")
        layout.addWidget(self.update_kicad_button)

        # Button for updating Ngspice
        self.update_ngspice_button = QPushButton("Update Ngspice")
        self.update_ngspice_button.clicked.connect(self.run_ngspice_gui)
        self.update_ngspice_button.setStyleSheet("font-size: 14px; padding: 10px 0;")
        layout.addWidget(self.update_ngspice_button)

        # Button for downloading GHDL packages
        self.download_ghdl_button = QPushButton("Download Packages")
        self.download_ghdl_button.clicked.connect(self.run_ghdl_download_packages)
        self.download_ghdl_button.setStyleSheet("font-size: 14px; padding: 10px 0;")
        layout.addWidget(self.download_ghdl_button)

        # Button for updating GHDL
        self.update_ghdl_button = QPushButton("Update GHDL")
        self.update_ghdl_button.clicked.connect(self.run_ghdl_gui)
        self.update_ghdl_button.setStyleSheet("font-size: 14px; padding: 10px 0;")
        layout.addWidget(self.update_ghdl_button)

        # Button for updating Verilator
        self.update_verilator_button = QPushButton("Update Verilator")
        self.update_verilator_button.clicked.connect(self.run_verilator_gui)
        self.update_verilator_button.setStyleSheet("font-size: 14px; padding: 10px 0;")
        layout.addWidget(self.update_verilator_button)

        self.setLayout(layout)
    
    def adjust_position(self):
        screen = QApplication.desktop().screenGeometry()
        widget = self.geometry()
        x = (screen.width() - widget.width()) // 2
        y = (screen.height() - widget.height()) // 3  # Move up slightly
        self.move(x, y)

    def run_kicad_gui(self):
        """Run the kicad_gui.py script."""
        try:
            subprocess.run(["python", "kicad_gui.py"], check=True)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"Failed to run KiCad update: {e}")

    def run_ngspice_gui(self):
        """Run the ngspice_gui.py script."""
        try:
            subprocess.run(["python", "ngspice_gui.py"], check=True)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"Failed to run Ngspice update: {e}")

    def run_ghdl_download_packages(self):
        """Run the ghdl_download_packages.py script."""
        try:
            subprocess.run(["python", "download_packages.py"], check=True)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"Failed to download GHDL packages: {e}")

    def run_ghdl_gui(self):
        """Run the ghdl_gui.py script."""
        try:
            subprocess.run(["python", "ghdl_gui.py"], check=True)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"Failed to run GHDL update: {e}")

    def run_verilator_gui(self):
        """Run the verilator_gui.py script."""
        try:
            subprocess.run(["python", "verilator_gui.py"], check=True)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"Failed to run Verilator update: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToolManagerUpdater()
    window.show()
    sys.exit(app.exec_())
