#!/usr/bin/env python3
import os
import sys
import json
import ctypes
import subprocess
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel, QTabWidget,
    QMessageBox, QFrame, QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

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
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", PYTHON, f'"{script}"', None, 1
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
        self.setWindowTitle("eSim Tool Manager")
        self.setGeometry(100, 100, 820, 720)
        self.setMinimumSize(880, 760)

        central = QWidget()
        self.setCentralWidget(central)
        self._main_layout = QVBoxLayout(central)
        self._main_layout.setSpacing(0)
        self._main_layout.setContentsMargins(0, 0, 0, 0)

        self._main_layout.addWidget(self._create_header())

        self._status_frame = self._create_status_panel()
        self._main_layout.addWidget(self._status_frame)

        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane { border: none; background: white; }
            QTabBar::tab {
                background: #f5f5f5; color: #555;
                padding: 12px 24px; margin-right: 2px;
                border: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                font-size: 13px; font-weight: 500;
            }
            QTabBar::tab:selected { background: white; color: #4A90E2; }
            QTabBar::tab:hover    { background: #e8e8e8; }
        """)
        tabs.addTab(self._create_installation_tab(), "Installation")
        tabs.addTab(self._create_management_tab(),   "Management")
        tabs.addTab(self._create_uninstall_tab(),     "Uninstall")
        tabs.addTab(self._create_about_tab(),         "About")
        self._main_layout.addWidget(tabs)
        self._main_layout.addWidget(self._create_footer())

    def _create_header(self):
        frame = QFrame()
        frame.setFixedHeight(140)
        frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5B9BD5, stop:1 #4A90E2);
            }
        """)
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(30, 20, 30, 20)

        logo = QLabel("⚙️")
        logo.setStyleSheet("font-size: 48px; background: transparent;")
        layout.addWidget(logo)

        vbox = QVBoxLayout()
        vbox.setSpacing(5)
        t1 = QLabel("eSim Tool Manager")
        t1.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        t1.setStyleSheet("color: white; background: transparent;")
        t2 = QLabel("Package Management System  •  Windows Edition")
        t2.setFont(QFont("Arial", 11))
        t2.setStyleSheet("color: rgba(255,255,255,0.9); background: transparent;")
        vbox.addWidget(t1)
        vbox.addWidget(t2)
        vbox.addStretch()
        layout.addLayout(vbox)
        layout.addStretch()
        return frame

    def _create_status_panel(self):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background: #f8f9fa;
                border-bottom: 1px solid #e0e0e0;
            }
        """)
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(30, 12, 30, 12)

        lbl = QLabel("📦 Installed:")
        lbl.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        lbl.setStyleSheet("color: #666; background: transparent;")
        layout.addWidget(lbl)

        for key, label in TOOL_LABELS.items():
            ver = self.installed_versions.get(key, "Not installed")
            if ver != "Not installed":
                text = (f"<span style='color:#28a745;'>●</span> {label} "
                        f"<span style='color:#666;'>{ver}</span>")
            else:
                text = (f"<span style='color:#dc3545;'>○</span> {label} "
                        f"<span style='color:#999;'>—</span>")
            l2 = QLabel(text)
            l2.setFont(QFont("Arial", 9))
            l2.setStyleSheet("background: transparent; margin-left: 10px;")
            layout.addWidget(l2)

        layout.addStretch()

        rbtn = QPushButton("↻ Refresh")
        rbtn.setFont(QFont("Arial", 9))
        rbtn.setFixedHeight(26)
        rbtn.setCursor(Qt.PointingHandCursor)
        rbtn.setStyleSheet("""
            QPushButton {
                background: #e9ecef; border: 1px solid #ced4da;
                border-radius: 4px; padding: 2px 10px; color: #555;
            }
            QPushButton:hover { background: #dee2e6; }
        """)
        rbtn.clicked.connect(self._refresh_status)
        layout.addWidget(rbtn)
        return frame

    def _create_installation_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        desc = QLabel(
            "Install eSim with the required simulation tools.\n"
            "Choose Analog for circuit design and SPICE simulation, "
            "or Digital to also include HDL simulators."
        )
        desc.setFont(QFont("Arial", 11))
        desc.setStyleSheet("color: #666;")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        layout.addWidget(self._create_install_card(
            title       = "🔌  Analog Mode",
            description = ("Installs eSim, KiCad (latest), and Ngspice (latest) "
                           "for schematic and analog/mixed-signal simulation."),
            features    = ["✓ eSim EDA Platform",
                           "✓ KiCad",
                           "✓ Ngspice",
                           "✓ eSim Component Libraries"],
            disk_space  = "~1.5 GB",
            btn_text    = "Install Analog Mode",
            btn_color   = "#28a745",
            callback    = self._install_analog,
        ))

        layout.addWidget(self._create_install_card(
            title       = "💻  Digital Mode",
            description = ("Installs Analog Mode PLUS GHDL, Verilator, "
                           "and LLVM for VHDL and Verilog digital simulation."),
            features    = ["✓ Analog Mode",
                           "✓ GHDL",
                           "✓ Verilator",
                           "✓ LLVM "],
            disk_space  = "~3.0 GB",
            btn_text    = "Install Digital Mode",
            btn_color   = "#4A90E2",
            callback    = self._install_digital,
        ))

        self.progress_frame = QFrame()
        self.progress_frame.setVisible(False)
        self.progress_frame.setStyleSheet(
            "QFrame { background: #1e1e1e; border-radius: 6px; }"
        )
        pf_layout = QVBoxLayout(self.progress_frame)
        pf_layout.setContentsMargins(12, 10, 12, 10)
        pf_layout.setSpacing(6)

        pf_title = QLabel("Installation Progress")
        pf_title.setFont(QFont("Arial", 9, QFont.Weight.Bold))
        pf_title.setStyleSheet("color: #aaa; background: transparent;")
        pf_layout.addWidget(pf_title)

        self.progress_log = QLabel("")
        self.progress_log.setFont(QFont("Consolas", 9))
        self.progress_log.setStyleSheet(
            "color: #d4d4d4; background: transparent;"
        )
        self.progress_log.setWordWrap(True)
        self.progress_log.setAlignment(Qt.AlignTop)
        self.progress_log.setMinimumHeight(60)
        pf_layout.addWidget(self.progress_log)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background: #333; border-radius: 3px; border: none;
            }
            QProgressBar::chunk {
                background: #4A90E2; border-radius: 3px;
            }
        """)
        pf_layout.addWidget(self.progress_bar)
        layout.addWidget(self.progress_frame)
        layout.addStretch()
        return tab

    def _create_install_card(self, title, description, features,
                              disk_space, btn_text, btn_color, callback):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: white;
                border: none;
                border-radius: 8px;
            }
        """)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(10)

        t = QLabel(title)
        t.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        t.setStyleSheet("color: #333; background: transparent;")
        layout.addWidget(t)

        d = QLabel(description)
        d.setFont(QFont("Arial", 10))
        d.setStyleSheet("color: #666; background: transparent;")
        d.setWordWrap(True)
        layout.addWidget(d)

        f = QLabel("    ".join(features))
        f.setFont(QFont("Arial", 9))
        f.setStyleSheet("color: #555; background: transparent;")
        f.setWordWrap(True)
        layout.addWidget(f)

        bottom = QHBoxLayout()
        dl = QLabel(f"💾 {disk_space}")
        dl.setFont(QFont("Arial", 9))
        dl.setStyleSheet("color: #999; background: transparent;")
        bottom.addWidget(dl)
        bottom.addStretch()

        btn = QPushButton(btn_text)
        btn.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        btn.setCursor(Qt.PointingHandCursor)
        btn.setMinimumHeight(40)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: {btn_color}; color: white;
                border: none; border-radius: 4px; padding: 10px 24px;
            }}
            QPushButton:hover     {{ background: {darken_color(btn_color)}; }}
            QPushButton:pressed   {{ background: {darken_color(btn_color, 0.3)}; }}
            QPushButton:disabled  {{ background: #aaa; color: #ddd; }}
        """)
        btn.clicked.connect(callback)
        bottom.addWidget(btn)
        layout.addLayout(bottom)
        return card

    def _create_management_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        desc = QLabel("Update individual packages or manage specific tool versions:")
        desc.setFont(QFont("Arial", 11))
        desc.setStyleSheet("color: #666;")
        layout.addWidget(desc)

        btn = QPushButton("⚙   Open Full Tool Manager")
        btn.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedHeight(50)
        btn.setStyleSheet("""
            QPushButton {
                background: #4A90E2; color: white;
                border: none; border-radius: 6px; padding: 12px;
            }
            QPushButton:hover { background: #3a7bc8; }
        """)
        btn.clicked.connect(self._open_full_manager)
        layout.addWidget(btn)

        info = QLabel("""
<p style='color:#555; font-size:10pt; line-height:1.7;'>
<b>The Full Tool Manager allows you to:</b><br>
&nbsp;&nbsp;• Install or update <b>eSim</b> (v2.2, 2.3, 2.4, 2.5)<br>
&nbsp;&nbsp;• Install or update <b>KiCad</b> (v6, 7, 8, 9, latest)<br>
&nbsp;&nbsp;• Install or update <b>Ngspice</b> (v35–42, latest)<br>
&nbsp;&nbsp;• Install or update <b>GHDL</b> (v4.0.0, 4.1.0, 5.0.0, 5.1.1, latest)<br>
&nbsp;&nbsp;• Install or update <b>Verilator</b> (v5.006, 5.018, 5.026, 5.032, latest)<br>
&nbsp;&nbsp;• Install or update <b>LLVM</b> (v13–19, latest)<br>
&nbsp;&nbsp;• <b>Uninstall</b> any tool individually
</p>
        """)
        info.setWordWrap(True)
        info.setStyleSheet(
            "background: #f8f9fa; padding: 16px; border-radius: 6px;"
            "border: 1px solid #e0e0e0;"
        )
        layout.addWidget(info)
        layout.addStretch()
        return tab

    def _create_uninstall_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(16)

        # Warning banner
        warn = QFrame()
        warn.setStyleSheet("""
            QFrame {
                background: #fff3cd;
                border-left: 4px solid #ffc107;
                border-radius: 4px;
            }
        """)
        wl = QVBoxLayout(warn)
        wl.setContentsMargins(16, 12, 16, 12)
        wt = QLabel("⚠️  Warning")
        wt.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        wt.setStyleSheet("color: #856404; background: transparent;")
        wd = QLabel(
            "Uninstalling packages will remove them permanently. "
            "This action cannot be undone."
        )
        wd.setFont(QFont("Arial", 10))
        wd.setStyleSheet("color: #856404; background: transparent;")
        wd.setWordWrap(True)
        wl.addWidget(wt)
        wl.addWidget(wd)
        layout.addWidget(warn)

        desc = QLabel("Select what to uninstall:")
        desc.setFont(QFont("Arial", 11))
        desc.setStyleSheet("color: #666;")
        layout.addWidget(desc)

        def make_btn(text, color, callback):
            b = QPushButton(text)
            b.setFont(QFont("Arial", 10))
            b.setCursor(Qt.PointingHandCursor)
            b.setFixedHeight(46)
            dark = darken_color(color, 0.1)
            b.setStyleSheet(f"""
                QPushButton {{
                    background: {color}; color: white;
                    border: none; border-radius: 6px;
                    text-align: left; padding-left: 16px;
                }}
                QPushButton:hover {{ background: {dark}; }}
            """)
            b.clicked.connect(callback)
            return b

        layout.addWidget(make_btn(
            "🗑️   Uninstall Digital Packages  (GHDL + Verilator + LLVM)",
            "#dc3545", self._uninstall_digital
        ))
        layout.addWidget(make_btn(
            "🗑️   Uninstall Analog Packages  (KiCad + Ngspice)",
            "#e67e22", self._uninstall_analog
        ))
        layout.addWidget(make_btn(
            "🗑️   Uninstall Everything  (eSim + All Packages)",
            "#6c757d", self._uninstall_all
        ))

        sep = QLabel("— or uninstall tools individually via Full Tool Manager —")
        sep.setFont(QFont("Arial", 9))
        sep.setAlignment(Qt.AlignCenter)
        sep.setStyleSheet("color: #aaa;")
        layout.addWidget(sep)

        indiv = QPushButton("⚙   Open Full Tool Manager (Individual Uninstall)")
        indiv.setFont(QFont("Arial", 10))
        indiv.setCursor(Qt.PointingHandCursor)
        indiv.setFixedHeight(40)
        indiv.setStyleSheet("""
            QPushButton {
                background: white; color: #4A90E2;
                border: 1px solid #4A90E2; border-radius: 6px;
            }
            QPushButton:hover { background: #eaf3fb; }
        """)
        indiv.clicked.connect(self._open_full_manager)
        layout.addWidget(indiv)
        layout.addStretch()
        return tab

    def _create_about_tab(self):
        """Create about tab optimized for Windows 10/11"""
        tab = QWidget()
        tab.setStyleSheet("background-color: #ffffff;")
        
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(50, 40, 50, 40)
        layout.setSpacing(15)
        
        title = QLabel("About eSim Tool Manager")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #0056b3; margin-bottom: 5px;")
        layout.addWidget(title)        

        info_text = """
        <div style='font-family: "Segoe UI", sans-serif; font-size: 10.5pt; color: #333; line-height: 1.5;'>
            <p><b>Key Features:</b><br>
            <span style='color: #555;'>• Install analog or digital simulation packages<br>
            • Update individual package versions<br>
            • Uninstall packages selectively and Integrated with eSim GUI</span></p>
            
            <p><b>Supported Packages:</b><br>
            <span style='color: #555;'>• KiCad: 6.0.11, 7.0.11, 8.0.9<br>
            • Ngspice: 35, 36, 37, 38, 39, 40, 41, 42, 43<br>
            • GHDL: 3.0.0, 4.0.0, 4.1.0, nightly and Verilator: 4.228, 5.020, 5.026, 5.030</span></p>
        </div>
        """
        
        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        info_label.setStyleSheet("""
            background-color: #fcfcfc; 
            padding: 25px; 
            border: 1px solid #e0e0e0; 
            border-radius: 4px;
        """)
        layout.addWidget(info_label)
        
        layout.addStretch()
        return tab

    def _create_footer(self):
        footer = QFrame()
        footer.setFixedHeight(40)
        footer.setStyleSheet("""
            QFrame {
                background: #f5f5f5;
                border-top: 1px solid #e0e0e0;
            }
        """)
        layout = QHBoxLayout(footer)
        layout.setContentsMargins(20, 0, 20, 0)
        lbl = QLabel(
            "eSim Tool Manager"
        )
        lbl.setFont(QFont("Arial", 9))
        lbl.setStyleSheet("color: #999; background: transparent;")
        layout.addWidget(lbl)
        layout.addStretch()
        return footer

    def _refresh_status(self):
        self.installed_versions = load_installed_versions()
        new_panel = self._create_status_panel()
        self._main_layout.replaceWidget(self._status_frame, new_panel)
        self._status_frame.deleteLater()
        self._status_frame = new_panel

    def _install_analog(self):
        reply = QMessageBox.question(
            self, "Confirm Analog Mode Installation",
            "Install Analog Mode?\n\n"
            "This will install:\n"
            "  • eSim\n  • KiCad (latest)\n  • Ngspice (latest)\n\n"
            "Estimated size: ~1.5 GB\n"
            "This may take 20–40 minutes.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
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
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
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
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
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
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
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
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
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
        app = QApplication(sys.argv)
        msg = QMessageBox()
        msg.setWindowTitle("Administrator Required")
        msg.setIcon(QMessageBox.Warning)
        msg.setText(
            "eSim Tool Manager needs Administrator privileges\n"
            "to install and update tools.\n\n"
            "Click OK to relaunch as Administrator."
        )
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        if msg.exec() == QMessageBox.Ok:
            relaunch_as_admin()
        sys.exit(0)

    app = QApplication(sys.argv)
    app.setFont(QFont("Arial", 10))
    app.setStyle("Fusion")

    win = ToolManagerWindow()
    win.show()

    screen = app.desktop().screenGeometry()
    win.move(
        (screen.width()  - win.width())  // 2,
        (screen.height() - win.height()) // 3
    )
    sys.exit(app.exec())


if __name__ == "__main__":
    main()