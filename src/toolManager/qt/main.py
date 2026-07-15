from toolManager.main import ToolManagerWindow, main
from toolManager.registry import TOOLS, CATEGORIES
from toolManager.constants import IS_WINDOWS
from toolManager.qt.gui_fixed import ToolManagerGUI

ANALOG_TOOLS = CATEGORIES["analog"]
DIGITAL_TOOLS = CATEGORIES["digital"]
TOOL_LABELS = {tid: spec.label for tid, spec in TOOLS.items()
                if tid in CATEGORIES["analog"] or tid in CATEGORIES["digital"]}
TOOL_VERSIONS = {
    "esim": "2.4",
    "kicad": "latest",
    "ngspice": "latest",
    "ghdl": "latest",
    "verilator": "latest",
    "llvm": "latest",
}

try:
    from toolManager.platform_utils import is_admin, relaunch_as_admin
except ImportError:
    import ctypes
    import os
    import sys

    def is_admin():
        if IS_WINDOWS:
            try:
                return ctypes.windll.shell32.IsUserAnAdmin()
            except Exception:
                return False
        return True

    def relaunch_as_admin():
        script = sys.argv[0]
        python_exe = sys.executable
        if python_exe.lower().endswith("python.exe"):
            pythonw_exe = python_exe[:-10] + "pythonw.exe"
            if os.path.exists(pythonw_exe):
                python_exe = pythonw_exe
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", python_exe, f'"{script}"', None, 1
        )

__all__ = [
    "ToolManagerWindow", "main", "ToolManagerGUI",
    "TOOL_LABELS", "TOOL_VERSIONS", "ANALOG_TOOLS", "DIGITAL_TOOLS",
    "IS_WINDOWS", "is_admin", "relaunch_as_admin",
]
