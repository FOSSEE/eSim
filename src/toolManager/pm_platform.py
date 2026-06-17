"""
platform.py — Unified OS detection, subprocess helpers, and admin functions.

Central module for all platform-specific logic in the eSim Tool Manager.
Absorbs constants.py, platform_utils.py, is_admin/relaunch_as_admin, and
subprocess helpers from utils.py.

Usage:
    from platform import IS_WINDOWS, IS_LINUX, IS_MAC
    from platform import is_admin, run_cmd_safe, print_status
"""

import os
import sys
import platform as _platform
import subprocess
import shutil
import threading
import time
import warnings
from pathlib import Path
from typing import Optional


# ── OS Flags ──────────────────────────────────────────────────────────────

IS_WINDOWS: bool = sys.platform == "win32"
IS_LINUX:   bool = sys.platform.startswith("linux")
IS_MAC:     bool = sys.platform == "darwin"
IS_MACOS:   bool = IS_MAC  # backward-compat alias


# ── OS Identification ─────────────────────────────────────────────────────

def get_os_id() -> str:
    """Returns a standardized OS identifier ('win32', 'linux', 'darwin')."""
    if IS_WINDOWS:
        return "win32"
    if IS_LINUX:
        return "linux"
    if IS_MAC:
        return "darwin"
    return "unknown"


# ── Default Paths ─────────────────────────────────────────────────────────

DEFAULT_MSYS2_PATH = Path(r"C:\msys64")
MSYS2_PATH = DEFAULT_MSYS2_PATH  # canonical name
DEFAULT_ESIM_DIR = Path(r"C:\FOSSEE\eSim")
DEFAULT_INFO_FILE = "information.json"
DEFAULT_DOWNLOAD_DIR = "Download"


# ── MSYS2 Path Helpers ────────────────────────────────────────────────────

def get_msys2_path() -> Path:
    """Returns the default MSYS2 installation path on Windows."""
    if not IS_WINDOWS:
        raise RuntimeError("get_msys2_path() is only valid for Windows")
    return Path(os.environ.get("MSYS2_PATH", str(DEFAULT_MSYS2_PATH)))


def get_mysys2_path() -> Path:
    """Deprecated: use get_msys2_path() instead."""
    warnings.warn("get_mysys2_path is deprecated, use get_msys2_path", DeprecationWarning, stacklevel=2)
    return get_msys2_path()


# ── Subprocess Flags ──────────────────────────────────────────────────────

if IS_WINDOWS:
    def subprocess_flags() -> dict:
        """Return Popen kwargs that hide the console window on Windows."""
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = subprocess.SW_HIDE
        return {"creationflags": subprocess.CREATE_NO_WINDOW, "startupinfo": si}
else:
    def subprocess_flags() -> dict:
        """No-op on Linux/macOS — returns empty dict."""
        return {}


# ── Package Manager Detection (Linux + macOS) ─────────────────────────────

_LINUX_PM_CANDIDATES: list[tuple[str, str]] = [
    ("apt-get", "apt"),
    ("dnf", "dnf"),
    ("yum", "yum"),
    ("pacman", "pacman"),
    ("zypper", "zypper"),
    ("apk", "apk"),
]

_MAC_PM_CANDIDATES: list[tuple[str, str]] = [
    ("brew", "brew"),
    ("port", "port"),
    ("nix", "nix"),
]


def detect_package_manager() -> Optional[str]:
    """Detect the active system package manager by checking PATH."""
    if IS_WINDOWS:
        return None
    if IS_LINUX:
        for cmd, name in _LINUX_PM_CANDIDATES:
            if shutil.which(cmd):
                return name
    if IS_MAC:
        for cmd, name in _MAC_PM_CANDIDATES:
            if shutil.which(cmd):
                return name
    return None


# ── Distro Label ──────────────────────────────────────────────────────────

def distro_label() -> str:
    """Return a human-readable distro name (e.g. 'Ubuntu 24.04')."""
    if IS_WINDOWS:
        return f"Windows {_platform.release()}"
    if IS_MAC:
        return f"macOS {_platform.mac_ver()[0]}"
    try:
        info = _platform.freedesktop_os_release()
    except AttributeError:
        try:
            info = {}
            with open("/etc/os-release") as f:
                for line in f:
                    line = line.strip()
                    if "=" in line:
                        k, _, v = line.partition("=")
                        info[k] = v.strip('"')
        except (OSError, ValueError):
            return "Linux"
    except OSError:
        return "Linux"
    name = info.get("NAME", "Linux")
    version = info.get("VERSION_ID", "")
    return f"{name} {version}".strip()


# ── Admin / Elevation ─────────────────────────────────────────────────────

def is_admin() -> bool:
    """Check if the current process has administrator/root privileges."""
    if not IS_WINDOWS:
        return True
    try:
        import ctypes
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def relaunch_as_admin() -> None:
    """Relaunch the current script with administrator privileges (Windows only)."""
    if not IS_WINDOWS:
        return
    import ctypes
    python_exe = sys.executable
    if python_exe.lower().endswith("python.exe"):
        pythonw_exe = python_exe[:-10] + "pythonw.exe"
        if os.path.exists(pythonw_exe):
            python_exe = pythonw_exe
    script = str(Path(sys.argv[0]).resolve())
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", python_exe, f'"{script}"', None, 1
    )


# ── Subprocess Helpers ────────────────────────────────────────────────────

def run_cmd_safe(cmd, timeout=30, cwd=None, env=None):
    """
    Execute a command safely without showing a window on Windows.
    Returns subprocess.CompletedProcess or None on failure.
    """
    try:
        kwargs = {}
        if IS_WINDOWS:
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            si.wShowWindow = subprocess.SW_HIDE
            kwargs["startupinfo"] = si
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
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
            **kwargs
        )
        return result
    except Exception as e:
        print(f"Command failed: {e}", flush=True)
        return None


def run_cmd_stream(cmd, timeout=900, cwd=None, env=None):
    """
    Execute a command and stream its output to stdout in real-time.
    Returns (returncode, full_output_string).
    """
    try:
        popen_kwargs = {}
        if IS_WINDOWS:
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            si.wShowWindow = subprocess.SW_HIDE
            popen_kwargs["startupinfo"] = si
            popen_kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW

        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=False,
            encoding="utf-8",
            errors="ignore",
            cwd=cwd,
            env=env,
            **popen_kwargs
        )

        output_lines = []

        def _kill():
            try:
                proc.kill()
            except Exception:
                pass

        timer = threading.Timer(timeout, _kill)
        try:
            timer.start()
            for line in proc.stdout:
                line = line.rstrip()
                if line:
                    print(line, flush=True)
                    output_lines.append(line)
            proc.wait()
        finally:
            timer.cancel()

        return proc.returncode, "\n".join(output_lines)
    except Exception as e:
        print(f"[ERROR] Command failed: {e}", flush=True)
        return -1, str(e)


def which(exe):
    """Wrapper for shutil.which."""
    return shutil.which(exe)


def print_status(state: str, installed: str, target: str) -> None:
    """
    Print a formatted status string for Tool Manager pipe protocol.
    Format: state|installed_version|target_version
    """
    if installed:
        installed = str(installed).strip().replace("\n", "").replace("\r", "")
    print(f"{state}|{installed}|{target}", flush=True)
