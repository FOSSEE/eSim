import sys
import subprocess
import json
import datetime

def install_pyqt5():
    """Checks if PyQt5 is installed and installs it if missing."""
    try:
        import PyQt5
        print("PyQt5 is already installed.")
    except ImportError:
        print("PyQt5 is not installed. Installing now...")
        subprocess.run(["sudo", "apt-get", "install", "-y", "python3-pyqt5"], check=True)
        print("PyQt5 installation complete.")

install_pyqt5()

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import Qt

class ESimToolManager(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title = QLabel("Tool Manager for eSim", self)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px 0;")
        layout.addWidget(title)
        
        desc_analog = QLabel("Install the eSim for the Analog Project (KiCad and Ngspice)", self)
        desc_analog.setStyleSheet("font-size: 14px; padding: 30px 0 10px 0;")
        layout.addWidget(desc_analog)

        btn_install_analog = QPushButton("Install eSim (Analog Mode)", self)
        btn_install_analog.setStyleSheet("font-size: 14px; padding: 5px 0;")
        btn_install_analog.clicked.connect(lambda: self.run_installation("analog"))
        layout.addWidget(btn_install_analog)
        
        desc_digital = QLabel("Install the eSim for the Digital Project (All Packages)", self)
        desc_digital.setStyleSheet("font-size: 14px; padding: 30px 0 10px 0;")
        layout.addWidget(desc_digital)

        btn_install_digital = QPushButton("Install eSim (Digital Mode)", self)
        btn_install_digital.setStyleSheet("font-size: 14px; padding: 5px 0;")
        btn_install_digital.clicked.connect(lambda: self.run_installation("digital"))
        layout.addWidget(btn_install_digital)
        
        desc_updater = QLabel("Open the Updater to update the packages to the latest versions", self)
        desc_updater.setStyleSheet("font-size: 14px; padding: 30px 0 10px 0;")
        layout.addWidget(desc_updater)

        btn_updater_gui = QPushButton("eSim Updater", self)
        btn_updater_gui.setStyleSheet("font-size: 14px; padding: 5px 0;")
        btn_updater_gui.clicked.connect(lambda: self.run_command("python3 updater_gui.py"))
        layout.addWidget(btn_updater_gui)
        
        desc_uninstall_digital = QLabel("Uninstall the digital packages (Verilator and GHDL)", self)
        desc_uninstall_digital.setStyleSheet("font-size: 14px; padding: 30px 0 10px 0;")
        layout.addWidget(desc_uninstall_digital)
        
        btn_uninstall_digital = QPushButton("Uninstall Digital Packages", self)
        btn_uninstall_digital.setStyleSheet("font-size: 14px; padding: 5px 0;")
        btn_uninstall_digital.clicked.connect(lambda: self.run_uninstallation("digital"))
        layout.addWidget(btn_uninstall_digital)
        
        desc_uninstall_all = QLabel("Uninstall all the packages of eSim", self)
        desc_uninstall_all.setStyleSheet("font-size: 14px; padding: 30px 0 10px 0;")
        layout.addWidget(desc_uninstall_all)
        
        btn_uninstall_all = QPushButton("Uninstall All Packages", self)
        btn_uninstall_all.setStyleSheet("font-size: 14px; padding: 5px 0;")
        btn_uninstall_all.clicked.connect(lambda: self.run_uninstallation("all"))
        layout.addWidget(btn_uninstall_all)
        
        self.setLayout(layout)
        self.setWindowTitle("eSim Tool Manager")
        self.resize(400, 300)
        self.adjust_position()
    
    def adjust_position(self):
        screen = QApplication.desktop().screenGeometry()
        widget = self.geometry()
        x = (screen.width() - widget.width()) // 2
        y = (screen.height() - widget.height()) // 3  # Move up slightly
        self.move(x, y)

    def run_installation(self, mode):
        command = f"./install-eSim.sh --install --{mode}"
        print(f"Executing: {command}")
        subprocess.run(command, shell=True)
        self.update_json(mode)
        self.show_message(f"The eSim for {mode} mode has been successfully installed.")

    def run_uninstallation(self, mode):
        if mode == "digital":
            command = "./install-eSim.sh --uninstall --digital"
            message = "The digital packages (Verilator and GHDL) have been successfully uninstalled."
        else:
            command = "./install-eSim.sh --uninstall"
            message = "All eSim packages have been successfully uninstalled."
        
        print(f"Executing: {command}")
        subprocess.run(command, shell=True)
        self.show_message(message)

    def get_version(self, package_name):
        version_commands = {
            "ngspice": ["ngspice", "-v"],
            "kicad": ["apt-cache", "policy", "kicad"],  # Use apt-cache to get installed version
            "ghdl": ["ghdl", "--version"],
            "verilator": ["verilator", "--version"]
        }

        if package_name in version_commands:
            try:
                result = subprocess.run(version_commands[package_name], capture_output=True, text=True, check=True)
                output_lines = result.stdout.strip().split("\n")

                if package_name == "ngspice":
                    for line in output_lines:
                        if "ngspice-" in line:
                            return line.split("ngspice-")[1].split()[0]  # Extract version from "** ngspice-XX"
                elif package_name == "ghdl":
                    return output_lines[0].split()[1]  # Extract version from "GHDL X.XX"
                elif package_name == "verilator":
                    return output_lines[0].split()[1]  # Extract version from "Verilator X.XXX"
                elif package_name == "kicad":
                    for line in output_lines:
                        if "Installed:" in line:
                            full_version = line.split("Installed:")[1].strip().split()[0]  # Extract full version
                            return full_version.split("-")[0]  # Extract only "6.0.11"
                    return "Not Installed"

                return output_lines[0]  # Default case, return first line
            except (subprocess.CalledProcessError, FileNotFoundError, IndexError):
                return "Unknown"
        
        return "Unknown"
    
    def update_json(self, mode):
        json_file = "information.json"
        try:
            with open(json_file, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("JSON file not found or empty. Initializing...")
            data = {"important_packages": []}
        
        installed_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for package in data.get("important_packages", []):
            if package["package_name"] in ["ngspice", "kicad"]:
                package["installed"] = "Yes"
                package["installed_date"] = installed_date
                package["version"] = self.get_version(package["package_name"])
            if mode == "digital" and package["package_name"] in ["ghdl", "verilator"]:
                package["installed"] = "Yes"
                package["installed_date"] = installed_date
                package["version"] = self.get_version(package["package_name"])
        
        with open(json_file, "w") as file:
            json.dump(data, file, indent=4)
        print("Updated information.json")

    def show_message(self, message):
        """Displays a pop-up message box with the given message."""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Completed")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def run_command(self, command):
        print(f"Executing: {command}")
        subprocess.run(command, shell=True)
        print("Done!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ESimToolManager()
    ex.show()
    sys.exit(app.exec_())