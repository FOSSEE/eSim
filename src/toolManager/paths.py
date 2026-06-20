#!/usr/bin/env python3
"""
Platform-aware path resolution for eSim Tool Manager.
Uses pathlib for cross-platform compatibility.
"""

import os
import sys
import platform
from pathlib import Path
from typing import Optional

try:
    from .platform_utils import (
        DEFAULT_MSYS2_PATH, DEFAULT_ESIM_DIR, 
        DEFAULT_INFO_FILE, DEFAULT_DOWNLOAD_DIR,
        IS_WINDOWS
    )
except (ImportError, ValueError):
    from platform_utils import (
        DEFAULT_MSYS2_PATH, DEFAULT_ESIM_DIR, 
        DEFAULT_INFO_FILE, DEFAULT_DOWNLOAD_DIR,
        IS_WINDOWS
    )


def get_toolmanager_root() -> Path:
    """Returns the absolute path to the toolManager directory."""
    return Path(__file__).resolve().parent


def get_application_root() -> Path:
    """Returns the absolute path to the eSim application root (parent of src)."""
    # Assuming the structure: esim_root/src/toolManager/paths.py
    # This traverses up from toolManager -> src -> esim_root
    return get_toolmanager_root().parent.parent


def get_download_cache_dir() -> Path:
    """Returns the directory used for caching downloads."""
    path = get_toolmanager_root() / DEFAULT_DOWNLOAD_DIR
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_install_state_path() -> Path:
    """Returns the path to the information.json state file."""
    return get_toolmanager_root() / DEFAULT_INFO_FILE


def get_temp_dir() -> Path:
    """Returns a platform-appropriate temporary directory for toolManager."""
    if IS_WINDOWS:
        temp = Path(os.environ.get("TEMP", "C:\\temp")) / "eSimToolManager"
    else:
        temp = Path("/tmp/eSimToolManager")
    
    temp.mkdir(parents=True, exist_ok=True)
    return temp


def resolve_user_data_dir() -> Path:
    """
    Returns the user data directory for eSim configuration.
    Follows OS standards (AppData on Windows, ~/.config on Linux).
    """
    if IS_WINDOWS:
        return Path(os.environ.get("APPDATA", "~")).expanduser() / "eSim"
    else:
        return Path("~/.config/eSim").expanduser()


def get_msys2_default_root() -> Path:
    """
    Returns the default MSYS2 installation path on Windows.
    Used as a fallback when MSYS2 is not in the system PATH.
    """
    return DEFAULT_MSYS2_PATH


def get_esim_default_install_dir() -> Path:
    """
    Returns the default eSim installation path on Windows.
    Used as a fallback when eSim environment variables are not set.
    """
    return DEFAULT_ESIM_DIR
