import os
import json
import subprocess
import datetime
import requests
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QLabel, QVBoxLayout, QPushButton, QComboBox, QProgressBar

# Define BASE_DIR as the directory where this Python file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE_PATH = os.path.join(BASE_DIR, "install_details.json")  # JSON file path
GHDL_PACKAGE_NAME = "ghdl"

# Load JSON data
def load_json_data():
    if os.path.exists(JSON_FILE_PATH):
        try:
            with open(JSON_FILE_PATH, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"important_packages": []}
    return {"important_packages": []}

# Save JSON data
def save_json_data(data):
    with open(JSON_FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)

# Find package in JSON data
def find_package(data, package_name):
    return next((pkg for pkg in data["important_packages"] if pkg["package_name"] == package_name), None)

# Install GHDL in a thread-safe way
class InstallThread(QThread):
    finished = pyqtSignal(str)

    def __init__(self, version):
        super().__init__()
        self.version = version

    def run(self):
        result = install_ghdl(self.version)
        self.finished.emit(result)

# Hardcoded GHDL versions and their tarball URLs
GHDL_VERSIONS = [
    {"name": "v4.1.0", "tarball_url": "https://github.com/ghdl/ghdl/archive/refs/tags/v4.1.0.tar.gz"},
    {"name": "v4.0.0", "tarball_url": "https://github.com/ghdl/ghdl/archive/refs/tags/v4.0.0.tar.gz"},
    {"name": "v3.0.0", "tarball_url": "https://github.com/ghdl/ghdl/archive/refs/tags/v3.0.0.tar.gz"}
]

# Install GHDL function (adjusted for hardcoded versions)
def install_ghdl(selected_version=None):
    try:
        print("Installing GHDL...")

        # Step 1: Install dependencies
        subprocess.run(
            ["sudo", "apt", "install", "-y", "build-essential", "gcc", "gnat", "zlib1g-dev", "wget"],
            check=True
        )

        # Find the selected version details from the hardcoded list
        version_data = next((v for v in GHDL_VERSIONS if v["name"] == selected_version), None)
        if not version_data:
            return f"Error: Version {selected_version} not found."

        tarball_url = version_data["tarball_url"]
        tarball_name = os.path.join(BASE_DIR, "ghdl.tar.gz")

        # Step 2: Download the tarball
        print(f"Downloading GHDL from {tarball_url}...")
        result = subprocess.run(["wget", "-O", tarball_name, tarball_url])
        if result.returncode != 0:
            return f"Failed to download GHDL. Check the URL: {tarball_url}"

        subprocess.run(["tar", "-xvf", tarball_name], check=True)

        # Step 3: Build and install GHDL
        extracted_dir = next((d for d in os.listdir('.') if os.path.isdir(d) and d.startswith("ghdl")), None)
        if not extracted_dir:
            return "Error: Extracted GHDL source directory not found."
        os.chdir(extracted_dir)
        subprocess.run(["./configure"], check=True)
        subprocess.run(["make"], check=True)
        subprocess.run(["sudo", "make", "install"], check=True)

        # Step 4: Clean up
        os.chdir(BASE_DIR)  # Return to the base directory
        if os.path.exists(tarball_name):
            os.remove(tarball_name)  # Delete the tarball
        extracted_ghdl_dir = os.path.join(BASE_DIR, extracted_dir)
        if os.path.exists(extracted_ghdl_dir):
            subprocess.run(["sudo", "rm", "-rf", extracted_ghdl_dir])  # Delete the extracted directory

        # Step 5: Update JSON details
        data = load_json_data()
        package = find_package(data, GHDL_PACKAGE_NAME)
        installed_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if package:
            # Update existing entry
            package.update({
                "version": selected_version,
                "installed": "Yes",
                "installed_date": installed_date,
                "install_directory": "/usr/local/bin"
            })
        else:
            # Create a new entry
            data["important_packages"].append({
                "package_name": GHDL_PACKAGE_NAME,
                "version": selected_version,
                "installed": "Yes",
                "installed_date": installed_date,
                "install_directory": "/usr/local/bin"
            })
        save_json_data(data)  # Save the updated JSON

        return f"GHDL version {selected_version} installed successfully."
    except subprocess.CalledProcessError as e:
        return f"Installation failed: {e}"
    except Exception as e:
        return f"An error occurred: {e}"

