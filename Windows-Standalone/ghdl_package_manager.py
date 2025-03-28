import os
import subprocess
import requests
import zipfile
import json
from pathlib import Path
import datetime
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QMessageBox, QApplication
from logging_setup import log_info, log_error, log_warning

# Constants
GHDL_RELEASE_API = "https://api.github.com/repos/ghdl/ghdl/releases/latest"
TOOLS_DIR = os.path.join(os.getcwd(), "tools")
GHDL_DIR = os.path.join(TOOLS_DIR, "ghdl")
JSON_FILE_PATH = os.path.join(os.getcwd(), "install_details.json")

# Ensure the tools directory exists
os.makedirs(TOOLS_DIR, exist_ok=True)

def load_json_data():
    try:
        if os.path.exists(JSON_FILE_PATH):
            with open(JSON_FILE_PATH, "r") as json_file:
                return json.load(json_file)
        else:
            log_warning(f"JSON file {JSON_FILE_PATH} not found. Using default structure.")
            return {"important_packages": []}
    except json.JSONDecodeError as e:
        log_error(f"Failed to parse JSON file {JSON_FILE_PATH}: {e}")
        return {"important_packages": []}

def save_json_data(data):
    try:
        with open(JSON_FILE_PATH, "w") as json_file:
            json.dump(data, json_file, indent=4)
        log_info(f"JSON data saved to {JSON_FILE_PATH}.")
    except Exception as e:
        log_error(f"Failed to save JSON data to {JSON_FILE_PATH}: {e}")

def find_package(data, package_name):
    return next((pkg for pkg in data["important_packages"] if pkg["package_name"] == package_name), None)

def update_installation_status_ghdl():
    try:
        data = load_json_data()
        package = find_package(data, "ghdl")

        if package:
            if os.path.exists(GHDL_DIR):
                # Update with the correct version and current date
                package.update({
                    "version": get_installed_version() or "-",
                    "installed": "Yes",
                    "installed_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "install_directory": GHDL_DIR
                })
                log_info("Updated existing GHDL installation details.")
            else:
                package.update({
                    "version": "-",
                    "installed": "No",
                    "installed_date": "-",
                    "install_directory": "-"
                })
                log_warning("GHDL directory not found. Marked as not installed.")
        else:
            # Add a new entry
            data["important_packages"].append({
                "package_name": "ghdl",
                "version": "-",
                "installed": "No",
                "installed_date": "-",
                "install_directory": "-"
            })
            log_info("Added new GHDL entry to installation details.")

        save_json_data(data)
    except Exception as e:
        log_error(f"Error updating GHDL installation status: {e}")


def fetch_latest_version():
    try:
        response = requests.get(GHDL_RELEASE_API)
        response.raise_for_status()
        release_data = response.json()
        log_info("Fetched the latest GHDL version from GitHub API.")
        return release_data.get("tag_name", None), release_data.get("assets", [])
    except requests.RequestException as e:
        log_error(f"Error fetching latest release from GitHub API: {e}")
        return None, []

def get_download_url(assets):
    windows_keywords = ["windows", "win64", "mingw", "mcode"]
    for asset in assets:
        if any(keyword in asset["name"].lower() for keyword in windows_keywords) and asset["browser_download_url"].endswith(".zip"):
            log_info(f"Found suitable asset for Windows: {asset['browser_download_url']}.")
            return asset["browser_download_url"]
    log_warning("No suitable asset found for Windows.")
    return None

