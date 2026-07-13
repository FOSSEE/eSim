#!/usr/bin/env python3
"""
Utility functions for eSim Tool Manager.

This module contains generic backend helper functions for subprocess execution,
command resolution, and status reporting. These utilities are extracted to 
promote portability and reuse across different Tool Manager components.

Part of the portability-path-resolution roadmap.
"""

import os
import sys
import subprocess
import shutil
import platform
import threading
import time
from pathlib import Path

from constants import DEFAULT_MSYS2_PATH, DEFAULT_ESIM_DIR
from platform_utils import subprocess_flags

WIN_KICAD_PATHS = [
    (r"C:\Program Files\KiCad\9.0\bin\kicad.exe", "9"),
    (r"C:\Program Files\KiCad\8.0\bin\kicad.exe", "8"),
    (r"C:\Program Files\KiCad\7.0\bin\kicad.exe", "7"),
    (r"C:\Program Files\KiCad\6.0\bin\kicad.exe", "6"),
    (r"C:\Program Files (x86)\KiCad\9.0\bin\kicad.exe", "9"),
    (r"C:\Program Files (x86)\KiCad\8.0\bin\kicad.exe", "8"),
    (r"C:\Program Files (x86)\KiCad\7.0\bin\kicad.exe", "7"),
    (r"C:\Program Files (x86)\KiCad\6.0\bin\kicad.exe", "6"),
]

WIN_NGSPICE_PATHS = [
    r"C:\Program Files\ngspice\bin\ngspice.exe",
    r"C:\Program Files (x86)\ngspice\bin\ngspice.exe",
    r"C:\ngspice\bin\ngspice.exe",
]

WIN_LLVM_PATHS = [
    r"C:\Program Files\LLVM\bin\clang.exe",
    r"C:\Program Files (x86)\LLVM\bin\clang.exe",
]

# Locations for MSYS2/MinGW64. The FOSSEE fallback supports the bundled
# MSYS2 environment provided by some eSim installers to ensure 
# zero-dependency operation.
FOSSEE_MSYS_CANDIDATES = [
    Path(r"C:\msys64\mingw64"),
    Path(r"C:\FOSSEE\MSYS\mingw64"),
]

# ==================== HELPERS ====================

def run_cmd_safe(cmd, timeout=30, cwd=None, env=None):
    """
    Executes a command safely without showing a window on Windows.
    Returns the subprocess.CompletedProcess result or None if failed.
    """
    try:
        flags = subprocess_flags()
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            shell=False,
            timeout=timeout,
            startupinfo=flags.get("startupinfo"),
            creationflags=flags.get("creationflags", 0),
            encoding='utf-8',
            errors='ignore',
            cwd=cwd,
            env=env
        )
        return result
    except Exception as e:
        print(f"Command failed: {e}")
        return None

def run_cmd_stream(cmd, timeout=900, cwd=None, env=None):
    """
    Executes a command and streams its output to stdout in real-time.
    Returns a tuple of (returncode, full_output_string).
    """
    try:
        flags = subprocess_flags()

        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=False,
            startupinfo=flags.get("startupinfo"),
            creationflags=flags.get("creationflags", 0),
            encoding='utf-8',
            errors='ignore',
            cwd=cwd,
            env=env
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
    """
    Generic wrapper for shutil.which to locate an executable.
    """
    return shutil.which(exe)

def print_status(state, installed, target):
    """
    Prints a formatted status string for Tool Manager communication.
    Format: state|installed_version|target_version
    """
    if installed:
        installed = str(installed).strip().replace('\n', '').replace('\r', '')
    print(f"{state}|{installed}|{target}", flush=True)

def get_msys2_bash():
    """
    Returns the path to MSYS2 bash.exe if found, else None.
    """
    bash_path = DEFAULT_MSYS2_PATH / "usr" / "bin" / "bash.exe"
    return bash_path if bash_path.exists() else None

def get_msys2_mingw_root():
    """
    Returns the path to MSYS2 mingw64 root if found, else None.
    """
    for candidate in FOSSEE_MSYS_CANDIDATES:
        if candidate.exists():
            return candidate
    return None

def get_msys2_mingw_bin():
    """
    Returns the path to MSYS2 mingw64/bin if found, else None.
    """
    for candidate in FOSSEE_MSYS_CANDIDATES:
        bin_dir = candidate / "bin"
        if bin_dir.exists():
            return bin_dir
    return None
