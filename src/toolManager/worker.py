from PyQt6.QtCore import QThread, pyqtSignal
import os, subprocess, threading
from pm_platform import IS_LINUX

class BaseWorker(QThread):
    def __init__(self, timeout=None, parent=None):
        super().__init__(parent)
        self._timeout = timeout; self._process = None; self._timeout_timer = None; self._cancelled = False

    def cancel(self):
        self._cancelled = True; self._kill_process()

    def _is_cancelled(self): return self._cancelled

    def _make_popen(self, args, **kwargs):
        defaults = {"stdout": subprocess.PIPE, "stderr": subprocess.STDOUT, "text": True,
                     "encoding": "utf-8", "errors": "ignore"}
        defaults.update(kwargs)
        self._cancel_timeout()
        self._process = subprocess.Popen(args, **defaults)
        if self._timeout is not None:
            self._timeout_timer = threading.Timer(self._timeout, self._kill_process)
            self._timeout_timer.daemon = True; self._timeout_timer.start()
        return self._process

    def _iter_stream(self, proc):
        try:
            for line in iter(proc.stdout.readline, ""):
                yield line.rstrip()
        except OSError: pass
        if proc.poll() is None: proc.wait()

    def _kill_process(self):
        self._cancel_timeout()
        proc = self._process
        if proc is not None and proc.poll() is None:
            try: proc.kill(); proc.wait()
            except: pass

    def _cancel_timeout(self):
        if self._timeout_timer is not None: self._timeout_timer.cancel(); self._timeout_timer = None

    def run(self):
        try: self._do_run()
        finally: self._cancel_timeout(); self._kill_process(); self._process = None

    def _do_run(self): raise NotImplementedError

class InstallWorker(BaseWorker):
    progress = pyqtSignal(str); finished = pyqtSignal(bool)

    def __init__(self, tools, backend_path, python_path="python3", timeout=None):
        super().__init__(timeout)
        self.tools = tools; self.backend_path = backend_path; self.python_path = python_path

    def _do_run(self):
        success = True
        for tool, version in self.tools:
            if self._is_cancelled(): break
            label = tool.replace("_", " ").title()
            self.progress.emit(f"Installing {label} {version}...")
            try:
                proc = self._make_popen([self.python_path, self.backend_path, "install", tool, version])
                for line in self._iter_stream(proc):
                    if line:
                        self.progress.emit(f"  {line}")
                        if "[ERROR]" in line or "install_failed|" in line: success = False
                if proc.returncode != 0: success = False
            except Exception as e:
                self.progress.emit(f"  [ERROR] {tool}: {e}"); success = False
        self.finished.emit(success)

class CommandWorker(BaseWorker):
    finished = pyqtSignal(str, str); progress = pyqtSignal(str, str)

    def __init__(self, tool, args, password=None, timeout=None):
        super().__init__(timeout)
        self.tool = tool; self.args = args; self.password = password

    def _do_run(self):
        output_lines = []
        try:
            proc = self._make_popen(self.args, stdin=subprocess.PIPE, text=True) if (self.password and IS_LINUX) else self._make_popen(self.args)
            if self.password and IS_LINUX:
                proc.stdin.write(self.password + "\n"); proc.stdin.flush(); proc.stdin.close()
            for line in self._iter_stream(proc):
                if line: output_lines.append(line); self.progress.emit(self.tool, line)
            output = "\n".join(output_lines)
        except subprocess.TimeoutExpired: output = "error|none|Operation timed out"
        except Exception as e: output = f"error|none|{str(e)}"
        self.finished.emit(self.tool, output)

class InstallerThread(BaseWorker):
    progress = pyqtSignal(str, int); log_output = pyqtSignal(str); finished = pyqtSignal(bool, str)
    _PROGRESS_KEYWORDS = [
        (["removing","purge","uninstall"], 10, "Removing old version..."),
        (["updating","update","apt update"], 20, "Updating package lists..."),
        (["installing dependencies","install -y"], 30, "Installing dependencies..."),
        (["downloading","extracting","tar -x"], 40, "Extracting files..."),
        (["configuring","./configure"], 50, "Configuring..."),
        (["compiling","building","make -j","make["], 70, "Compiling (this may take a while)..."),
        (["installing","make install"], 85, "Installing..."),
        (["verifying","success","installed successfully"], 95, "Verifying installation..."),
    ]

    def __init__(self, packages_to_install, scripts_dir=None, timeout=None):
        super().__init__(timeout)
        self.packages = packages_to_install; self.scripts_dir = scripts_dir

    def _do_run(self):
        total = len(self.packages)
        base_dir = self.scripts_dir or os.path.dirname(os.path.abspath(__file__))
        for pkg_idx, (name, version, script_name) in enumerate(self.packages):
            if self._is_cancelled(): self.finished.emit(False, "Cancelled by user"); return
            base_progress = int((pkg_idx / total) * 100)
            self.progress.emit(f"Starting {name} {version}...", base_progress)
            script_path = os.path.join(base_dir, script_name)
            if not os.path.exists(script_path):
                self.finished.emit(False, f"Script not found: {script_name}"); return
            proc = self._make_popen(["bash", script_path, version], bufsize=1, universal_newlines=True)
            step_progress = 0
            for line in self._iter_stream(proc):
                if not line: continue
                self.log_output.emit(line)
                for kw, pct, msg in self._PROGRESS_KEYWORDS:
                    if any(w in line.lower() for w in kw):
                        step_progress = pct
                        self.progress.emit(f"{name}: {msg}", min(base_progress + int((pct / 100) * (100 / total)), 99)); break
            if proc.returncode != 0:
                self.finished.emit(False, f"Failed: {name} (exit code {proc.returncode})"); return
        self.progress.emit("Installation complete!", 100)
        self.finished.emit(True, f"Successfully installed {total} package(s)")
