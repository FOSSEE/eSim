"""
worker.py — Unified QThread workers with cancellation and timeout support.

All workers subclass BaseWorker which provides:
  - Thread-safe cancellation (manual flag — works before/after thread start)
  - Subprocess lifecycle management (auto-kill on thread exit)
  - Timeout via threading.Timer
  - Common subprocess helpers (_make_popen, _iter_stream)

Usage:
    worker = InstallWorker(tools, backend_path, python_path="python3")
    worker.progress.connect(on_progress)
    worker.finished.connect(on_finished)
    worker.start()
    ...
    worker.cancel()  # thread-safe cancellation, safe before start too

Thread safety:
  - Do NOT call UI methods from within run() — emit signals instead
  - Qt delivers cross-thread signals as queued connections automatically
  - Cancellation flag (bool) is atomic under CPython's GIL
  - Timeout timer uses threading.Timer (daemon thread, auto-cleanup)
"""

from PyQt6.QtCore import QThread, pyqtSignal

import os
import subprocess
import threading

from pm_platform import IS_LINUX


class BaseWorker(QThread):
    """Base class for tool manager workers.

    Provides thread-safe cancellation, subprocess lifecycle management,
    optional timeout, and helpers for running subprocesses with
    line-by-line output streaming.

    Subclasses override _do_run() (not run()) so that process cleanup
    is guaranteed even if the thread exits mid-operation.
    """

    def __init__(self, timeout=None, parent=None):
        super().__init__(parent)
        self._timeout = timeout
        self._process = None
        self._timeout_timer = None
        self._cancelled = False

    # ---- Cancellation API (thread-safe) ----

    def cancel(self):
        """Request cancellation. Kills the subprocess if running.

        Safe to call before the thread starts (e.g. from __init__),
        during execution, or after completion.
        """
        self._cancelled = True
        self._kill_process()

    def _is_cancelled(self):
        """Check if cancellation was requested. Thread-safe."""
        return self._cancelled

    # ---- Subprocess helpers ----

    def _make_popen(self, args, **kwargs):
        """Create a subprocess.Popen with common defaults.

        Stores the process handle in self._process so it can be killed
        on cancel, timeout, or thread exit.  Starts a timeout timer if
        self._timeout is set.

        Returns the Popen object.
        """
        defaults = dict(
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="ignore",
        )
        defaults.update(kwargs)
        self._cancel_timeout()
        self._process = subprocess.Popen(args, **defaults)
        if self._timeout is not None:
            self._timeout_timer = threading.Timer(
                self._timeout, self._kill_process
            )
            self._timeout_timer.daemon = True
            self._timeout_timer.start()
        return self._process

    def _iter_stream(self, proc):
        """Yield stripped lines from *proc*.stdout in real time.

        Uses the sentinel pattern (iter + readline) for immediate line
        delivery, which is important for progress-parsing workers such
        as InstallerThread.

        Handles broken-pipe errors gracefully when the process is
        killed externally (cancel / timeout).
        """
        try:
            for line in iter(proc.stdout.readline, ""):
                yield line.rstrip()
        except OSError:
            pass
        if proc.poll() is None:
            proc.wait()

    def _kill_process(self):
        """Kill the running subprocess if it is still alive."""
        self._cancel_timeout()
        proc = self._process
        if proc is not None and proc.poll() is None:
            try:
                proc.kill()
                proc.wait()
            except OSError:
                pass

    def _cancel_timeout(self):
        """Cancel the pending timeout timer if one is active."""
        if self._timeout_timer is not None:
            self._timeout_timer.cancel()
            self._timeout_timer = None

    # ---- Thread lifecycle ----

    def run(self):
        """Entry point for the thread.  Guarantees subprocess cleanup
        and timeout cancellation regardless of how _do_run exits."""
        try:
            self._do_run()
        finally:
            self._cancel_timeout()
            self._kill_process()
            self._process = None

    def _do_run(self):
        """Override in subclasses to perform work.

        Called inside run() — subprocess cleanup is automatic.
        Emit signals here; never call UI methods directly.
        """
        raise NotImplementedError


# ====================================================================
# InstallWorker — matches main.py::InstallWorker
# Signals:  progress(str), finished(bool)
# ====================================================================

class InstallWorker(BaseWorker):
    """Worker that installs a list of (tool, version) pairs sequentially
    by spawning tool_manager_windows.py as a subprocess for each tool.

    Signals
    -------
    progress : str
        Status message during installation.
    finished : bool
        True only if every tool in the list installed without error.
    """

    progress = pyqtSignal(str)
    finished = pyqtSignal(bool)

    def __init__(self, tools, backend_path, python_path="python3",
                 timeout=None):
        super().__init__(timeout)
        self.tools = tools
        self.backend_path = backend_path
        self.python_path = python_path

    def _do_run(self):
        success = True
        for tool, version in self.tools:
            if self._is_cancelled():
                break

            label = tool.replace("_", " ").title()
            self.progress.emit(f"Installing {label} {version}...")

            try:
                proc = self._make_popen(
                    [self.python_path, self.backend_path,
                     "install", tool, version],
                )
                for line in self._iter_stream(proc):
                    if line:
                        self.progress.emit(f"  {line}")
                        if "[ERROR]" in line or "install_failed|" in line:
                            success = False
                if proc.returncode != 0:
                    success = False
            except Exception as e:
                self.progress.emit(f"  [ERROR] {tool}: {e}")
                success = False

        self.finished.emit(success)


