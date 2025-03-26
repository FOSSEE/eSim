import os
import json
import subprocess
import datetime
import shutil
from packaging import version
from packaging.version import InvalidVersion
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox
from logging_setup import log_info, log_error, log_warning

# Define the tools directory and JSON file path
TOOLS_DIR = os.path.join(os.getcwd(), "tools")
NGSPICE_DIR = os.path.join(TOOLS_DIR, "ngspice")
JSON_FILE_PATH = os.path.join(os.getcwd(), "install_details.json")

# Path to the Ngspice installation directory
NGSPICE_TOOL_FOLDER = os.path.join(os.getcwd(), "tool", "ngspice")

# Ensure the tools directory exists
os.makedirs(TOOLS_DIR, exist_ok=True)

# Lambda to define the install command
install_command = lambda version: f"choco install -y ngspice --version={version}"

# Load JSON data from the file
def load_json_data():
    try:
        if os.path.exists(JSON_FILE_PATH):
            with open(JSON_FILE_PATH, "r") as json_file:
                return json.load(json_file)
        else:
            log_warning(f"JSON file {JSON_FILE_PATH} not found. Using default structure.")
            return {"important_packages": [], "pip_packages": []}
    except json.JSONDecodeError as e:
        log_error(f"Failed to parse JSON file {JSON_FILE_PATH}: {e}")
        return {"important_packages": [], "pip_packages": []}

# Save JSON data to the file
def save_json_data(data):
    try:
        with open(JSON_FILE_PATH, "w") as json_file:
            json.dump(data, json_file, indent=4)
        log_info(f"JSON data saved to {JSON_FILE_PATH}.")
    except Exception as e:
        log_error(f"Failed to save JSON data to {JSON_FILE_PATH}: {e}")

# Find a package by name in the important_packages list
def find_package(data, package_name):
    return next((pkg for pkg in data["important_packages"] if pkg["package_name"] == package_name), None)

# Update installation status
def update_installation_status_ngspice():
    try:
        data = load_json_data()
        package = find_package(data, "ngspice")

        if package:
            if os.path.exists(NGSPICE_DIR):
                current_version = package.get("version", "-")
                installed_date = package.get("installed_date", "-")

                # Update package details
                package.update({
                    "version": current_version,
                    "installed": "Yes",
                    "installed_date": installed_date,
                    "install_directory": NGSPICE_DIR
                })
                log_info("Updated existing Ngspice installation details.")
            else:
                # Mark as not installed
                package.update({
                    "version": "-",
                    "installed": "No",
                    "installed_date": "-",
                    "install_directory": "-"
                })
                log_warning("Ngspice directory not found. Marked as not installed.")
        else:
            # Add a new entry if not present
            data["important_packages"].append({
                "package_name": "ngspice",
                "version": "-",
                "installed": "No",
                "installed_date": "-",
                "install_directory": "-"
            })
            log_info("Added new Ngspice entry to installation details.")

        save_json_data(data)
    except Exception as e:
        log_error(f"Error updating Ngspice installation status: {e}")

# Get the installed version of a package
def get_installed_version(package_name):
    data = load_json_data()
    package = find_package(data, package_name)
    if package and package["installed"] == "Yes":
        return package.get("version", "Unknown")
    return "Not Installed"

# Install ngspice
def install_ngspice(selected_version):
    try:
        if not selected_version:
            log_warning("Ngspice installation attempted without selecting a version.")
            return "Please select a version."

        command = install_command(selected_version)
        subprocess.run(command, check=True, shell=True)

        choco_lib_path = os.path.join("C:\\ProgramData\\chocolatey\\lib", "ngspice")
        if not os.path.exists(choco_lib_path):
            log_error("Installation succeeded but Ngspice directory not found.")
            return "Installation succeeded but Ngspice directory not found."

        if os.path.exists(NGSPICE_DIR):
            shutil.rmtree(NGSPICE_DIR)
        shutil.move(choco_lib_path, TOOLS_DIR)

        # Load and update JSON data
        data = load_json_data()
        package = find_package(data, "ngspice")

        if package:
            # Update package details
            installed_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            package.update({
                "version": selected_version,
                "installed": "Yes",
                "installed_date": installed_date,
                "install_directory": NGSPICE_DIR
            })
        else:
            # Add a new package entry
            data["important_packages"].append({
                "package_name": "ngspice",
                "version": selected_version,
                "installed": "Yes",
                "installed_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "install_directory": NGSPICE_DIR
            })

        save_json_data(data)
        log_info(f"Ngspice version {selected_version} installed successfully.")
        return f"Ngspice version {selected_version} installed successfully."
    except subprocess.CalledProcessError as e:
        log_error(f"Installation failed: {e}")
        return f"Installation failed: {e}"
    except Exception as e:
        log_error(f"An error occurred during installation: {e}")
        return f"An error occurred: {e}"

