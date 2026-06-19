"""backends/linux — LinuxBackend implementation.

Concrete ``Backend`` subclass for Linux.  Delegates package management
to :mod:`pm`, executable discovery to :mod:`search`, and file operations
to :mod:`file_ops`.
"""

import os
import shutil
import subprocess
import threading
from pathlib import Path
from typing import Optional

from ..base import Backend
from . import file_ops as _file_ops
from . import pm as _pm
from . import search as _search


# Serialise bash-script execution so concurrent install/update operations
# don't contend for package-manager locks (dpkg, pacman-db, etc.).
_BASH_LOCK = threading.Lock()


class LinuxBackend(Backend):
    """Backend for Linux distributions (apt, dnf, pacman, zypper, etc.)."""

    # ── Identification ──────────────────────────────────────────────────

    @property
    def name(self) -> str:
        return "linux"

    # ── Initialisation ──────────────────────────────────────────────────

    def __init__(self, base_dir: Optional[Path] = None):
        super().__init__()
        self._base_dir = base_dir or Path(__file__).resolve().parent.parent.parent
        self._download_dir = self._base_dir / "Download"
        self._download_dir.mkdir(parents=True, exist_ok=True)

        # Detect system package manager at init time
        from pm_platform import detect_package_manager
        self._pm_name: Optional[str] = detect_package_manager()

    # ── Subprocess helper (shared with pm.py / search.py) ──────────────

    def run_cmd(self, cmd, timeout=30, cwd=None, env=None):
        """Run *cmd* and return a CompletedProcess or None on failure."""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                shell=False,
                timeout=timeout,
                encoding="utf-8",
                errors="ignore",
                cwd=cwd,
                env=env,
            )
            return result
        except Exception:
            return None

    def which(self, exe: str) -> Optional[str]:
        """Locate *exe* on PATH."""
        return shutil.which(exe)

    def print_status(self, state, installed, target):
        """Print pipe-delimited status for the subprocess protocol."""
        if installed:
            installed = str(installed).strip().replace("\n", "").replace("\r", "")
        print(f"{state}|{installed}|{target}", flush=True)

    # ── Executable discovery (Backend ABC) ──────────────────────────────

    def _search_fn(self, tool_id: str, version: str):
        """Return a callable that searches for *tool_id* on Linux.

        Each callable returns ``(path, installed_version)``.
        """
        _S = {
            "kicad":     lambda: _search.find_kicad(version, self.run_cmd, self.which),
            "ngspice":   lambda: _search.find_ngspice(version, self.run_cmd, self.which),
            "ghdl":      lambda: _search.find_ghdl(version, self.run_cmd, self.which),
            "verilator": lambda: _search.find_verilator(version, self.run_cmd, self.which),
            "llvm":      lambda: _search.find_llvm(version, self.run_cmd, self.which),
            "esim":      lambda: _search.find_tool("esim", version, self.run_cmd, self.which),
            "chocolatey": lambda: (None, None),  # N/A on Linux
            "pyqt":      lambda: self._find_pyqt(version),
        }
        return _S.get(tool_id)

    def _find_pyqt(self, version: str) -> tuple[Optional[str], Optional[str]]:
        """Check for PyQt6 availability on Linux."""
        result = self.run_cmd(
            [sys.executable, "-c",
             "import PyQt6.QtCore; print(PyQt6.QtCore.PYQT_VERSION_STR)"],
            timeout=10,
        )
        if result and result.returncode == 0:
            ver = (result.stdout or "").strip()
            return ("PyQt6", ver) if ver else (None, None)
        return None, None

    def find_executable(self, tool_id: str, version: str) -> Optional[str]:
        fn = self._search_fn(tool_id, version)
        if fn is None:
            return None
        exe_path, _ = fn()
        return exe_path

    def find_executable_with_version(
        self, tool_id: str, version: str
    ) -> tuple[Optional[str], Optional[str]]:
        fn = self._search_fn(tool_id, version)
        if fn is None:
            return None, None
        return fn()

    def get_tool_version(self, exe_path: str) -> Optional[str]:
        """Extract version from a tool binary."""
        try:
            result = self.run_cmd([exe_path, "--version"])
            if result and result.returncode == 0:
                line = (result.stdout or "").split("\n")[0].strip()
                parts = line.split()
                if parts:
                    return parts[-1]
        except Exception:
            pass
        return None

    # ── Package management (Backend ABC) ────────────────────────────────

    def install_package(
        self,
        package: str,
        version: str,
        fallback_versions: Optional[list[str]] = None,
    ) -> bool:
        """Install *package* via the detected system package manager.

        Falls back to *fallback_versions* if the primary version fails.
        """
        if not self._pm_name:
            self.print_status("not_supported", "none", version)
            return False

        versions_to_try = [version]
        if fallback_versions:
            versions_to_try.extend(fallback_versions)

        for v in versions_to_try:
            if v == "latest":
                if _pm.pm_install(self._pm_name, package, self.run_cmd):
                    return True
            else:
                # Try installing the exact version
                pkg_spec = f"{package}={v}" if self._pm_name == "apt" else package
                if self._pm_name == "pacman":
                    pkg_spec = package  # pacman handles versions differently
                if _pm.pm_install(self._pm_name, pkg_spec, self.run_cmd):
                    return True
        return False

    def uninstall_package(self, package: str, version: str) -> bool:
        """Uninstall *package* via the detected system package manager."""
        if not self._pm_name:
            self.print_status("not_supported", "none", version)
            return False
        return _pm.pm_uninstall(self._pm_name, package, self.run_cmd)

    # ── File operations (Backend ABC) ──────────────────────────────────

    def download_file(self, url: str, filename: str) -> Path:
        result = _file_ops.download_file(url, filename, self._download_dir)
        if result is None:
            raise RuntimeError(f"Download failed: {url}")
        return result

    def extract_zip(self, archive: Path, dest_dir: Path) -> bool:
        return _file_ops.extract_zip(archive, dest_dir)

    def extract_7z(self, archive: Path, dest_dir: Path) -> bool:
        return _file_ops.extract_7z(archive, dest_dir, run_cmd=self.run_cmd)

    def run_installer(self, exe_path: str, *args: str) -> bool:
        return _file_ops.run_installer(
            exe_path, list(args), run_cmd=self.run_cmd
        )

    # ── Linux-specific helpers ──────────────────────────────────────────

    def sudo_is_cached(self) -> bool:
        """Check whether a sudo credential is still alive (``sudo -n``).

        Returns ``True`` if the user can run a passwordless sudo command
        (i.e. the credential was cached by a recent ``sudo -S -v`` call).
        """
        result = self.run_cmd(["sudo", "-n", "true"])
        return result is not None and result.returncode == 0

    def ensure_sudo(self, password: str) -> bool:
        """Cache a sudo credential via ``sudo -S -v``.

        The password is piped to ``sudo -S -v`` once; if successful the
        cached credential lasts roughly 15 minutes.  The password string
        is discarded immediately after the call.
        Returns ``True`` if the credential was cached.
        """
        try:
            proc = subprocess.Popen(
                ["sudo", "-S", "-v"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            proc.communicate(input=password + "\n", timeout=10)
            return proc.returncode == 0
        except Exception:
            return False

    def clean_package_locks(self) -> None:
        """Remove stale package-manager lock files.

        On failure the lock is held by a *live* process we skip it.
        Only locks that refer to a non-existent process are removed.
        """
        lock_paths = {
            "apt": [
                "/var/lib/dpkg/lock-frontend",
                "/var/lib/dpkg/lock",
                "/var/cache/apt/archives/lock",
            ],
            "pacman": ["/var/lib/pacman/db.lck"],
            "dnf":    ["/var/run/yum.pid"],
            "zypper": ["/var/run/zypp.pid"],
            "pkg":    [],
            "xbps":   [],
        }.get(self._pm_name, [])

        for lock in lock_paths:
            # Only remove if the lock-file process is gone
            self.run_cmd(
                f"sudo lsof {lock} 2>/dev/null || sudo rm -f {lock}".split(),
                timeout=10,
            )

    def run_bash_script(
        self,
        script_path: str,
        *args: str,
        cwd: Optional[Path] = None,
    ) -> bool:
        """Run a bash script (from SCRIPT_MAPPING) with real-time output.

        The script is resolved relative to ``self._base_dir`` if it is
        a relative path.  Output is streamed to stdout so the GUI's
        CommandWorker can display it in the debug box in real time.
        Returns True on success.
        """
        with _BASH_LOCK:
            self.clean_package_locks()
            script = Path(script_path)
            if not script.is_absolute():
                script = self._base_dir / script_path
            if not script.exists():
                self.print_status("missing_script", "none", script_path)
                return False

            cmd = ["bash", str(script)] + list(args)
            rc, _ = self.run_stream(cmd, timeout=900, cwd=cwd or self._base_dir)
            ok = rc == 0
            if not ok:
                self.print_status("script_failed", str(rc), script_path)
            return ok

    # ── Paths (Backend ABC) ─────────────────────────────────────────────

    @property
    def base_dir(self) -> Path:
        return self._base_dir

    @property
    def download_dir(self) -> Path:
        return self._download_dir

    # ── MSYS2 (N/A on Linux) ────────────────────────────────────────────

    @property
    def msys2_bash(self) -> Optional[Path]:
        return None

    @property
    def msys2_mingw_bin(self) -> Optional[Path]:
        return None


import sys  # noqa: E402 (used by _find_pyqt)
