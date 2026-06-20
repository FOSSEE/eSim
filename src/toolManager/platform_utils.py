import os, sys, platform as _platform, subprocess, shutil, threading, warnings
from pathlib import Path
from typing import Optional

IS_WINDOWS = sys.platform == "win32"
IS_LINUX = sys.platform.startswith("linux")
IS_MAC = sys.platform == "darwin"

def get_os_id():
    if IS_WINDOWS: return "win32"
    if IS_LINUX: return "linux"
    if IS_MAC: return "darwin"
    return "unknown"

DEFAULT_MSYS2_PATH = Path(r"C:\msys64")
MSYS2_PATH = DEFAULT_MSYS2_PATH
DEFAULT_ESIM_DIR = Path(r"C:\FOSSEE\eSim")
DEFAULT_INFO_FILE = "information.json"
DEFAULT_DOWNLOAD_DIR = "Download"

def get_msys2_path():
    if not IS_WINDOWS: raise RuntimeError("get_msys2_path() is only valid for Windows")
    return Path(os.environ.get("MSYS2_PATH", str(DEFAULT_MSYS2_PATH)))

def get_mysys2_path():
    warnings.warn("get_mysys2_path is deprecated, use get_msys2_path", DeprecationWarning, stacklevel=2)
    return get_msys2_path()

if IS_WINDOWS:
    def subprocess_flags():
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = subprocess.SW_HIDE
        return {"creationflags": subprocess.CREATE_NO_WINDOW, "startupinfo": si}
else:
    def subprocess_flags(): return {}

_LINUX_PM = [("apt-get","apt"),("dnf","dnf"),("yum","yum"),("pacman","pacman"),("zypper","zypper"),("apk","apk")]
_MAC_PM = [("brew","brew"),("port","port"),("nix","nix")]

def detect_package_manager():
    if IS_WINDOWS: return None
    for cmd, name in (_LINUX_PM if IS_LINUX else _MAC_PM if IS_MAC else []):
        if shutil.which(cmd): return name
    return None

def distro_label():
    if IS_WINDOWS: return f"Windows {_platform.release()}"
    if IS_MAC: return f"macOS {_platform.mac_ver()[0]}"
    try: info = _platform.freedesktop_os_release()
    except (AttributeError, OSError):
        try:
            info = {}
            with open("/etc/os-release") as f:
                for line in f:
                    if "=" in line: k, _, v = line.partition("="); info[k] = v.strip('"')
        except: return "Linux"
    return f"{info.get('NAME','Linux')} {info.get('VERSION_ID','')}".strip()

def is_admin():
    if not IS_WINDOWS: return True
    try: return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except: return False

def relaunch_as_admin():
    if not IS_WINDOWS: return
    import ctypes
    python_exe = sys.executable
    if python_exe.lower().endswith("python.exe"):
        pythonw = python_exe[:-10] + "pythonw.exe"
        if os.path.exists(pythonw): python_exe = pythonw
    ctypes.windll.shell32.ShellExecuteW(None, "runas", python_exe, f'"{Path(sys.argv[0]).resolve()}"', None, 1)

def run_cmd_stream(cmd, timeout=900, cwd=None, env=None):
    try:
        kwargs = subprocess_flags()
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, shell=False, encoding="utf-8", errors="ignore", cwd=cwd, env=env, **kwargs)
        out_lines = []
        def kill():
            try: proc.kill()
            except: pass
        timer = threading.Timer(timeout, kill)
        try:
            timer.start()
            for line in proc.stdout:
                line = line.rstrip()
                if line: print(line, flush=True); out_lines.append(line)
            proc.wait()
        finally: timer.cancel()
        return proc.returncode, "\n".join(out_lines)
    except Exception as e:
        print(f"[ERROR] Command failed: {e}", flush=True)
        return -1, str(e)

which = shutil.which

def print_status(state, installed, target):
    if installed: installed = str(installed).strip().replace("\n","").replace("\r","")
    print(f"{state}|{installed}|{target}", flush=True)
