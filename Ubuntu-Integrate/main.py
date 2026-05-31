#!/usr/bin/env python3
import sys
import subprocess
import json
import os
import re
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QTabWidget, 
                             QMessageBox, QFrame, QScrollArea, QGridLayout)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon, QPixmap


class ToolManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.installed_versions = {}
        self.load_installed_versions()
        self.initUI()
        
    def load_installed_versions(self):
        self.installed_versions = {}
        
        print("🔍 Detecting installed package versions...")
        
        # KiCad (use dpkg)
        try:
            result = subprocess.run(['dpkg', '-l', 'kicad'], 
                                   capture_output=True, text=True, timeout=5)
            if result.returncode == 0 and 'ii' in result.stdout:
                match = re.search(r'kicad\s+(\d+\.\d+\.?\d*)', result.stdout)
                if match:
                    self.installed_versions['kicad'] = match.group(1)
                    print(f"  ✓ KiCad: {match.group(1)}")
        except Exception as e:
            print(f"  KiCad detection error: {e}")
        
        # Ngspice
        try:
            result = subprocess.run(['ngspice', '--version'], 
                                   capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                match = re.search(r'ngspice[- ]?(\d+)', result.stdout.lower())
                if match:
                    self.installed_versions['ngspice'] = match.group(1)
                    print(f"  ✓ Ngspice: {match.group(1)}")
        except Exception as e:
            print(f"  Ngspice detection error: {e}")
        
        try:
            result = subprocess.run(['ghdl', '--version'], 
                                   capture_output=True, text=True, timeout=5)
            
            # GHDL often outputs to stderr, so combine both
            output = result.stdout + result.stderr
            
            if output:
                # Look for version pattern
                match = re.search(r'ghdl[-\s]?(\d+\.\d+\.?\d*)', output, re.IGNORECASE)
                if not match:
                    match = re.search(r'(\d+\.\d+\.?\d+)', output)
                
                if match:
                    self.installed_versions['ghdl'] = match.group(1)
                    print(f"  ✓ GHDL: {match.group(1)}")
                else:
                    print(f"  GHDL output but no version found")
            else:
                print("  GHDL: No output from command")
                
        except FileNotFoundError:
            print("  ✗ GHDL: Not installed (command not found)")
        except subprocess.TimeoutExpired:
            print("  GHDL: Timeout")
        except Exception as e:
            print(f"  GHDL detection error: {e}")
        
        # Verilator
        try:
            result = subprocess.run(['verilator', '--version'], 
                                   capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                match = re.search(r'(\d+\.\d+)', result.stdout)
                if match:
                    self.installed_versions['verilator'] = match.group(1)
                    print(f"  ✓ Verilator: {match.group(1)}")
        except Exception as e:
            print(f"  Verilator detection error: {e}")
        
        print(f"✓ Detection complete: {len(self.installed_versions)} packages found\n")
            
    def initUI(self):
        self.setWindowTitle('eSim Tool Manager')
        self.setGeometry(100, 100, 800, 700)
        self.setMinimumSize(750, 650)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        header = self.create_header()
        main_layout.addWidget(header)
        
        status_panel = self.create_status_panel()
        main_layout.addWidget(status_panel)
        
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: white;
            }
            QTabBar::tab {
                background: #f5f5f5;
                color: #000;
                padding: 12px 24px;
                min-width: 100px;
                margin-right: 1px;
                border: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                font-size: 13px;
                font-weight: 500;
            }
            QTabBar::tab:selected {
                background: white;
                color: #b87333;
            }
            QTabBar::tab:hover {
                background: #e8e8e8;
            }
        """)
        
        tabs.addTab(self.create_installation_tab(), "Installation")
        tabs.addTab(self.create_management_tab(), "Management")
        tabs.addTab(self.create_uninstall_tab(), "Uninstall")
        tabs.addTab(self.create_about_tab(), "About")
        
        main_layout.addWidget(tabs)
        
        footer = self.create_footer()
        main_layout.addWidget(footer)

    def create_header(self):
        header_frame = QFrame()
        header_frame.setFixedHeight(140)
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #b87333, stop:1 #a0622d);
            }
        """)

        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(30, 20, 30, 20)

        logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(__file__), 'images', 'toolmanager.png')
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            scaled_pixmap = pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        else:
            logo_label.setText("⚙️")
            logo_label.setStyleSheet("font-size: 48px; background: transparent;")

        header_layout.addWidget(logo_label)
        title_layout = QVBoxLayout()
        title_layout.setSpacing(5)

        title = QLabel("eSim Tool Manager")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: white; background: transparent;")

        subtitle = QLabel("Tool And Package Management System")
        subtitle.setFont(QFont("Arial", 11))
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.9); background: transparent;")

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        title_layout.addStretch()

        header_layout.addLayout(title_layout)
        header_layout.addStretch()

        return header_frame

    def create_status_panel(self):
        status_frame = QFrame()
        status_frame.setStyleSheet("""
            QFrame {
                background: #f8f9fa;
                border-bottom: 1px solid #e0e0e0;
            }
        """)
        
        status_layout = QHBoxLayout(status_frame)
        status_layout.setContentsMargins(30, 15, 30, 15)
        
        title_label = QLabel("📦 Installed Packages:")
        title_label.setFont(QFont("Arial", 10, QFont.Bold))
        title_label.setStyleSheet("color: #666; background: transparent;")
        status_layout.addWidget(title_label)
        
        packages = [
            ('KiCad', self.installed_versions.get('kicad', 'Not installed')),
            ('Ngspice', self.installed_versions.get('ngspice', 'Not installed')),
            ('GHDL', self.installed_versions.get('ghdl', 'Not installed')),
            ('Verilator', self.installed_versions.get('verilator', 'Not installed'))
        ]
        
        for name, version in packages:
            if version != 'Not installed':
                status_text = f"<span style='color: #28a745;'>●</span> {name} <span style='color: #666;'>{version}</span>"
            else:
                status_text = f"<span style='color: #dc3545;'>○</span> {name} <span style='color: #999;'>—</span>"
            
            status_label = QLabel(status_text)
            status_label.setFont(QFont("Arial", 9))
            status_label.setStyleSheet("background: transparent; margin-left: 15px;")
            status_layout.addWidget(status_label)
        
        status_layout.addStretch()
        return status_frame
    
    def create_installation_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        desc = QLabel("Install eSim with required simulation tools. Choose your installation mode:")
        desc.setFont(QFont("Arial", 11))
        desc.setStyleSheet("color: #666; margin-bottom: 10px;")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        analog_card = self.create_install_card(
            title="Analog Mode Installation",
            description="Installs KiCad 8.0 and Ngspice 40 for analog circuit simulation.",
            features=["✓ KiCad Schematic Editor", "✓ Ngspice Simulator", "✓ Basic Component Libraries"],
            disk_space="~800 MB",
            button_text="Install Analog Mode",
            button_color="#28a745",
            callback=self.install_analog
        )
        layout.addWidget(analog_card)
        
        digital_card = self.create_install_card(
            title="Digital Mode Installation",
            description="Installs Analog Mode PLUS GHDL 4.0 and Verilator 4.210 for digital simulation.",
            features=["✓ Everything in Analog Mode", "✓ GHDL (VHDL Simulator)", "✓ Verilator (Verilog Simulator)"],
            disk_space="~1.5 GB",
            button_text="Install Digital Mode",
            button_color="#4A90E2",
            callback=self.install_digital
        )
        layout.addWidget(digital_card)
        
        layout.addStretch()
        return tab
    
    def create_install_card(self, title, description, features, disk_space, button_text, button_color, callback):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 8px;
            }
            QFrame:hover {
                border-color: #c0c0c0;
            }
        """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 20, 25, 20)
        card_layout.setSpacing(12)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 13, QFont.Bold))
        title_label.setStyleSheet("color: #333; background: transparent;")
        card_layout.addWidget(title_label)
        
        desc_label = QLabel(description)
        desc_label.setFont(QFont("Arial", 10))
        desc_label.setStyleSheet("color: #666; background: transparent;")
        desc_label.setWordWrap(True)
        card_layout.addWidget(desc_label)
        
        features_text = "  ".join(features)
        features_label = QLabel(features_text)
        features_label.setFont(QFont("Arial", 9))
        features_label.setStyleSheet("color: #555; background: transparent; margin-top: 5px;")
        features_label.setWordWrap(True)
        card_layout.addWidget(features_label)
        
        bottom_layout = QHBoxLayout()
        
        disk_label = QLabel(f"💾 {disk_space}")
        disk_label.setFont(QFont("Arial", 9))
        disk_label.setStyleSheet("color: #999; background: transparent;")
        bottom_layout.addWidget(disk_label)
        
        bottom_layout.addStretch()
        
        install_btn = QPushButton(button_text)
        install_btn.setFont(QFont("Arial", 11, QFont.Bold))
        install_btn.setCursor(Qt.PointingHandCursor)
        install_btn.setMinimumHeight(40)
        install_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {button_color};
                color: #FFFFFF;
                border: none;
                border-radius: 4px;
                padding: 10px 24px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(button_color)};
            }}
            QPushButton:pressed {{
                background-color: {self.darken_color(button_color, 0.3)};
            }}
        """)
        install_btn.clicked.connect(callback)
        bottom_layout.addWidget(install_btn)
        
        card_layout.addLayout(bottom_layout)
        
        return card
    
    def darken_color(self, hex_color, amount=0.15):
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r = max(0, int(r * (1 - amount)))
        g = max(0, int(g * (1 - amount)))
        b = max(0, int(b * (1 - amount)))
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def create_management_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        desc = QLabel("Update individual packages to newer or different versions:")
        desc.setFont(QFont("Arial", 11))
        desc.setStyleSheet("color: #666;")
        layout.addWidget(desc)
        
        updater_btn = QPushButton("🔄 Open Package Updater")
        updater_btn.setFont(QFont("Arial", 11, QFont.Bold))
        updater_btn.setCursor(Qt.PointingHandCursor)
        updater_btn.setFixedHeight(50)
        updater_btn.setStyleSheet("""
            QPushButton {
                background: #4A90E2;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px;
            }
            QPushButton:hover {
                background: #3a7bc8;
            }
        """)
        updater_btn.clicked.connect(self.open_updater)
        layout.addWidget(updater_btn)
        
        info_text = """
        <p style='color: #666; font-size: 10pt;'>
        <b>The Package Updater allows you to:</b><br>
        • Update KiCad to version 6.0.11, 7.0.11 or 8.0.9<br>
        • Update Ngspice to version 35, 36, 37, 38, 39, 40, or latest<br>
        • Update GHDL to version 3.0.0, 4.0.0, 4.1.0, or nightly<br>
        • Update Verilator to version 4.228, 5.020, 5.026, or 5.030
        </p>
        """
        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        info_label.setStyleSheet("background: #f8f9fa; padding: 15px; border-radius: 6px;")
        layout.addWidget(info_label)
        
        layout.addStretch()
        return tab
    
    def create_uninstall_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        warning_frame = QFrame()
        warning_frame.setStyleSheet("""
            QFrame {
                background: #fff3cd;
                border-left: 4px solid #ffc107;
                border-radius: 4px;
                padding: 15px;
            }
        """)
        warning_layout = QVBoxLayout(warning_frame)
        
        warning_icon = QLabel("⚠️ Warning")
        warning_icon.setFont(QFont("Arial", 12, QFont.Bold))
        warning_icon.setStyleSheet("color: #856404; background: transparent;")
        
        warning_text = QLabel("Uninstalling packages will remove them from your system. This action cannot be undone.")
        warning_text.setFont(QFont("Arial", 10))
        warning_text.setStyleSheet("color: #856404; background: transparent;")
        warning_text.setWordWrap(True)
        
        warning_layout.addWidget(warning_icon)
        warning_layout.addWidget(warning_text)
        
        layout.addWidget(warning_frame)
        
        desc = QLabel("Select what to uninstall:")
        desc.setFont(QFont("Arial", 11))
        desc.setStyleSheet("color: #666; margin-top: 10px;")
        layout.addWidget(desc)
        
        digital_btn = QPushButton("Uninstall Digital Packages (GHDL + Verilator)")
        digital_btn.setFont(QFont("Arial", 10))
        digital_btn.setCursor(Qt.PointingHandCursor)
        digital_btn.setFixedHeight(45)
        digital_btn.setStyleSheet("""
            QPushButton {
                background: #dc3545;
                color: white;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: #c82333;
            }
        """)
        digital_btn.clicked.connect(self.uninstall_digital)
        layout.addWidget(digital_btn)
        
        complete_btn = QPushButton("Uninstall Everything (eSim + All Packages)")
        complete_btn.setFont(QFont("Arial", 10))
        complete_btn.setCursor(Qt.PointingHandCursor)
        complete_btn.setFixedHeight(45)
        complete_btn.setStyleSheet("""
            QPushButton {
                background: #6c757d;
                color: white;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: #5a6268;
            }
        """)
        complete_btn.clicked.connect(self.uninstall_complete)
        layout.addWidget(complete_btn)
        
        layout.addStretch()
        return tab
    
    def create_about_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        title = QLabel("About eSim Tool Manager")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: #333;")
        layout.addWidget(title)
        
        info_text = """
        <p style='font-size: 11pt; color: #555; line-height: 1.6;'>
	<b>Key Features:</b><br>
	• Install analog or digital simulation packages<br>
	• Update individual package versions<br>
	• Uninstall packages selectively<br>
	• Integrated with eSim GUI<br><br>   
	<b>Supported Packages:</b><br>
	• KiCad: 6.0.11, 7.0.11, 8.0.9<br>
	• Ngspice: 35, 36, 37, 38, 39, 40, 41, 42, 43<br>
	• GHDL: 3.0.0, 4.0.0, 4.1.0, nightly and Verilator: 4.228, 5.020, 5.026, 5.030<br><br>
	</p>
	"""
        
        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        info_label.setStyleSheet("background: #f8f9fa; padding: 20px; border-radius: 8px;")
        layout.addWidget(info_label)
        
        layout.addStretch()
        return tab
    
    def create_footer(self):
        footer = QFrame()
        footer.setFixedHeight(40)
        footer.setStyleSheet("""
            QFrame {
                background: #f5f5f5;
                border-top: 1px solid #e0e0e0;
            }
        """)
        
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(20, 0, 20, 0)
        
        footer_text = QLabel("eSim Tool Manager • FOSSEE, IIT Bombay")
        footer_text.setFont(QFont("Arial", 9))
        footer_text.setStyleSheet("color: #999; background: transparent;")
        
        footer_layout.addWidget(footer_text)
        footer_layout.addStretch()
        
        return footer
   
    
    def install_analog(self):
        reply = QMessageBox.question(
            self,
            'Confirm Installation',
            'Install Analog Mode?\n\nThis will install KiCad and Ngspice.',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.run_installation('--install-analog')


    def install_digital(self):
        reply = QMessageBox.question(
            self,
            'Confirm Installation',
            'Install Digital Mode?\n\nThis will install KiCad, Ngspice, GHDL, and Verilator.',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.run_installation('--install-digital')
    
    def run_installation(self, mode):
        try:
            script_path = os.path.join(os.path.dirname(__file__), 'install-eSim.sh')
            subprocess.Popen(['xterm', '-e', f'bash {script_path} {mode}'])
            QMessageBox.information(self, 'Installation Started',
                                  f'Installation has started in a new terminal window.\n\n'
                                  f'Please wait for it to complete.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to start installation:\n{str(e)}')
    
    def open_updater(self):
        try:
            updater_path = os.path.join(os.path.dirname(__file__), 'updater_gui.py')
            subprocess.Popen(['python3', updater_path])
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to open updater:\n{str(e)}')
    
    def uninstall_digital(self):
        reply = QMessageBox.warning(self, 'Confirm Uninstall',
                                   'Uninstall digital packages (GHDL and Verilator)?\n\n'
                                   'This will remove GHDL and Verilator from your system.\n'
                                   'This action cannot be undone!',
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                uninstall_script = """#!/bin/bash
echo "========================================="
echo "Uninstalling Digital Packages"
echo "========================================="

check_ghdl() {
    if command -v ghdl &> /dev/null; then
        echo "✓ GHDL command found"
        return 0
    else
        echo "✗ GHDL command not found"
        return 1
    fi
}

echo ""
echo "Current state before uninstall:"
echo "--------------------------------"
check_ghdl
if command -v verilator &> /dev/null; then
    echo "✓ Verilator command found"
else
    echo "✗ Verilator command not found"
fi
echo ""

echo "Removing GHDL..."
echo "--------------------------------"

if dpkg -l | grep -q ghdl; then
    echo "Found GHDL package(s) installed via apt"
    sudo apt-get remove --purge -y ghdl ghdl-llvm ghdl-gcc ghdl-common 2>/dev/null
    sudo apt-get autoremove -y
    echo "✓ GHDL packages removed"
else
    echo "No GHDL packages found via apt"
fi

echo "Removing manual GHDL installations..."
sudo rm -rf /usr/local/bin/ghdl
sudo rm -rf /usr/local/lib/ghdl
sudo rm -rf /usr/local/share/ghdl
sudo rm -rf /usr/lib/ghdl
echo "✓ Manual GHDL files removed"

echo ""
echo "Removing Verilator..."
echo "--------------------------------"
if dpkg -l | grep -q verilator; then
    echo "Found Verilator package installed via apt"
    sudo apt-get remove --purge -y verilator 2>/dev/null
    echo "✓ Verilator package removed"
fi

echo "Removing manual Verilator installations..."
sudo rm -rf /usr/local/bin/verilator
sudo rm -rf /usr/local/share/verilator
sudo rm -rf /usr/local/include/verilator
sudo rm -rf /usr/lib/verilator
sudo rm -rf /usr/share/verilator
echo "✓ Manual Verilator files removed"

echo ""
echo "Cleaning up unused packages..."
echo "--------------------------------"
sudo apt-get autoremove -y

echo ""
echo "========================================="
echo "Verifying uninstallation:"
echo "--------------------------------"
echo -n "GHDL: "
if command -v ghdl &> /dev/null; then
    echo "❌ Still installed"
else
    echo "✅ Successfully removed"
fi

echo -n "Verilator: "
if command -v verilator &> /dev/null; then
    echo "❌ Still installed"
else
    echo "✅ Successfully removed"
fi
echo "========================================="

echo ""
read -p "Press Enter to close..."
"""
                script_file = '/tmp/uninstall_digital.sh'
                with open(script_file, 'w') as f:
                    f.write(uninstall_script)
                os.chmod(script_file, 0o755)
                
                subprocess.Popen(['xterm', '-e', f'bash {script_file}'])
                QMessageBox.information(self, 'Uninstall Started',
                                      'Uninstallation has started in a new terminal window.\n\n'
                                      'The window will show detailed progress and verification.')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to uninstall:\n{str(e)}')
    
    def uninstall_complete(self):
        reply = QMessageBox.warning(self, 'Confirm Complete Uninstall',
                                   'Uninstall eSim and ALL packages?\n\n'
                                   'This will remove eSim, KiCad, Ngspice, GHDL, Verilator, and all libraries.\n'
                                   'This action cannot be undone!',
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                script_path = os.path.join(os.path.dirname(__file__), 'install-eSim.sh')
                subprocess.Popen(['xterm', '-e', f'bash {script_path} --uninstall'])
                QMessageBox.information(self, 'Uninstall Started',
                                      'Complete uninstallation has started in a new terminal window.')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to uninstall:\n{str(e)}')


def main():
    app = QApplication(sys.argv)
    
    # Set application-wide font
    font = QFont("Arial", 10)
    app.setFont(font)
    
    window = ToolManagerWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
