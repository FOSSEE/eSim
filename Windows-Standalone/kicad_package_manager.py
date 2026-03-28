import os
import json
import subprocess
import shutil
import datetime
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox
from logging_setup import log_info, log_error, log_warning

# Paths and constants
TOOLS_DIR = os.path.join(os.getcwd(), "tools")
KICAD_DIR = os.path.join(TOOLS_DIR, "kicad")
JSON_FILE_PATH = os.path.join(os.getcwd(), "install_details.json")
INSTALL_COMMAND = lambda version: f"choco install -y kicad --version={version}"

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



def get_kicad_install_path():
    possible_paths = [
        "C:\\Program Files\\KiCad",
        "C:\\Program Files (x86)\\KiCad"
    ]
    return next((p for p in possible_paths if os.path.exists(p)), None)




# Update installation status
def update_installation_status_kicad():
    try:
        data = load_json_data()
        package = find_package(data, "kicad")

        install_path = get_kicad_install_path()

        if package:
            if install_path:
                package.update({
                    "version": package.get("version", "-"),
                    "installed": "Yes",
                    "installed_date": package.get("installed_date", "-"),
                    "install_directory": install_path
                })
                log_info("KiCad detected in system.")
            else:
                package.update({
                    "version": "-",
                    "installed": "No",
                    "installed_date": "-",
                    "install_directory": "-"
                })
                log_warning("KiCad not found. Marked as not installed.")
        else:
            data["important_packages"].append({
                "package_name": "kicad",
                "version": "-",
                "installed": "No",
                "installed_date": "-",
                "install_directory": "-"
            })

        save_json_data(data)

    except Exception as e:
        log_error(f"Error updating KiCad status: {e}")



