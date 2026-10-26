import importlib.metadata
import os
import sys
import subprocess
import yaml

from PyQt5.QtCore import QObject, Qt, pyqtSignal, QRunnable, QThreadPool, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *

try:
    from tool_manager_gui import dependency, installer
except ImportError:
    import dependency
    import installer


# ---------------- SIGNALS ----------------
class WorkerSignals(QObject):
    log = pyqtSignal(str)
    error = pyqtSignal(str)
    finished = pyqtSignal()
    progress = pyqtSignal(str, int)


# ---------------- WORKER ----------------
class Worker(QRunnable):
    def __init__(self, fn):
        super().__init__()
        self.fn = fn
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            self.fn(self.signals)
        except Exception as e:
            self.signals.error.emit(str(e))
        finally:
            self.signals.finished.emit()


# ---------------- GUI ----------------
class ToolManagerGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.threadpool = QThreadPool()
        self.progress_bars = {}
        self.log_buffer = []

        self.setWindowTitle(f"eSim Tool Manager - v{self.show_version()}")
        self.setGeometry(400, 200, 900, 550)

        self.tools_data = self.load_tools_yaml()

        self.init_ui()
        self.update_dependency_status()

    # ---------- YAML ----------
    def load_tools_yaml(self):
        try:
            path = os.path.join(os.path.dirname(__file__), "tools.yml")
            with open(path, encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            return data.get("tools", {})
        except Exception as e:
            print("YAML Error:", e)
            return {}

    # ---------- UI ----------
    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()

        title = QLabel("eSim Tool Manager")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Tool", "Version", "Description", "Installed", "Status"]
        )
        self.table.setRowCount(len(self.tools_data))

        for row, (tool, info) in enumerate(self.tools_data.items()):
            checkbox = QCheckBox(tool)
            self.table.setCellWidget(row, 0, checkbox)

            combo = QComboBox()
            combo.addItems(["latest"] + info.get("versions", []))
            self.table.setCellWidget(row, 1, combo)

            self.table.setItem(row, 2, QTableWidgetItem(info.get("description", "")))
            self.table.setItem(row, 3, QTableWidgetItem("-"))
            self.table.setItem(row, 4, QTableWidgetItem("Checking..."))

        layout.addWidget(self.table)

        # Buttons
        btn_layout = QHBoxLayout()

        self.install_btn = QPushButton("Install")
        self.install_btn.clicked.connect(self.install_tool)
        btn_layout.addWidget(self.install_btn)

        self.update_btn = QPushButton("Update")
        self.update_btn.clicked.connect(self.update_tool)
        btn_layout.addWidget(self.update_btn)

        self.uninstall_btn = QPushButton("Uninstall")
        self.uninstall_btn.clicked.connect(self.uninstall_tool)
        btn_layout.addWidget(self.uninstall_btn)

        layout.addLayout(btn_layout)

        # Refresh
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.update_dependency_status)
        layout.addWidget(self.refresh_btn)

        # Output
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        # Command
        cmd_layout = QHBoxLayout()

        self.command_input = QLineEdit()
        self.command_input.returnPressed.connect(self.execute_command)
        cmd_layout.addWidget(self.command_input)

        run_btn = QPushButton("Run")
        run_btn.clicked.connect(self.execute_command)
        cmd_layout.addWidget(run_btn)

        layout.addLayout(cmd_layout)

        central.setLayout(layout)

    # ---------- PROGRESS ----------
    def add_progress_column(self):
        if self.table.columnCount() == 5:
            self.table.insertColumn(5)
            self.table.setHorizontalHeaderItem(5, QTableWidgetItem("Progress"))

    def remove_progress_column(self):
        if self.table.columnCount() == 6:
            self.table.removeColumn(5)
        self.progress_bars.clear()

    def add_progress_bar(self, row, tool_name):
        bar = QProgressBar()
        bar.setRange(0, 100)
        bar.setValue(0)

        bar.setStyleSheet("""
        QProgressBar {
            border: none;
            background-color: #1e1e2e;
            border-radius: 8px;
            text-align: center;
            color: white;
        }
        QProgressBar::chunk {
            background-color: #7aa2f7;
            border-radius: 8px;
        }
        """)

        self.table.setCellWidget(row, 5, bar)
        self.progress_bars[tool_name] = bar

    def update_progress(self, tool, value):
        if tool in self.progress_bars:
            self.progress_bars[tool].setValue(value)

    # ---------- LOG ----------
    def log(self, text):
        self.log_buffer.append(text)
        if len(self.log_buffer) >= 5:
            self.output.append("\n".join(self.log_buffer))
            self.log_buffer.clear()

    # ---------- TASK RUNNER ----------
    def run_task(self, task):
        worker = Worker(task)

        worker.signals.log.connect(self.log)
        worker.signals.error.connect(lambda e: self.log(f"Error: {e}"))
        worker.signals.progress.connect(self.update_progress)
        worker.signals.finished.connect(self.task_done)

        self.threadpool.start(worker)

    def task_done(self):
        self.update_dependency_status()
        self.remove_progress_column()

    # ---------- SELECT ----------
    def get_selected(self):
        selected = []
        for row in range(self.table.rowCount()):
            if self.table.cellWidget(row, 0).isChecked():
                tool = self.table.cellWidget(row, 0).text()
                version = self.table.cellWidget(row, 1).currentText()
                selected.append((tool, version, row))
        return selected

    # ---------- ACTIONS ----------
    def install_tool(self):
        selected = self.get_selected()
        if not selected:
            self.log("Select tools first")
            return

        self.add_progress_column()

        for t, _, row in selected:
            self.add_progress_bar(row, t)

        def task(signals):
            total = len(selected)

            for i, (t, v, _) in enumerate(selected):
                try:
                    signals.log.emit(f"Installing {t} ({v})...")
                    installer.install_tool(t, version=v, log=signals.log.emit)

                    progress = int(((i + 1) / total) * 100)
                    signals.progress.emit(t, progress)

                except Exception as e:
                    signals.log.emit(f"{t} failed: {e}")

        self.run_task(task)

    def update_tool(self):
        selected = self.get_selected()
        if not selected:
            self.log("Select tools first")
            return

        self.add_progress_column()

        for t, _, row in selected:
            self.add_progress_bar(row, t)

        def task(signals):
            results = dependency.check_dependencies()
            installed_map = {t.lower(): status for t, status, _ in results}

            total = len(selected)

            for i, (t, _, _) in enumerate(selected):
                try:
                    if installed_map.get(t.lower()) != "installed":
                        signals.log.emit(f"{t} not installed. Skipping.")
                        continue

                    installer.install_tool(t, version="latest", log=signals.log.emit)

                    progress = int(((i + 1) / total) * 100)
                    signals.progress.emit(t, progress)

                except Exception as e:
                    signals.log.emit(f"{t} update failed: {e}")

        self.run_task(task)

    def uninstall_tool(self):
        selected = self.get_selected()
        if not selected:
            self.log("Select tools first")
            return

        self.add_progress_column()

        for t, _, row in selected:
            self.add_progress_bar(row, t)

        def task(signals):
            total = len(selected)

            for i, (t, _, _) in enumerate(selected):
                try:
                    installer.uninstall_tool(t, log=signals.log.emit)

                    progress = int(((i + 1) / total) * 100)
                    signals.progress.emit(t, progress)

                except Exception as e:
                    signals.log.emit(f"{t} uninstall failed: {e}")

        self.run_task(task)

    # ---------- STATUS ----------
    def update_dependency_status(self):
        try:
            results = dependency.check_dependencies()
            data = {t.lower(): (s, v) for t, s, v in results}

            for row in range(self.table.rowCount()):
                tool = self.table.cellWidget(row, 0).text().lower()
                status, version = data.get(tool, ("not installed", "-"))

                self.table.setItem(row, 3, QTableWidgetItem(version))
                self.table.setItem(row, 4, QTableWidgetItem(status))

        except Exception as e:
            self.log(str(e))

    # ---------- COMMAND ----------
    def execute_command(self):
        cmd = self.command_input.text().strip()
        self.command_input.clear()
        self.log(f"> {cmd}")

    # ---------- VERSION ----------
    def show_version(self):
        try:
            return importlib.metadata.version("esim-tools-manager")
        except:
            return "0.2"


# ---------- MAIN ----------
def main():
    app = QApplication(sys.argv)
    win = ToolManagerGUI()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()