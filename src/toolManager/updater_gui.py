#!/usr/bin/env python3
import sys
import subprocess
import json
import os
import re
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QCheckBox,
                             QComboBox, QMessageBox, QFrame, QProgressBar,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QAbstractItemView)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

class InstallerThread(QThread):
    progress = pyqtSignal(str, int)
    log_output = pyqtSignal(str)  # NEW: For terminal output
    finished = pyqtSignal(bool, str)
    
    def __init__(self, packages_to_install):
        super().__init__()
        self.packages = packages_to_install
        
    def run(self):
        total = len(self.packages)
        for pkg_idx, (package_name, version, script_name) in enumerate(self.packages):
            try:
                base_progress = int((pkg_idx / total) * 100)
                self.progress.emit(f"Starting {package_name} {version}...", base_progress)
                
                script_path = os.path.join(os.path.dirname(__file__), script_name)
                if not os.path.exists(script_path):
                    self.finished.emit(False, f"Script not found: {script_name}")
                    return
                
                process = subprocess.Popen(
                    ['bash', script_path, version],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )
                
                step_progress = 0
                for line in iter(process.stdout.readline, ''):
                    if line:
                        self.log_output.emit(line.rstrip())
                        
                        line_lower = line.lower()
                        if any(word in line_lower for word in ['removing', 'purge', 'uninstall']):
                            step_progress = 10
                            msg = f"{package_name}: Removing old version..."
                        elif any(word in line_lower for word in ['updating', 'update', 'apt update']):
                            step_progress = 20
                            msg = f"{package_name}: Updating package lists..."
                        elif any(word in line_lower for word in ['installing dependencies', 'install -y']):
                            step_progress = 30
                            msg = f"{package_name}: Installing dependencies..."
                        elif any(word in line_lower for word in ['downloading', 'extracting', 'tar -x']):
                            step_progress = 40
                            msg = f"{package_name}: Extracting files..."
                        elif any(word in line_lower for word in ['configuring', './configure']):
                            step_progress = 50
                            msg = f"{package_name}: Configuring..."
                        elif any(word in line_lower for word in ['compiling', 'building', 'make -j', 'make[']):
                            step_progress = 70
                            msg = f"{package_name}: Compiling (this may take a while)..."
                        elif any(word in line_lower for word in ['installing', 'make install']):
                            step_progress = 85
                            msg = f"{package_name}: Installing..."
                        elif any(word in line_lower for word in ['verifying', 'success', 'installed successfully']):
                            step_progress = 95
                            msg = f"{package_name}: Verifying installation..."
                        else:
                            continue  # Don't spam progress updates
                        
                        total_progress = base_progress + int((step_progress / 100) * (100 / total))
                        self.progress.emit(msg, min(total_progress, 99))
                
                process.stdout.close()
                return_code = process.wait()
                
                if return_code != 0:
                    self.finished.emit(False, f"Failed: {package_name} (exit code {return_code})")
                    return
                    
            except Exception as e:
                self.finished.emit(False, f"Error: {str(e)}")
                return
        
        self.progress.emit("Installation complete!", 100)
        self.finished.emit(True, f"Successfully installed {total} package(s)")


class PackageUpdaterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.installed_versions = {}
        
        self.available_versions = {
            'KiCad': ['6.0.11', '7.0.11', '8.0.9'],
            'Ngspice': ['35', '36', '37', '38', '39', '40', '41', '42', '43'],  # ALL VERSIONS!
            'GHDL': ['3.0.0', '4.0.0', '4.1.0', 'nightly'],
            'Verilator': ['4.228', '5.020', '5.026', '5.030']
        }
        self.script_mapping = {
            'KiCad': 'update-kicad-final.sh',
            'Ngspice': 'nghdl/update-ngspice-final.sh',  # Correct path!
            'GHDL': 'nghdl/update-ghdl-with-dependency.sh',
            'Verilator': 'nghdl/update-verilator-final.sh'
        }
        
        self.detect_installed_versions()
        self.initUI()
        
    def detect_installed_versions(self):
        self.installed_versions = {}
        
        print("🔍 Detecting installed package versions...")
        
        try:
            result = subprocess.run(['dpkg', '-l', 'kicad'], 
                                   capture_output=True, text=True, timeout=2)
            if result.returncode == 0 and 'ii' in result.stdout:
                match = re.search(r'kicad\s+(\d+\.\d+\.?\d*)', result.stdout)
                if match:
                    ver = match.group(1)
                    self.installed_versions['KiCad'] = ver
                    print(f"  ✓ KiCad: {ver}")
        except:
            print(f"  ✗ KiCad: Not installed")
        
        try:
            result = subprocess.run(['ngspice', '--version'], 
                                   capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                match = re.search(r'ngspice[- ]?(\d+)', result.stdout.lower())
                if match:
                    ver = match.group(1)
                    self.installed_versions['Ngspice'] = ver
                    print(f"  ✓ Ngspice: {ver}")
        except:
            print(f"  ✗ Ngspice: Not installed")
        
        try:
            result = subprocess.run(['ghdl', '--version'], 
                                   capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                match = re.search(r'(\d+\.\d+\.?\d*)', result.stdout)
                if match:
                    ver = match.group(1)
                    self.installed_versions['GHDL'] = ver
                    print(f"  ✓ GHDL: {ver}")
        except:
            print(f"  ✗ GHDL: Not installed")
        
        try:
            result = subprocess.run(['verilator', '--version'], 
                                   capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                match = re.search(r'(\d+\.\d+)', result.stdout)
                if match:
                    ver = match.group(1)
                    self.installed_versions['Verilator'] = ver
                    print(f"  ✓ Verilator: {ver}")
        except:
            print(f"  ✗ Verilator: Not installed")
        
        print(f"✓ Detection complete: {len(self.installed_versions)} packages found\n")
    
    def refresh_versions(self):
        print("\n🔄 Refreshing...")
        self.detect_installed_versions()
        
        for row, package_name in enumerate(['KiCad', 'Ngspice', 'GHDL', 'Verilator']):
            current_ver = self.installed_versions.get(package_name, 'Not installed')
            
            current_item = QTableWidgetItem(current_ver)
            current_item.setFont(QFont("Segoe UI", 9))
            if current_ver != 'Not installed':
                current_item.setForeground(Qt.darkGreen)
            else:
                current_item.setForeground(Qt.red)
            self.table.setItem(row, 2, current_item)
            
            if current_ver in self.available_versions[package_name]:
                self.combos[package_name].setCurrentText(current_ver)
        
        installed_list = '\n'.join([f"  • {k}: {v}" for k, v in self.installed_versions.items()])
        not_installed = [k for k in ['KiCad', 'Ngspice', 'GHDL', 'Verilator'] 
                        if k not in self.installed_versions]
        not_installed_list = '\n'.join([f"  • {k}" for k in not_installed])
        
        msg = "✓ Refreshed!\n\n"
        if installed_list:
            msg += f"Installed:\n{installed_list}\n"
        if not_installed_list:
            msg += f"\nNot Installed:\n{not_installed_list}"
        
        QMessageBox.information(self, 'Refreshed', msg)
    
    def initUI(self):
        self.setWindowTitle('eSim Package Updater v2.2')
        self.setGeometry(150, 150, 750, 500)
        self.setMinimumSize(700, 450)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        header = self.create_header()
        main_layout.addWidget(header)
        
        table_frame = QWidget()
        table_frame.setStyleSheet("background: white;")
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(10, 10, 10, 10)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setRowCount(4)
        self.table.setHorizontalHeaderLabels(['', 'Package', 'Current Version', 'Update To'])
        
        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #e0e0e0;
                background-color: white;
                border: 1px solid #d0d0d0;
                selection-background-color: #e5f3ff;
            }
            QTableWidget::item {
                padding: 2px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #e5f3ff;
                color: black;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 4px;
                border: none;
                border-right: 1px solid #d0d0d0;
                border-bottom: 1px solid #d0d0d0;
                font-weight: normal;
                color: #333;
            }
        """)
        
        self.table.setFont(QFont("Segoe UI", 9))
        self.table.horizontalHeader().setFont(QFont("Segoe UI", 9))
        
        self.table.setColumnWidth(0, 40)
        self.table.setColumnWidth(1, 120)
        self.table.setColumnWidth(2, 200)
        self.table.setColumnWidth(3, 220)
        
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(True)
        
        for i in range(4):
            self.table.setRowHeight(i, 28)
        
        self.checkboxes = {}
        self.combos = {}
        
        for row, package_name in enumerate(['KiCad', 'Ngspice', 'GHDL', 'Verilator']):
            checkbox = QCheckBox()
            checkbox.setStyleSheet("margin-left: 12px;")
            checkbox_widget = QWidget()
            checkbox_layout = QHBoxLayout(checkbox_widget)
            checkbox_layout.addWidget(checkbox)
            checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            self.table.setCellWidget(row, 0, checkbox_widget)
            self.checkboxes[package_name] = checkbox
            
            name_item = QTableWidgetItem(package_name)
            name_item.setFont(QFont("Segoe UI", 9))
            self.table.setItem(row, 1, name_item)
            
            current_ver = self.installed_versions.get(package_name, 'Not installed')
            current_item = QTableWidgetItem(current_ver)
            current_item.setFont(QFont("Segoe UI", 9))
            if current_ver != 'Not installed':
                current_item.setForeground(Qt.darkGreen)
            else:
                current_item.setForeground(Qt.red)
            self.table.setItem(row, 2, current_item)
            
            combo = QComboBox()
            combo.setFont(QFont("Segoe UI", 9))
            combo.setStyleSheet("""
                QComboBox {
                    border: 1px solid #adadad;
                    padding: 2px 5px;
                    background: white;
                    color: black;
                }
                QComboBox:hover {
                    border: 1px solid #0078d7;
                }
                QComboBox::drop-down {
                    border: none;
                    width: 18px;
                }
                QComboBox::down-arrow {
                    image: none;
                    border-left: 4px solid transparent;
                    border-right: 4px solid transparent;
                    border-top: 4px solid #333;
                    margin-right: 4px;
                }
                QComboBox QAbstractItemView {
                    background: white;
                    color: black;
                    selection-background-color: #0078d7;
                    selection-color: white;
                    border: 1px solid #adadad;
                }
            """)
            
            for version in self.available_versions[package_name]:
                combo.addItem(version)
            
            if current_ver in self.available_versions[package_name]:
                combo.setCurrentText(current_ver)
            
            self.combos[package_name] = combo
            self.table.setCellWidget(row, 3, combo)
        
        table_layout.addWidget(self.table)
        main_layout.addWidget(table_frame)
        
        self.progress_frame = self.create_progress()
        main_layout.addWidget(self.progress_frame)
        self.progress_frame.hide()
        
        buttons = self.create_buttons()
        main_layout.addWidget(buttons)
    
    def create_header(self):
        header = QFrame()
        header.setFixedHeight(60)
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5B9BD5, stop:1 #4A90E2);
            }
        """)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(15, 8, 15, 8)
        
        icon = QLabel("📦")
        icon.setStyleSheet("font-size: 28px; background: transparent;")
        layout.addWidget(icon)
        
        title_layout = QVBoxLayout()
        title = QLabel("Package Updater")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: white; background: transparent;")
        
        subtitle = QLabel("Real-time progress • Ngspice 35-43 • Ubuntu 22.04")
        subtitle.setFont(QFont("Segoe UI", 8))
        subtitle.setStyleSheet("color: rgba(255,255,255,0.9); background: transparent;")
        
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        
        return header
    
    def create_progress(self):
        frame = QFrame()
        frame.setStyleSheet("background: #f0f0f0; border-top: 1px solid #d0d0d0;")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(15, 10, 15, 10)
        
        self.status_label = QLabel("Preparing...")
        self.status_label.setFont(QFont("Segoe UI", 9))
        layout.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(18)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #adadad;
                border-radius: 0px;
                text-align: center;
                background: white;
            }
            QProgressBar::chunk {
                background-color: #06b025;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        return frame
    
    def create_buttons(self):
        frame = QFrame()
        frame.setFixedHeight(55)
        frame.setStyleSheet("background: #f0f0f0; border-top: 1px solid #d0d0d0;")
        
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(12, 10, 12, 10)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setFixedSize(85, 26)
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.setStyleSheet(self.get_win_button_style())
        refresh_btn.clicked.connect(self.refresh_versions)
        layout.addWidget(refresh_btn)
        
        layout.addSpacing(10)
        
        select_btn = QPushButton("Select All")
        select_btn.setFixedSize(75, 26)
        select_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        select_btn.setStyleSheet(self.get_win_button_style())
        select_btn.clicked.connect(lambda: [cb.setChecked(True) for cb in self.checkboxes.values()])
        layout.addWidget(select_btn)
        
        deselect_btn = QPushButton("Deselect All")
        deselect_btn.setFixedSize(85, 26)
        deselect_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        deselect_btn.setStyleSheet(self.get_win_button_style())
        deselect_btn.clicked.connect(lambda: [cb.setChecked(False) for cb in self.checkboxes.values()])
        layout.addWidget(deselect_btn)
        
        layout.addStretch()
        
        self.update_btn = QPushButton("Update Selected")
        self.update_btn.setFixedSize(120, 28)
        self.update_btn.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        self.update_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                border: 1px solid #005a9e;
                padding: 4px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QPushButton:pressed {
                background-color: #004578;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
                border: 1px solid #adadad;
            }
        """)
        self.update_btn.clicked.connect(self.start_update)
        layout.addWidget(self.update_btn)
        
        return frame
    
    def get_win_button_style(self):
        return """
            QPushButton {
                background-color: #e1e1e1;
                color: black;
                border: 1px solid #adadad;
                padding: 3px;
                font-size: 9pt;
            }
            QPushButton:hover {
                background-color: #e5f1fb;
                border: 1px solid #0078d7;
            }
            QPushButton:pressed {
                background-color: #cce4f7;
            }
        """
    
    def start_update(self):
        selected = []
        for pkg, cb in self.checkboxes.items():
            if cb.isChecked():
                ver = self.combos[pkg].currentText()
                script = self.script_mapping[pkg]
                selected.append((pkg, ver, script))
        
        if not selected:
            QMessageBox.warning(self, 'No Selection', 'Please select packages.')
            return
        
        pkg_list = "\n".join([f"{n} → {v}" for n, v, _ in selected])
        reply = QMessageBox.question(self, 'Confirm',
                                    f'Update these packages?\n\n{pkg_list}\n\n'
                                    f'This will take several minutes.',
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.No:
            return
        
        self.progress_frame.show()
        self.update_btn.setEnabled(False)
        
        self.thread = InstallerThread(selected)
        self.thread.progress.connect(self.update_progress)
        self.thread.log_output.connect(self.print_log)
        self.thread.finished.connect(self.done)
        self.thread.start()
    
    def update_progress(self, msg, pct):
        self.status_label.setText(msg)
        self.progress_bar.setValue(pct)
    
    def print_log(self, line):
        """Print script output to terminal"""
        print(line)
    
    def done(self, success, msg):
        self.update_btn.setEnabled(True)
        if success:
            QMessageBox.information(self, 'Success', msg)
            self.refresh_versions()
        else:
            QMessageBox.critical(self, 'Failed', msg)


def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 9))
    window = PackageUpdaterWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
