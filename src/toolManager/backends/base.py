"""
backends/base.py — Abstract interface for platform-specific backends.

All platform implementations (Windows, Linux, macOS) inherit from
Backend and implement the abstract methods below.  Tool functions in
backends/tools/*.py receive a Backend instance and call its methods
for all platform-specific operations.

Usage:
    class WindowsBackend(Backend):
        def find_executable(self, tool_id, version):
            ...
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Tuple


class Backend(ABC):
    """Platform-specific operations for tool management.

    Subclasses must implement all abstract methods.  Concrete methods
    (run_cmd, print_status, etc.) use shared utilities from utils.py
    and can be overridden if needed.
    """

    # ── Identification ────────────────────────────────────────────────

    @property
    @abstractmethod
    def name(self) -> str:
        """Platform identifier: 'win32', 'linux', 'darwin'."""
        ...

    # ── Executable discovery ──────────────────────────────────────────

    @abstractmethod
    def find_executable(self, tool_id: str, version: str) -> Optional[str]:
        """Locate an installed tool binary.

        Returns the full path to the executable, or None if not found.
        The *version* hint may be used to pick a specific installation.
        """
        ...

    def find_executable_with_version(
        self, tool_id: str, version: str
    ) -> tuple[Optional[str], Optional[str]]:
        """Locate an installed tool binary and return (path, installed_version).

        Default implementation calls find_executable then get_tool_version.
        Override in platform backends when the version can be inferred
        from the search path itself (e.g. KiCad directory structure).
        """
        exe = self.find_executable(tool_id, version)
        if exe:
            return exe, self.get_tool_version(exe)
        return None, None

    @abstractmethod
    def get_tool_version(self, exe_path: str) -> Optional[str]:
        """Extract the installed version string from a tool binary."""
        ...

    # ── Package management ────────────────────────────────────────────

    @abstractmethod
    def install_package(
        self,
        package: str,
        version: str,
        fallback_versions: Optional[list[str]] = None,
    ) -> bool:
        """Install *package* at *version* via the platform's package manager.

        Returns True on success.  *fallback_versions* is an ordered list
        of alternative version strings to try if the primary fails.
        """
        ...

    @abstractmethod
    def uninstall_package(self, package: str, version: str) -> bool:
        ...

    # ── File operations ───────────────────────────────────────────────

    @abstractmethod
    def download_file(self, url: str, filename: str) -> Path:
        """Download *url* to *download_dir* / *filename* and return the path."""
        ...

    @abstractmethod
    def extract_zip(self, archive: Path, dest_dir: Path) -> bool:
        ...

    @abstractmethod
    def extract_7z(self, archive: Path, dest_dir: Path) -> bool:
        ...

    @abstractmethod
    def run_installer(self, exe_path: str, *args: str) -> bool:
        """Run an executable installer (.exe, .msi) and wait for completion."""
        ...

    # ── Paths ─────────────────────────────────────────────────────────

    @property
    @abstractmethod
    def base_dir(self) -> Path:
        """Root directory of the tool manager (toolManager/)."""
        ...

    @property
    @abstractmethod
    def download_dir(self) -> Path:
        """Directory for cached downloads (toolManager/Download/)."""
        ...

    # ── Windows-specific (return None on other platforms) ─────────────

    @property
    def msys2_bash(self) -> Optional[Path]:
        """Path to MSYS2 bash.exe, or None if unavailable."""
        return None

    @property
    def msys2_mingw_bin(self) -> Optional[Path]:
        """Path to MSYS2 mingw64/bin, or None if unavailable."""
        return None
