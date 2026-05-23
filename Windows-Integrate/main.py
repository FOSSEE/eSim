import os
import sys
import json
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import Qt


LOG_FILE = r"C:\FOSSEE\Tool-Manager\logs.txt"

from datetime import datetime

def write_log(message):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{time}] {message}\n")
# Path to the information.json file
INFO_JSON = r"C:\FOSSEE\Tool-Manager\information.json"


def get_version_safe(tool_name):
    try:
        exe_path = None
        cmd = []

        # ---------- KiCad ----------
        if tool_name == "kicad":
            exe_path = r"C:\FOSSEE\KiCad\bin\kicad-cli.exe"
            cmd = [exe_path, "--version"]

        # ---------- Ngspice ----------
        elif tool_name == "ngspice":
            exe_path = r"C:\FOSSEE\nghdl-simulator\bin\ngspice.exe"

            if not os.path.exists(exe_path):
                return "Not Installed"

            try:
        # Run ngspice in batch mode (NO GUI)
                result = subprocess.run(
                    [exe_path, "-b", "-v"],
                    capture_output=True,
                    text=True,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )

                output = (result.stdout + result.stderr).strip()

                if not output:
                    return "Unknown"

        # Extract version line
                for line in output.split("\n"):
                    if "ngspice" in line.lower():
                        return line.strip()

                return output.split("\n")[0]

            except Exception:
                return "Error"
        # ---------- GHDL ----------
        elif tool_name == "ghdl":
            exe_path = r"C:\FOSSEE\MSYS\mingw64\bin\ghdl.exe"
            cmd = [exe_path, "--version"]

        # ---------- Verilator ----------
        elif tool_name == "verilator":
            possible_paths = [
                r"C:\FOSSEE\MSYS\mingw64\bin\verilator.exe",
                r"C:\FOSSEE\MSYS\mingw64\bin\verilator_bin.exe"
            ]

            for path in possible_paths:
                if os.path.exists(path):
                    exe_path = path
                    break

            if not exe_path:
                return "Not Installed"

            cmd = [exe_path, "--version"]

        else:
            return "Unknown"

        # Final check
        if not exe_path or not os.path.exists(exe_path):
            return "Not Installed"

        # 🔥 Prevent opening GUI apps
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        output = (result.stdout + result.stderr).strip()

        if not output:
            return "Unknown"

        return output.split("\n")[0]

    except FileNotFoundError:
        return "Not Installed"
    except Exception:
        return "Error"





