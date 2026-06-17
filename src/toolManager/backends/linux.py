"""
backends/linux.py — Linux backend implementation.

Currently a minimal skeleton.  Most tools on Linux are installed via
bash scripts (see SCRIPT_MAPPING in registry.py).  This backend will
be expanded as native package-manager support grows.
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Optional

from .base import Backend


class LinuxBackend(Backend):
    """Backend for Linux (apt/dnf/pacman + bash scripts)."""

    @property
    def name(self) -> str:
        return "linux"

    def __init__(self, base_dir: Optional[Path] = None):
        super().__init__()
        self._base_dir = base_dir or Path(__file__).resolve().parent.parent
        self._download_dir = self._base_dir / "Download"
        self._download_dir.mkdir(parents=True, exist_ok=True)

    # ── Executable discovery ──────────────────────────────────────────

    def find_executable(self, tool_id: str, version: str) -> Optional[str]:
        return shutil.which(tool_id)

    def get_tool_version(self, exe_path: str) -> Optional[str]:
        try:
            result = subprocess.run(
                [exe_path, "--version"],
                capture_output=True, text=True, timeout=10,
            )
            line = result.stdout.split("\n")[0].strip()
            return line.split()[-1] if line else None
        except Exception:
            return None

    # ── Package management ────────────────────────────────────────────

    def install_package(
        self,
        package: str,
        version: str,
        fallback_versions: Optional[list[str]] = None,
    ) -> bool:
        return False  # TODO: implement apt/dnf/pacman install

    def uninstall_package(self, package: str, version: str) -> bool:
        return False  # TODO

    # ── File operations ───────────────────────────────────────────────

    def download_file(self, url: str, filename: str) -> Path:
        import urllib.request
        dest = self._download_dir / filename
        urllib.request.urlretrieve(url, dest)
        return dest

    def extract_zip(self, archive: Path, dest_dir: Path) -> bool:
        import zipfile
        try:
            with zipfile.ZipFile(archive) as zf:
                zf.extractall(dest_dir)
            return True
        except Exception:
            return False

    def extract_7z(self, archive: Path, dest_dir: Path) -> bool:
        return False  # TODO: use system 7z or patool

    def run_installer(self, exe_path: str, *args: str) -> bool:
        return False  # TODO

    # ── Paths ─────────────────────────────────────────────────────────

    @property
    def base_dir(self) -> Path:
        return self._base_dir

    @property
    def download_dir(self) -> Path:
        return self._download_dir