def fetch_latest_versions():
    try:
        result = subprocess.run(
            "choco search kicad --exact --all-versions",
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        versions = []
        for line in result.stdout.splitlines():
            if line.startswith("kicad"):
                parts = line.split()
                if len(parts) > 1:
                    version_string = parts[1].strip()
                    if version_string.replace('.', '').isdigit():
                        versions.append(version_string)
        log_info("Fetched latest KiCad versions.")
        return versions[:3] if versions else ["Unknown"]
    except subprocess.CalledProcessError as e:
        log_error(f"Failed to fetch KiCad versions: {e}")
        return ["Unknown"]

def install_kicad(selected_version, progress_callback=None):
    try:
        if not selected_version:
            return "Please select a version."

        command = f"choco install -y kicad --version={selected_version}"
        log_info(f"Running command: {command}")

        #  Run with progress
        run_command_with_progress(command, progress_callback)

        # Move installed files
        # ✅ KiCad installs in Program Files
        kicad_install_path = "C:\\Program Files\\KiCad"

        if not os.path.exists(kicad_install_path):
            return "Installation failed: KiCad not found in Program Files."

        install_directory = kicad_install_path

        # Update JSON
        data = load_json_data()
        package = find_package(data, "kicad")
        installed_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if package:
            package.update({
                "version": selected_version,
                "installed": "Yes",
                "installed_date": installed_date,
                "install_directory": KICAD_DIR
            })
        else:
            data["important_packages"].append({
                "package_name": "kicad",
                "version": selected_version,
                "installed": "Yes",
                "installed_date": installed_date,
                "install_directory": KICAD_DIR
            })

        save_json_data(data)

        return f"KiCad version {selected_version} installed successfully."

    except Exception as e:
        log_error(f"Error installing KiCad: {e}")
        return f"Error: {e}"


from dependencies import run_command_with_progress




def update_kicad(progress_callback=None):
    latest_versions = fetch_latest_versions()
    latest_version = latest_versions[0] if latest_versions and latest_versions[0] != "Unknown" else None

    if not latest_version:
        return "Failed to fetch latest version."

    try:
        command = f"choco install -y kicad --version={latest_version}"

        # ✅ Run with progress
        run_command_with_progress(command, progress_callback)

        # ✅ KiCad installs in Program Files
        possible_paths = [
            "C:\\Program Files\\KiCad",
            "C:\\Program Files (x86)\\KiCad"
        ]

        install_directory = next((p for p in possible_paths if os.path.exists(p)), None)

        if not install_directory:
            return "Installation failed: KiCad not found in Program Files."

        # ✅ FIX: define installed_date
        installed_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # ✅ Update JSON
        data = load_json_data()
        package = find_package(data, "kicad")

        if package:
            package.update({
                "version": latest_version,
                "installed": "Yes",
                "installed_date": installed_date,
                "install_directory": install_directory
            })
        else:
            data["important_packages"].append({
                "package_name": "kicad",
                "version": latest_version,
                "installed": "Yes",
                "installed_date": installed_date,
                "install_directory": install_directory
            })

        # ✅ FIX: save JSON
        save_json_data(data)

        return f"KiCad updated successfully to version {latest_version}"

    except Exception as e:
        log_error(f"Error updating KiCad: {e}")
        return f"Error: {e}"


class KiCadInstallerApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def get_button_style(self):
        return """
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



    def init_ui(self):
        self.setWindowTitle("KiCad Installer")
        self.resize(400, 400)
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

        layout = QVBoxLayout()

        from PyQt5.QtWidgets import QProgressBar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)



        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # Title label
        title_label = QLabel("Install KiCad with GUI")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title_label)

        # Update the JSON status file on launch
        update_installation_status_kicad()
        
        # Fetch the latest versions
        self.latest_versions = fetch_latest_versions()

        # Get installed version
        data = load_json_data()
        kicad_package = find_package(data, "kicad")
        install_path = get_kicad_install_path()

        if install_path:
            self.installed_version = kicad_package["version"] if kicad_package else "Unknown"
        else:
            self.installed_version = "Not Installed"

        # Display installed and latest versions
        self.installed_version_label = QLabel(
            f"Installed Version: {self.installed_version}"
            if self.installed_version != "Not Installed"
            else "KiCad is not installed"
        )
        self.installed_version_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.installed_version_label)

        self.latest_version_label = QLabel(
            f"Latest Version: {self.latest_versions[0]}"
            if self.latest_versions and self.latest_versions[0] != "Unknown"
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
            and self.latest_versions
            and self.latest_versions[0] != "Unknown"
        ):
            is_outdated = self.installed_version < self.latest_versions[0]
            if is_outdated:
                self.update_label.setText("Your version is out of date. Please update.")
                self.update_label.setStyleSheet("color: red;")
            else:
                self.update_label.setText("You are using the latest version.")
                self.update_label.setStyleSheet("color: green;")

        # Dropdown for version selection
        dropdown_label = QLabel("Select KiCad Version:")
        dropdown_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(dropdown_label)

        self.version_dropdown = QComboBox()
        self.version_dropdown.addItems(self.latest_versions)
        self.version_dropdown.setStyleSheet(self.get_dropdown_style())
        layout.addWidget(self.version_dropdown)

        # Install button
        install_button = QPushButton("Install KiCad")
    
        install_button.setStyleSheet(self.get_button_style())
        install_button.clicked.connect(self.install_button_action)
        layout.addWidget(install_button)

        # Update button
        update_button = QPushButton("Update KiCad")
        update_button.setStyleSheet(self.get_button_style())
        update_button.clicked.connect(self.update_button_action)
        layout.addWidget(update_button)

        self.setLayout(layout)

    def install_button_action(self):
        data = load_json_data()
        package = find_package(data, "kicad")
        self.installed_version = package["version"] if package and package["installed"] == "Yes" else "Not Installed"

        if self.installed_version != "Not Installed":
            QMessageBox.information(self, "Installation Status", "The KiCad package is already installed.")
            return

        selected_version = self.version_dropdown.currentText()
        if not selected_version:
            QMessageBox.critical(self, "Error", "Please select a version.")
            return

    # ✅ RESET BAR
        self.progress_bar.setValue(0)

    # ✅ Progress callback
        def update_progress(output):
            self.progress_bar.setValue(min(self.progress_bar.value() + 5, 95))
            QtWidgets.QApplication.processEvents()

    # ✅ Run install
        result = install_kicad(selected_version, update_progress)

    # ✅ COMPLETE
        self.progress_bar.setValue(100)

        QMessageBox.information(self, "Installation Status", result)

    # ✅ Reset smoothly
        QtCore.QTimer.singleShot(1500, lambda: self.progress_bar.setValue(0))

        update_installation_status_kicad()
        self.update_labels()

    def update_button_action(self):
        self.progress_bar.setValue(0)

        def update_progress(output):
            self.progress_bar.setValue(min(self.progress_bar.value() + 5, 95))
            QtWidgets.QApplication.processEvents()

        result = update_kicad(update_progress)

        self.progress_bar.setValue(100)

        QMessageBox.information(self, "Update Status", result)

    # ✅ Smooth reset
        QtCore.QTimer.singleShot(1500, lambda: self.progress_bar.setValue(0))

        update_installation_status_kicad()
        self.update_labels()

    def update_labels(self):
        install_path = get_kicad_install_path()

        data = load_json_data()
        package = find_package(data, "kicad")

        if install_path:
            version = package["version"] if package else "Unknown"
            self.installed_version = version
            self.installed_version_label.setText(f"Installed Version: {version}")
        else:
            self.installed_version = "Not Installed"
            self.installed_version_label.setText("KiCad is not installed")

        if self.installed_version == self.latest_versions[0]:
            self.update_label.setText("You are using the latest version.")
            self.update_label.setStyleSheet("color: green;")
        else:
            self.update_label.setText("Your version is out of date. Please update.")
            self.update_label.setStyleSheet("color: red;")

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
    window = KiCadInstallerApp()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
