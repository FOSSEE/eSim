import sys
import subprocess
import json
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QComboBox,
    QPushButton,
    QMessageBox,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class KiCadInstallerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KiCad Installer")
        self.setGeometry(100, 100, 400, 250)

        # Initialize attributes
        self.json_file = "install_details.json"
        self.installed_status = "No"  # Tracks installation status dynamically
        self.installed_version = None  # Tracks installed version
        self.install_directory = None  # Tracks the install directory
        self.latest_version = "8.0.8-0~ubuntu20.04.1"  # Latest available version

        self.init_ui()
        self.check_kicad_installation()  # Check and update installation status on startup

    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()

        # Title Label
        title_label = QLabel("Install KiCad with GUI")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Installed Version Info
        self.installed_version_label = QLabel("Installed Version: Checking...")
        layout.addWidget(self.installed_version_label)

        # Latest Version Info
        self.latest_version_label = QLabel(f"Latest Version: {self.latest_version}")
        layout.addWidget(self.latest_version_label)

        # Status Info
        self.status_label = QLabel("Select a version to install or update.")
        self.status_label.setStyleSheet("color: green;")
        layout.addWidget(self.status_label)

        # Dropdown for version selection
        version_label = QLabel("Select KiCad Version:")
        layout.addWidget(version_label)

        self.version_dropdown = QComboBox()
        self.version_dropdown.addItems(["8.0", "7.0", "6.0"])
        layout.addWidget(self.version_dropdown)

        # Install Button
        self.install_button = QPushButton("Install KiCad")
        self.install_button.clicked.connect(self.install_kicad)
        layout.addWidget(self.install_button)

        # Update Button
        self.update_button = QPushButton("Update KiCad")
        self.update_button.clicked.connect(self.update_kicad)
        layout.addWidget(self.update_button)

        self.setLayout(layout)

    def check_kicad_installation(self):
        """Check if KiCad is installed and update the JSON file."""
        try:
            # Check if KiCad is installed
            install_directory = subprocess.check_output("which kicad", shell=True, text=True).strip()
            installed_version = subprocess.check_output(
                "dpkg -s kicad | grep 'Version' | awk '{print $2}'", shell=True, text=True
            ).strip()

            # Update status and JSON
            self.installed_status = "Yes"
            self.installed_version = installed_version
            self.install_directory = install_directory
            self.update_json(installed=True, version=installed_version, install_directory=install_directory)

            # Update UI
            self.installed_version_label.setText(f"Installed Version: {installed_version}")
        except subprocess.CalledProcessError:
            # KiCad is not installed
            self.installed_status = "No"
            self.installed_version = None
            self.install_directory = None
            self.update_json(installed=False, version="", install_directory="")
            self.installed_version_label.setText("Installed Version: Not Installed")

    def update_json(self, installed, version, install_directory):
        """Update the JSON file with the installed status, version, and directory."""
        try:
            # Load or initialize JSON data
            try:
                with open(self.json_file, "r") as file:
                    data = json.load(file)
            except FileNotFoundError:
                data = {"important_packages": []}

            # Update or add KiCad details
            updated = False
            for package in data.get("important_packages", []):
                if package.get("package_name").lower() == "kicad":
                    package.update({
                        "version": version if installed else "-",
                        "installed": "Yes" if installed else "No",
                        "installed_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S") if installed else "-",
                        "install_directory": install_directory if installed else "-",
                    })
                    updated = True
                    break

            if not updated:
                data["important_packages"].append({
                    "package_name": "kicad",
                    "version": version if installed else "-",
                    "installed": "Yes" if installed else "No",
                    "installed_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S") if installed else "-",
                    "install_directory": install_directory if installed else "-",
                })

            # Save back to the JSON file
            with open(self.json_file, "w") as file:
                json.dump(data, file, indent=4)

        except Exception as e:
            self.show_message("Error", f"Failed to update JSON file: {e}", is_success=False)

    def install_kicad(self):
        """Install the selected version of KiCad."""
        # Check installation status dynamically
        if self.installed_status.lower() == "yes":
            self.show_message("Already Installed", "The package is already installed.")
            return

        # Proceed with installation if not installed
        version = self.version_dropdown.currentText()

        try:
            # Add the appropriate PPA
            self.add_ppa(version)
            # Update package list and install
            self.run_command("sudo apt-get update")
            self.run_command(f"sudo apt-get install -y kicad={version}*")

            # Fetch the actual installed version and update JSON
            installed_version = subprocess.check_output(
                "dpkg -s kicad | grep 'Version' | awk '{print $2}'", shell=True, text=True
            ).strip()
            install_directory = subprocess.check_output("which kicad", shell=True, text=True).strip()
            self.update_json(installed=True, version=installed_version, install_directory=install_directory)

            # Update UI
            self.installed_status = "Yes"
            self.installed_version = installed_version
            self.install_directory = install_directory
            self.installed_version_label.setText(f"Installed Version: {installed_version}")
            self.show_message("Success", f"KiCad version {installed_version} installed successfully!")
        except Exception as e:
            self.show_message("Error", str(e), is_success=False)

    def update_kicad(self):
        """Update KiCad to the selected version."""
        if self.installed_status.lower() == "no":
            self.show_message("Error", "Please install the package first.", is_success=False)
            return

        # Check if the installed version matches the latest version
        if self.installed_version == self.latest_version:
            self.show_message("Latest Version", "You are using the latest version.")
            return

        version = self.version_dropdown.currentText()

        try:
            # Add the appropriate PPA
            self.add_ppa(version)
            # Update package list and install
            self.run_command("sudo apt-get update")
            self.run_command(f"sudo apt-get install --only-upgrade -y kicad={version}*")

            # Fetch the actual installed version and update JSON
            installed_version = subprocess.check_output(
                "dpkg -s kicad | grep 'Version' | awk '{print $2}'", shell=True, text=True
            ).strip()
            install_directory = subprocess.check_output("which kicad", shell=True, text=True).strip()
            self.update_json(installed=True, version=installed_version, install_directory=install_directory)

            # Update UI
            self.installed_status = "Yes"
            self.installed_version = installed_version
            self.installed_version_label.setText(f"Installed Version: {installed_version}")
            self.show_message("Success", f"KiCad has been updated to version {installed_version}!")
        except Exception as e:
            self.show_message("Error", str(e), is_success=False)


    def add_ppa(self, version):
        """Add the appropriate PPA for the selected version."""
        if version == "6.0":
            self.run_command("sudo add-apt-repository -y ppa:kicad/kicad-6.0-releases")
        elif version == "7.0":
            self.run_command("sudo add-apt-repository -y ppa:kicad/kicad-7.0-releases")
        elif version == "8.0":
            self.run_command("sudo add-apt-repository -y ppa:kicad/kicad-8.0-releases")

    def run_command(self, command):
        """Run a shell command."""
        try:
            subprocess.run(command, shell=True, check=True, text=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Error while running command: {e}")

    def show_message(self, title, message, is_success=True):
        """Show a message box with the given title and message."""
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        if is_success:
            msg_box.setIcon(QMessageBox.Information)
        else:
            msg_box.setIcon(QMessageBox.Critical)
        msg_box.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KiCadInstallerApp()
    window.show()
    sys.exit(app.exec_())
