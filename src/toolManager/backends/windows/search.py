"""
Windows executable search helpers.

Each ``find_<tool>(version, run_cmd, which, ...)`` returns ``(path, version)``
or ``(None, None)``.  The ``run_cmd`` and ``which`` callbacks are injected so
tests can provide mocks.
"""

import os
import re
from pathlib import Path
from typing import Callable, Optional


# ====================================================================
# KiCad
# ====================================================================

def find_kicad(version: Optional[str] = None,
               which: Callable = None,
               run_cmd: Callable = None,
               win_kicad_paths: list = None) -> tuple:
    """Search standard paths, Windows registry, and PATH for KiCad."""
    if win_kicad_paths is None:
        win_kicad_paths = []

    for path, major in win_kicad_paths:
        if os.path.exists(path):
            install_dir = os.path.dirname(os.path.dirname(path))
            full_ver = major + ".x"
            for fname in ["version.txt", "VERSION"]:
                vfile = os.path.join(install_dir, fname)
                if os.path.exists(vfile):
                    try:
                        with open(vfile) as f:
                            m = re.search(r'(\d+\.\d+\.\d+)', f.read())
                            if m:
                                full_ver = m.group(1)
                    except Exception:
                        pass
            if version is None or str(version) in ("latest", major):
                return path, full_ver

    try:
        import winreg
        for hive in [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]:
            for arch in [winreg.KEY_READ | winreg.KEY_WOW64_64KEY,
                         winreg.KEY_READ | winreg.KEY_WOW64_32KEY]:
                try:
                    reg = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
                    with winreg.OpenKey(hive, reg, 0, arch) as key:
                        for i in range(winreg.QueryInfoKey(key)[0]):
                            try:
                                sub = winreg.EnumKey(key, i)
                                with winreg.OpenKey(key, sub) as sk:
                                    name = winreg.QueryValueEx(
                                        sk, "DisplayName")[0]
                                    if "KiCad" in name:
                                        dv = winreg.QueryValueEx(
                                            sk, "DisplayVersion")[0]
                                        loc = winreg.QueryValueEx(
                                            sk, "InstallLocation")[0]
                                        exe = os.path.join(
                                            loc, "bin", "kicad.exe")
                                        major = dv.split(".")[0] \
                                            if dv else "unknown"
                                        if version is None or \
                                           str(version) in ("latest", major):
                                            return (exe if os.path.exists(exe)
                                                    else loc), dv
                            except OSError:
                                pass
                except OSError:
                    pass
    except Exception:
        pass

    ep = which("kicad") or which("kicad.exe")
    return (ep, "unknown") if ep else (None, None)


# ====================================================================
# Ngspice
# ====================================================================

def find_ngspice(version: Optional[str] = None,
                 which: Callable = None,
                 run_cmd: Callable = None,
                 win_ngspice_paths: list = None,
                 choco_list: Callable = None) -> tuple:
    """Search Chocolatey, standard paths, and PATH for Ngspice."""
    if choco_list:
        found_ver = choco_list("ngspice")
        if found_ver:
            exe = _find_ngspice_exe(which, win_ngspice_paths)
            if version is None or found_ver.startswith(str(version)):
                return exe or "ngspice", found_ver

    exe = _find_ngspice_exe(which, win_ngspice_paths)
    if exe:
        return exe, "unknown"

    return None, None


def _find_ngspice_exe(which: Callable = None,
                      win_ngspice_paths: list = None) -> Optional[str]:
    if win_ngspice_paths:
        for p in win_ngspice_paths:
            if os.path.exists(p):
                return p
    return which("ngspice") or which("ngspice.exe")


# ====================================================================
# LLVM / Clang
# ====================================================================

def find_llvm(version: Optional[str] = None,
              which: Callable = None,
              run_cmd: Callable = None,
              win_llvm_paths: list = None) -> tuple:
    """Search standard paths and PATH for LLVM/Clang."""
    import platform as _platform

    if _platform.system() == "Windows":
        import ctypes
        try:
            ctypes.windll.user32.SendMessageTimeoutW(
                0xFFFF, 0x001A, 0, "Environment", 0x0002, 5000,
                ctypes.c_long())
        except Exception:
            pass

    paths = win_llvm_paths or []
    for path in paths:
        if os.path.exists(path):
            found_ver = _clang_version_from_output(path, run_cmd)
            if found_ver:
                if version is None or found_ver.startswith(str(version)):
                    return path, found_ver

    for exe_name in ["clang.exe", "clang", "clang++", "clang++.exe"]:
        exe_path = which(exe_name)
        if exe_path:
            found_ver = _clang_version_from_output(exe_path, run_cmd)
            if found_ver:
                if version is None or found_ver.startswith(str(version)):
                    return exe_path, found_ver

    return None, None


def _clang_version_from_output(exe_path: str,
                               run_cmd: Callable) -> Optional[str]:
    try:
        result = run_cmd([exe_path, "--version"])
        if result and result.returncode == 0:
            m = re.search(r'clang version (\d+)\.', result.stdout)
            if m:
                return m.group(1)
            m = re.search(r'LLVM version (\d+)', result.stdout)
            if m:
                return m.group(1)
    except Exception:
        pass
    return None


