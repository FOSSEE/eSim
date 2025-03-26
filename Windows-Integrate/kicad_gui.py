import sys
import os
import shutil
import subprocess
import json
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QMessageBox
from PyQt5.QtCore import Qt

# Define paths
INSTALL_DIR = r"C:\FOSSEE"
DOWNLOAD_DIR = os.path.join(INSTALL_DIR, "Tool-Manager", "Download")
KICAD_DIR = os.path.join(INSTALL_DIR, "KiCad")
BASE_DIR = r"C:\FOSSEE\Tool-Manager"
INFO_JSON = os.path.join(BASE_DIR, "information.json")

# Available KiCad versions for the user to choose (displayed as 7.0.11 and 8.0.9)
KICAD_USER_VERSIONS = ["7.0.11", "8.0.9"]
# Internal versions used for file paths (7.0 and 8.0)
KICAD_INTERNAL_VERSIONS = {"7.0.11": "7.0", "8.0.9": "8.0"}

LATEST_VERSION = "8.0.9"  # Latest version to be shown in the dropdown
KICAD_PACKAGES = {v: f"kicad-{v}.exe" for v in KICAD_USER_VERSIONS}

# Define paths for KiCad library files
KICAD_LIBRARY_DIR = r"C:\FOSSEE\eSim\library\kicadLibrary"
KICAD_SYMBOLS_DIR = os.path.join(KICAD_DIR, "share", "kicad", "symbols")
KICAD_TEMPLATES_DIR = os.path.join(KICAD_DIR, "share", "kicad", "template")
SYM_LIB_TABLE_SOURCE = os.path.join(KICAD_LIBRARY_DIR, "template", "sym-lib-table")

def get_installed_version_from_json():
    """Get the installed KiCad version from the information.json file."""
    if os.path.exists(INFO_JSON):
        with open(INFO_JSON, "r") as f:
            data = json.load(f)
        for package in data["important_packages"]:
            if package["package_name"] == "kicad":
                return package["version"]
    return None

def update_information_json(version):
    """Update the information.json file with the installed version and date."""
    if os.path.exists(INFO_JSON):
        with open(INFO_JSON, "r") as f:
            data = json.load(f)
    else:
        data = {"important_packages": []}
    
    # Update or add the KiCad entry
    updated = False
    for package in data["important_packages"]:
        if package["package_name"] == "kicad":
            package["version"] = version
            package["installed_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            updated = True
            break
    
    if not updated:
        data["important_packages"].append({
            "package_name": "kicad",
            "version": version,
            "installed_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    with open(INFO_JSON, "w") as f:
        json.dump(data, f, indent=4)

def copy_kicad_libraries(version):
    """Copy the KiCad library files after installation."""
    # Get the internal version (7.0 or 8.0) from the user selected version (7.0.11 or 8.0.9)
    internal_version = KICAD_INTERNAL_VERSIONS[version]
    
    # Set the sym-lib-table destination path dynamically based on the selected version
    sym_lib_table_dest = os.path.join(os.environ['USERPROFILE'], "AppData", "Roaming", "kicad", internal_version, "sym-lib-table")
    sym_lib_table_dest_shared = os.path.join(KICAD_TEMPLATES_DIR, "sym-lib-table")
    
    # Copy symbols from the library
    if os.path.exists(KICAD_SYMBOLS_DIR):
        shutil.copytree(os.path.join(KICAD_LIBRARY_DIR, "eSim-symbols"), KICAD_SYMBOLS_DIR, dirs_exist_ok=True)
        print(f"Copied symbols to {KICAD_SYMBOLS_DIR}")
    else:
        print(f"{KICAD_SYMBOLS_DIR} does not exist!")

    # Copy sym-lib-table file
    if os.path.exists(SYM_LIB_TABLE_SOURCE):
        shutil.copy(SYM_LIB_TABLE_SOURCE, sym_lib_table_dest)
        print(f"Copied sym-lib-table from {SYM_LIB_TABLE_SOURCE} to {sym_lib_table_dest}")
        shutil.copy(SYM_LIB_TABLE_SOURCE, sym_lib_table_dest_shared)
        print(f"Copied sym-lib-table from {SYM_LIB_TABLE_SOURCE} to {sym_lib_table_dest_shared}")
    else:
        print(f"{SYM_LIB_TABLE_SOURCE} does not exist!")

class KiCadUpdater(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("KiCad Updater")
        self.setGeometry(200, 200, 400, 200)

        layout = QVBoxLayout()

        self.title_label = QLabel("KiCad Updater", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; padding: 10px 0;")
        layout.addWidget(self.title_label)

        # Get the installed version from the JSON
        self.installed_version = get_installed_version_from_json()

        # Display the installed version or a message if not found
        if self.installed_version:
            self.version_label = QLabel(f"Installed Version: {self.installed_version}")
        else:
            self.version_label = QLabel("Installed Version: Not found")
        
        self.version_label.setStyleSheet("font-size: 14px; padding: 10px 0;")
        layout.addWidget(self.version_label)

        # Status message
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        # Dropdown for version selection
        self.dropdown_label = QLabel("Select the KiCad version to update:")
        self.dropdown_label.setStyleSheet("font-size: 14px; padding: 5px 0;")
        layout.addWidget(self.dropdown_label)

        self.version_dropdown = QComboBox()
        self.version_dropdown.addItems(KICAD_USER_VERSIONS)
        self.version_dropdown.setStyleSheet("font-size: 14px; padding: 5px 0;")
        layout.addWidget(self.version_dropdown)

        # Update button
        self.update_button = QPushButton("Update KiCad")
        self.update_button.clicked.connect(self.install_kicad)
        self.update_button.setStyleSheet("font-size: 14px; padding: 10px 0;")
        layout.addWidget(self.update_button)

        self.setLayout(layout)

        # Check if the user is using the latest version
        self.check_for_updates()

    def check_for_updates(self):
        """Check if the installed version is the latest one."""
        if self.installed_version == LATEST_VERSION:
            self.update_status_label("You are using the latest version.", "green")
        elif self.installed_version:
            self.update_status_label("Please update. Your package is out of date.", "red")
        else:
            self.update_status_label("KiCad is not installed.", "red")

    def update_status_label(self, message, color="black"):
        """Update the status label with a message and color."""
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"color: {color}; font-size: 14px; padding: 10px 0;")

    def install_kicad(self):
        """Installs the selected KiCad version."""
        version = self.version_dropdown.currentText()
        package_name = KICAD_PACKAGES[version]
        archive_path = os.path.join(DOWNLOAD_DIR, package_name)

        if not os.path.exists(archive_path):
            self.update_status_label(f"Error: {package_name} not found in {DOWNLOAD_DIR}", "red")
            return

        # Install logic for KiCad (silent installation)
        install_command = [archive_path, "/S", "/allusers", f"/D={KICAD_DIR}"]
        try:
            result = subprocess.run(install_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Installation complete for {version}")
        except subprocess.CalledProcessError as e:
            self.update_status_label(f"Error during installation: {e}", "red")
            return

        # Copy libraries after installation
        copy_kicad_libraries(version)

        # Update UI after installation
        self.version_label.setText(f"Installed Version: {version}")
        self.update_status_label("Installation Complete!", "green")

        # Update the version in the JSON file after successful installation
        update_information_json(version)

        # Show popup message
        QMessageBox.information(self, "Update Complete", f"The KiCad is updated to version {version}.")

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KiCadUpdater()
    window.show()
    sys.exit(app.exec_())