def download_ghdl(url, version):
    try:
        log_info(f"Downloading GHDL from {url}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        zip_path = os.path.join(TOOLS_DIR, f"ghdl-{version}.zip")
        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        log_info(f"GHDL downloaded to {zip_path}.")
        return zip_path
    except Exception as e:
        log_error(f"Error downloading GHDL: {e}")
        return None

def extract_ghdl(zip_path):
    try:
        log_info(f"Extracting {zip_path}...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(TOOLS_DIR)
        os.remove(zip_path)
        log_info(f"GHDL extracted successfully to {TOOLS_DIR}.")
        return True
    except Exception as e:
        log_error(f"Error extracting GHDL: {e}")
        return False

def add_to_path():
    try:
        tools_bin_path = str(Path(TOOLS_DIR).resolve())
        subprocess.run(f'setx PATH "%PATH%;{tools_bin_path}"', shell=True, check=True)
        log_info(f"Added {tools_bin_path} to the system PATH.")
        return True
    except subprocess.CalledProcessError as e:
        log_error(f"Error adding GHDL to PATH: {e}")
        return False

def load_install_details():
    """
    Load the installation details from the JSON file.
    """
    if os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {"important_packages": []}
    return {"important_packages": []}

def update_install_details(version, success):
    """
    Update the `install_details.json` file with GHDL installation details.
    """
    data = load_install_details()
    for package in data.get("important_packages", []):
        if package["package_name"] == "ghdl":
            package.update({
                "version": version if success else "-",
                "installed": "Yes" if success else "No",
                "installed_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") if success else "-",
                "install_directory": TOOLS_DIR if success else "-"
            })
            break
    else:
        data["important_packages"].append({
            "package_name": "ghdl",
            "version": version if success else "-",
            "installed": "Yes" if success else "No",
            "installed_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") if success else "-",
            "install_directory": TOOLS_DIR if success else "-"
        })

    with open(JSON_FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Installation details updated in {JSON_FILE_PATH}.")

def get_installed_version():
    """
    Get the currently installed version of GHDL.
    """
    data = load_install_details()
    for package in data.get("important_packages", []):
        if package["package_name"] == "ghdl" and package["installed"] == "Yes":
            return package["version"]
    return None

def install_ghdl():
    installed_version = get_installed_version()
    if installed_version:
        log_info(f"GHDL already installed (version {installed_version}).")
        return f"You have already installed the package (version {installed_version})."

    version, assets = fetch_latest_version()
    if not version or not assets:
        log_error("Failed to fetch the latest GHDL version or assets.")
        return "Failed to fetch the latest GHDL version or assets."

    download_url = get_download_url(assets)
    if not download_url:
        log_error("No suitable GHDL asset found for Windows.")
        return "No suitable GHDL asset found for Windows."

    zip_path = download_ghdl(download_url, version)
    if not zip_path:
        log_error(f"Failed to download GHDL version {version}.")
        return f"Failed to download GHDL version {version}."

    if not extract_ghdl(zip_path):
        log_error(f"Failed to extract GHDL archive from {zip_path}.")
        return "Failed to extract the GHDL archive."

    if not add_to_path():
        log_warning("Failed to add tools directory to the system PATH.")
        return "Failed to add tools directory to the system PATH."

    # Update installation details
    update_install_details(version, True)
    log_info(f"GHDL version {version} installed successfully in {TOOLS_DIR}.")
    return f"GHDL version {version} installed successfully."


def update_ghdl():
    installed_version = get_installed_version()
    latest_version, _ = fetch_latest_version()

    if installed_version == latest_version:
        log_info("GHDL is up-to-date.")
        return "You are using the latest version."

    log_info("Updating GHDL to the latest version.")
    return install_ghdl()

class GHDLInstallerApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("GHDL Installer")
        self.resize(400, 400)
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # Title label
        title_label = QLabel("Install GHDL with GUI")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title_label)

        # Update the JSON status file on launch
        update_installation_status_ghdl()

        # Installation status label
        self.status_label = QLabel()
        self.status_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.status_label)

        # Installed version label
        self.version_label = QLabel()
        self.version_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.version_label)

        # Install button
        install_button = QPushButton("Install GHDL")
        install_button.setStyleSheet(self.get_button_style())
        install_button.clicked.connect(self.install_button_action)
        layout.addWidget(install_button)

        # Update button
        update_button = QPushButton("Update GHDL")
        update_button.setStyleSheet(self.get_button_style())
        update_button.clicked.connect(self.update_button_action)
        layout.addWidget(update_button)

        self.setLayout(layout)

        # Update status and version labels on startup
        self.update_status_labels()

    def update_status_labels(self):
        installed_version = get_installed_version()
        if installed_version:
            self.status_label.setText("GHDL is installed.")
            self.status_label.setStyleSheet("color: green;")
            self.version_label.setText(f"Installed version: {installed_version}")
        else:
            self.status_label.setText("GHDL is not installed.")
            self.status_label.setStyleSheet("color: red;")
            self.version_label.setText("Installed version: -")

    def install_button_action(self):
        result = install_ghdl()
        QMessageBox.information(self, "Installation Status", result)
        self.update_status_labels()
        update_installation_status_ghdl()

    def update_button_action(self):
        result = update_ghdl()
        QMessageBox.information(self, "Update Status", result)
        self.update_status_labels()
        update_installation_status_ghdl()

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

def main():
    app = QApplication([])
    window = GHDLInstallerApp()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
