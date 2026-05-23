import os
import subprocess
from typing import Self
import requests
import zipfile
import json
from pathlib import Path
import datetime
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QMessageBox, QApplication, QProgressBar
from logging_setup import log_info, log_error, log_warning


def is_ghdl_installed():
    try:
        subprocess.check_output("ghdl --version", shell=True)
        return True
    except:
        return False
# Constants
GHDL_RELEASE_API = "https://api.github.com/repos/ghdl/ghdl/releases/latest"
TOOLS_DIR = os.path.join(os.getcwd(), "tools")


def get_ghdl_install_path():
    for folder in os.listdir(TOOLS_DIR):
        if folder.lower().startswith("ghdl"):
            return os.path.join(TOOLS_DIR, folder)
    return None  


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



def detect_ghdl_version_from_cmd():
    try:
        result = subprocess.check_output("ghdl --version", shell=True, text=True)
        return result.splitlines()[0]
    except:
        return None



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
    data = load_json_data()
    package = find_package(data, "ghdl")

    if is_ghdl_installed():  
        version = "Detected"   

        if package:
            package.update({
                "version": version,
                "installed": "Yes",
                "install_directory": "System PATH"
            })
        else:
            data["important_packages"].append({
                "package_name": "ghdl",
                "version": version,
                "installed": "Yes",
                "install_directory": "System PATH"
            })
    else:
        if package:
            package.update({
                "version": "-",
                "installed": "No",
                "install_directory": "-"
            })

    save_json_data(data)


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


def download_ghdl(url, version, progress_callback=None):
    try:
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0

        zip_path = os.path.join(TOOLS_DIR, f"ghdl-{version}.zip")

        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)

                    if total_size > 0 and progress_callback:
                        percent = int((downloaded / total_size) * 100)
                        progress_callback(percent)

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

def install_ghdl(progress_callback=None):
    installed_version = detect_ghdl_version_from_cmd() or get_installed_version()
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

    def progress(val):
        if progress_callback:
            progress_callback(val, f"Downloading... {val}%")

    zip_path = download_ghdl(download_url, version, progress)

    if not zip_path:
        log_error(f"Failed to download GHDL version {version}.")
        return f"Failed to download GHDL version {version}."

    if not extract_ghdl(zip_path):
        log_error(f"Failed to extract GHDL archive from {zip_path}.")
        return "Failed to extract the GHDL archive."

    if not add_to_path():
        log_warning("Failed to add tools directory to the system PATH.")
        return "Failed to add tools directory to the system PATH."
    

    if not add_to_path():
        log_warning("Failed to add tools directory to the system PATH.")
        return "Failed to add tools directory to the system PATH."

# FIX 4 (ADD HERE)
    update_install_details(version, True)
    update_installation_status_ghdl()

    log_info(f"GHDL version {version} installed successfully in {TOOLS_DIR}.")
    return f"GHDL version {version} installed successfully."
    
    # Update installation details
    update_install_details(version, True)
    log_info(f"GHDL version {version} installed successfully in {TOOLS_DIR}.")
    return f"GHDL version {version} installed successfully."


def update_ghdl(progress_callback=None):
    installed_version = detect_ghdl_version_from_cmd() or get_installed_version()
    latest_version, _ = fetch_latest_version()

    if is_ghdl_installed():
        version = detect_ghdl_version_from_cmd() or "Unknown"
        log_info(f"GHDL already installed (version {version}).")
        return f"You have already installed GHDL (version {version})."

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

        # 🔹 Progress Label
        self.progress_label = QLabel("Ready")
        layout.addWidget(self.progress_label)

        # 🔹 Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # 🔹 Title
        title_label = QLabel("Install GHDL with GUI")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title_label)

        # Update JSON status
        update_installation_status_ghdl()

        # 🔹 Status label
        self.status_label = QLabel()
        self.status_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.status_label)

        # 🔹 Version label
        self.version_label = QLabel()
        self.version_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.version_label)

        # 🔹 Install Button
        install_button = QPushButton("Install GHDL")
        install_button.clicked.connect(self.install_button_action)
        layout.addWidget(install_button)

        # 🔹 Update Button
        update_button = QPushButton("Update GHDL")
        update_button.clicked.connect(self.update_button_action)
        layout.addWidget(update_button)

        self.setLayout(layout)

        # Update labels
        self.update_status_labels()

    # ✅ THIS WAS MISSING (MAIN ERROR FIX)
    def update_progress(self, percent, text):
        self.progress_bar.setValue(percent)
        self.progress_label.setText(text)
        QtWidgets.QApplication.processEvents()


    def install_with_progress(self, percent, text, command):
        self.update_progress(percent, text)
        os.system(command)

    def update_status_labels(self):
        installed_version = detect_ghdl_version_from_cmd() or get_installed_version()

        if installed_version:
            self.status_label.setText("GHDL is installed.")
            self.status_label.setStyleSheet("color: green;")
            self.version_label.setText(f"Installed version: {installed_version}")
        else:
            self.status_label.setText("GHDL is not installed.")
            self.status_label.setStyleSheet("color: red;")
            self.version_label.setText("Installed version: -")

    def install_button_action(self):
        if is_ghdl_installed():
            QMessageBox.information(self, "Info", "GHDL is already installed.")
            return
        self.update_progress(0, "Starting GHDL installation...")

        version, assets = fetch_latest_version()
        download_url = get_download_url(assets)

        if not download_url:
            QMessageBox.critical(self, "Error", "Download URL not found")
            return

        def progress(val):
            self.update_progress(val, f"Downloading... {val}%")

        zip_path = download_ghdl(download_url, version, progress)

        if not zip_path:
            QMessageBox.critical(self, "Error", "Download failed")
            return

        self.update_progress(80, "Extracting...")
        extract_ghdl(zip_path)

        self.update_progress(90, "Setting PATH...")
        add_to_path()

        update_install_details(version, True)
        update_installation_status_ghdl()

        self.update_progress(100, "Done ✅")

        QMessageBox.information(self, "Success", "GHDL Installed Successfully")

        self.update_status_labels()
        update_installation_status_ghdl()




    



    def update_button_action(self):
        self.update_progress(0, "Checking updates...")

        def progress(percent, text):
            self.update_progress(percent, text)

        result = update_ghdl(progress)

        self.update_progress(100, "Update Completed ✅")

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