class ToolManagerUpdater(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("eSim Tool Manager (Updater)")

        self.resize(400, 300)
        self.adjust_position()

        layout = QVBoxLayout()

        self.title_label = QLabel("eSim Tool Manager (Updater)", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; padding: 10px 0;")
        layout.addWidget(self.title_label)

        # Fetch versions
        kicad_version = get_version_safe("kicad")
        ngspice_version = get_version_safe("ngspice")
        ghdl_version = get_version_safe("ghdl")
        verilator_version = get_version_safe("verilator")

        # Display versions
        self.kicad_version_label = QLabel(f"KiCad Version: {kicad_version}")
        self.kicad_version_label.setStyleSheet("font-size: 14px;")
        self.ngspice_version_label = QLabel(f"Ngspice Version: {ngspice_version}")
        self.ngspice_version_label.setStyleSheet("font-size: 14px;")
        self.ghdl_version_label = QLabel(f"GHDL Version: {ghdl_version}")
        self.ghdl_version_label.setStyleSheet("font-size: 14px;")
        self.verilator_version_label = QLabel(f"Verilator Version: {verilator_version}")
        self.verilator_version_label.setStyleSheet("font-size: 14px;")

        layout.addWidget(self.kicad_version_label)
        layout.addWidget(self.ngspice_version_label)
        layout.addWidget(self.ghdl_version_label)
        layout.addWidget(self.verilator_version_label)

        # Buttons
        self.update_kicad_button = QPushButton("Update KiCad")
        self.update_kicad_button.clicked.connect(self.run_kicad_gui)
        layout.addWidget(self.update_kicad_button)

        self.update_ngspice_button = QPushButton("Update Ngspice")
        self.update_ngspice_button.clicked.connect(self.run_ngspice_gui)
        layout.addWidget(self.update_ngspice_button)

        self.download_ghdl_button = QPushButton("Download Packages")
        self.download_ghdl_button.clicked.connect(self.run_ghdl_download_packages)
        layout.addWidget(self.download_ghdl_button)

        self.update_ghdl_button = QPushButton("Update GHDL")
        self.update_ghdl_button.clicked.connect(self.run_ghdl_gui)
        layout.addWidget(self.update_ghdl_button)

        self.update_verilator_button = QPushButton("Update Verilator")
        self.update_verilator_button.clicked.connect(self.run_verilator_gui)
        layout.addWidget(self.update_verilator_button)

        
        # Dependencies Check Button
        self.dep_btn = QPushButton("Check Dependencies")
        self.dep_btn.clicked.connect(self.check_dependencies)
        layout.addWidget(self.dep_btn)
        self.fix_btn = QPushButton("Auto Fix Dependencies")
        self.fix_btn.clicked.connect(self.auto_fix_dependencies)
        layout.addWidget(self.fix_btn)
        # Logs Viewer Button
        self.logs_btn = QPushButton("View Logs")
        self.logs_btn.clicked.connect(self.view_logs)
        layout.addWidget(self.logs_btn)
        self.setLayout(layout)
    def adjust_position(self):
        screen = QApplication.primaryScreen().availableGeometry()
        widget = self.geometry()
        x = (screen.width() - widget.width()) // 2
        y = (screen.height() - widget.height()) // 3
        self.move(x, y)

    def run_kicad_gui(self):
        try:
            write_log("Running KiCad Update")
            subprocess.Popen([sys.executable, "kicad_gui.py"])
            write_log("KiCad Updated successfully")
            self.refresh_versions()
        except subprocess.CalledProcessError as e:
            write_log(f"KiCad Update Failed: {e}")
            QMessageBox.critical(self, "Error", f"Failed to run KiCad update: {e}")

    def run_ngspice_gui(self):
        try:
            write_log("Running Ngspice Update")
            subprocess.Popen([sys.executable, "ngspice_gui.py"])
            write_log("Ngspice Updated Successfully")
            self.refresh_versions()
        except subprocess.CalledProcessError as e:
            write_log(f"Ngspice Update Failed: {e}")
            QMessageBox.critical(self, "Error", f"Failed to run Ngspice update: {e}")

    def run_ghdl_download_packages(self):
        try:
            write_log(" Downloading Packages ")
            subprocess.Popen([sys.executable, "download_packages.py"])
            write_log("Downloaded Packages Successfully")
            self.refresh_versions()
        except subprocess.CalledProcessError as e:
            write_log(f"Downloading Packages Failed: {e}")
            QMessageBox.critical(self, "Error", f"Failed to download GHDL packages: {e}")

    def run_ghdl_gui(self):
        try:
            write_log("Running GHDL Update")
            subprocess.Popen([sys.executable, "ghdl_gui.py"])
            write_log("GHDL Updated Successfully")
            self.refresh_versions()
        except subprocess.CalledProcessError as e:
            write_log(f"GHDL Update Failed: {e}")
            QMessageBox.critical(self, "Error", f"Failed to run GHDL update: {e}")

    def run_verilator_gui(self):
        try:
            write_log("Running Verilator Update")
            subprocess.Popen([sys.executable, "verilator_gui.py"])
            write_log("Verilator Updated Successfully")
            self.refresh_versions()
        except subprocess.CalledProcessError as e:
            write_log(f"Verilator Update Failed: {e}")
            QMessageBox.critical(self, "Error", f"Failed to run Verilator update: {e}")

    def refresh_versions(self):
        self.kicad_version_label.setText(f"KiCad: {get_version_safe('kicad')}")
        self.ngspice_version_label.setText(f"Ngspice: {get_version_safe('ngspice')}")
        self.ghdl_version_label.setText(f"GHDL: {get_version_safe('ghdl')}")
        self.verilator_version_label.setText(f"Verilator: {get_version_safe('verilator')}")
    def check_dependencies(self):
        missing = []

    # Check Python
        try:
            import sys
        except:
            missing.append("Python")

    # Check required libraries
        try:
            import py7zr
        except:
            missing.append("py7zr")

        try:
            import requests
        except:
            missing.append("requests")

    # Check tools paths
        verilator_path = r"C:\FOSSEE\MSYS\mingw64\bin\verilator_bin.exe"
        ngspice_path = r"C:\FOSSEE\nghdl-simulator\bin\ngspice.exe"
        ghdl_path = r"C:\FOSSEE\MSYS\mingw64\bin\ghdl.exe"
        kicad_path = r"C:\FOSSEE\KiCad\bin\kicad-cli.exe"

        if not os.path.exists(verilator_path):
            missing.append("Verilator")

        if not os.path.exists(ngspice_path):
            missing.append("Ngspice")

        if not os.path.exists(ghdl_path):
            missing.append("GHDL")

        if not os.path.exists(kicad_path):
            missing.append("KiCad")

    # ✅ Show result AFTER ALL CHECKS
        if missing:
            QMessageBox.warning(
                self,
                "Missing Dependencies",
                "Missing:\n" + "\n".join(missing)
            )
        else:
            QMessageBox.information(
                self,
                "All Good",
                "All dependencies are installed "
            )
    def auto_fix_dependencies(self):
        missing = []

        verilator_path = r"C:\FOSSEE\MSYS\mingw64\bin\verilator_bin.exe"
        ngspice_path = r"C:\FOSSEE\nghdl-simulator\bin\ngspice.exe"
        ghdl_path = r"C:\FOSSEE\MSYS\mingw64\bin\ghdl.exe"
        kicad_path = r"C:\FOSSEE\KiCad\bin\kicad-cli.exe"

        if not os.path.exists(verilator_path):
            missing.append("verilator_gui.py")

        if not os.path.exists(ngspice_path):
            missing.append("ngspice_gui.py")

        if not os.path.exists(ghdl_path):
            missing.append("ghdl_gui.py")

        if not os.path.exists(kicad_path):
            missing.append("kicad_gui.py")

        if not missing:
            QMessageBox.information(self, "All Good", "Nothing to fix ")
            return

        for script in missing:
            try:
                write_log(f"Auto fixing using {script}")
                subprocess.run([sys.executable, script], check=True)
            except Exception as e:
                write_log(f"Auto fix failed for {script}: {e}")

        QMessageBox.information(self, "Done", "Auto-fix process completed ")
        self.refresh_versions()



    def view_logs(self):
        log_file = r"C:\FOSSEE\Tool-Manager\logs.txt"

        if not os.path.exists(log_file):
            QMessageBox.warning(self, "Error", "Log file not found!")
            return

        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit

        dialog = QDialog(self)
        dialog.setWindowTitle("Logs")
        dialog.resize(600, 400)

        layout = QVBoxLayout()

        text_area = QTextEdit()
        text_area.setReadOnly(True)

        with open(log_file, "r") as file:
            text_area.setText(file.read())

        layout.addWidget(text_area)
        dialog.setLayout(layout)

        dialog.exec_()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToolManagerUpdater()
    window.show()
    sys.exit(app.exec_())