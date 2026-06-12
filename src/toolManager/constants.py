#!/usr/bin/env python3
"""
Shared constants and platform identification for eSim Tool Manager.
"""

import sys
import platform
from pathlib import Path

# Platform Identification
IS_WINDOWS = sys.platform == "win32"
IS_LINUX = sys.platform.startswith("linux")
IS_MACOS = sys.platform == "darwin"

def get_os_id() -> str:
    """Returns a standardized OS identifier string used in registry keys."""
    if IS_WINDOWS:
        return "win32"
    if IS_LINUX:
        return "linux"
    if IS_MACOS:
        return "darwin"
    return "unknown"

# Default Windows Installation Paths (Fallbacks)
# These are used when tools are not found in the system PATH.
DEFAULT_MSYS2_PATH = Path(r"C:\msys64")
DEFAULT_ESIM_DIR = Path(r"C:\FOSSEE\eSim")

# Tool Manager Defaults
DEFAULT_INFO_FILE = "information.json"
DEFAULT_DOWNLOAD_DIR = "Download"
