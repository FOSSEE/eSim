#!/usr/bin/env python3
import os
import sys
import json
import ctypes
import subprocess
from pathlib import Path
from PyQt6.QtWidgets import (
    QScrollArea,
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QGridLayout, QPushButton, QLabel, QTabWidget,
    QMessageBox, QFrame, QProgressBar, QStackedWidget,
    QListWidget, QListWidgetItem, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor

# ==================== CONFIG ====================
BASE_DIR = Path(__file__).resolve().parent
INFO_JSON = BASE_DIR / "information.json"
FULL_GUI  = BASE_DIR / "gui_fixed.py"
PYTHON    = sys.executable

ANALOG_TOOLS  = ["esim", "kicad", "ngspice"]
DIGITAL_TOOLS = ["esim", "kicad", "ngspice", "ghdl", "verilator", "llvm"]

TOOL_LABELS = {
    "esim":      "eSim",
    "kicad":     "KiCad",
    "ngspice":   "Ngspice",
    "ghdl":      "GHDL",
    "verilator": "Verilator",
    "llvm":      "LLVM",
}

TOOL_VERSIONS = {
    "esim":      "2.4",
    "kicad":     "latest",
    "ngspice":   "latest",
    "ghdl":      "latest",
    "verilator": "latest",
    "llvm":      "latest",
}

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def relaunch_as_admin():
    script = str(Path(__file__).resolve())
    
    # Swap to pythonw.exe to suppress the black console window
    python_exe = PYTHON
    if python_exe.lower().endswith("python.exe"):
        pythonw_exe = python_exe[:-10] + "pythonw.exe"
        if os.path.exists(pythonw_exe):
            python_exe = pythonw_exe

    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", python_exe, f'"{script}"', None, 1
    )

def load_installed_versions():
    versions = {k: "Not installed" for k in TOOL_LABELS}
    try:
        if INFO_JSON.exists():
            with open(INFO_JSON) as f:
                data = json.load(f)
            for pkg in data.get("important_packages", []):
                name = pkg.get("package_name", "")
                ver  = pkg.get("version", "Not installed")
                if name in versions and ver not in ("", "Not installed"):
                    versions[name] = ver
    except Exception as e:
        print(f"Could not load version info: {e}")
    return versions

def darken_color(hex_color, amount=0.15):
    h = hex_color.lstrip("#")
    r = max(0, int(int(h[0:2], 16) * (1 - amount)))
    g = max(0, int(int(h[2:4], 16) * (1 - amount)))
    b = max(0, int(int(h[4:6], 16) * (1 - amount)))
    return f"#{r:02x}{g:02x}{b:02x}"

class InstallWorker(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool)

    def __init__(self, tools):
        super().__init__()
        self.tools = tools

    def run(self):
        success = True
        backend = str(BASE_DIR / "tool_manager_windows.py")
        for tool, version in self.tools:
            self.progress.emit(
                f"Installing {TOOL_LABELS.get(tool, tool)} {version}..."
            )
            try:
                proc = subprocess.Popen(
                    [PYTHON, backend, "install", tool, version],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding="utf-8",
                    errors="ignore"
                )
                for line in proc.stdout:
                    line = line.rstrip()
                    if line:
                        self.progress.emit(f"  {line}")
                        if "[ERROR]" in line or "install_failed|" in line:
                            success = False
                proc.wait()
                if proc.returncode != 0:
                    success = False
            except Exception as e:
                self.progress.emit(f"  [ERROR] {tool}: {e}")
                success = False
        self.finished.emit(success)


