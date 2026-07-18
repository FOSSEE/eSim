import os
import sys
from PyQt6 import QtWidgets
from pathlib import Path

ICELANG_ROOT = os.path.join(os.path.dirname(__file__), '..', 'icelang')
PLUGIN_ROOT  = os.path.join(os.path.dirname(__file__), '..', 'icelang_plugin')

for p in [ICELANG_ROOT, str(Path(PLUGIN_ROOT).parent)]:
    if p not in sys.path:
        sys.path.insert(0, p)


def open_icelang(parent=None):
    path, _ = QtWidgets.QFileDialog.getOpenFileName(
        parent,
        "Open ICELang source file",
        str(Path.home()),
        "ICELang files (*.ilang);;All files (*)"
    )
    if not path:
        return

    output_dir = str(Path(path).parent / "output")
    os.makedirs(output_dir, exist_ok=True)

    try:
        os.environ.setdefault("ICELANG_ROOT", ICELANG_ROOT)
        from icelang_plugin.runner import run, RunnerError
        result = run(path, output_dir)
        QtWidgets.QMessageBox.information(
            parent,
            "ICELang",
            f"Compiled successfully.\n\n"
            f"Schematic: {result['kicad_sch']}\n"
            f"SPICE:     {result.get('spice_cir', 'N/A')}\n\n"
            f"Open the schematic in KiCad to view."
        )
    except Exception as e:
        QtWidgets.QMessageBox.critical(
            parent,
            "ICELang Error",
            str(e)
        )
