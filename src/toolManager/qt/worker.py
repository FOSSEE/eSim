from PyQt6.QtCore import QThread, pyqtSignal
import subprocess
import sys

try:
    from toolManager.worker import BaseWorker, CommandWorker, InstallWorker, InstallerThread
except ImportError:
    from toolManager.gui_fixed import CommandWorker
    from toolManager.updater_gui import InstallerThread

    class BaseWorker(QThread):
        def cancel(self):
            pass

    try:
        from toolManager.worker import InstallWorker
    except ImportError:
        from pathlib import Path
        from toolManager.registry import TOOLS

        BASE_DIR = Path(__file__).resolve().parent.parent
        PYTHON = sys.executable

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
                    label = TOOLS[tool].label if tool in TOOLS else tool
                    self.progress.emit(f"Installing {label} {version}...")
                    try:
                        proc = subprocess.Popen(
                            [PYTHON, backend, "install", tool, version],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            text=True,
                            encoding="utf-8",
                            errors="ignore",
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

__all__ = ["BaseWorker", "CommandWorker", "InstallWorker", "InstallerThread"]
