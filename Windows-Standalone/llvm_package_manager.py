import os
import json
import subprocess
import datetime
import shutil
from packaging import version
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox, QProgressBar

# Paths
TOOLS_DIR = os.path.join(os.getcwd(), "tools")
LLVM_DIR = os.path.join(TOOLS_DIR, "llvm")
CHOCO_PATH = "C:\\ProgramData\\chocolatey\\lib\\llvm"
JSON_FILE_PATH = os.path.join(os.getcwd(), "install_details.json")

os.makedirs(TOOLS_DIR, exist_ok=True)


# ---------------- JSON ---------------- #
def load_json():
    if os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, "r") as f:
            return json.load(f)
    return {"important_packages": []}


def save_json(data):
    with open(JSON_FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)


def get_package(data):
    return next((p for p in data["important_packages"] if p["package_name"] == "llvm"), None)


# ---------------- VERSION ---------------- #
def fetch_versions():
    try:
        result = subprocess.run(
            "choco search llvm --exact --all-versions",
            shell=True,
            capture_output=True,
            text=True
        )

        versions = []
        for line in result.stdout.splitlines():
            if line.startswith("llvm"):
                v = line.split()[1]
                if v.replace(".", "").isdigit():
                    versions.append(v)

        return versions[:3] if versions else ["Unknown"]

    except:
        return ["Unknown"]


# ---------------- WORKER ---------------- #
class Worker(QtCore.QThread):
    progress = QtCore.pyqtSignal(int)
    finished = QtCore.pyqtSignal(str)

    def __init__(self, version):
        super().__init__()
        self.version = version

    def run(self):
        try:
            cmd = f"choco install -y llvm --version={self.version}"

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                shell=True
            )

            progress = 0

            for line in process.stdout:
                if "Downloading" in line:
                    progress = 30
                elif "Installing" in line:
                    progress = 60
                elif "installed" in line.lower():
                    progress = 90

                self.progress.emit(progress)

            process.wait()

            if process.returncode != 0:
                self.finished.emit("Installation failed")
                return

            # FIX PATH
            if os.path.exists(LLVM_DIR):
                shutil.rmtree(LLVM_DIR)

            if os.path.exists(CHOCO_PATH):
                shutil.move(CHOCO_PATH, LLVM_DIR)

            # SAVE JSON
            data = load_json()
            pkg = get_package(data)

            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if pkg:
                pkg.update({
                    "version": self.version,
                    "installed": "Yes",
                    "installed_date": now,
                    "install_directory": LLVM_DIR
                })
            else:
                data["important_packages"].append({
                    "package_name": "llvm",
                    "version": self.version,
                    "installed": "Yes",
                    "installed_date": now,
                    "install_directory": LLVM_DIR
                })

            save_json(data)

            self.progress.emit(100)
            self.finished.emit("Success")

        except Exception as e:
            self.finished.emit(str(e))
import os
import json
import datetime

JSON_FILE_PATH = os.path.join(os.getcwd(), "install_details.json")
LLVM_DIR = os.path.join(os.getcwd(), "tools", "llvm")


def update_installation_status_llvm():
    try:
        # Load JSON
        if os.path.exists(JSON_FILE_PATH):
            with open(JSON_FILE_PATH, "r") as f:
                data = json.load(f)
        else:
            data = {"important_packages": []}

        # Find LLVM package
        package = None
        for pkg in data.get("important_packages", []):
            if pkg["package_name"] == "llvm":
                package = pkg
                break

        # Check if installed
        if os.path.exists(LLVM_DIR):
            version = "-"
            installed = "Yes"
            install_dir = LLVM_DIR
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            version = "-"
            installed = "No"
            install_dir = "-"
            date = "-"

        # Update or add
        if package:
            package.update({
                "version": version,
                "installed": installed,
                "installed_date": date,
                "install_directory": install_dir
            })
        else:
            data["important_packages"].append({
                "package_name": "llvm",
                "version": version,
                "installed": installed,
                "installed_date": date,
                "install_directory": install_dir
            })

        # Save JSON
        with open(JSON_FILE_PATH, "w") as f:
            json.dump(data, f, indent=4)

        print("LLVM status updated")

    except Exception as e:
        print("Error updating LLVM status:", e)

# ---------------- UI ---------------- #
class LLVMInstallerApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("LLVM Installer")
        self.resize(400, 400)

        layout = QVBoxLayout()

        title = QLabel("Install LLVM with GUI")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        self.versions = fetch_versions()

        self.installed_label = QLabel("")
        layout.addWidget(self.installed_label)

        self.latest_label = QLabel("")
        layout.addWidget(self.latest_label)

        self.update_label = QLabel("")
        layout.addWidget(self.update_label)

        self.dropdown = QComboBox()
        self.dropdown.addItems(self.versions)
        layout.addWidget(self.dropdown)

        # ONLY ADDITION
        self.progress = QProgressBar()
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        install_btn = QPushButton("Install LLVM")
        install_btn.clicked.connect(self.install)
        layout.addWidget(install_btn)

        update_btn = QPushButton("Update LLVM")
        update_btn.clicked.connect(self.update)
        layout.addWidget(update_btn)

        self.setLayout(layout)

        # INITIAL LOAD
        self.refresh_ui()

    # ---------------- REFRESH ---------------- #
    def refresh_ui(self):
        data = load_json()
        pkg = get_package(data)

        latest = self.versions[0] if self.versions else "-"

        self.latest_label.setText(f"Latest Version: {latest}")

        if pkg and pkg.get("installed") == "Yes":
            installed = pkg.get("version", "-")
            self.installed_label.setText(f"Installed Version: {installed}")

            try:
                if version.parse(installed) < version.parse(latest):
                    self.update_label.setText("Your version is out of date. Please update.")
                    self.update_label.setStyleSheet("color:red;")
                else:
                    self.update_label.setText("You are using the latest version.")
                    self.update_label.setStyleSheet("color:green;")
            except:
                self.update_label.setText("")
        else:
            self.installed_label.setText("LLVM is not installed")
            self.update_label.setText("")

    # ---------------- INSTALL ---------------- #
    def install(self):
        version_selected = self.dropdown.currentText()

        self.worker = Worker(version_selected)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.finished.connect(self.done)

        self.progress.setValue(0)
        self.worker.start()

    # ---------------- UPDATE ---------------- #
    def update(self):
        latest = self.versions[0]

        self.worker = Worker(latest)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.finished.connect(self.done)

        self.progress.setValue(0)
        self.worker.start()

    def done(self, msg):
        QMessageBox.information(self, "Status", msg)

        # REFRESH EVERYTHING
        self.versions = fetch_versions()
        self.dropdown.clear()
        self.dropdown.addItems(self.versions)

        self.refresh_ui()


# ---------------- MAIN ---------------- #
def main():
    app = QtWidgets.QApplication([])
    window = LLVMInstallerApp()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()