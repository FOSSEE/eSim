import sys as _sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Tuple
from platform_utils import run_cmd_stream as _run_cmd_stream

class Backend(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def find_executable(self, tool_id: str, version: str) -> Optional[str]: ...

    @abstractmethod
    def get_tool_version(self, exe_path: str) -> Optional[str]: ...

    @abstractmethod
    def install_package(self, package: str, version: str, fallback_versions: Optional[list[str]] = None) -> bool: ...

    @abstractmethod
    def uninstall_package(self, package: str, version: str) -> bool: ...

    @abstractmethod
    def download_file(self, url: str, filename: str) -> Path: ...

    @abstractmethod
    def extract_zip(self, archive: Path, dest_dir: Path) -> bool: ...

    @abstractmethod
    def extract_7z(self, archive: Path, dest_dir: Path) -> bool: ...

    @abstractmethod
    def run_installer(self, exe_path: str, *args: str) -> bool: ...

    @property
    @abstractmethod
    def base_dir(self) -> Path: ...

    @property
    @abstractmethod
    def download_dir(self) -> Path: ...

    def find_executable_with_version(self, tool_id: str, version: str) -> Tuple[Optional[str], Optional[str]]:
        exe = self.find_executable(tool_id, version)
        return (exe, self.get_tool_version(exe)) if exe else (None, None)

    def run_cmd(self, cmd, timeout=30, cwd=None, env=None):
        import subprocess
        try:
            return subprocess.run(cmd, capture_output=True, text=True, shell=False,
                timeout=timeout, encoding="utf-8", errors="ignore", cwd=cwd, env=env)
        except: return None

    def run_stream(self, cmd, timeout=900, cwd=None, env=None):
        return _run_cmd_stream(cmd, timeout=timeout, cwd=cwd, env=env)

    @property
    def msys2_bash(self) -> Optional[Path]: return None

    @property
    def msys2_mingw_bin(self) -> Optional[Path]: return None