# ====================================================================
# GHDL
# ====================================================================

def find_ghdl(version: Optional[str] = None,
              which: Callable = None,
              run_cmd: Callable = None,
              base_dir: Path = None,
              msys_bin: Path = None,
              msys_env: dict = None) -> tuple:
    """Search custom install dir, MSYS2, and PATH for GHDL."""
    if base_dir:
        custom_exe = base_dir / "bin" / "ghdl.exe"
        if custom_exe.exists():
            found_ver = _ghdl_version_from_output(str(custom_exe), run_cmd)
            if found_ver:
                if version is None or found_ver.startswith(str(version)):
                    return str(custom_exe), found_ver

    if msys_bin:
        msys2_ghdl = msys_bin / "ghdl.exe"
        if msys2_ghdl.exists():
            found_ver = _ghdl_version_from_output(
                str(msys2_ghdl), run_cmd, msys_env)
            if found_ver:
                if version is None or found_ver.startswith(str(version)):
                    return str(msys2_ghdl), found_ver

    ghdl_exe = which("ghdl")
    if ghdl_exe:
        found_ver = _ghdl_version_from_output(ghdl_exe, run_cmd)
        if found_ver:
            if version is None or found_ver.startswith(str(version)):
                return ghdl_exe, found_ver

    return None, None


def _ghdl_version_from_output(exe_path: str, run_cmd: Callable,
                              env: dict = None) -> Optional[str]:
    try:
        kwargs = {}
        if env is not None:
            kwargs["env"] = env
        result = run_cmd([exe_path, "--version"], **kwargs)
        if result and result.returncode == 0:
            m = re.search(r'GHDL\s+(\d+\.\d+(?:\.\d+)?)', result.stdout)
            if m:
                return m.group(1)
    except Exception:
        pass
    return None


# ====================================================================
# Verilator
# ====================================================================

def find_verilator(version: Optional[str] = None,
                   which: Callable = None,
                   run_cmd: Callable = None,
                   msys_bin: Path = None,
                   msys_env: dict = None) -> tuple:
    """Search MSYS2 then PATH for Verilator."""
    if msys_bin:
        for exe_name in ["verilator.exe", "verilator_bin.exe", "verilator"]:
            msys2_exe = msys_bin / exe_name
            if msys2_exe.exists():
                found_ver = _verilator_version_from_output(
                    str(msys2_exe), run_cmd, msys_env)
                if found_ver:
                    if version is None or version == "latest" or \
                       found_ver.startswith(str(version)):
                        return str(msys2_exe), found_ver
                return str(msys2_exe), "unknown"

    for exe_name in ["verilator.exe", "verilator", "verilator_bin.exe"]:
        exe_path = which(exe_name)
        if exe_path:
            found_ver = _verilator_version_from_output(exe_path, run_cmd)
            if found_ver:
                if version is None or version == "latest" or \
                   found_ver.startswith(str(version)):
                    return exe_path, found_ver
            return exe_path, "unknown"

    return None, None


def _verilator_version_from_output(exe_path: str, run_cmd: Callable,
                                   env: dict = None) -> Optional[str]:
    try:
        kwargs = {}
        if env is not None:
            kwargs["env"] = env
        result = run_cmd([exe_path, "--version"], timeout=10, **kwargs)
        if result and result.returncode == 0:
            for line in result.stdout.split('\n'):
                if "Verilator" in line:
                    m = re.search(r'Verilator\s+(\d+\.\d+)', line)
                    if m:
                        return m.group(1)
    except Exception:
        pass
    return None


# ====================================================================
# Chocolatey itself
# ====================================================================

def find_chocolatey(version: Optional[str] = None,
                    which: Callable = None,
                    run_cmd: Callable = None) -> tuple:
    """Find Chocolatey itself (choco.exe)."""
    choco_exe = which("choco")
    if choco_exe:
        try:
            result = run_cmd([choco_exe, "--version"])
            if result and result.returncode == 0:
                found_ver = result.stdout.strip()
                if version is None or found_ver.startswith(str(version)):
                    return choco_exe, found_ver
        except Exception:
            pass
    return None, None


# ====================================================================
# PyQt (special case — not a traditional executable)
# ====================================================================

def find_pyqt(version: Optional[str] = None,
              run_cmd: Callable = None) -> tuple:
    """Find PyQt6 via Python import."""
    import sys
    for _ in range(2):
        try:
            result = run_cmd(
                [sys.executable, "-c",
                 "import PyQt6.QtCore; "
                 "print(PyQt6.QtCore.PYQT_VERSION_STR)"])
            if result and result.returncode == 0:
                found_ver = result.stdout.strip()
                if version is None or found_ver.startswith(str(version)):
                    return "PyQt6", found_ver
        except Exception:
            pass

    try:
        result = run_cmd(
            [sys.executable, "-m", "pip", "show", "PyQt6"])
        if result and result.returncode == 0:
            for line in result.stdout.split('\n'):
                if line.lower().startswith('version:'):
                    found_ver = line.split(':')[1].strip()
                    if version is None or found_ver.startswith(str(version)):
                        return "PyQt6", found_ver
    except Exception:
        pass

    return None, None