# ==================== MAIN WINDOW ====================
class ToolManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.installed_versions = load_installed_versions()
        self._install_worker    = None
        self._status_frame      = None
        self.initUI()

    def initUI(self):
        from PyQt6.QtGui import QIcon
        self.setWindowTitle("eSim Tool Manager")
        self.setGeometry(100, 100, 1150, 900)
        self.setMinimumSize(1050, 850)

        icon_path = os.path.join(BASE_DIR, "..", "..", "images", "icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            import sys
            if sys.platform == "win32":
                import ctypes
                myappid = 'esim.toolmanager.1.0'
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        central = QWidget()
        central.setStyleSheet("background-color: #f8fafc;")
        self.setCentralWidget(central)
        self._main_layout = QVBoxLayout(central)
        self._main_layout.setSpacing(0)
        self._main_layout.setContentsMargins(0, 0, 0, 0)

        self._main_layout.addWidget(self._create_header())
        self._status_frame = self._create_status_panel()
        self._main_layout.addWidget(self._status_frame)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(0)
        content_layout.setContentsMargins(0, 0, 0, 0)

        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(240)
        self.sidebar.setStyleSheet("""
            QListWidget {
                background-color: #ffffff;
                border-right: 1px solid #e2e8f0;
                border-top: none; border-bottom: none; border-left: none;
                padding-top: 15px; outline: 0;
            }
            QListWidget::item {
                padding: 16px 25px;
                color: #64748b;
                font-family: 'Segoe UI'; font-size: 15px; font-weight: bold;
                border-left: 4px solid transparent;
            }
            QListWidget::item:hover {
                background-color: #f1f5f9; color: #1e293b;
            }
            QListWidget::item:selected {
                background-color: #eff6ff; color: #2563eb;
                border-left: 4px solid #2563eb;
            }
        """)
        items = ["🔌   Installation Suite", "⚙   Advanced Manager", "🗑️   Uninstall Tools", "ℹ   About eSim"]
        for item in items:
            self.sidebar.addItem(item)
            
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self._create_installation_tab())
        self.stacked_widget.addWidget(self._create_management_tab())
        self.stacked_widget.addWidget(self._create_uninstall_tab())
        self.stacked_widget.addWidget(self._create_about_tab())
        
        self.sidebar.currentRowChanged.connect(self.stacked_widget.setCurrentIndex)
        
        content_layout.addWidget(self.sidebar)
        content_layout.addWidget(self.stacked_widget)
        
        self._main_layout.addLayout(content_layout)
        self._main_layout.addWidget(self._create_footer())
        
        self.sidebar.setCurrentRow(0)

    def _add_shadow(self, widget):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 20))
        shadow.setOffset(0, 6)
        widget.setGraphicsEffect(shadow)

    def _create_header(self):
        frame = QFrame()
        frame.setFixedHeight(150)
        frame.setStyleSheet("""
            .QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0f172a, stop:1 #1e293b);
                border-bottom: 1px solid #334155;
            }
        """)
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(45, 25, 45, 25)

        logo = QLabel("📦")
        logo.setStyleSheet("font-size: 55px; background: transparent;")
        layout.addWidget(logo)

        vbox = QVBoxLayout()
        vbox.setSpacing(6)
        t1 = QLabel("eSim Tool Manager")
        t1.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        t1.setStyleSheet("color: white; background: transparent;")
        t2 = QLabel("Centralized administration for your EDA toolchains, simulation engines, and compiler infrastructure.")
        t2.setFont(QFont("Segoe UI", 12))
        t2.setStyleSheet("color: #94a3b8; background: transparent;")
        t2.setWordWrap(True)
        vbox.addWidget(t1)
        vbox.addWidget(t2)
        vbox.addStretch()
        layout.addLayout(vbox, stretch=1)
        return frame

    def _refresh_status(self):
        QMessageBox.information(self, "Refresh", "Please restart the Tool Manager to refresh the status panel.")

    def _create_status_panel(self):
        frame = QFrame()
        frame.setStyleSheet("""
            .QFrame {
                background: #ffffff;
                border-bottom: 1px solid #e2e8f0;
            }
        """)
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(45, 15, 45, 15)

        lbl = QLabel("📌 Active Installations:")
        lbl.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        lbl.setStyleSheet("color: #334155; background: transparent;")
        layout.addWidget(lbl)

        for key, label in TOOL_LABELS.items():
            ver = self.installed_versions.get(key, "Not installed")
            if ver != "Not installed":
                text = (f"<span style='color:#10b981;'>●</span> {label} <span style='color:#475569; font-weight:bold;'>{ver}</span>")
            else:
                text = (f"<span style='color:#ef4444;'>○</span> {label} <span style='color:#94a3b8;'>—</span>")
            l2 = QLabel(text)
            l2.setFont(QFont("Segoe UI", 10))
            l2.setStyleSheet("color: #475569; background: transparent; margin-left: 18px;")
            layout.addWidget(l2)

        layout.addStretch()

        rbtn = QPushButton("↻ Refresh")
        rbtn.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        rbtn.setFixedHeight(34)
        rbtn.setCursor(Qt.CursorShape.PointingHandCursor)
        rbtn.setStyleSheet("""
            QPushButton {
                background: #ffffff; border: 1px solid #cbd5e1;
                border-radius: 6px; padding: 4px 18px; color: #475569;
            }
            QPushButton:hover { background: #f1f5f9; color: #0f172a; border-color: #94a3b8; }
        """)
        rbtn.clicked.connect(self._refresh_status)
        layout.addWidget(rbtn)
        return frame

    def _create_installation_tab(self):
        tab = QWidget()
        tab.setStyleSheet("background-color: #f8fafc;")
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(45, 40, 45, 40)
        layout.setSpacing(25)

        desc = QLabel(
            "Welcome to the eSim environment setup. Please select your preferred installation profile below.\n"
            "The Analog profile provisions the core circuit design and SPICE engines, while the Digital profile extends your workspace with advanced HDL simulation toolchains."
        )
        desc.setFont(QFont("Segoe UI", 12))
        desc.setStyleSheet("color: #475569; line-height: 1.5;")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        card1 = self._create_install_card(
            title       = "🔌  Analog Simulation Suite",
            description = ("<div style='line-height: 1.6;'>Deploys the core <b>eSim EDA platform</b> alongside <b>KiCad</b> and <b>Ngspice</b> "
                           "to provide a comprehensive environment for schematic capture and mixed-signal simulation.</div>"),
            features    = ["✓ eSim Core Engine", "✓ KiCad Design Suite", "✓ Ngspice Simulator", "✓ Standard Component Libraries"],
            disk_space  = "~1.5 GB",
            btn_text    = "Initialize Analog Suite",
            btn_color   = "#10b981",
            callback    = self._install_analog,
        )
        layout.addWidget(card1)

        card2 = self._create_install_card(
            title       = "💻  Digital & HDL Toolchain",
            description = ("<div style='line-height: 1.6;'>Installs the complete <b>Analog Suite</b> and seamlessly integrates <b>GHDL</b>, <b>Verilator</b>, "
                           "and <b>LLVM</b>, enabling high-performance VHDL and SystemVerilog compilation.</div>"),
            features    = ["✓ Analog Suite Included", "✓ GHDL Compiler", "✓ Verilator Engine", "✓ LLVM Infrastructure"],
            disk_space  = "~3.0 GB",
            btn_text    = "Initialize Digital Suite",
            btn_color   = "#3b82f6",
            callback    = self._install_digital,
        )
        layout.addWidget(card2)

        self.progress_frame = QFrame()
        self.progress_frame.setVisible(False)
        self.progress_frame.setStyleSheet(".QFrame { background: #1e293b; border-radius: 8px; box-shadow: inset 0 2px 4px rgba(0,0,0,0.1); }")
        pf_layout = QVBoxLayout(self.progress_frame)
        pf_layout.setContentsMargins(20, 16, 20, 16)
        pf_layout.setSpacing(8)

        pf_title = QLabel("Installation Progress")
        pf_title.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        pf_title.setStyleSheet("color: #94a3b8; background: transparent;")
        pf_layout.addWidget(pf_title)

        self.progress_log = QLabel("")
        self.progress_log.setFont(QFont("Consolas", 10))
        self.progress_log.setStyleSheet("color: #f8fafc; background: transparent;")
        self.progress_log.setWordWrap(True)
        self.progress_log.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.progress_log.setMinimumHeight(60)
        pf_layout.addWidget(self.progress_log)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setStyleSheet("""
            QProgressBar { background: #334155; border-radius: 4px; border: none; }
            QProgressBar::chunk { background: #3b82f6; border-radius: 4px; }
        """)
        pf_layout.addWidget(self.progress_bar)
        layout.addWidget(self.progress_frame)
        
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setWidget(tab)
        return scroll

    def _create_install_card(self, title, description, features, disk_space, btn_text, btn_color, callback):
        from PyQt6.QtWidgets import QSizePolicy
        card = QFrame()
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        card.setStyleSheet("""
            .QFrame {
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
            }
            .QFrame:hover { border: 1px solid #cbd5e1; }
        """)
        self._add_shadow(card)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(14)

        top_row = QHBoxLayout()
        t = QLabel(title)
        t.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        t.setStyleSheet("color: #0f172a; background: transparent; border: none; letter-spacing: 0.5px;")
        top_row.addWidget(t)

        top_row.addStretch()

        dl = QLabel(f"💾 {disk_space}")
        dl.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        dl.setStyleSheet("color: #94a3b8; background: transparent; border: none; padding-top: 6px;")
        dl.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        top_row.addWidget(dl)

        layout.addLayout(top_row)

        d = QLabel(description)
        d.setFont(QFont("Segoe UI", 12))
        d.setStyleSheet("color: #334155; background: transparent; border: none;")
        d.setWordWrap(True)
        d.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(d)

        features_layout = QGridLayout()
        features_layout.setSpacing(10)
        features_layout.setColumnStretch(0, 1)
        features_layout.setColumnStretch(1, 1)
        for i, feat in enumerate(features):
            lbl = QLabel(feat.replace("✓", "<span style='color: #10b981; font-weight: bold;'>✓</span>"))
            lbl.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
            lbl.setStyleSheet("color: #475569; background: transparent; border: none;")
            lbl.setTextFormat(Qt.TextFormat.RichText)
            features_layout.addWidget(lbl, i // 2, i % 2)
        layout.addLayout(features_layout)

        layout.addSpacing(15)

        bottom = QHBoxLayout()
        bottom.addStretch()

        btn = QPushButton(btn_text)
        btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setMinimumHeight(50)
        btn.setMinimumWidth(340)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: {btn_color}; color: white;
                border: none; border-radius: 8px; padding: 12px 24px;
            }}
            QPushButton:hover     {{ background: {darken_color(btn_color)}; }}
            QPushButton:pressed   {{ background: {darken_color(btn_color, 0.3)}; }}
            QPushButton:disabled  {{ background: #cbd5e1; color: #f1f5f9; }}
        """)
        btn.clicked.connect(callback)
        bottom.addWidget(btn)
        bottom.addStretch()

        layout.addLayout(bottom)
        return card

    def _create_management_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(45, 45, 45, 45)
        layout.setSpacing(25)

        desc = QLabel("Access the Advanced Package Manager for granular control over individual tool versions and dependencies.")
        desc.setFont(QFont("Segoe UI", 13))
        desc.setStyleSheet("color: #475569;")
        layout.addWidget(desc)

        card = QFrame()
        card.setStyleSheet("""
            .QFrame {
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
            }
        """)
        self._add_shadow(card)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(20)

        info = QLabel(
            "<b>Advanced Package Management Capabilities:</b><br><br>"
            "&nbsp;&nbsp;• <b>Core Platform:</b> Upgrade or configure <b>eSim</b> (v2.2 – v2.5)<br>"
            "&nbsp;&nbsp;• <b>Schematic Capture:</b> Manage <b>KiCad</b> installations (v6, 7, 8, 9, or latest)<br>"
            "&nbsp;&nbsp;• <b>Analog Simulation:</b> Control <b>Ngspice</b> versions (v35–42, or latest)<br>"
            "&nbsp;&nbsp;• <b>Digital Toolchains:</b> Deploy <b>GHDL</b> (v4.0.0 – 5.1.1) and <b>Verilator</b> (v5.006 – 5.032)<br>"
            "&nbsp;&nbsp;• <b>Compiler Infrastructure:</b> Maintain <b>LLVM</b> frameworks (v13–19)<br>"
            "&nbsp;&nbsp;• <b>Maintenance:</b> Safely uninstall, repair, or refresh specific packages as needed"
        )
        info.setFont(QFont("Segoe UI", 11))
        info.setStyleSheet("color: #334155; line-height: 1.6; background: transparent; border: none;")
        info.setWordWrap(True)
        card_layout.addWidget(info)
        card_layout.addSpacing(10)

        btn = QPushButton("⚙  Launch Advanced Tool Manager")
        btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFixedHeight(50)
        btn.setStyleSheet("""
            QPushButton {
                background: #3b82f6; color: white;
                border: none; border-radius: 8px; padding: 12px;
            }
            QPushButton:hover { background: #2563eb; }
        """)
        btn.clicked.connect(self._open_full_manager)
        card_layout.addWidget(btn)
        
        layout.addWidget(card)
        layout.addStretch()
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setWidget(tab)
        return scroll

    def _create_uninstall_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(45, 45, 45, 45)
        layout.setSpacing(25)

        warn = QFrame()
        warn.setStyleSheet("""
            .QFrame {
                background: #fffbeb;
                border-left: 6px solid #f59e0b;
                border-radius: 8px;
            }
        """)
        self._add_shadow(warn)
        wl = QVBoxLayout(warn)
        wl.setContentsMargins(25, 20, 25, 20)
        wt = QLabel("⚠️  Warning")
        wt.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        wt.setStyleSheet("color: #b45309; background: transparent; border: none;")
        wd = QLabel(
            "Proceed with caution. Uninstalling packages will permanently remove the associated binaries and configurations from your system. "
            "This action is irreversible."
        )
        wd.setFont(QFont("Segoe UI", 12))
        wd.setStyleSheet("color: #d97706; background: transparent; border: none;")
        wd.setWordWrap(True)
        wl.addWidget(wt)
        wl.addWidget(wd)
        layout.addWidget(warn)

        desc = QLabel("Select the component suites you wish to remove:")
        desc.setFont(QFont("Segoe UI", 13))
        desc.setStyleSheet("color: #475569;")
        layout.addWidget(desc)

        def make_btn(text, color, callback):
            b = QPushButton(text)
            b.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.setFixedHeight(54)
            dark = darken_color(color, 0.1)
            b.setStyleSheet(f"""
                QPushButton {{
                    background: {color}; color: white;
                    border: none; border-radius: 8px;
                    text-align: left; padding-left: 25px;
                }}
                QPushButton:hover {{ background: {dark}; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            """)
            b.clicked.connect(callback)
            return b

        layout.addWidget(make_btn("🗑️   Remove Digital Toolchains  (GHDL, Verilator, LLVM)", "#ef4444", self._uninstall_digital))
        layout.addWidget(make_btn("🗑️   Remove Analog Suites  (KiCad, Ngspice)", "#f59e0b", self._uninstall_analog))
        layout.addWidget(make_btn("🗑️   Completely Uninstall eSim  (Removes Core and All Packages)", "#64748b", self._uninstall_all))

        layout.addSpacing(15)
        sep = QLabel("— Or selectively remove individual tools via the Advanced Manager —")
        sep.setFont(QFont("Segoe UI", 10))
        sep.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sep.setStyleSheet("color: #94a3b8;")
        layout.addWidget(sep)

        indiv = QPushButton("⚙   Launch Advanced Tool Manager")
        indiv.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        indiv.setCursor(Qt.CursorShape.PointingHandCursor)
        indiv.setFixedHeight(48)
        indiv.setStyleSheet("""
            QPushButton {
                background: white; color: #3b82f6;
                border: 2px solid #3b82f6; border-radius: 8px;
            }
            QPushButton:hover { background: #eff6ff; }
        """)
        indiv.clicked.connect(self._open_full_manager)
        layout.addWidget(indiv)
        layout.addStretch()
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setWidget(tab)
        return scroll

    def _create_about_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(45, 45, 45, 45)
        layout.setSpacing(25)
        
        card = QFrame()
        card.setStyleSheet("""
            .QFrame {
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
            }
        """)
        self._add_shadow(card)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(20)

        title = QLabel("About eSim Tool Manager")
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        title.setStyleSheet("color: #0f172a; margin-bottom: 10px; background: transparent; border: none;")
        card_layout.addWidget(title)        

        info_text = """
        <div style='font-family: "Segoe UI", sans-serif; font-size: 11pt; color: #334155; line-height: 1.8;'>
            <p><b>Platform Capabilities:</b><br>
            <span style='color: #64748b;'>• Streamlined deployment of comprehensive analog and digital simulation environments<br>
            • Granular version control and independent package updating<br>
            • Deep integration with the primary eSim graphical interface and backend architecture</span></p>
            
            <p><b>Supported Ecosystem:</b><br>
            <span style='color: #64748b;'>• <b>KiCad</b>: 6.0.11, 7.0.11, 8.0.9<br>
            • <b>Ngspice</b>: 35, 36, 37, 38, 39, 40, 41, 42, 43<br>
            • <b>GHDL</b>: 3.0.0, 4.0.0, 4.1.0, nightly builds<br>
            • <b>Verilator</b>: 4.228, 5.020, 5.026, 5.030</span></p>
        </div>
        """
        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        info_label.setStyleSheet("background: transparent; border: none;")
        card_layout.addWidget(info_label)
        
        layout.addWidget(card)
        layout.addStretch()
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setWidget(tab)
        return scroll

    def _create_footer(self):
        footer = QFrame()
        footer.setFixedHeight(45)
        footer.setStyleSheet("""
            .QFrame {
                background: #f1f5f9;
                border-top: 1px solid #cbd5e1;
            }
        """)
        layout = QHBoxLayout(footer)
        layout.setContentsMargins(25, 0, 25, 0)
        lbl = QLabel("eSim Tool Manager - Powered by PyQt6  •  Advanced Implementation")
        lbl.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        lbl.setStyleSheet("color: #64748b; background: transparent;")
        layout.addWidget(lbl)
        layout.addStretch()
        return footer
    def _install_analog(self):
        reply = QMessageBox.question(
            self, "Confirm Analog Mode Installation",
            "Install Analog Mode?\n\n"
            "This will install:\n"
            "  • eSim\n  • KiCad (latest)\n  • Ngspice (latest)\n\n"
            "Estimated size: ~1.5 GB\n"
            "This may take 20–40 minutes.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._run_install(
                [(t, TOOL_VERSIONS[t]) for t in ANALOG_TOOLS],
                "Analog Mode"
            )

    def _install_digital(self):
        reply = QMessageBox.question(
            self, "Confirm Digital Mode Installation",
            "Install Digital Mode?\n\n"
            "This will install:\n"
            "  • eSim\n  • KiCad (latest)\n  • Ngspice (latest)\n"
            "  • GHDL (latest)\n  • Verilator (latest)\n  • LLVM (latest)\n\n"
            "Estimated size: ~3.0 GB\n"
            "This may take 40–80 minutes.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._run_install(
                [(t, TOOL_VERSIONS[t]) for t in DIGITAL_TOOLS],
                "Digital Mode"
            )

    def _run_install(self, tools, mode_name):
        self.progress_frame.setVisible(True)
        self.progress_log.setText(f"Starting {mode_name} installation...")
        self.progress_bar.setRange(0, 0)
        self._install_worker = InstallWorker(tools)
        self._install_worker.progress.connect(self._on_progress)
        self._install_worker.finished.connect(
            lambda ok: self._on_install_done(ok, mode_name)
        )
        self._install_worker.start()

    def _on_progress(self, line):
        lines = self.progress_log.text().split("\n")[-7:] + [line]
        self.progress_log.setText("\n".join(lines))

    def _on_install_done(self, success, mode_name):
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(1)
        self._refresh_status()
        if success:
            self.progress_log.setText(f"✓ {mode_name} installation complete!")
            QMessageBox.information(
                self, "Installation Complete",
                f"{mode_name} installed successfully!\n\n"
                "All tools are ready to use.\n"
                "Click Refresh in the status bar to update version display."
            )
        else:
            self.progress_log.setText(
                f"⚠ {mode_name} finished with some issues.\n"
                "Open Full Tool Manager to check individual tools."
            )
            QMessageBox.warning(
                self, "Installation Finished with Warnings",
                f"{mode_name} completed but some tools may not have\n"
                "installed correctly.\n\n"
                "Open the Full Tool Manager to check and fix individual tools."
            )

    def _open_full_manager(self):
        if not FULL_GUI.exists():
            QMessageBox.critical(
                self, "File Not Found",
                f"gui_fixed.py not found at:\n{FULL_GUI}\n\n"
                f"Make sure all files are in:\n{BASE_DIR}"
            )
            return
        try:
            subprocess.Popen(
                [PYTHON, str(FULL_GUI)],
                creationflags=(subprocess.CREATE_NO_WINDOW
                               if sys.platform == "win32" else 0)
            )
        except Exception as e:
            QMessageBox.critical(self, "Error",
                                 f"Failed to open Tool Manager:\n{e}")

    def _uninstall_digital(self):
        reply = QMessageBox.warning(
            self, "Confirm Uninstall",
            "Uninstall digital packages?\n\n"
            "Removes: GHDL • Verilator • LLVM\n\n"
            "This cannot be undone!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._run_uninstall(
                [("ghdl","none"), ("verilator","none"), ("llvm","none")],
                "Digital packages"
            )

    def _uninstall_analog(self):
        reply = QMessageBox.warning(
            self, "Confirm Uninstall",
            "Uninstall analog packages?\n\n"
            "Removes: KiCad • Ngspice\n\n"
            "This cannot be undone!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._run_uninstall(
                [("kicad","none"), ("ngspice","none")],
                "Analog packages"
            )

    def _uninstall_all(self):
        reply = QMessageBox.warning(
            self, "Confirm Complete Uninstall",
            "Uninstall EVERYTHING?\n\n"
            "Removes: eSim • KiCad • Ngspice\n"
            "         GHDL • Verilator • LLVM\n\n"
            "This cannot be undone!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._run_uninstall(
                [(t, "none") for t in DIGITAL_TOOLS],
                "All packages"
            )

    def _run_uninstall(self, tools, label):
        try:
            backend = str(BASE_DIR / "tool_manager_windows.py")
            for tool, _ in tools:
                subprocess.Popen(
                    [PYTHON, backend, "uninstall", tool, "none"],
                    creationflags=(subprocess.CREATE_NO_WINDOW
                                   if sys.platform == "win32" else 0)
                )
            QMessageBox.information(
                self, "Uninstall Started",
                f"Uninstalling {label} in the background.\n\n"
                "This may take a few minutes.\n"
                "Click Refresh to update the status display when done."
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to uninstall:\n{e}")


def main():
    if sys.platform == "win32" and not is_admin():
        # Note: We deliberately skip a manual PyQt consent dialog here because
        # Windows will natively prompt the user with a UAC shield anyway.
        relaunch_as_admin()
        sys.exit(0)

    app = QApplication(sys.argv)
    app.setFont(QFont("Arial", 10))
    app.setStyle("Fusion")

    win = ToolManagerWindow()
    win.show()

    screen = app.primaryScreen().geometry()
    win.move(
        (screen.width()  - win.width())  // 2,
        (screen.height() - win.height()) // 3
    )
    sys.exit(app.exec())


if __name__ == "__main__":
    main()