# Fetch the latest version of ngspice
def fetch_latest_version():
    try:
        result = subprocess.run(
            "choco search ngspice --exact --all-versions",
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        # Extract and clean versions
        versions = []
        for line in result.stdout.splitlines():
            if line.startswith("ngspice"):
                parts = line.split()
                if len(parts) > 1:
                    version_string = parts[1].strip()
                    # Ensure only valid version strings are added
                    if version_string.replace('.', '').isdigit():  # Check if valid version format
                        versions.append(version_string)
        return versions[:3] if versions else ["Unknown"]
    except subprocess.CalledProcessError as e:
        print(f"Failed to fetch versions: {e}")
        return ["Unknown"]

# Check for updates
def check_for_updates(installed_version, latest_version):
    try:
        # Ignore invalid versions like '-'
        if installed_version == "-" or latest_version == "-" or installed_version == "Not Installed":
            return False
        return version.parse(installed_version) < version.parse(latest_version)
    except InvalidVersion:
        print(f"Invalid version format: installed='{installed_version}', latest='{latest_version}'")
        return False

# Update ngspice
def update_ngspice():
    latest_versions = fetch_latest_version()
    latest_version = latest_versions[0] if latest_versions and latest_versions[0] != "Unknown" else None

    if not latest_version:
        log_warning("Failed to fetch the latest version for Ngspice.")
        return "Failed to fetch the latest version."

    try:
        # Run the update command
        subprocess.run(f"choco install -y ngspice --version={latest_version}", shell=True, check=True)

        # Move the updated files to the tools directory
        choco_lib_path = os.path.join("C:\\ProgramData\\chocolatey\\lib", "ngspice")
        if os.path.exists(NGSPICE_DIR):
            shutil.rmtree(NGSPICE_DIR)
        shutil.move(choco_lib_path, TOOLS_DIR)

        # Update the JSON file with the new version
        data = load_json_data()
        package = find_package(data, "ngspice")
        installed_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if package:
            package.update({
                "version": latest_version,
                "installed_date": installed_date,
                "install_directory": NGSPICE_DIR
            })
        else:
            data["important_packages"].append({
                "package_name": "ngspice",
                "version": latest_version,
                "installed": "Yes",
                "installed_date": installed_date,
                "install_directory": NGSPICE_DIR
            })

        save_json_data(data)
        log_info(f"Ngspice has been updated to version {latest_version}.")
        return f"Ngspice has been updated to version {latest_version}."
    except subprocess.CalledProcessError as e:
        log_error(f"Error occurred during Ngspice update: {e}")
        return f"Error occurred during update: {e}"
    except Exception as e:
        log_error(f"Error: {e}")
        return f"Error: {e}"

class NgspiceInstallerApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Ngspice Installer")
        self.resize(400, 400)
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # Title label
        title_label = QLabel("Install Ngspice with GUI")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title_label)

        # Update the JSON status file on launch
        update_installation_status_ngspice()

        # Fetch the latest three versions
        self.latest_versions = fetch_latest_version()

        # Get installed version
        data = load_json_data()
        ngspice_package = find_package(data, "ngspice")
        self.installed_version = (
            ngspice_package["version"] if ngspice_package and ngspice_package["installed"] == "Yes" else "Not Installed"
        )

        # Display installed and latest versions
        self.installed_version_label = QLabel(
            f"Installed Version: {self.installed_version}"
            if self.installed_version != "Not Installed"
            else "Ngspice is not installed"
        )
        self.installed_version_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.installed_version_label)

        self.latest_version_label = QLabel(
            f"Latest Version: {self.latest_versions[0]}"
            if self.latest_versions[0] != "Unknown"
            else "Latest version unknown"
        )
        self.latest_version_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.latest_version_label)

        # Update message label
        self.update_label = QLabel("")
        self.update_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.update_label)

        # Check for updates on program launch
        if (
            self.installed_version != "Not Installed"
            and self.latest_versions[0] != "Unknown"
            and self.installed_version != "-"
        ):
            is_outdated = self.installed_version != self.latest_versions[0]
            if is_outdated:
                self.update_label.setText("Your version is out of date. Please update.")
                self.update_label.setStyleSheet("color: red;")
            else:
                self.update_label.setText("You are using the latest version.")
                self.update_label.setStyleSheet("color: green;")

        # Dropdown for version selection
        dropdown_label = QLabel("Select Ngspice Version:")
        dropdown_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(dropdown_label)

        self.version_dropdown = QComboBox()
        self.version_dropdown.addItems(self.latest_versions)
        self.version_dropdown.setStyleSheet(self.get_dropdown_style())
        layout.addWidget(self.version_dropdown)

        # Install button
        install_button = QPushButton("Install Ngspice")
        install_button.setStyleSheet(self.get_button_style())
        install_button.clicked.connect(self.install_button_action)
        layout.addWidget(install_button)

        # Update button
        update_button = QPushButton("Update Ngspice")
        update_button.setStyleSheet(self.get_button_style())
        update_button.clicked.connect(self.update_button_action)
        layout.addWidget(update_button)

        self.setLayout(layout)

    def install_button_action(self):
        data = load_json_data()
        package = find_package(data, "ngspice")
        self.installed_version = package["version"] if package and package["installed"] == "Yes" else "Not Installed"

        if self.installed_version != "Not Installed":
            QMessageBox.information(self, "Installation Status", "The Ngspice package is already installed.")
            return

        selected_version = self.version_dropdown.currentText()
        if not selected_version:
            QMessageBox.critical(self, "Error", "Please select a version.")
            return

        result = install_ngspice(selected_version)
        QMessageBox.information(self, "Installation Status", result)

        update_installation_status_ngspice()
        self.update_labels()

    def update_button_action(self):
        self.latest_versions = fetch_latest_version()
        latest_version = self.latest_versions[0] if self.latest_versions[0] != "Unknown" else None

        if not latest_version:
            QMessageBox.critical(self, "Update Status", "Failed to fetch the latest version. Please try again later.")
            return

        data = load_json_data()
        package = find_package(data, "ngspice")
        installed_version = package["version"] if package and package["installed"] == "Yes" else "Not Installed"

        if installed_version == latest_version:
            QMessageBox.information(self, "Update Status", "You are already using the latest version.")
            return

        result = update_ngspice()
        if "Error" in result:
            QMessageBox.critical(self, "Update Status", result)
        else:
            QMessageBox.information(self, "Update Status", f"Ngspice has been updated to version {latest_version}.")
            update_installation_status_ngspice()
            self.update_labels()

    def update_labels(self):
        data = load_json_data()
        package = find_package(data, "ngspice")
        self.installed_version = package["version"] if package and package["installed"] == "Yes" else "Not Installed"

        self.installed_version_label.setText(
            f"Installed Version: {self.installed_version}"
            if self.installed_version != "Not Installed"
            else "Ngspice is not installed"
        )

        if self.installed_version == self.latest_versions[0]:
            self.update_label.setText("You are using the latest version.")
            self.update_label.setStyleSheet("color: green;")
        else:
            self.update_label.setText("Your version is out of date. Please update.")
            self.update_label.setStyleSheet("color: red;")

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

    def get_dropdown_style(self):
        return (
            """
            QComboBox {
                font-size: 14px;
                padding: 5px;
                border-radius: 5px;
                border: 1px solid gray;
                background-color: white;
            }
            QComboBox:hover {
                border: 1px solid #4682B4;
            }
            QComboBox::drop-down {
                border: none;
            }
            """
        )

# Main application loop
def main():
    app = QtWidgets.QApplication([])
    window = NgspiceInstallerApp()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
