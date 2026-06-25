import os, re
from pathlib import Path
from typing import Callable, Optional, List, Tuple

def find_chocolatey(version, which_fn, run_cmd):
    exe = which_fn("choco")
    if not exe: return (None, None)
    result = run_cmd([exe, "--version"])
    ver = result.stdout.strip() if result and result.returncode == 0 else None
    return (exe, ver)

def find_kicad(version, which_fn, run_cmd, win_kicad_paths=None):
    win_kicad_paths = win_kicad_paths or []
    for path, ver in win_kicad_paths:
        if os.path.exists(path):
            ver_file = Path(path).parent.parent / "version.txt"
            if ver_file.exists():
                m = re.search(r'(\d+\.\d+\.\d+)', ver_file.read_text())
                if m: return (path, m.group(1))
            return (path, ver)
    exe = which_fn("kicad") or which_fn("kicad.exe")
    if exe: return (exe, _get_version(exe, run_cmd))
    try:
        import winreg
        for hive in [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]:
            for flag in [winreg.KEY_WOW64_64KEY, winreg.KEY_WOW64_32KEY]:
                try:
                    with winreg.OpenKey(hive, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\kicad.exe", 0, winreg.KEY_READ | flag) as k:
                        p = winreg.QueryValue(k, None)
                        if p and os.path.exists(p): return (p, _get_version(p, run_cmd))
                except: pass
        for hive in [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]:
            for flag in [winreg.KEY_WOW64_64KEY, winreg.KEY_WOW64_32KEY]:
                try:
                    with winreg.OpenKey(hive, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", 0, winreg.KEY_READ | flag) as key:
                        for i in range(winreg.QueryInfoKey(key)[0]):
                            try:
                                sub = winreg.EnumKey(key, i)
                                with winreg.OpenKey(key, sub) as sk:
                                    name = winreg.QueryValueEx(sk, "DisplayName")[0]
                                    if "KiCad" in name:
                                        dv = winreg.QueryValueEx(sk, "DisplayVersion")[0]
                                        loc = winreg.QueryValueEx(sk, "InstallLocation")[0]
                                        exe = os.path.join(loc, "bin", "kicad.exe")
                                        return (exe if os.path.exists(exe) else loc), dv
                            except: pass
                except: pass
    except: pass
    return (None, None)

def find_ngspice(version, which_fn, run_cmd, win_ngspice_paths=None, choco_list_fn=None):
    ver = choco_list_fn("ngspice") if choco_list_fn else None
    if ver: return (which_fn("ngspice") or which_fn("ngspice.exe") or "", ver)
    for p in (win_ngspice_paths or []):
        if os.path.exists(p): return (p, _get_version(p, run_cmd))
    exe = which_fn("ngspice") or which_fn("ngspice.exe")
    if exe: return (exe, _get_version(exe, run_cmd))
    return (None, None)

def find_llvm(version, which_fn, run_cmd, win_llvm_paths=None):
    try:
        import ctypes
        ctypes.windll.user32.SendMessageTimeoutW(0x1A, 0, 0, 0, 2, 5000, None)
    except: pass
    for p in (win_llvm_paths or []):
        if os.path.exists(p):
            ver = _clang_version(p, run_cmd)
            if ver: return (p, ver)
    for exe_name in ["clang.exe", "clang", "clang++", "clang++.exe", "clang-cl.exe"]:
        exe = which_fn(exe_name)
        if exe:
            ver = _clang_version(exe, run_cmd)
            return (exe, ver)
    return (None, None)

def _clang_version(exe_path, run_cmd):
    result = run_cmd([exe_path, "--version"])
    if result and result.returncode == 0:
        m = re.search(r'clang version (\d+)\.', result.stdout) or re.search(r'LLVM version (\d+)', result.stdout)
        return m.group(1) if m else None
    return None

def find_ghdl(version, which_fn, run_cmd, base_dir, msys2_mingw_bin, msys2_env):
    candidates = []
    base_exe = Path(base_dir) / "bin" / "ghdl.exe"
    if base_exe.exists(): candidates.append(str(base_exe))
    if msys2_mingw_bin:
        msys_exe = Path(msys2_mingw_bin) / "ghdl.exe"
        if msys_exe.exists(): candidates.append(str(msys_exe))
    path_exe = which_fn("ghdl") or which_fn("ghdl.exe")
    if path_exe: candidates.append(path_exe)
    for c in candidates:
        ver = _ghdl_version(c, run_cmd, msys2_env if msys2_mingw_bin else None)
        if ver: return (c, ver)
    return (None, None)

def _ghdl_version(exe_path, run_cmd, env):
    try:
        result = run_cmd([exe_path, "--version"])
        if result and result.returncode == 0:
            m = re.search(r'GHDL\s+(\d+\.\d+(?:\.\d+)?)', result.stdout)
            return m.group(1) if m else None
    except: pass
    return None

def find_verilator(version, which_fn, run_cmd, msys2_mingw_bin, msys2_env):
    candidates = []
    if msys2_mingw_bin:
        for name in ["verilator.exe", "verilator_bin.exe", "verilator"]:
            p = Path(msys2_mingw_bin) / name
            if p.exists(): candidates.append(str(p))
    path_exe = which_fn("verilator") or which_fn("verilator.exe")
    if path_exe: candidates.append(path_exe)
    for c in candidates:
        ver = _verilator_version(c, run_cmd, msys2_env)
        if ver: return (c, ver)
    return (None, None)

def _verilator_version(exe_path, run_cmd, env):
    try:
        result = run_cmd([exe_path, "--version"])
        if result and result.returncode == 0:
            m = re.search(r'Verilator\s+(\d+\.\d+)', result.stdout)
            return m.group(1) if m else None
    except: pass
    return None

def find_pyqt(version, run_cmd):
    import sys
    for _ in range(2):
        try:
            result = run_cmd([sys.executable, "-c",
                "import PyQt6.QtCore; print(PyQt6.QtCore.PYQT_VERSION_STR)"])
            if result and result.returncode == 0:
                ver = result.stdout.strip()
                return ("PyQt6", ver) if ver else None
        except: pass
    result = run_cmd([sys.executable, "-m", "pip", "show", "PyQt6"])
    if result and result.returncode == 0:
        m = re.search(r'Version:\s*(\S+)', result.stdout)
        return ("PyQt6", m.group(1)) if m else None
    return None

def _get_version(exe_path, run_cmd):
    result = run_cmd([exe_path, "--version"])
    if result and result.returncode == 0:
        parts = result.stdout.split("\n")[0].strip().split()
        return parts[-1] if parts else None
    return None
