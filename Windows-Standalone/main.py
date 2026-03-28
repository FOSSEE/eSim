import os
import sys
import subprocess
import json
from PyQt5 import QtWidgets, QtGui, QtCore

from ngspice_package_manager import update_installation_status_ngspice
from kicad_package_manager import update_installation_status_kicad
from ghdl_package_manager import update_installation_status_ghdl
from llvm_package_manager import update_installation_status_llvm
from chocolatey import check_chocolatey_directory


# ================= PATH SETUP =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE_PATH = os.path.join(BASE_DIR, "install_details.json")

if not os.path.exists(JSON_FILE_PATH):
    with open(JSON_FILE_PATH, "w") as f:
        json.dump({
            "important_packages": [],
            "pip_packages": []
        }, f)

NGSPICE_INSTALL_PROGRAM = os.path.join(os.getcwd(), "ngspice_package_manager.py")
KICAD_INSTALL_PROGRAM = os.path.join(os.getcwd(), "kicad_package_manager.py")
LLVM_INSTALL_PROGRAM = os.path.join(os.getcwd(), "llvm_package_manager.py")
GHDL_INSTALL_PROGRAM = os.path.join(os.getcwd(), "ghdl_package_manager.py")
PYTHON_PACKAGES_INSTALL_PROGRAM = os.path.join(os.getcwd(), "python_package_manager.py")
CHOCOLATEY_INSTALL_PROGRAM = os.path.join(os.getcwd(), "chocolatey.py")


# ================= DETECTION FUNCTIONS =================
def check_python_package(pkg):
    try:
        subprocess.check_output(f"pip show {pkg}", shell=True)
        return True
    except:
        return False


def is_ghdl_installed():
    try:
        subprocess.check_output("ghdl --version", shell=True)
        return True
    except:
        return False


# ================= MAIN UI =================
class DependenciesInstallerApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        

        self.setWindowTitle("Tool Manager")
        self.resize(400, 550)

        # Center window
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        self.move(
            (screen.width() - self.width()) // 2,
            (screen.height() - self.height()) // 2
        )

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        # Progress Bar
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setValue(0)
        self.layout.addWidget(self.progress_bar)

        # Heading
        heading = QtWidgets.QLabel("Tool Manager for eSim")
        heading.setFont(QtGui.QFont("Arial", 12))
        heading.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(heading)

        # Status label
        self.status_label = QtWidgets.QLabel("")
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.status_label)

        # Chocolatey label
        self.choco_label = QtWidgets.QLabel("Chocolatey Status: Checking...")
        self.choco_label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.choco_label)

        # Button Style
        button_style = """
        QPushButton {
            font-size: 14px;
            padding: 8px;
            border-radius: 8px;
            background-color: lightgray;
        }
        QPushButton:hover {
            background-color: #87CEFA;
        }
        """

        # Buttons
        self.add_button("Install Chocolatey", self.install_chocolatey, button_style)
        self.add_button("Install Ngspice", self.install_ngspice, button_style)
        self.add_button("Install KiCad", self.install_kicad, button_style)
        self.add_button("Install LLVM", self.install_llvm, button_style)
        self.add_button("Install GHDL", self.install_ghdl, button_style)
        self.add_button("Install Python Packages", self.install_python_packages, button_style)
        self.refresh_all()
        

    # ================= HELPERS =================
    def add_button(self, text, func, style):
        btn = QtWidgets.QPushButton(text)
        btn.setStyleSheet(style)
        btn.clicked.connect(func)
        self.layout.addWidget(btn)

    def set_progress(self, value):
        self.progress_bar.setValue(value)
        QtWidgets.QApplication.processEvents()

    def reset_progress(self):
        self.progress_bar.setValue(0)

    def refresh_all(self):
        # Update JSON statuses
        update_installation_status_ngspice()
        update_installation_status_kicad()
        update_installation_status_llvm()
        update_installation_status_ghdl()
        check_chocolatey_directory(JSON_FILE_PATH)

        self.update_status_label()
       

    # ================= STATUS =================
    def check_dependencies(self):
        with open(JSON_FILE_PATH, "r") as f:
            data = json.load(f)

        status = {pkg["package_name"]: pkg["installed"]
                  for pkg in data.get("important_packages", [])}

        # Override GHDL with real detection
        status["ghdl"] = "Yes" if is_ghdl_installed() else "No"

        return (
            status.get("ngspice", "No"),
            status.get("kicad", "No"),
            status.get("llvm", "No"),
            status.get("ghdl", "No"),
            status.get("chocolatey", "No"),
        )

    def update_status_label(self):
        ng, kc, ll, gh, ch = self.check_dependencies()

        missing = []
        installed = []

        for name, val in [("Ngspice", ng), ("KiCad", kc), ("LLVM", ll), ("GHDL", gh)]:
            (installed if val == "Yes" else missing).append(name)

        
        self.status_label.setText(
            f"❌ Missing: {', '.join(missing)}\n✅ Installed: {', '.join(installed)}"
        )

        self.choco_label.setText(
            "Chocolatey Installed" if ch == "Yes" else "Chocolatey Not Installed"
        )
        self.choco_label.setStyleSheet(
            "color: green;" if ch == "Yes" else "color: red;"
        )



    # ================= INSTALL FUNCTIONS =================
    def run_installer(self, name, script):
        try:
            if not os.path.exists(script):
                QtWidgets.QMessageBox.critical(self, "Error", f"{name} installer not found")
                print("ERROR PATH:", script)
                return

            print("Running script:", script)

            self.progress_bar.setValue(0)
            self.status_label.setText(f"Installing {name}...")

            process = subprocess.Popen(
                [sys.executable, script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            for line in iter(process.stdout.readline, ''):
                if "|" in line:
                    value, text = line.strip().split("|", 1)
                    try:
                        self.set_progress(int(value.replace("%", "")))
                    except:
                        pass
                    self.status_label.setText(text)
                else:
                    self.status_label.setText(line.strip())

                QtWidgets.QApplication.processEvents()

            stdout, stderr = process.communicate()

            if process.returncode != 0:
                print("ERROR:", stderr)
                QtWidgets.QMessageBox.critical(self, "Error", f"{name} installation failed ❌")
                self.progress_bar.setValue(0)
                return

            self.set_progress(100)
            QtWidgets.QMessageBox.information(self, "Success", f"{name} Installed ✅")

            self.refresh_all()
            self.progress_bar.setValue(0)

        except Exception as e:
            self.progress_bar.setValue(0)
            QtWidgets.QMessageBox.critical(self, "Error", str(e))

    def install_ngspice(self):
        self.run_installer("Ngspice", NGSPICE_INSTALL_PROGRAM)

    def install_kicad(self):
        self.run_installer("KiCad", KICAD_INSTALL_PROGRAM)

    def install_llvm(self):
        self.run_installer("LLVM", LLVM_INSTALL_PROGRAM)

    def install_ghdl(self):
        self.run_installer("GHDL", GHDL_INSTALL_PROGRAM)

    def install_chocolatey(self):
        self.run_installer("Chocolatey", CHOCOLATEY_INSTALL_PROGRAM)

    def install_python_packages(self):
        try:
            self.run_installer("Python Packages", PYTHON_PACKAGES_INSTALL_PROGRAM)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e))

# ================= MAIN =================
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = DependenciesInstallerApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()