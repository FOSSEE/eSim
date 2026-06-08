#!/usr/bin/env python3
"""
platform_utils.py
─────────────────
Central OS and distro detection module for eSim Tool Manager.

All platform-specific branching in the Tool Manager should import
constants and helpers from this module. Do NOT scatter sys.platform
checks across other files.

Exports
-------
IS_WINDOWS              bool
IS_LINUX                bool
IS_MAC                  bool
MSYS2_PATH              Path   (Windows: default C:\\msys64)
subprocess_flags()      dict   (suppress console window on Windows)
detect_package_manager() str | None
distro_label()          str

Note: privilege elevation (pkexec) is handled in tool_manager_linux.py,
not here. This module is detection-only.
"""

import sys
import platform
import shutil
from pathlib import Path

__version__ = "1.0.0"
__author__  = "Eashan Hasija"

__all__ = [
    "IS_WINDOWS", "IS_LINUX", "IS_MAC",
    "MSYS2_PATH",
    "subprocess_flags",
    "detect_package_manager",
    "distro_label",
]

# ── OS Flags ──────────────────────────────────────────────────────────────────
IS_WINDOWS: bool = sys.platform == "win32"
IS_LINUX:   bool = sys.platform.startswith("linux")
IS_MAC:     bool = sys.platform == "darwin"

# ── Windows: MSYS2 default install path ───────────────────────────────────────
# Previously hardcoded in tool_manager_windows.py L25 as:
#     MSYS2_PATH = Path(r"C:\msys64")
# Centralised here as the single place to change if the path changes.
import os
MSYS2_PATH: Path =  Path(os.environ.get("MSYS2_PATH", r"C:\msys64"))

# ── Subprocess flags ───────────────────────────────────────────────────────────
if IS_WINDOWS:
    import subprocess as _sp

    def subprocess_flags() -> dict:
        """Return Popen kwargs that hide the console window on Windows."""
        si = _sp.STARTUPINFO()
        si.dwFlags  |= _sp.STARTF_USESHOWWINDOW
        si.wShowWindow = _sp.SW_HIDE
        return {"creationflags": _sp.CREATE_NO_WINDOW, "startupinfo": si}
else:
    def subprocess_flags() -> dict:
        """No-op on Linux/macOS — returns empty dict."""
        return {}


# ── Package manager detection (Linux + macOS) ────────────────────────────────
# Linux candidates — checked in priority order
_LINUX_PM_CANDIDATES: list[tuple[str, str]] = [
    ("apt-get", "apt"),      # Ubuntu, Debian, Mint, Pop!_OS
    ("dnf",     "dnf"),      # Fedora, RHEL 8+, AlmaLinux, Rocky
    ("yum",     "yum"),      # CentOS 7, RHEL 7
    ("pacman",  "pacman"),   # Arch, Manjaro, EndeavourOS
    ("zypper",  "zypper"),   # openSUSE, SLES
    ("apk",     "apk"),      # Alpine
]

# macOS candidates — Homebrew is checked before MacPorts
# Homebrew installs to user space (no sudo needed)
# MacPorts installs system-wide (sudo needed)
_MAC_PM_CANDIDATES: list[tuple[str, str]] = [
    ("brew",    "brew"),     # Homebrew 
    ("port",    "port"),     # MacPorts
    ("nix",     "nix"),      # Nix
]


def detect_package_manager() -> str | None:
    """
    Detect the active system package manager by checking PATH.

    Supported platforms
    -------------------
    Linux   : 'apt', 'dnf', 'yum', 'pacman', 'zypper', 'apk'
    macOS   : 'brew' (Homebrew), 'port' (MacPorts), 'nix'
    Windows : always returns None (uses Chocolatey directly)

    Returns None if no supported package manager is found.

    Example
    -------
    >>> pm = detect_package_manager()
    >>> print(pm)   # 'apt' on Ubuntu, 'brew' on macOS, 'pacman' on Arch
    """
    if IS_WINDOWS:
        return None          # Windows uses Chocolatey directly in tool_manager_windows.py
    if IS_LINUX:
        for cmd, name in _LINUX_PM_CANDIDATES:
            if shutil.which(cmd):
                return name
    if IS_MAC:
        for cmd, name in _MAC_PM_CANDIDATES:
            if shutil.which(cmd):
                return name
    return None

# ── Linux: Human-readable distro string for GUI ───────────────────────────────
def distro_label() -> str:
    """
    Return a human-readable distro name read from /etc/os-release.

    Examples
    --------
    'Ubuntu 24.04', 'Fedora 40', 'Arch Linux', 'openSUSE Leap 15.5'
    Returns 'Linux' as fallback if the file cannot be parsed.
    Returns 'Windows' when called on Windows.
    """
    if IS_WINDOWS:
        return f"Windows {platform.release()}"   
    if IS_MAC:
        return f"macOS {platform.mac_ver()[0]}"
    try:
        info = platform.freedesktop_os_release()
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
    name    = info.get("NAME", "Linux")
    version = info.get("VERSION_ID", "")
    return f"{name} {version}".strip()