# ====================================================================
# CommandWorker — matches gui_fixed.py::CommandWorker
# Signals:  finished(str, str), progress(str, str)
# ====================================================================

class CommandWorker(BaseWorker):
    """Worker that runs an arbitrary subprocess command.

    On Linux, supports piping a sudo password via stdin.

    Signals
    -------
    progress : str, str
        Emitted for each output line with (tool_name, line).
    finished : str, str
        Emitted on completion with (tool_name, full_output).
    """

    finished = pyqtSignal(str, str)
    progress = pyqtSignal(str, str)

    def __init__(self, tool, args, password=None, timeout=None):
        super().__init__(timeout)
        self.tool = tool
        self.args = args
        self.password = password

    def _do_run(self):
        output_lines = []
        try:
            if self.password and IS_LINUX:
                proc = self._make_popen(
                    self.args,
                    stdin=subprocess.PIPE,
                    text=True,
                )
                proc.stdin.write(self.password + "\n")
                proc.stdin.flush()
                proc.stdin.close()
                for line in self._iter_stream(proc):
                    if line:
                        output_lines.append(line)
                        self.progress.emit(self.tool, line)
            else:
                proc = self._make_popen(self.args)
                for line in self._iter_stream(proc):
                    if line:
                        output_lines.append(line)
                        self.progress.emit(self.tool, line)

            output = "\n".join(output_lines)

        except subprocess.TimeoutExpired:
            output = "error|none|Operation timed out"
        except Exception as e:
            output = f"error|none|{str(e)}"

        self.finished.emit(self.tool, output)


# ====================================================================
# InstallerThread — matches updater_gui.py::InstallerThread
# Signals:  progress(str, int), log_output(str), finished(bool, str)
# ====================================================================

class InstallerThread(BaseWorker):
    """Worker that runs bash installation scripts for a list of packages.

    Parses script stdout keyword-by-keyword to estimate progress
    percentage, providing meaningful status feedback without needing
    structured progress reporting from the shell scripts themselves.

    Signals
    -------
    progress : str, int
        Status message with estimated completion percentage (0-100).
    log_output : str
        Every raw line emitted by the script (for terminal-style log).
    finished : bool, str
        (success, summary_message) emitted once all packages are done.
    """

    progress = pyqtSignal(str, int)
    log_output = pyqtSignal(str)
    finished = pyqtSignal(bool, str)

    # Keyword → estimated-progress-step mappings (within one package).
    # Order matters — later keywords overwrite earlier ones so progress
    # only moves forward.
    _PROGRESS_KEYWORDS = [
        (["removing", "purge", "uninstall"],                        10,
         "Removing old version..."),
        (["updating", "update", "apt update"],                      20,
         "Updating package lists..."),
        (["installing dependencies", "install -y"],                 30,
         "Installing dependencies..."),
        (["downloading", "extracting", "tar -x"],                   40,
         "Extracting files..."),
        (["configuring", "./configure"],                            50,
         "Configuring..."),
        (["compiling", "building", "make -j", "make["],            70,
         "Compiling (this may take a while)..."),
        (["installing", "make install"],                            85,
         "Installing..."),
        (["verifying", "success", "installed successfully"],        95,
         "Verifying installation..."),
    ]

    def __init__(self, packages_to_install, scripts_dir=None,
                 timeout=None):
        super().__init__(timeout)
        self.packages = packages_to_install
        self.scripts_dir = scripts_dir

    def _do_run(self):
        total = len(self.packages)
        base_dir = self.scripts_dir or os.path.dirname(
            os.path.abspath(__file__)
        )

        for pkg_idx, (package_name, version, script_name) in enumerate(
            self.packages
        ):
            if self._is_cancelled():
                self.finished.emit(False, "Cancelled by user")
                return

            try:
                base_progress = int((pkg_idx / total) * 100)
                self.progress.emit(
                    f"Starting {package_name} {version}...", base_progress
                )

                script_path = os.path.join(base_dir, script_name)
                if not os.path.exists(script_path):
                    self.finished.emit(
                        False, f"Script not found: {script_name}"
                    )
                    return

                proc = self._make_popen(
                    ["bash", script_path, version],
                    bufsize=1,
                    universal_newlines=True,
                )

                step_progress = 0
                for line in self._iter_stream(proc):
                    if not line:
                        continue
                    self.log_output.emit(line)

                    line_lower = line.lower()
                    msg = None
                    for keywords, progress_pct, progress_msg in \
                            self._PROGRESS_KEYWORDS:
                        if any(word in line_lower for word in keywords):
                            step_progress = progress_pct
                            msg = (
                                f"{package_name}: {progress_msg}"
                            )

                    if msg:
                        total_progress = base_progress + int(
                            (step_progress / 100) * (100 / total)
                        )
                        self.progress.emit(msg, min(total_progress, 99))

                return_code = proc.returncode
                if return_code != 0:
                    self.finished.emit(
                        False,
                        f"Failed: {package_name} "
                        f"(exit code {return_code})",
                    )
                    return

            except Exception as e:
                self.finished.emit(False, f"Error: {str(e)}")
                return

        self.progress.emit("Installation complete!", 100)
        self.finished.emit(
            True, f"Successfully installed {total} package(s)"
        )
