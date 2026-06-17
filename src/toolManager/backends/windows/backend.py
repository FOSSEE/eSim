"""
backends/windows/backend.py — WindowsBackend(Backend).

Wires together Chocolatey operations, executable search, and file
operations from sibling modules into a concrete Backend implementation.
"""

import io
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

from ..base import Backend
from . import choco as _choco
from . import file_ops as _file_ops
from . import search as _search


class WindowsBackend(Backend):
    """Backend for Windows (Chocolatey, MSYS2, direct downloads)."""

    @property
    def name(self) -> str:
        return "win32"

    def __init__(self, base_dir: Optional[Path] = None,
                 msys2_path: Optional[Path] = None):
        super().__init__()

        # Resolve base directory: toolManager/
        self._base_dir = base_dir or Path(__file__).resolve().parent.parent.parent
        self._download_dir = self._base_dir / "Download"
        self._download_dir.mkdir(parents=True, exist_ok=True)

        # MSYS2
        self._msys2_path = msys2_path or Path(r"C:\msys64")

        # Stdout encoding (Windows subprocess protocol)
        if sys.platform == "win32":
            sys.stdout = io.TextIOWrapper(
                sys.stdout.buffer, encoding='utf-8', errors='ignore')
            sys.stderr = io.TextIOWrapper(
                sys.stderr.buffer, encoding='utf-8', errors='ignore')

        # Import search path lists from registry
        from registry import (
            WIN_KICAD_PATHS, WIN_NGSPICE_PATHS, WIN_LLVM_PATHS,
        )
        self._win_kicad_paths = WIN_KICAD_PATHS
        self._win_ngspice_paths = WIN_NGSPICE_PATHS
        self._win_llvm_paths = WIN_LLVM_PATHS

    # ================================================================
    # Shared command execution (injectable into helper modules)
    # ================================================================

    def run_cmd(self, cmd, timeout=30, cwd=None, env=None):
        """Run *cmd* and return a CompletedProcess or None on failure."""
        try:
            if platform.system() == "Windows":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
                creationflags = subprocess.CREATE_NO_WINDOW
            else:
                startupinfo = None
                creationflags = 0

            result = subprocess.run(
                cmd, capture_output=True, text=True, shell=False,
                timeout=timeout,
                startupinfo=startupinfo, creationflags=creationflags,
                encoding='utf-8', errors='ignore',
                cwd=cwd, env=env,
            )
            return result
        except Exception:
            return None

    def which(self, exe):
        """Locate *exe* on PATH."""
        return shutil.which(exe)

    def print_status(self, state, installed, target):
        """Print pipe-delimited status for the subprocess protocol."""
        if installed:
            installed = str(installed).strip().replace('\n', '').replace('\r', '')
        print(f"{state}|{installed}|{target}", flush=True)

    # ================================================================
    # Executable discovery (Backend ABC)
    # ================================================================

    def _search_fn(self, tool_id: str, version: str):
        """Return a callable that searches for *tool_id*.

        Each callable returns ``(path, installed_version)``.
        """
        _S = {
            "chocolatey": lambda: _search.find_chocolatey(
                version, self.which, self.run_cmd),
            "kicad": lambda: _search.find_kicad(
                version, self.which, self.run_cmd, self._win_kicad_paths),
            "ngspice": lambda: _search.find_ngspice(
                version, self.which, self.run_cmd, self._win_ngspice_paths,
                lambda pkg: _choco.choco_list(pkg, self.run_cmd)),
            "llvm": lambda: _search.find_llvm(
                version, self.which, self.run_cmd, self._win_llvm_paths),
            "ghdl": lambda: _search.find_ghdl(
                version, self.which, self.run_cmd, self._base_dir,
                self.msys2_mingw_bin, self._msys2_env()),
            "verilator": lambda: _search.find_verilator(
                version, self.which, self.run_cmd,
                self.msys2_mingw_bin, self._msys2_env()),
            "pyqt": lambda: _search.find_pyqt(version, self.run_cmd),
        }
        return _S.get(tool_id)

    def find_executable(self, tool_id: str,
                        version: str) -> Optional[str]:
        fn = self._search_fn(tool_id, version)
        if fn is None:
            return None
        exe_path, _ = fn()
        return exe_path

    def find_executable_with_version(
        self, tool_id: str, version: str
    ) -> tuple:
        fn = self._search_fn(tool_id, version)
        if fn is None:
            return None, None
        return fn()

    def get_tool_version(self, exe_path: str) -> Optional[str]:
        """Extract version from a tool binary."""
        try:
            result = self.run_cmd([exe_path, "--version"])
            if result and result.returncode == 0:
                line = result.stdout.split("\n")[0].strip()
                parts = line.split()
                if parts:
                    return parts[-1]
        except Exception:
            pass
        return None

    # ================================================================
    # Package management (Backend ABC)
    # ================================================================

    def install_package(
        self,
        package: str,
        version: str,
        fallback_versions: Optional[list[str]] = None,
    ) -> bool:
        """Install via Chocolatey with optional version fallback chain."""
        from registry import NGSPICE_VERSIONS, LLVM_VERSIONS, KICAD_VERSIONS

        if version == "latest":
            return _choco.choco_install(package, version, self.run_cmd)

        versions_to_try = [version]
        if fallback_versions:
            versions_to_try.extend(fallback_versions)

        for v in versions_to_try:
            if _choco.choco_install(package, v, self.run_cmd):
                return True
        return False

    def uninstall_package(self, package: str, version: str) -> bool:
        """Uninstall via Chocolatey."""
        return _choco.choco_uninstall(package, version, self.run_cmd)

    # ================================================================
    # File operations (Backend ABC)
    # ================================================================

    def download_file(self, url: str, filename: str) -> Path:
        """Download to *download_dir* / *filename* with caching."""
        result = _file_ops.download_file(url, filename, self._download_dir)
        if result is None:
            raise RuntimeError(f"Download failed: {url}")
        return result

    def extract_zip(self, archive: Path, dest_dir: Path) -> bool:
        return _file_ops.extract_zip(archive, dest_dir)

    def extract_7z(self, archive: Path, dest_dir: Path) -> bool:
        return _file_ops.extract_7z(
            archive, dest_dir, run_cmd=self.run_cmd)

    def run_installer(self, exe_path: str, *args: str) -> bool:
        return _file_ops.run_installer(
            exe_path, list(args), self.run_cmd)

    # ================================================================
    # Paths (Backend ABC)
    # ================================================================

    @property
    def base_dir(self) -> Path:
        return self._base_dir

    @property
    def download_dir(self) -> Path:
        return self._download_dir

    # ================================================================
    # MSYS2 (Windows-specific)
    # ================================================================

    @property
    def msys2_bash(self) -> Optional[Path]:
        bash_path = self._msys2_path / "usr" / "bin" / "bash.exe"
        return bash_path if bash_path.exists() else None

    @property
    def msys2_mingw_bin(self) -> Optional[Path]:
        """Path to MSYS2 mingw64/bin, checking both standard and FOSSEE paths."""
        candidates = [
            self._msys2_path / "mingw64" / "bin",
            Path(r"C:\FOSSEE\MSYS\mingw64") / "bin",
        ]
        for c in candidates:
            if c.exists():
                return c
        return None

    @property
    def msys2_mingw_root(self) -> Optional[Path]:
        """Path to MSYS2 mingw64 root, checking both standard and FOSSEE paths."""
        candidates = [
            self._msys2_path / "mingw64",
            Path(r"C:\FOSSEE\MSYS\mingw64"),
        ]
        for c in candidates:
            if c.exists():
                return c
        return None

    def _msys2_env(self) -> dict:
        """Build env dict with MSYS2 paths on PATH."""
        env = os.environ.copy()
        paths = []

        msys_bin = self.msys2_mingw_bin
        if msys_bin:
            paths.append(str(msys_bin))

        msys_root = self.msys2_mingw_root
        if msys_root:
            usr_bin = msys_root.parent / "usr" / "bin"
            if usr_bin.exists():
                paths.append(str(usr_bin))

        if paths:
            env["PATH"] = os.pathsep.join(paths) + \
                          os.pathsep + env.get("PATH", "")
        return env

    def install_kicad_direct(self, target_version: str) -> bool:
        """Fallback: install KiCad via direct download (Windows, v6 only)."""
        from registry import TOOLS

        spec = TOOLS.get("kicad")
        if not spec:
            return False

        url = spec.get_download_url(target_version)
        if not url:
            self.print_status("not_supported", "none", target_version)
            return False

        print(f"[INFO] Attempting direct download from: {url}")
        exe_path = self.download_file(url, f"kicad-{target_version}.exe")
        if exe_path and self.run_installer(str(exe_path), "/SILENT"):
            return True
        return False
