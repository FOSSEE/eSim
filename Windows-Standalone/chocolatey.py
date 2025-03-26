import sys
import json
import os
from datetime import datetime
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QMessageBox
)
from logging_setup import log_info, log_error, log_warning

def get_chocolatey_version():
    """Get the installed Chocolatey version."""
    try:
        result = os.popen("choco -v").read().strip()
        return result if result else "Unknown"
    except Exception as e:
        log_error(f"Error retrieving Chocolatey version: {e}")
        return "Unknown"

def update_installation_status(json_file, package_name, version, installed, install_directory):
    try:
        # Load the existing JSON data
        if not os.path.exists(json_file):
            data = {"important_packages": [], "pip_packages": []}
        else:
            with open(json_file, "r") as f:
                data = json.load(f)

        # Update the important_packages section
        for package in data.get("important_packages", []):
            if package["package_name"] == package_name:
                package.update({
                    "version": version if installed else "-",
                    "installed": "Yes" if installed else "No",
                    "installed_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S") if installed else "-",
                    "install_directory": install_directory if installed else "-",
                })
                break
        else:
            # Add new package entry if not found
            data["important_packages"].append({
                "package_name": package_name,
                "version": version if installed else "-",
                "installed": "Yes" if installed else "No",
                "installed_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S") if installed else "-",
                "install_directory": install_directory if installed else "-"
            })

        # Save the updated JSON data
        with open(json_file, "w") as f:
            json.dump(data, f, indent=4)

        log_info(f"Updated {package_name} installation status in {json_file}. Version: {version}, Installed: {'Yes' if installed else 'No'}.")
    except Exception as e:
        log_error(f"Error updating installation status for {package_name}: {e}")

def check_chocolatey_directory(json_file):
    chocolatey_dir = "C:\\ProgramData\\chocolatey"
    try:
        if os.path.exists(chocolatey_dir):
            version = get_chocolatey_version()
            log_info(f"Chocolatey directory exists. Version: {version}.")
            update_installation_status(
                json_file=json_file,
                package_name="chocolatey",
                version=version,
                installed=True,
                install_directory=chocolatey_dir
            )
            return True
        else:
            log_warning("Chocolatey directory does not exist. Marking as not installed.")
            update_installation_status(
                json_file=json_file,
                package_name="chocolatey",
                version="-",
                installed=False,
                install_directory="-"
            )
            return False
    except Exception as e:
        log_error(f"Error checking Chocolatey directory: {e}")
        return False

class ChocolateyInstaller(QMainWindow):
    def __init__(self):
        super().__init__()
        self.json_file = "install_details.json"
        self.init_ui()
        self.installed = self.check_status()

    def init_ui(self):
        self.setWindowTitle("Chocolatey Installer")
        self.resize(400, 300)
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

        # Status label
        self.status_label = QLabel("Status: Checking...", self)
        self.status_label.setStyleSheet("font-size: 14px;")

        # Install button
        self.install_button = QPushButton("Install Chocolatey", self)
        self.install_button.setStyleSheet(self.get_button_style())
        self.install_button.clicked.connect(self.install_chocolatey)

        # Update button
        self.update_button = QPushButton("Update Chocolatey", self)
        self.update_button.setStyleSheet(self.get_button_style())
        self.update_button.clicked.connect(self.update_chocolatey)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.install_button)
        layout.addWidget(self.update_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def get_button_style(self):
        return (
            """
            QPushButton {
                font-size: 16px;
                padding: 10px;
                border-radius: 10px;
                border: 1px solid gray;
                background-color: lightgray;
                color: black;
            }
            QPushButton:hover {
                background-color: #87CEFA;
                border: 1px solid #4682B4;
                color: white;
            }
            """
        )

    def check_status(self):
        try:
            chocolatey_dir = "C:\\ProgramData\\chocolatey"
            if os.path.exists(chocolatey_dir):
                version = get_chocolatey_version()
                log_info(f"Chocolatey is already installed. Version: {version}.")
                self.status_label.setText(f"Status: Chocolatey is already installed (Version: {version}).")
                update_installation_status(
                    self.json_file,
                    "chocolatey",
                    version,
                    True,
                    chocolatey_dir
                )
                return True
            else:
                log_warning("Chocolatey is not installed.")
                self.status_label.setText("Status: Chocolatey is not installed.")
                update_installation_status(
                    self.json_file,
                    "chocolatey",
                    "-",
                    False,
                    "-"
                )
                return False
        except Exception as e:
            log_error(f"Error checking Chocolatey status: {e}")

    def install_chocolatey(self):
        if self.installed:
            log_info("Attempted to install Chocolatey, but it is already installed.")
            QMessageBox.information(self, "Information", "The package is already installed.")
            return

        install_script = (
            "Set-ExecutionPolicy Bypass -Scope Process -Force; "
            "[System.Net.ServicePointManager]::SecurityProtocol = "
            "[System.Net.ServicePointManager]::SecurityProtocol -bor 3072; "
            "iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
        )

        try:
            os.system(f"powershell -Command \"{install_script}\"")
            log_info("Chocolatey installed successfully.")
            QMessageBox.information(self, "Success", "Chocolatey installed successfully.")
            self.installed = True
            self.check_status()
        except Exception as e:
            log_error(f"Failed to install Chocolatey: {e}")
            QMessageBox.critical(self, "Error", f"Failed to install Chocolatey: {e}")

    def update_chocolatey(self):
        if not self.installed:
            log_warning("Attempted to update Chocolatey, but it is not installed.")
            QMessageBox.warning(self, "Warning", "Chocolatey is not installed. Please install it first.")
            return

        update_script = "choco upgrade chocolatey -y"

        try:
            os.system(f"powershell -Command \"{update_script}\"")
            log_info("Chocolatey updated successfully.")
            QMessageBox.information(self, "Success", "Chocolatey updated successfully.")
            self.check_status()
        except Exception as e:
            log_error(f"Failed to update Chocolatey: {e}")
            QMessageBox.critical(self, "Error", f"Failed to update Chocolatey: {e}")


if __name__ == "__main__":
    json_file = "install_details.json"
    check_chocolatey_directory(json_file)

    app = QApplication(sys.argv)
    window = ChocolateyInstaller()
    window.show()
    sys.exit(app.exec_())