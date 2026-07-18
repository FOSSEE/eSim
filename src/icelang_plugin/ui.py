"""
icelang_plugin.ui
=================
PyQt5 dialog layer for the ICELang KiCad plugin.

Provides run_dialog(), which is the only function called by __init__.py.
All compiler interaction goes through runner.run(). This file contains
zero compiler logic.
"""

import os
from pathlib import Path

try:
    from PyQt5.QtWidgets import (
        QDialog, QVBoxLayout, QHBoxLayout, QLabel,
        QPushButton, QFileDialog, QTextEdit, QLineEdit,
        QApplication, QMessageBox
    )
    from PyQt5.QtCore import Qt
    PYQT_AVAILABLE = True
except ImportError:
    PYQT_AVAILABLE = False

from icelang_plugin.runner import run, RunnerError


def run_dialog():
    """
    Entry point called by ICELangPlugin.Run().
    Opens the ICELang compiler dialog inside the running KiCad/eSim session.
    Falls back to a CLI prompt if PyQt5 is not available.
    """
    if PYQT_AVAILABLE:
        app = QApplication.instance()
        dialog = ICELangDialog()
        dialog.exec_()
    else:
        _cli_fallback()


def _cli_fallback():
    """
    Minimal CLI fallback when running outside a Qt context (e.g. tests).
    """
    ilang_path = input("Path to .ilang file: ").strip()
    output_dir = input("Output directory: ").strip()
    try:
        result = run(ilang_path, output_dir)
        print(f"Compiled: {result['kicad_sch']}")
    except RunnerError as e:
        print(f"Error: {e}")


if PYQT_AVAILABLE:
    class ICELangDialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle("ICELang Compiler")
            self.setMinimumWidth(520)
            self._build_ui()

        def _build_ui(self):
            layout = QVBoxLayout(self)

            # Source file row
            src_row = QHBoxLayout()
            self.src_field = QLineEdit()
            self.src_field.setPlaceholderText("Select a .ilang source file")
            src_row.addWidget(QLabel("Source:"))
            src_row.addWidget(self.src_field)
            browse_btn = QPushButton("Browse")
            browse_btn.clicked.connect(self._browse_source)
            src_row.addWidget(browse_btn)
            layout.addLayout(src_row)

            # Output dir row
            out_row = QHBoxLayout()
            self.out_field = QLineEdit()
            self.out_field.setPlaceholderText("Output directory (default: same as source)")
            out_row.addWidget(QLabel("Output:"))
            out_row.addWidget(self.out_field)
            out_browse = QPushButton("Browse")
            out_browse.clicked.connect(self._browse_output)
            out_row.addWidget(out_browse)
            layout.addLayout(out_row)

            # Log output
            self.log = QTextEdit()
            self.log.setReadOnly(True)
            self.log.setMinimumHeight(120)
            layout.addWidget(self.log)

            # Buttons
            btn_row = QHBoxLayout()
            compile_btn = QPushButton("Compile")
            compile_btn.clicked.connect(self._compile)
            close_btn = QPushButton("Close")
            close_btn.clicked.connect(self.accept)
            btn_row.addWidget(compile_btn)
            btn_row.addWidget(close_btn)
            layout.addLayout(btn_row)

        def _browse_source(self):
            path, _ = QFileDialog.getOpenFileName(
                self, "Select .ilang file", str(Path.home()),
                "ICELang files (*.ilang);;All files (*)"
            )
            if path:
                self.src_field.setText(path)
                if not self.out_field.text():
                    self.out_field.setText(str(Path(path).parent / "output"))

        def _browse_output(self):
            path = QFileDialog.getExistingDirectory(
                self, "Select output directory", str(Path.home())
            )
            if path:
                self.out_field.setText(path)

        def _compile(self):
            ilang_path = self.src_field.text().strip()
            output_dir = self.out_field.text().strip()

            if not ilang_path:
                self.log.append("Select a .ilang source file first.")
                return

            if not output_dir:
                output_dir = str(Path(ilang_path).parent / "output")
                self.out_field.setText(output_dir)

            self.log.append(f"Compiling {Path(ilang_path).name} ...")
            QApplication.processEvents()

            try:
                result = run(ilang_path, output_dir)
                self.log.append(f"OK  {result['kicad_sch']}")
                if result["spice_cir"]:
                    self.log.append(f"OK  {result['spice_cir']}")
                self.log.append("Done.")
            except RunnerError as e:
                self.log.append(f"Error: {e}")