# GUI Application
class GHDLInstallerApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("GHDL Installer")
        self.setGeometry(100, 100, 400, 350)
        layout = QVBoxLayout()

        # Title Label
        title_label = QLabel("GHDL Installer & Manager")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)

        # Check installation status
        self.refresh_package_status()

        # Fetch the hardcoded versions
        version_names = [v["name"] for v in GHDL_VERSIONS]
        self.latest_version = version_names[0] if version_names else "Unknown"

        # Installed Version Label
        self.installed_version_label = QLabel(f"Installed Version: {self.installed_version}")
        layout.addWidget(self.installed_version_label)

        # Latest Version Label
        self.latest_version_label = QLabel(f"Latest Version: {self.latest_version}")
        layout.addWidget(self.latest_version_label)

        # Status Label for Update Check
        self.status_label = QLabel("")
        self.update_status_message()
        layout.addWidget(self.status_label)

        # Dropdown for Version Selection
        dropdown_label = QLabel("Select Version to Install:")
        layout.addWidget(dropdown_label)

        self.version_dropdown = QComboBox()
        self.version_dropdown.addItems(version_names)
        layout.addWidget(self.version_dropdown)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        # Install Button
        install_button = QPushButton("Install GHDL")
        install_button.clicked.connect(self.install_ghdl_action)
        layout.addWidget(install_button)

        # Update Button
        update_button = QPushButton("Update")
        update_button.clicked.connect(self.update_ghdl_action)
        layout.addWidget(update_button)

        self.setLayout(layout)


    def refresh_package_status(self):
        """Check if GHDL is installed and update the package status in the JSON file."""
        data = load_json_data()
        package = find_package(data, GHDL_PACKAGE_NAME)
        if package and package.get("installed") == "Yes":
            self.installed_version = package.get("version", "Unknown")
        else:
            self.installed_version = "The package is not installed"

    def update_status_message(self):
        """Set the status message for updates."""
        if self.installed_version == "The package is not installed":
            self.status_label.setText("The package is not installed.")
            self.status_label.setStyleSheet("color: red;")
        elif self.installed_version == self.latest_version:
            self.status_label.setText("You are using the latest version.")
            self.status_label.setStyleSheet("color: green;")
        else:
            self.status_label.setText("Your package is out of date. Please update.")
            self.status_label.setStyleSheet("color: orange;")

    def install_ghdl_action(self):
        """Install the selected version of GHDL."""
        if self.installed_version != "The package is not installed":
            QMessageBox.information(self, "Installation Status", "The package is already installed.")
            return

        selected_version = self.version_dropdown.currentText()
        self.progress_bar.show()
        self.thread = InstallThread(selected_version)
        self.thread.finished.connect(self.show_message)
        self.thread.start()

    def update_ghdl_action(self):
        """Update GHDL to the latest version."""
        if self.installed_version == self.latest_version:
            QMessageBox.information(self, "Update Status", "You are using the latest version.")
            return

        self.progress_bar.show()
        self.thread = InstallThread(self.latest_version)
        self.thread.finished.connect(self.show_message)
        self.thread.start()

    def show_message(self, result):
        """Display the result of the installation or update."""
        QMessageBox.information(self, "Status", result)
        self.progress_bar.hide()
        self.refresh_ui()

    def refresh_ui(self):
        """Refresh the UI to show updated versions."""
        self.refresh_package_status()
        self.installed_version_label.setText(f"Installed Version: {self.installed_version}")
        self.update_status_message()

# Main Application Loop
def main():
    app = QtWidgets.QApplication([])
    window = GHDLInstallerApp()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
