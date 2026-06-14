#!/usr/bin/env python3
import os
import sys
import ctypes
import subprocess
import platform
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QProgressBar,
    QCheckBox, QComboBox,
    QPushButton, QLabel, QMessageBox, QTextEdit, QInputDialog, QLineEdit,
    QAbstractItemView
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
import logging

PYTHON     = sys.executable
SYSTEM     = platform.system()
IS_WINDOWS = SYSTEM == "Windows"
IS_LINUX   = SYSTEM == "Linux"

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if IS_WINDOWS:
    BACKEND = os.path.join(BASE_DIR, "tool_manager_windows.py")
elif IS_LINUX:
    BACKEND = os.path.join(BASE_DIR, "tool_manager_linux.py")
else:
    BACKEND = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tool_manager_windows.py")

TOOLS = {
    "esim": {
        "versions": ["latest", "2.4", "2.3", "2.2"],
        "desc": "eSim EDA platform by FOSSEE, IIT Bombay"
    },
    "kicad": {
        "versions": ["latest", "6", "7", "8", "9"],
        "desc": "PCB design and schematic capture tool"
    },
    "ngspice": {
        "versions": ["latest", "35", "36", "37", "38", "39", "40", "41", "42"],
        "desc": "SPICE-based analog circuit simulator"
    },
    "llvm": {
        "versions": ["latest", "13", "14", "15", "16", "17", "18", "19"],
        "desc": "Compiler infrastructure used by simulators"
    },
    "ghdl": {
        "versions": ["latest", "4.0.0", "4.1.0", "5.0.0", "5.1.1"],
        "desc": "VHDL simulator used in digital design"
    },
    "verilator": {
        "versions": ["latest", "5.006", "5.018", "5.026", "5.032"] if IS_WINDOWS else ["latest"],
        "desc": "Fast Verilog/SystemVerilog simulator"
    },
}

def is_admin():
    if IS_WINDOWS:
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except Exception:
            return False
    return True

def relaunch_as_admin():
    script = os.path.abspath(sys.argv[0])
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", PYTHON, f'"{script}"', None, 1
    )

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename="tool_manager_debug.log",
        filemode="a"
    )
    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    logging.getLogger("").addHandler(console)

class CommandWorker(QThread):
    finished = pyqtSignal(str, str)
    progress = pyqtSignal(str, str)

    def __init__(self, tool, args, password=None):
        super().__init__()
        self.tool     = tool
        self.args     = args
        self.password = password

    def run(self):
        output_lines = []
        try:
            if self.password and IS_LINUX:
                process = subprocess.Popen(
                    self.args,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )
                process.stdin.write(self.password + "\n")
                process.stdin.flush()
                process.stdin.close()
                for line in process.stdout:
                    line = line.rstrip()
                    if line:
                        output_lines.append(line)
                        self.progress.emit(self.tool, line)
                process.wait()
            else:
                process = subprocess.Popen(
                    self.args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding="utf-8",
                    errors="ignore"
                )
                for line in process.stdout:
                    line = line.rstrip()
                    if line:
                        output_lines.append(line)
                        self.progress.emit(self.tool, line)
                process.wait()

            output = "\n".join(output_lines)
        except subprocess.TimeoutExpired:
            output = "error|none|Operation timed out"
        except Exception as e:
            output = f"error|none|{str(e)}"

        self.finished.emit(self.tool, output)

class UninstallWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Uninstall Tools")
        self.setFixedSize(600, 550)
        self.setStyleSheet("background-color: #f8fafc;")
        self.workers  = []
        self._pending = set()
        self._build_ui()

    def _build_ui(self):
        font_normal = QFont("Segoe UI", 11)
        font_small  = QFont("Segoe UI", 9)
        font_bold   = QFont("Segoe UI", 11, QFont.Weight.Bold)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("🗑️ Uninstall Tools")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #1e293b;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        warn = QLabel("⚠️ Selected tools will be permanently removed.")
        warn.setFont(font_normal)
        warn.setAlignment(Qt.AlignmentFlag.AlignCenter)
        warn.setStyleSheet("color: #d97706; margin-bottom: 10px;")
        layout.addWidget(warn)

        self.tool_rows = {}
        for tool in TOOLS:
            row_layout = QHBoxLayout()
            
            tool_name = f" {tool.upper() if tool in ('esim', 'llvm', 'ghdl') else tool.title()}"
            chk = QCheckBox(tool_name)
            chk.setFont(font_bold)
            chk.setFixedWidth(180)
            chk.setStyleSheet("color: #334155; spacing: 8px;")
            
            status_lbl = QLabel("—")
            status_lbl.setFont(font_small)
            status_lbl.setStyleSheet("color: #94a3b8;")
            
            row_layout.addWidget(chk)
            row_layout.addWidget(status_lbl)
            layout.addLayout(row_layout)
            self.tool_rows[tool] = {"checkbox": chk, "status": status_lbl}

        layout.addSpacing(10)
        btn_row = QHBoxLayout()
        self.btn_toggle = QPushButton("☑️ Select All")
        self.btn_toggle.setFont(font_bold)
        self.btn_toggle.setFixedHeight(40)
        self.btn_toggle.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; border-radius: 6px; padding: 5px 15px;
            }
            QPushButton:hover { background-color: #e2e8f0; }
        """)
        self.btn_toggle.clicked.connect(self._toggle_all)

        self.btn_uninstall = QPushButton("🗑 Uninstall...")
        self.btn_uninstall.setFont(font_bold)
        self.btn_uninstall.setFixedHeight(40)
        self.btn_uninstall.setStyleSheet("""
            QPushButton { background-color: #ef4444; color: white; border-radius: 6px; padding: 5px 15px; }
            QPushButton:hover { background-color: #dc2626; }
            QPushButton:disabled { background-color: #fca5a5; color: #fef2f2; }
        """)
        self.btn_uninstall.clicked.connect(self._uninstall_selected)
        
        btn_row.addWidget(self.btn_toggle)
        btn_row.addWidget(self.btn_uninstall)
        layout.addLayout(btn_row)

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setFont(QFont("Consolas", 10))
        self.console.setFixedHeight(120)
        self.console.setStyleSheet("""
            QTextEdit {
                background-color: #1e293b; color: #f8fafc; border: 1px solid #475569; border-radius: 8px; padding: 10px;
            }
        """)
        layout.addWidget(self.console)

    def log(self, msg):
        self.console.append(msg)

    def _toggle_all(self):
        all_checked = all(r["checkbox"].isChecked() for r in self.tool_rows.values())
        for r in self.tool_rows.values():
            r["checkbox"].setChecked(not all_checked)
        self.btn_toggle.setText("Deselect All" if not all_checked else "Select All")

    def _uninstall_selected(self):
        selected = [t for t, r in self.tool_rows.items() if r["checkbox"].isChecked()]
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select tools to uninstall.")
            return

        reply = QMessageBox.question(
            self, "Confirm Uninstall",
            "Permanently uninstall:\n\n  " + "\n  ".join(selected) + "\n\nThis cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        self.btn_uninstall.setEnabled(False)
        self.btn_toggle.setEnabled(False)
        self._pending = set(selected)

        for tool in selected:
            self.tool_rows[tool]["status"].setText("Uninstalling...")
            self.tool_rows[tool]["status"].setStyleSheet("color:#3b82f6;font-weight:bold;")
            self.log(f"> Uninstalling {tool}...")
            worker = CommandWorker(tool, [PYTHON, BACKEND, "uninstall", tool, "none"])
            worker.finished.connect(self._on_done)
            worker.progress.connect(lambda t, line: self.log(f"  {line}"))
            self.workers.append(worker)
            worker.start()

    def _on_done(self, tool, output):
        r = self.tool_rows.get(tool)
        if not r:
            return

        known = {"not_installed", "uninstall_failed", "not_supported"}
        state = None
        for line in reversed(output.strip().split("\n")):
            line = line.strip()
            if "SyntaxWarning" in line or (line.startswith("C:") and ".py:" in line):
                continue
            if "|" in line and line.count("|") == 2:
                parts = line.split("|")
                if parts[0].strip() in known:
                    state = parts[0].strip()
                    break
        if state is None:
            state = "not_installed" if ("[OK]" in output and "uninstalled" in output) else "uninstall_failed"

        if state == "not_installed":
            r["status"].setText("✓ Uninstalled")
            r["status"].setStyleSheet("color:#10b981;font-weight:bold;")
            self.log(f"[OK] {tool} removed")
        elif state == "not_supported":
            r["status"].setText("— Not supported")
            r["status"].setStyleSheet("color:#94a3b8;")
        else:
            r["status"].setText("✗ Failed")
            r["status"].setStyleSheet("color:#ef4444;font-weight:bold;")
            self.log(f"[FAIL] {tool} uninstall failed")

        self._pending.discard(tool)
        if not self._pending:
            self.btn_uninstall.setEnabled(True)
            self.btn_toggle.setEnabled(True)
            self.log("\n> All uninstall operations complete.")

    def closeEvent(self, event):
        for w in self.workers:
            w.quit()
            w.wait(1000)
        event.accept()

class ToolManagerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("eSim Tool & Package Manager")
        self.setMinimumSize(1200, 700)
        self.setStyleSheet("background-color: #f8fafc;")
        
        from PyQt6.QtGui import QIcon
        icon_path = os.path.join(BASE_DIR, "..", "..", "images", "icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            if IS_WINDOWS:
                myappid = 'esim.toolmanager.1.0'
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
                
        self.workers       = []
        self.sudo_password = None
        self.active_tools  = set()
        self.build_ui()
        self.check_all()

    def build_ui(self):
        font_header = QFont("Segoe UI", 12, QFont.Weight.Bold)
        font_normal = QFont("Segoe UI", 11)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header Section
        header_layout = QVBoxLayout()
        header_layout.setSpacing(5)
        title = QLabel("📦 eSim Tool & Package Manager")
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        title.setStyleSheet("color: #1e293b;")
        
        subtitle = QLabel("Manage your EDA tools, simulators, and compiler infrastructure seamlessly.")
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setStyleSheet("color: #64748b; margin-bottom: 10px;")
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addLayout(header_layout)

        # Table Section
        self.table = QTableWidget(len(TOOLS), 5)
        self.table.setHorizontalHeaderLabels(
            ["Tool", "Version", "Description", "Installed Version", "Status"]
        )
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        # Modern Table Styling
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                alternate-background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                selection-background-color: #e0f2fe;
                selection-color: #0f172a;
                outline: none;
            }
            QHeaderView::section {
                background-color: #f1f5f9;
                color: #334155;
                font-weight: bold;
                font-size: 13px;
                padding: 12px;
                border: none;
                border-bottom: 2px solid #cbd5e1;
            }
            QTableWidget::item {
                padding: 5px 10px;
                border-bottom: 1px solid #f1f5f9;
            }
            QScrollBar:vertical {
                border: none;
                background: #f1f5f9;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #cbd5e1;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #94a3b8;
            }
        """)
        
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setStretchLastSection(True)
        
        self.table.setColumnWidth(0, 180)
        self.table.setColumnWidth(1, 160)
        self.table.setColumnWidth(3, 220)
        self.table.setColumnWidth(4, 200)

        for c in range(5):
            self.table.horizontalHeaderItem(c).setFont(font_header)

        self.rows = {}
        for row, tool in enumerate(TOOLS):
            # Column 0: Checkbox
            tool_name = f" {tool.upper() if tool in ('esim', 'llvm', 'ghdl') else tool.title()}"
            chk = QCheckBox(tool_name)
            chk.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
            chk.setStyleSheet("color: #334155; padding-left: 5px; spacing: 10px;")
            self.table.setCellWidget(row, 0, chk)

            # Column 1: Combo Box
            combo_widget = QWidget()
            combo_layout = QHBoxLayout(combo_widget)
            combo_layout.setContentsMargins(5, 5, 5, 5)
            combo = QComboBox()
            combo.addItems(TOOLS[tool]["versions"])
            combo.setEnabled(False)
            combo.setFont(font_normal)
            combo.setStyleSheet("""
                QComboBox {
                    border: 1px solid #cbd5e1;
                    border-radius: 4px;
                    padding: 4px 8px;
                    background-color: white;
                    color: #334155;
                }
                QComboBox:disabled {
                    background-color: #f1f5f9;
                    color: #94a3b8;
                }
                QComboBox::drop-down {
                    border: none;
                    width: 20px;
                }
            """)
            combo_layout.addWidget(combo)
            self.table.setCellWidget(row, 1, combo_widget)

            # Column 2: Description
            desc = QLabel(TOOLS[tool]["desc"])
            desc.setFont(font_normal)
            desc.setStyleSheet("color: #475569; padding-left: 5px;")
            desc.setWordWrap(True)
            self.table.setCellWidget(row, 2, desc)

            # Column 3: Installed Version
            installed = QLabel("Checking...")
            installed.setFont(font_normal)
            installed.setStyleSheet("color: #94a3b8; font-style: italic; padding-left: 5px;")
            self.table.setCellWidget(row, 3, installed)

            # Column 4: Status
            status = QLabel("Checking...")
            status.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
            status.setStyleSheet("color: #f59e0b; padding-left: 5px;")
            self.table.setCellWidget(row, 4, status)

            chk.stateChanged.connect(lambda s, c=combo: c.setEnabled(s == Qt.CheckState.Checked.value))
            self.rows[tool] = {
                "checkbox": chk, "combo": combo,
                "installed": installed, "status": status
            }

        self.table.verticalHeader().setDefaultSectionSize(60)
        layout.addWidget(self.table)

        # Buttons Section
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        
        btn_check     = QPushButton("🔍 Check Selected")
        btn_install   = QPushButton("⬇ Install Selected")
        btn_update    = QPushButton("🔄 Update Selected")
        btn_refresh   = QPushButton("🔁 Refresh All")
        btn_uninstall = QPushButton("🗑 Uninstall...")
        
        primary_btn_style = """
            QPushButton { background-color: #3b82f6; color: white; border-radius: 6px; padding: 10px 15px; font-weight: bold; }
            QPushButton:hover { background-color: #2563eb; }
            QPushButton:disabled { background-color: #f1f5f9; color: #64748b; border: 1px solid #e2e8f0; }
        """
        secondary_btn_style = """
            QPushButton { background-color: #ffffff; color: #475569; border: 1px solid #cbd5e1; border-radius: 6px; padding: 10px 15px; font-weight: bold; }
            QPushButton:hover { background-color: #f1f5f9; }
            QPushButton:disabled { background-color: #f1f5f9; color: #64748b; border: 1px solid #e2e8f0; }
        """
        danger_btn_style = """
            QPushButton { background-color: #ffffff; color: #e11d48; border: 1px solid #fecdd3; border-radius: 6px; padding: 10px 15px; font-weight: bold; }
            QPushButton:hover { background-color: #fff1f2; }
            QPushButton:disabled { background-color: #f1f5f9; color: #64748b; border: 1px solid #e2e8f0; }
        """

        btn_install.setStyleSheet(secondary_btn_style)
        btn_update.setStyleSheet(secondary_btn_style)
        btn_check.setStyleSheet(secondary_btn_style)
        btn_refresh.setStyleSheet(secondary_btn_style)
        btn_uninstall.setStyleSheet(danger_btn_style)

        for b in (btn_check, btn_install, btn_update, btn_refresh, btn_uninstall):
            b.setFont(font_normal)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_layout.addWidget(b)

        btn_check.clicked.connect(self.check_selected)
        btn_install.clicked.connect(self.install_selected)
        btn_update.clicked.connect(self.update_selected)
        btn_refresh.clicked.connect(self.refresh_all)
        btn_uninstall.clicked.connect(self.open_uninstall_window)

        self.btn_check   = btn_check
        self.btn_install = btn_install
        self.btn_update  = btn_update

        layout.addLayout(btn_layout)

        # Console Section
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setFont(QFont("Consolas", 10))
        self.console.setFixedHeight(160)
        self.console.setStyleSheet("""
            QTextEdit {
                background-color: #1e293b; color: #f8fafc; border: 1px solid #475569; border-radius: 8px; padding: 12px;
            }
        """)
        layout.addWidget(self.console)

    def log(self, msg):
        self.console.append(msg)

    def refresh_all(self):
        self.log("> Refreshing all tool statuses...")
        for tool in self.rows:
            self.rows[tool]["status"].setText("Refreshing...")
            self.rows[tool]["status"].setStyleSheet("color:#3b82f6;font-weight:bold;padding-left:5px;")
            self.rows[tool]["installed"].setText("Checking...")
            self.rows[tool]["installed"].setStyleSheet("color:#94a3b8;font-style:italic;padding-left:5px;")
        QApplication.processEvents()
        self.check_all()

    def get_sudo_password(self):
        if IS_LINUX and self.sudo_password is None:
            password, ok = QInputDialog.getText(
                self, "Authentication Required",
                "Enter your sudo password:", QLineEdit.Password
            )
            if ok and password:
                self.sudo_password = password
                return True
            return False
        return True

    def run_cmd(self, tool, cmd, needs_sudo=False):
        password = None
        if needs_sudo and IS_LINUX:
            password = self.sudo_password

        if tool in self.active_tools:
            self.log(f"[BUSY] {tool} is already running - please wait")
            return

        self.active_tools.add(tool)
        self._set_action_buttons(False)

        worker = CommandWorker(tool, cmd, password)
        worker.finished.connect(self.update_row)
        worker.finished.connect(lambda t, o, _tool=tool: self._on_worker_done(_tool))
        worker.progress.connect(lambda t, line: self.log(f"  {line}"))
        self.workers.append(worker)
        worker.start()

    def _on_worker_done(self, tool):
        self.active_tools.discard(tool)
        if not self.active_tools:
            self._set_action_buttons(True)

    def _set_action_buttons(self, enabled):
        for attr in ["btn_install", "btn_update", "btn_check"]:
            btn = getattr(self, attr, None)
            if btn:
                btn.setEnabled(enabled)
                btn.setStyleSheet("" if enabled else "background-color:#aaa;color:#666;")

    def update_row(self, tool, output):
        if tool not in self.rows:
            return
        r             = self.rows[tool]
        installed_lbl = r["installed"]
        status_lbl    = r["status"]

        QApplication.processEvents()

        known_states = {
            "installed", "not_installed", "wrong_version",
            "install_failed", "update_failed", "error",
            "not_supported", "uninstall_failed"
        }
        status_line = None
        for line in reversed(output.strip().split("\n")):
            line = line.strip()
            if not line:
                continue
            if "SyntaxWarning" in line or (line.startswith("C:") and ".py:" in line):
                continue
            if "|" in line and line.count("|") == 2:
                parts = line.split("|")
                if len(parts) == 3 and parts[0].strip() in known_states:
                    status_line = line
                    break

        if not status_line:
            self.log(f"{tool}: No status received. Output: {output[:200]}")
            installed_lbl.setText("Error")
            installed_lbl.setStyleSheet("color:red")
            status_lbl.setText("No Status")
            status_lbl.setStyleSheet("color:red")
            return

        try:
            parts     = status_line.split("|")
            state     = parts[0].strip()
            installed = parts[1].strip()

            if installed and installed not in ("none", "unknown"):
                installed_lbl.setText(installed)
            elif installed == "unknown":
                installed_lbl.setText("Installed (ver unknown)")
            else:
                installed_lbl.setText("Not installed")

            if state == "installed":
                installed_lbl.setStyleSheet("color:#10b981;font-weight:bold;padding-left:5px;")
                status_lbl.setText("✓ Installed")
                status_lbl.setStyleSheet("color:#10b981;font-weight:bold;padding-left:5px;")
            elif state == "not_installed":
                installed_lbl.setStyleSheet("color:#ef4444;padding-left:5px;")
                status_lbl.setText("✗ Not Installed")
                status_lbl.setStyleSheet("color:#ef4444;font-weight:bold;padding-left:5px;")
            elif state == "wrong_version":
                installed_lbl.setStyleSheet("color:#f59e0b;font-weight:bold;padding-left:5px;")
                status_lbl.setText("⚠️ Wrong Version")
                status_lbl.setStyleSheet("color:#f59e0b;font-weight:bold;padding-left:5px;")
            elif state in ("install_failed", "update_failed", "uninstall_failed"):
                installed_lbl.setStyleSheet("color:#ef4444;padding-left:5px;")
                status_lbl.setText("✗ Failed")
                status_lbl.setStyleSheet("color:#ef4444;font-weight:bold;padding-left:5px;")
            elif state == "error":
                installed_lbl.setStyleSheet("color:#ef4444;padding-left:5px;")
                status_lbl.setText("✗ Error")
                status_lbl.setStyleSheet("color:#ef4444;font-weight:bold;padding-left:5px;")
            else:
                status_lbl.setText(state.replace("_", " ").title())
                status_lbl.setStyleSheet("color:#3b82f6;font-weight:bold;padding-left:5px;")

            self.table.repaint()
            QApplication.processEvents()

        except (ValueError, IndexError) as e:
            self.log(f"{tool}: Parse error: {e}, Line: {status_line}")
            installed_lbl.setText("Parse Error")
            installed_lbl.setStyleSheet("color:#ef4444;padding-left:5px;")
            status_lbl.setText("Parse Error")
            status_lbl.setStyleSheet("color:#ef4444;font-weight:bold;padding-left:5px;")

    def check_all(self):
        for tool in self.rows:
            self.run_cmd(tool, [PYTHON, BACKEND, "check", tool, "none"])

    def check_selected(self):
        for tool, r in self.rows.items():
            if r["checkbox"].isChecked():
                version = r["combo"].currentText()
                self.log(f"> Checking {tool} (target: {version})")
                self.run_cmd(tool, [PYTHON, BACKEND, "check", tool, version])

    def install_selected(self):
        selected = [t for t, r in self.rows.items() if r["checkbox"].isChecked()]
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select tools to install.")
            return
        if IS_LINUX and not self.get_sudo_password():
            QMessageBox.warning(self, "Auth Failed", "Sudo password required.")
            return
        for tool in selected:
            r       = self.rows[tool]
            version = r["combo"].currentText()
            self.log(f"> Installing {tool} version {version}...")
            r["status"].setText("Installing...")
            r["status"].setStyleSheet("color:#3b82f6;font-weight:bold;padding-left:5px;")
            self.run_cmd(tool, [PYTHON, BACKEND, "install", tool, version], needs_sudo=True)

    def update_selected(self):
        selected = [t for t, r in self.rows.items() if r["checkbox"].isChecked()]
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select tools to update.")
            return
        if IS_LINUX and not self.get_sudo_password():
            QMessageBox.warning(self, "Auth Failed", "Sudo password required.")
            return
        for tool in selected:
            r       = self.rows[tool]
            version = r["combo"].currentText()
            self.log(f"> Updating {tool} to version {version}...")
            r["status"].setText("Updating...")
            r["status"].setStyleSheet("color:#3b82f6;font-weight:bold;padding-left:5px;")
            self.run_cmd(tool, [PYTHON, BACKEND, "update", tool, version], needs_sudo=True)

    def open_uninstall_window(self):
        self._uninstall_win = UninstallWindow()
        self._uninstall_win.show()

    def closeEvent(self, event):
        for worker in self.workers:
            worker.quit()
            worker.wait(1000)
        event.accept()


if __name__ == "__main__":
    if IS_WINDOWS and not is_admin():
        app = QApplication(sys.argv)
        msg = QMessageBox()
        msg.setWindowTitle("Administrator Required")
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText(
            "Tool Manager needs Administrator privileges to install/update tools.\n\n"
            "Click OK to relaunch as Administrator."
        )
        msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        if msg.exec() == QMessageBox.StandardButton.Ok:
            relaunch_as_admin()
        sys.exit(0)

    app = QApplication(sys.argv)
    setup_logging()
    gui = ToolManagerGUI()
    gui.show()
    sys.exit(app.exec())
