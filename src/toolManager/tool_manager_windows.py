#!/usr/bin/env python3

import os
import sys
import subprocess
import shutil
import platform
import argparse
import re
import json
import urllib.request
import zipfile
import time
import io
from pathlib import Path
from platform_utils import IS_WINDOWS, get_mysys2_path

# Add local directory to path for backend utility imports
_local_path = str(Path(__file__).resolve().parent)
if _local_path not in sys.path:
    sys.path.insert(0, _local_path)

try:
    MSYS2_PATH = get_mysys2_path();
except RuntimeError as e:
    print(e)

from utils import (
    run_cmd_safe, run_cmd_stream, which, print_status,
    DEFAULT_ESIM_DIR, WIN_KICAD_PATHS,
    WIN_NGSPICE_PATHS, WIN_LLVM_PATHS, get_msys2_bash, 
    get_msys2_mingw_bin
)

if IS_WINDOWS:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='ignore')

BASE_DIR = Path(__file__).resolve().parent
STATE_FILE = BASE_DIR / "information.json"
BASE_DIR.mkdir(parents=True, exist_ok=True)

DOWNLOAD_DIR = BASE_DIR / "Download"
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

VERILATOR_VERSIONS = {
    "5.006": "verilator-5.006.7z",
    "5.018": "verilator-5.018.7z",
    "5.026": "verilator-5.026.7z",
    "5.032": "verilator-5.032.7z",
    "latest": None, 
}

KICAD_VERSIONS = {
    "6": ["6.0.11", "6.0.10", "6.0.9", "6.0.8"],  
    "7": ["7.0.11", "7.0.10", "7.0.9"],  
    "8": ["8.0.9", "8.0.8", "8.0.7"],  
    "9": ["9.0.7", "9.0.6", "9.0.5"], 
    "latest": None
}

KICAD_6_DIRECT_URLS = {
    "6.0.11": "https://github.com/KiCad/kicad-source-mirror/releases/download/6.0.11/kicad-6.0.11-x86_64.exe",
    "6.0.10": "https://github.com/KiCad/kicad-source-mirror/releases/download/6.0.10/kicad-6.0.10-x86_64.exe",
    "6.0.9": "https://github.com/KiCad/kicad-source-mirror/releases/download/6.0.9/kicad-6.0.9-x86_64.exe",
}

NGSPICE_VERSIONS = {
    "35": "35",
    "36": "36", 
    "37": "37",
    "38": "38",
    "39": "39",
    "40": "40",
    "41": "41",
    "42": "42",
    "latest": None
}

LLVM_VERSIONS = {
    "13": "13.0.1",
    "14": "14.0.6",
    "15": "15.0.7",
    "16": "16.0.6",
    "17": "17.0.6",
    "18": "18.1.8",
    "19": "19.1.5",
    "latest": None
}

ESIM_VERSIONS = {
    "2.4":    "https://static.fossee.in/esim/installation-files/eSim-2.4_installer.exe",
    "2.3":    "https://static.fossee.in/esim/installation-files/eSim-2.3_installer.exe",
    "2.2":    "https://static.fossee.in/esim/installation-files/eSim-2.2_installer.exe",
    "latest": "https://static.fossee.in/esim/installation-files/eSim-2.4_installer.exe",
}


def _get_package(filename, url, label=""):
    local = DOWNLOAD_DIR / filename
    if local.exists():
        print(f"[LOCAL] Using cached: {filename}", flush=True)
        return local
    dest = DOWNLOAD_DIR / filename
    print(f"[DOWNLOAD] {label or filename}", flush=True)
    try:
        def _hook(n, bs, total):
            if total > 0 and n % 50 == 0:
                pct = min(n * bs * 100 / total, 100)
                mb  = min(n * bs, total) / (1024*1024)
                tot = total / (1024*1024)
                print(f"[DOWNLOAD] {pct:.1f}% ({mb:.1f}/{tot:.1f} MB)", flush=True)
        urllib.request.urlretrieve(url, dest, _hook)
        print("[OK] Download complete", flush=True)
        return dest
    except Exception as e:
        print(f"[ERROR] Download failed: {e}", flush=True)
        if dest.exists():
            dest.unlink()
        return None



def find_kicad_fixed(version=None):
    versioned = WIN_KICAD_PATHS
    for path, major in versioned:
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
                                    name = winreg.QueryValueEx(sk, "DisplayName")[0]
                                    if "KiCad" in name:
                                        dv  = winreg.QueryValueEx(sk, "DisplayVersion")[0]
                                        loc = winreg.QueryValueEx(sk, "InstallLocation")[0]
                                        exe = os.path.join(loc, "bin", "kicad.exe")
                                        major = dv.split(".")[0] if dv else "unknown"
                                        if version is None or str(version) in ("latest", major):
                                            return (exe if os.path.exists(exe) else loc), dv
                            except OSError:
                                pass
                except OSError:
                    pass
    except Exception:
        pass

    ep = which("kicad") or which("kicad.exe")
    return (ep, "unknown") if ep else (None, None)

def find_ngspice_safe(version=None):
    choco = which("choco") or which("choco.exe")
    if choco:
        try:
            for choco_cmd in [
                [choco, "list", "--exact", "ngspice"],
                [choco, "list", "--local-only", "--exact", "ngspice"],
            ]:
                result = run_cmd_safe(choco_cmd, timeout=15)
                if result and result.returncode == 0:
                    for line in result.stdout.splitlines():
                        m = re.match(r'ngspice\s+(\S+)', line, re.IGNORECASE)
                        if m:
                            found_ver = m.group(1)
                            exe = _find_ngspice_exe()
                            if version is None or found_ver.startswith(str(version)):
                                return exe or "ngspice", found_ver
                            return exe or "ngspice", found_ver
                    break 
        except Exception:
            pass

    exe = _find_ngspice_exe()
    if exe:
        return exe, "unknown"

    return None, None


def _find_ngspice_exe():
    for p in WIN_NGSPICE_PATHS:
        if os.path.exists(p):
            return p
    return which("ngspice") or which("ngspice.exe")

def find_llvm_fixed(version=None):
    if IS_WINDOWS:
        import ctypes
        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x001A
        SMTO_ABORTIFHUNG = 0x0002
        result = ctypes.c_long()
        try:
            ctypes.windll.user32.SendMessageTimeoutW(
                HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment",
                SMTO_ABORTIFHUNG, 5000, ctypes.byref(result)
            )
        except:
            pass
    
    common_paths = WIN_LLVM_PATHS
    
    for path in common_paths:
        if os.path.exists(path):
            try:
                result = run_cmd_safe([path, "--version"])
                if result and result.returncode == 0:
                    match = re.search(r'clang version (\d+)\.', result.stdout)
                    if match:
                        found_ver = match.group(1)
                        if version is None or found_ver.startswith(str(version)):
                            return path, found_ver
                    match = re.search(r'LLVM version (\d+)', result.stdout)
                    if match:
                        found_ver = match.group(1)
                        if version is None or found_ver.startswith(str(version)):
                            return path, found_ver
            except:
                pass
    
    for exe_name in ["clang.exe", "clang", "clang++", "clang++.exe"]:
        exe_path = which(exe_name)
        if exe_path:
            try:
                result = run_cmd_safe([exe_path, "--version"])
                if result and result.returncode == 0:
                    match = re.search(r'clang version (\d+)\.', result.stdout)
                    if match:
                        found_ver = match.group(1)
                        if version is None or found_ver.startswith(str(version)):
                            return exe_path, found_ver
                    match = re.search(r'LLVM version (\d+)', result.stdout)
                    if match:
                        found_ver = match.group(1)
                        if version is None or found_ver.startswith(str(version)):
                            return exe_path, found_ver
            except:
                pass
    return None, None

def find_pyqt_fixed(version=None):
    try:
        result = run_cmd_safe([sys.executable, "-c", "import PyQt6.QtCore; print(PyQt6.QtCore.PYQT_VERSION_STR)"])
        if result and result.returncode == 0:
            found_ver = result.stdout.strip()
            if version is None or found_ver.startswith(str(version)):
                return "PyQt6", found_ver
    except:
        pass
    
    try:
        result = run_cmd_safe([sys.executable, "-c", "import PyQt6.QtCore; print(PyQt6.QtCore.PYQT_VERSION_STR)"])
        if result and result.returncode == 0:
            found_ver = result.stdout.strip()
            if version is None or found_ver.startswith(str(version)):
                return "PyQt6", found_ver
    except:
        pass
    
    try:
        result = run_cmd_safe([sys.executable, "-m", "pip", "show", "PyQt6"])
        if result and result.returncode == 0:
            for line in result.stdout.split('\n'):
                if line.lower().startswith('version:'):
                    found_ver = line.split(':')[1].strip()
                    if version is None or found_ver.startswith(str(version)):
                        return "PyQt6", found_ver
    except:
        pass
    
    return None, None
def get_msys2_env():
    env = os.environ.copy()
    paths = []
    msys_bin = get_msys2_mingw_bin()
    if msys_bin: paths.append(str(msys_bin))
    msys_root = MSYS2_PATH
    if msys_root:
        usr_bin = msys_root.parent / "usr" / "bin"
        if usr_bin.exists(): paths.append(str(usr_bin))
    if paths:
        env["PATH"] = os.pathsep.join(paths) + os.pathsep + env.get("PATH", "")
    return env

def find_ghdl(version=None):
    custom_exe = BASE_DIR / "bin" / "ghdl.exe"
    if custom_exe.exists():
        try:
            result = run_cmd_safe([str(custom_exe), "--version"], env=get_msys2_env())
            if result and result.returncode == 0:
                match = re.search(r'GHDL\s+(\d+\.\d+(?:\.\d+)?)', result.stdout)
                if match:
                    found_ver = match.group(1)
                    if version is None or found_ver.startswith(str(version)):
                        return str(custom_exe), found_ver
        except:
            pass
    
    msys_bin = get_msys2_mingw_bin()
    if msys_bin:
        msys2_ghdl = msys_bin / "ghdl.exe"
        if msys2_ghdl.exists():
            try:
                result = run_cmd_safe([str(msys2_ghdl), "--version"], env=get_msys2_env())
                if result and result.returncode == 0:
                    match = re.search(r'GHDL\s+(\d+\.\d+(?:\.\d+)?)', result.stdout)
                    if match:
                        found_ver = match.group(1)
                        if version is None or found_ver.startswith(str(version)):
                            return str(msys2_ghdl), found_ver
            except:
                pass
    
    ghdl_exe = which("ghdl")
    if ghdl_exe:
        try:
            result = run_cmd_safe([ghdl_exe, "--version"])
            if result and result.returncode == 0:
                match = re.search(r'GHDL\s+(\d+\.\d+(?:\.\d+)?)', result.stdout)
                if match:
                    found_ver = match.group(1)
                    if version is None or found_ver.startswith(str(version)):
                        return ghdl_exe, found_ver
        except:
            pass
    
    return None, None

def find_verilator(version=None):
    msys_bin = get_msys2_mingw_bin()
    if msys_bin:
        for exe_name in ["verilator.exe", "verilator_bin.exe", "verilator"]:
            msys2_exe = msys_bin / exe_name
            if msys2_exe.exists():
                try:
                    result = run_cmd_safe([str(msys2_exe), "--version"], timeout=10, env=get_msys2_env())
                    if result and result.returncode == 0:
                        for line in result.stdout.split('\n'):
                            if "Verilator" in line:
                                match = re.search(r'Verilator\s+(\d+\.\d+)', line)
                                if match:
                                    found_ver = match.group(1)
                                    if version is None or version == "latest" or found_ver.startswith(str(version)):
                                        return str(msys2_exe), found_ver
                                return str(msys2_exe), "unknown"
                except:
                    return str(msys2_exe), "unknown"
    
    for exe_name in ["verilator.exe", "verilator", "verilator_bin.exe"]:
        exe_path = which(exe_name)
        if exe_path:
            try:
                result = run_cmd_safe([exe_path, "--version"], timeout=10)
                if result and result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if "Verilator" in line:
                            match = re.search(r'Verilator\s+(\d+\.\d+)', line)
                            if match:
                                found_ver = match.group(1)
                                if version is None or version == "latest" or found_ver.startswith(str(version)):
                                    return exe_path, found_ver
                    return exe_path, "unknown"
            except:
                pass
    
    return None, None

def find_chocolatey(version=None):
    choco_exe = which("choco")
    if choco_exe:
        try:
            result = run_cmd_safe([choco_exe, "--version"])
            if result and result.returncode == 0:
                found_ver = result.stdout.strip()
                if version is None or found_ver.startswith(str(version)):
                    return choco_exe, found_ver
        except:
            pass
    return None, None

def check_chocolatey(target_version):
    if target_version == "none":
        exe, version = find_chocolatey(None)
        if exe:
            print_status("installed", version or "unknown", "latest")
        else:
            print_status("not_installed", "none", "latest")
        return

    exe, version = find_chocolatey(target_version)
    
    if exe:
        if target_version == "latest":
            print_status("installed", version, target_version)
        elif version == target_version:
            print_status("installed", version, target_version)
        else:
            print_status("wrong_version", version, target_version)
    else:
        print_status("not_installed", "none", target_version)

def install_chocolatey(target_version, upgrade=False):
    choco_exe, current_version = find_chocolatey(target_version)
    if choco_exe and not upgrade:
        check_chocolatey(target_version)
        return
    
    print(f"{'Upgrading' if upgrade else 'Installing'} Chocolatey...")
    cmd = [
        "powershell", "-Command",
        "Set-ExecutionPolicy Bypass -Scope Process -Force; "
        "[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; "
        "iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
    ]
    
    result = run_cmd_safe(cmd, timeout=600)
    if result and result.returncode == 0:
        exe, installed_version = find_chocolatey(None)
        if exe:
            print_status("installed", installed_version or "unknown", target_version)
        else:
            print_status("install_failed", "not_found", target_version)
    else:
        print_status("install_failed", "choco_error", target_version)

def check_kicad(target_version):
    exe, version = find_kicad_fixed(None)
    if target_version == "none":
        print_status("installed" if exe else "not_installed",
                     version or "none", "latest")
        return
    if exe:
        if target_version == "latest":
            print_status("installed", version or "unknown", target_version)
        elif version in (None, "unknown"):
            print_status("installed", "unknown", target_version)
        elif version.startswith(f"{target_version}.") or version.startswith(f"{target_version}x"):
            print_status("installed", version, target_version)
        else:
            print_status("wrong_version", version, target_version)
    else:
        print_status("not_installed", "none", target_version)

def install_kicad(target_version, upgrade=False):
    choco_exe, _ = find_chocolatey(None)
    if not choco_exe:
        print_status("install_failed", "choco_missing", target_version)
        return
    
    print(f"{'Upgrading' if upgrade else 'Installing'} KiCad {target_version}...")
    
    if target_version == "6":
        print("[INFO] KiCad 6 detected - Chocolatey's download links are broken (osdn.net)")
        print("[INFO] Using direct download from GitHub instead...")
        
        print("Running KiCad cleanup...")
        cleanup_kicad()
        
        success = install_kicad_direct("6.0.11")
        if not success:
            success = install_kicad_direct("6.0.10")
        if not success:
            success = install_kicad_direct("6.0.9")
        
        if success:
            return
        else:
            print_status("install_failed", "direct_download_failed", target_version)
            return
    
    version_candidates = KICAD_VERSIONS.get(target_version, target_version)
    
    if not isinstance(version_candidates, list):
        version_candidates = [version_candidates] if version_candidates else [None]
    
    cleanup_kicad()
    
    time.sleep(2)  
    
    
    installation_success = False
    last_error = None
    
    for exact_version in version_candidates:
        if exact_version is None:
            print(f"[CHOCO] Attempting to install latest KiCad...")
            cmd = ["choco", "install", "kicad", "-y", "--no-progress", "--ignore-checksums"]
        else:
            print(f"[CHOCO] Attempting to install KiCad {exact_version}...")
            cmd = [
                "choco", "install", "kicad",
                "--version", exact_version,
                "-y",
                "--no-progress",
                "--force",
                "--allow-downgrade",
                "--ignore-checksums",
                "--execution-timeout", "600"
            ]
        
        print(f"[CHOCO] Running: {' '.join(cmd)}")
        rc, out = run_cmd_stream(cmd, timeout=1500)
        
        if rc != 0:
            out_lower = out.lower()
            if "osdn.net" in out_lower or "404" in out_lower:
                print("[ERROR] Download URL is broken (osdn.net issue)")
                print("[INFO] Chocolatey's KiCad links are outdated")
                break
            elif "checksum" in out_lower:
                print("[ERROR] Checksum verification failed")
            elif "download" in out_lower and "failed" in out_lower:
                print("[ERROR] Download failed")
            continue
        
        print("[CHOCO] Verifying installation...")
        time.sleep(3)
        
        exe, installed_version = find_kicad_fixed(None)
        if exe:
            print(f"[SUCCESS] KiCad {installed_version} installed successfully!")
            print_status("installed", installed_version, target_version)
            installation_success = True
            break
        
        check_paths = [
            (r"C:\Program Files\KiCad\9.0\bin\kicad.exe", "9"),
            (r"C:\Program Files\KiCad\8.0\bin\kicad.exe", "8"),
            (r"C:\Program Files\KiCad\7.0\bin\kicad.exe", "7"),
            (r"C:\Program Files\KiCad\6.0\bin\kicad.exe", "6"),
        ]
        
        for path, ver in check_paths:
            if os.path.exists(path):
                print(f"[SUCCESS] Found KiCad at: {path}")
                print_status("installed", f"{ver}.x", target_version)
                installation_success = True
                break
        
        if installation_success:
            break
        
        last_error = out
    
    if not installation_success:
        print(f"[ERROR] All installation attempts failed for KiCad {target_version}")
        
        error_msg = "installation_failed"
        if last_error:
            if "osdn.net" in last_error.lower() or "404" in last_error.lower():
                error_msg = "broken_download_url"
                print("[INFO] The Chocolatey package has broken download URLs")
                print("[TIP] This is a known issue with older KiCad packages")
            elif "checksum" in last_error.lower():
                error_msg = "checksum_failed"
            elif "download" in last_error.lower():
                error_msg = "download_failed"
            else:
                error_msg = last_error[:50].replace('\n', ' ').replace('|', '_')
        
        print_status("install_failed", error_msg, target_version)

def cleanup_kicad():
    print("Step 1/3: Chocolatey uninstall...")
    uninstall_cmd = ["choco", "uninstall", "kicad", "-y", "--force-dependencies", "--remove-dependencies", "--no-progress"]
    run_cmd_safe(uninstall_cmd, timeout=180)
    
    print("Step 2/3: Manual file cleanup...")
    powershell_cleanup = r"""
    Get-Process -Name "*kicad*" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
    
    $paths = @(
        "C:\Program Files\KiCad",
        "C:\Program Files\KiCad 9.0",
        "C:\Program Files\KiCad 8.0",
        "C:\Program Files\KiCad 7.0",
        "C:\Program Files\KiCad 6.0",
        "C:\Program Files (x86)\KiCad",
        "$env:LOCALAPPDATA\KiCad",
        "$env:APPDATA\kicad"
    )
    
    foreach ($path in $paths) {
        if (Test-Path $path) {
            Write-Host "Removing: $path"
            Remove-Item -Path $path -Recurse -Force -ErrorAction SilentlyContinue
            Start-Sleep -Milliseconds 500
        }
    }
    """
    ps_cmd = ["powershell", "-Command", powershell_cleanup]
    run_cmd_safe(ps_cmd, timeout=180)
    
    print("Step 3/3: Clearing Chocolatey cache...")
    cache_cmd = ["choco", "cache", "remove", "--expired", "-y"]
    run_cmd_safe(cache_cmd, timeout=60)

def install_kicad_direct(version):
    if version not in KICAD_6_DIRECT_URLS:
        print(f"[ERROR] No direct download URL for version {version}")
        return False
    
    url = KICAD_6_DIRECT_URLS[version]
    print(f"[INFO] Downloading KiCad {version} from GitHub...")
    print(f"[URL] {url}")
    
    import tempfile
    temp_dir = Path(tempfile.gettempdir())
    installer_path = temp_dir / f"kicad-{version}-installer.exe"
    
    try:
        print("[INFO] Downloading... (this may take 5-10 minutes, file is ~800MB)")
        
        def reporthook(blocknum, blocksize, totalsize):
            if totalsize > 0:
                percent = min(blocknum * blocksize * 100 / totalsize, 100)
                if blocknum % 50 == 0:
                    mb_done = min(blocknum * blocksize, totalsize) / (1024 * 1024)
                    mb_total = totalsize / (1024 * 1024)
                    print(f"[DOWNLOAD] {percent:.1f}% ({mb_done:.1f} MB / {mb_total:.1f} MB)", flush=True)
        
        urllib.request.urlretrieve(url, installer_path, reporthook=reporthook)
        print(f"\n[OK] Downloaded to: {installer_path}")
        
        if not installer_path.exists():
            print("[ERROR] Download failed - file not found")
            return False
        
        file_size_mb = installer_path.stat().st_size / (1024 * 1024)
        print(f"[INFO] Downloaded file size: {file_size_mb:.1f} MB")
        
        if file_size_mb < 100:
            print("[ERROR] Downloaded file is too small - likely corrupted")
            return False
        
        print("[INFO] Running silent installation...")
        print("[NOTE] This may take 5-10 minutes...")
        
        install_cmd = [
            str(installer_path),
            "/S", 
            "/NCRC", 
        ]
        
        result = subprocess.run(install_cmd, timeout=900)
        
        print("[INFO] Waiting for installation to complete...")
        time.sleep(10)
         
        exe, installed_version = find_kicad_fixed(None)
        if exe:
            print(f"[SUCCESS] KiCad {installed_version} installed successfully!")
            print_status("installed", installed_version or version, "6")
            return True
        
        for path in [r"C:\Program Files\KiCad\6.0\bin\kicad.exe"]:
            if os.path.exists(path):
                print(f"[SUCCESS] KiCad installed at: {path}")
                print_status("installed", version, "6")
                return True
        
        print("[ERROR] Installation completed but KiCad not found")
        print("[TIP] Check C:\\Program Files\\KiCad manually")
        return False
        
    except urllib.error.URLError as e:
        print(f"[ERROR] Download failed: {e}")
        print("[TIP] Check your internet connection")
        return False
    except Exception as e:
        print(f"[ERROR] Installation failed: {e}")
        return False
    finally:
        if installer_path.exists():
            try:
                print("[INFO] Cleaning up installer file...")
                installer_path.unlink()
            except:
                pass

def check_ngspice(target_version):
    exe, version = find_ngspice_safe(None)
    if target_version == "none":
        print_status("installed" if exe else "not_installed",
                     version or "none", "latest")
        return
    if exe:
        if target_version == "latest":
            print_status("installed", version or "unknown", target_version)
        elif version == "unknown":
            print_status("installed", "unknown", target_version)
        elif version == target_version or (version and version.startswith(str(target_version))):
            print_status("installed", version, target_version)
        else:
            print_status("wrong_version", version or "unknown", target_version)
    else:
        print_status("not_installed", "none", target_version)

def install_ngspice(target_version, upgrade=False):
    choco_exe, _ = find_chocolatey(None)
    if not choco_exe:
        print_status("install_failed", "choco_missing", target_version)
        return
    
    exact_version = NGSPICE_VERSIONS.get(target_version, target_version)
    
    print("Uninstalling existing ngspice...")
    uninstall_cmd = ["choco", "uninstall", "ngspice", "-y", "--force-dependencies", "--no-progress"]
    run_cmd_safe(uninstall_cmd, timeout=180)
    
    print(f"[1/3] Removing existing ngspice...")
    print(f"[2/3] Installing ngspice {target_version} via Chocolatey...")
    
    if target_version == "latest":
        cmd = ["choco", "install", "ngspice", "-y", "--no-progress"]
    else:
        cmd = ["choco", "install", "ngspice", "--version", exact_version, "-y", "--no-progress", "--allow-downgrade", "--force"]
    
    rc, out = run_cmd_stream(cmd, timeout=300)
    
    if rc == 0:
        print("[3/3] Verifying installation...")
        time.sleep(2)
        exe, installed_version = find_ngspice_safe(None)
        if exe:
            print(f"[OK] ngspice {installed_version or 'unknown'} installed successfully")
            print_status("installed", installed_version or "unknown", target_version)
        else:
            print_status("install_failed", "not_found", target_version)
    else:
        print_status("install_failed", out[-50:].replace('\n',' ').replace('|','_') or "unknown_error", target_version)

def check_llvm(target_version):
    if target_version == "none":
        exe, version = find_llvm_fixed(None)
        if exe:
            print_status("installed", version or "unknown", "latest")
        else:
            print_status("not_installed", "none", "latest")
        return

    exe, version = find_llvm_fixed(target_version)
    
    if exe and version:
        if target_version == "latest" or version == target_version:
            print_status("installed", version, target_version)
        else:
            print_status("wrong_version", version, target_version)
    else:
        print_status("not_installed", "none", target_version)

def install_llvm(target_version, upgrade=False):
    choco_exe, _ = find_chocolatey(None)
    if not choco_exe:
        print_status("install_failed", "choco_missing", target_version)
        return
    
    exact_version = LLVM_VERSIONS.get(target_version, target_version)
    
    print(f"[1/3] Removing existing LLVM...")
    run_cmd_stream(["choco", "uninstall", "llvm", "-y", "--no-progress"], timeout=180)
    
    print(f"[2/3] Installing LLVM {target_version} ({exact_version}) via Chocolatey...")
    
    if target_version == "latest":
        cmd = ["choco", "install", "llvm", "-y", "--no-progress"]
    else:
        cmd = ["choco", "install", "llvm", "--version", exact_version, "-y", "--no-progress", "--allow-downgrade", "--force"]
    
    rc, out = run_cmd_stream(cmd, timeout=300)
    
    if rc == 0:
        print("[3/3] Verifying LLVM installation...")
        time.sleep(3)

        common_paths = [
            r"C:\Program Files\LLVM\bin\clang.exe",
            r"C:\Program Files (x86)\LLVM\bin\clang.exe",
        ]
        for path in common_paths:
            if os.path.exists(path):
                result = run_cmd_safe([path, "--version"], timeout=10)
                if result and result.returncode == 0:
                    match = re.search(r'clang version (\d+)\.', result.stdout)
                    if match:
                        found_ver = match.group(1)
                        print(f"[SUCCESS] LLVM {found_ver} installed at {path}")
                        print_status("installed", found_ver, target_version)
                        return
                print(f"[SUCCESS] LLVM installed at {path}")
                print_status("installed", exact_version or target_version, target_version)
                return

        print("[ERROR] LLVM verification failed - exe not found after install")
        print_status("install_failed", "verification_failed", target_version)
    else:
        print_status("install_failed", out[-50:].replace('\n',' ').replace('|','_') or "choco_error", target_version)

def check_pyqt(target_version):
    if target_version == "none":
        package, version = find_pyqt_fixed(None)
        if package:
            print_status("installed", version or "unknown", "latest")
        else:
            print_status("not_installed", "none", "latest")
        return

    package, version = find_pyqt_fixed(target_version)
    
    if package and version:
        if target_version == "latest":
            print_status("installed", version, target_version)
        elif version.startswith(target_version):
            print_status("installed", version, target_version)
        else:
            print_status("wrong_version", version, target_version)
    else:
        print_status("not_installed", "none", target_version)

def install_pyqt(target_version, upgrade=False):
    print(f"{'Upgrading' if upgrade else 'Installing'} PyQt {target_version}...")
    
    if target_version.startswith("6.") or target_version == "latest":
        package = "PyQt6"
    else:
        package = "PyQt6"
    
    if target_version == "latest":
        cmd = [sys.executable, "-m", "pip", "install", package, "--upgrade"]
    else:
        uninstall_cmd = [sys.executable, "-m", "pip", "uninstall", package, "-y"]
        run_cmd_safe(uninstall_cmd, timeout=60)
        cmd = [sys.executable, "-m", "pip", "install", f"{package}=={target_version}"]
    
    result = run_cmd_safe(cmd, timeout=300)
    
    if result and result.returncode == 0:
        package_found, version_found = find_pyqt_fixed(None)
        if package_found:
            print_status("installed", version_found or target_version, target_version)
        else:
            print_status("install_failed", "verification_failed", target_version)
    else:
        error_msg = result.stderr if result else "unknown_error"
        print_status("install_failed", error_msg[:100], target_version)

def check_ghdl_tool(target_version):
    if target_version == "none":
        exe, version = find_ghdl(None)
        if exe:
            print_status("installed", version or "unknown", "latest")
        else:
            print_status("not_installed", "none", "latest")
        return

    exe, version = find_ghdl(target_version)
    
    if exe and version:
        if target_version == "latest":
            print_status("installed", version, target_version)
        elif version.startswith(target_version):
            print_status("installed", version, target_version)
        else:
            print_status("wrong_version", version, target_version)
    else:
        print_status("not_installed", "none", target_version)

def install_ghdl(v, upgrade=False):
    
    urls = {
        "4.0.0": "https://github.com/ghdl/ghdl/releases/download/v4.0.0/ghdl-MINGW32.zip",
        "4.1.0": "https://github.com/ghdl/ghdl/releases/download/v4.1.0/ghdl-MINGW32.zip",
        
        "5.0.0": "https://github.com/ghdl/ghdl/releases/download/v5.0.1/ghdl-mcode-5.0.1-mingw64.zip",
        "5.1.1": "https://github.com/ghdl/ghdl/releases/download/v5.1.1/ghdl-mcode-5.1.1-mingw64.zip",
        "latest": "https://github.com/ghdl/ghdl/releases/download/v5.1.1/ghdl-mcode-5.1.1-mingw64.zip",
    }
    
    if v not in urls:
        print_status("not_supported", "none", v)
        return
    
    url = urls[v]
    print(f"Installing GHDL {v} from: {url}")
    
    install_dir = BASE_DIR / "ghdl" / v
    if upgrade and install_dir.exists():
        shutil.rmtree(install_dir, ignore_errors=True)
    
    install_dir.mkdir(parents=True, exist_ok=True)
    zip_file = install_dir / "download.zip"
    
    try:
        def _ghdl_hook(n, bs, total):
            if total > 0 and n % 50 == 0:
                pct = min(n * bs * 100 / total, 100)
                mb_done = min(n * bs, total) / (1024 * 1024)
                mb_total = total / (1024 * 1024)
                print(f"[DOWNLOAD] {pct:.1f}% ({mb_done:.1f} MB / {mb_total:.1f} MB)", flush=True)
        urllib.request.urlretrieve(url, zip_file, _ghdl_hook)
        print("[OK] Download complete")
    except Exception as e:
        print(f"[ERROR] Download failed: {e}")
        print_status("install_failed", "download_error", v)
        return
    
    try:
        with zipfile.ZipFile(zip_file, 'r') as zf:
            files = zf.namelist()
            print(f"Archive contains {len(files)} files")
            print("[INFO] Extracting package... This may take several minutes.", flush=True)
            zf.extractall(install_dir)
            print("[OK] Extraction complete")
    except Exception as e:
        print(f"[ERROR] Extraction failed: {e}")
        print_status("install_failed", "extract_error", v)
        return
    finally:
        if zip_file.exists():
            zip_file.unlink()
    
    ghdl_exe = None
    for root, dirs, files in os.walk(install_dir):
        for file in files:
            if file.lower() == "ghdl.exe":
                ghdl_exe = Path(root) / file
                print(f"Found: {ghdl_exe}")
                break
        if ghdl_exe:
            break
    
    if ghdl_exe:
        bin_dir = BASE_DIR / "bin"
        bin_dir.mkdir(exist_ok=True)
        dest_exe = bin_dir / "ghdl.exe"
        
        shutil.copy2(ghdl_exe, dest_exe)
        print(f"[OK] Installed to: {dest_exe}")
        
        result = run_cmd_safe([str(dest_exe), "--version"], env=get_msys2_env())
        if result and result.returncode == 0:
            match = re.search(r'GHDL\s+(\d+\.\d+(?:\.\d+)?)', result.stdout)
            version = match.group(1) if match else "unknown"
            print(f"[OK] GHDL {version} ready to use")
            print_status("installed", version, v)
        else:
            print(f"[WARNING] Version check failed")
            print_status("installed", v, v)
    else:
        print(f"[ERROR] No ghdl.exe found in archive")
        print_status("install_failed", "no_exe", v)

def run_msys2_command(cmd, timeout=300):
    bash_exe = get_msys2_bash()
    
    if not bash_exe:
        print(f"[ERROR] MSYS2 not found at {MSYS2_PATH}")
        return None
    
    full_cmd = [str(bash_exe), "-lc", cmd]
    
    try:
        rc, out = run_cmd_stream(full_cmd, timeout)
        class _R:
            def __init__(self, rc, out):
                self.returncode = rc
                self.stdout = out
                self.stderr = ""
        return _R(rc, out)
    except Exception as e:
        print(f"[ERROR] MSYS2 command failed: {e}")
        return None

def check_verilator_tool(target_version):
    if target_version == "none":
        exe, version = find_verilator(None)
        if exe:
            print_status("installed", version or "unknown", "latest")
        else:
            print_status("not_installed", "none", "latest")
        return

    exe, version = find_verilator(target_version)
    
    if exe and version:
        if target_version == "latest":
            print_status("installed", version, target_version)
        elif version == target_version or target_version in version:
            print_status("installed", version, target_version)
        else:
            print_status("wrong_version", version, target_version)
    else:
        print_status("not_installed", "none", target_version)

def _install_verilator_from_7z(archive_path, v):
    try:
        import py7zr
    except ImportError:
        print("[ERROR] py7zr not installed. Run: pip install py7zr")
        print_status("install_failed", "py7zr_missing", v)
        return False

    extract_dir = DOWNLOAD_DIR / "verilator_extract"
    if extract_dir.exists():
        shutil.rmtree(extract_dir, ignore_errors=True)
    extract_dir.mkdir(parents=True, exist_ok=True)

    print(f"[1/3] Extracting {archive_path.name}... This may take several minutes.", flush=True)
    try:
        with py7zr.SevenZipFile(archive_path, mode='r') as archive:
            archive.extractall(extract_dir)
        print("[1/3] Extraction complete")
    except Exception as e:
        print(f"[ERROR] Extraction failed: {e}")
        print_status("install_failed", "extract_error", v)
        return False

    dest_msys = MSYS2_PATH
    if not dest_msys:
        print("[ERROR] MSYS2 not found. Install MSYS2 at C:\\msys64 first.")
        print_status("install_failed", "msys2_missing", v)
        return False

    print(f"[2/3] Copying files to {dest_msys}...")
    try:
        extracted = extract_dir / "verilator"
        if not extracted.exists():
            subdirs = [d for d in extract_dir.iterdir() if d.is_dir()]
            extracted = subdirs[0] if subdirs else extract_dir

        for sub in ["bin", "share", "include"]:
            src = extracted / sub
            if src.exists():
                shutil.copytree(str(src), str(dest_msys / sub), dirs_exist_ok=True)

        pkgconfig = extracted / "share" / "pkgconfig"
        if pkgconfig.exists():
            shutil.copytree(str(pkgconfig), str(dest_msys / "pkgconfig"), dirs_exist_ok=True)

        shutil.rmtree(extract_dir, ignore_errors=True)
        print("[2/3] Files copied successfully")
    except Exception as e:
        print(f"[ERROR] Copy failed: {e}")
        print_status("install_failed", "copy_error", v)
        return False

    print("[3/3] Verifying installation...")
    time.sleep(2)
    exe, installed_ver = find_verilator(None)
    if exe:
        print(f"[OK] Verilator {installed_ver or v} is ready")
        return True
    else:
        print("[WARNING] Files copied but could not verify version")
        return True


def install_verilator(v, upgrade=False):
    print(f"[INFO] {'Upgrading' if upgrade else 'Installing'} Verilator {v}...")

    if v != "latest" and v in VERILATOR_VERSIONS:
        fname = VERILATOR_VERSIONS[v]
        archive = DOWNLOAD_DIR / fname
        if archive.exists():
            print(f"[INFO] Using local archive: {fname}")
            if _install_verilator_from_7z(archive, v):
                exe, installed_ver = find_verilator(None)
                print_status("installed", installed_ver or v, v)
            return
        else:
            print(f"[INFO] Archive not found: {archive}")
            print(f"[INFO] To install Verilator {v}:")
            print(f"[INFO]   1. Get '{fname}' from FOSSEE/senior")
            print(f"[INFO]   2. Place it in: {DOWNLOAD_DIR}")
            print(f"[INFO] Falling back to latest via MSYS2...")

    bash_exe = get_msys2_bash()
    if not bash_exe:
        print(f"[ERROR] MSYS2 not found at {MSYS2_PATH}")
        print_status("install_failed", "msys2_missing", v)
        return

    try:
        print("[MSYS2] Step 1/3: Updating package database...")
        run_msys2_command("pacman -Syu --noconfirm 2>&1 || true")

        if upgrade:
            print("[MSYS2] Step 2/3: Removing existing Verilator...")
            run_msys2_command("pacman -R --noconfirm mingw-w64-x86_64-verilator 2>/dev/null || true")
        else:
            print("[MSYS2] Step 2/3: Preparing...")

        print("[MSYS2] Step 3/3: Installing Verilator (may take a few minutes)...")
        result = run_msys2_command("pacman -S --noconfirm mingw-w64-x86_64-verilator")

        if result and result.returncode == 0:
            print("[MSYS2] Waiting for installation to settle...")
            time.sleep(5)
            exe, installed_version = find_verilator(None)
            if not exe:
                time.sleep(3)
                exe, installed_version = find_verilator(None)
            if exe:
                if v == "latest":
                    print_status("installed", installed_version or "unknown", "latest")
                elif installed_version and v in installed_version:
                    print_status("installed", installed_version, v)
                else:
                    print_status("installed", installed_version or "unknown", v)
            else:
                print_status("install_failed", "not_found_after_install", v)
        else:
            error_msg = "msys2_install_failed"
            if result and result.stderr:
                error_msg = result.stderr[:100].replace('\n', ' ').replace('|', '_')
            print_status("install_failed", error_msg, v)

    except Exception as e:
        print_status("install_failed", str(e)[:50], v)

def read_state():
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {"important_packages": []}

def write_state(data):
    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def update_state(package_name, version):
    from datetime import datetime
    data = read_state()
    for pkg in data["important_packages"]:
        if pkg["package_name"] == package_name:
            pkg["version"] = version
            pkg["installed_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            write_state(data)
            return
    data["important_packages"].append({
        "package_name": package_name,
        "version": version,
        "installed_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })
    write_state(data)

def get_state_version(package_name):
    data = read_state()
    for pkg in data["important_packages"]:
        if pkg["package_name"] == package_name:
            return pkg.get("version")
    return None


ESIM_DIR = DEFAULT_ESIM_DIR


def check_esim(target_version):
    indicators = [
        BASE_DIR / "eSim.bat",
        BASE_DIR / "src" / "frontEnd" / "Application.py",
        ESIM_DIR / "eSim.bat",
        ESIM_DIR / "uninst-eSim.exe",
        ESIM_DIR / "src" / "frontEnd" / "Application.py",
    ]
    for p in indicators:
        if p.exists():
            ver = get_state_version("esim") or "unknown"
            tv  = target_version if target_version != "none" else "latest"
            if tv in ("latest", "none") or tv == ver:
                print_status("installed", ver, tv)
            else:
                print_status("wrong_version", ver, tv)
            return
    tv = target_version if target_version != "none" else "latest"
    print_status("not_installed", "none", tv)


def install_esim(target_version, upgrade=False):
    ver_key     = target_version if target_version in ESIM_VERSIONS else "latest"
    url         = ESIM_VERSIONS[ver_key]
    display_ver = target_version if target_version != "latest" else "2.4"
    fname       = f"eSim-{display_ver}_installer.exe"

    print(f"[INFO] Installing eSim {display_ver}...")
    print("[INFO] Large file (~400MB) - may take several minutes to download.")

    installer = _get_package(fname, url, label=f"eSim {display_ver} installer")
    if not installer:
        for pattern in ["eSim*installer*.exe", "eSim*.exe", "esim*.exe"]:
            matches = list(DOWNLOAD_DIR.glob(pattern))
            if matches:
                installer = matches[0]
                break
    if not installer:
        print(f"[ERROR] eSim installer not found. Place it in {DOWNLOAD_DIR}")
        print_status("install_failed", "installer_not_found", target_version)
        return

    print(f"[INFO] Running installer: {installer.name}")
    print("[INFO] Silent install in progress (10-20 min). Please wait...")
    try:
        subprocess.run([str(installer), "/S"], timeout=1800)
        time.sleep(20)
        for p in [BASE_DIR / "eSim.bat", BASE_DIR / "src" / "frontEnd" / "Application.py", ESIM_DIR / "eSim.bat", ESIM_DIR / "uninst-eSim.exe"]:
            if p.exists():
                update_state("esim", display_ver)
                print(f"[OK] eSim {display_ver} installed")
                print_status("installed", display_ver, target_version)
                return
        print("[ERROR] eSim installed but could not verify")
        print_status("install_failed", "verification_failed", target_version)
    except subprocess.TimeoutExpired:
        print_status("install_failed", "timeout", target_version)
    except Exception as e:
        print(f"[ERROR] {e}")
        print_status("install_failed", str(e)[:50], target_version)


def uninstall_esim(target_version="none"):
    uninst = ESIM_DIR / "uninst-eSim.exe"
    if uninst.exists():
        print("[1/2] Running eSim uninstaller...")
        try:
            subprocess.run([str(uninst), "/S"], timeout=600)
            time.sleep(10)
        except Exception as e:
            print(f"[WARNING] {e}")
    else:
        print("[WARNING] Uninstaller not found - removing folder...")
        ps = (r'@("C:\FOSSEE\eSim") | ' +
              r'ForEach-Object { if (Test-Path $_) { Remove-Item $_ -Recurse -Force -EA SilentlyContinue } }')
        run_cmd_stream(["powershell", "-Command", ps], timeout=120)
    print("[2/2] Verifying removal...")
    if not (ESIM_DIR / "eSim.bat").exists():
        print("[OK] eSim uninstalled")
        print_status("not_installed", "none", "none")
    else:
        print_status("uninstall_failed", "still_found", "none")



def uninstall_kicad(target_version="none"):
    print("[1/3] Stopping KiCad processes...")
    run_cmd_stream(["powershell", "-Command",
        "Get-Process -Name '*kicad*' -EA SilentlyContinue | Stop-Process -Force -EA SilentlyContinue"
    ], timeout=30)
    print("[2/3] Uninstalling via Chocolatey...")
    choco = which("choco") or which("choco.exe")
    if choco:
        run_cmd_stream([choco, "uninstall", "kicad", "-y", "--force-dependencies", "--no-progress"], timeout=300)
    print("[3/3] Removing leftover files...")
    ps = (r'@("C:\Program Files\KiCad","C:\Program Files (x86)\KiCad") | ' +
          r'ForEach-Object { if (Test-Path $_) { Remove-Item $_ -Recurse -Force -EA SilentlyContinue; Write-Host "Removed: $_" } }')
    run_cmd_stream(["powershell", "-Command", ps], timeout=120)
    exe, _ = find_kicad_fixed(None)
    if not exe:
        print("[OK] KiCad uninstalled")
        print_status("not_installed", "none", "none")
    else:
        print_status("uninstall_failed", "still_found", "none")


def uninstall_ngspice(target_version="none"):
    print("[1/2] Uninstalling ngspice...")
    choco = which("choco") or which("choco.exe")
    if choco:
        run_cmd_stream([choco, "uninstall", "ngspice", "-y", "--force-dependencies", "--no-progress"], timeout=180)
    else:
        ps = (r'@("C:\Program Files\ngspice","C:\Program Files (x86)\ngspice") | ' +
              r'ForEach-Object { if (Test-Path $_) { Remove-Item $_ -Recurse -Force -EA SilentlyContinue } }')
        run_cmd_stream(["powershell", "-Command", ps], timeout=60)
    print("[2/2] Verifying removal...")
    if not _find_ngspice_exe():
        print("[OK] Ngspice uninstalled")
        print_status("not_installed", "none", "none")
    else:
        print_status("uninstall_failed", "still_found", "none")


def uninstall_llvm(target_version="none"):
    print("[1/2] Uninstalling LLVM...")
    choco = which("choco") or which("choco.exe")
    if choco:
        run_cmd_stream([choco, "uninstall", "llvm", "-y", "--no-progress"], timeout=180)
    else:
        ps = (r'@("C:\Program Files\LLVM","C:\Program Files (x86)\LLVM") | ' +
              r'ForEach-Object { if (Test-Path $_) { Remove-Item $_ -Recurse -Force -EA SilentlyContinue } }')
        run_cmd_stream(["powershell", "-Command", ps], timeout=60)
    print("[2/2] Verifying removal...")
    exe, _ = find_llvm_fixed(None)
    if not exe:
        print("[OK] LLVM uninstalled")
        print_status("not_installed", "none", "none")
    else:
        print_status("uninstall_failed", "still_found", "none")


def uninstall_ghdl(target_version="none"):
    print("[1/2] Removing GHDL files...")
    for p in [BASE_DIR / "bin" / "ghdl.exe",
              MSYS2_PATH / "mingw64" / "bin" / "ghdl.exe",
              Path(r"C:\FOSSEE\MSYS\mingw64\bin\ghdl.exe")]:
        if p.exists():
            p.unlink()
            print(f"[OK] Removed: {p}")
    ghdl_dir = BASE_DIR / "ghdl"
    if ghdl_dir.exists():
        shutil.rmtree(ghdl_dir, ignore_errors=True)
    print("[2/2] Verifying removal...")
    exe, _ = find_ghdl(None)
    if not exe:
        print("[OK] GHDL uninstalled")
        print_status("not_installed", "none", "none")
    else:
        print_status("uninstall_failed", "still_found", "none")


def uninstall_verilator(target_version="none"):
    print("[1/2] Removing Verilator...")
    bash_exe = MSYS2_PATH / "usr" / "bin" / "bash.exe"
    if bash_exe.exists():
        run_cmd_stream([str(bash_exe), "-lc",
                        "pacman -R --noconfirm mingw-w64-x86_64-verilator 2>&1 || true"],
                       timeout=120)
    for msys_bin in [MSYS2_PATH / "mingw64" / "bin",
                     Path(r"C:\FOSSEE\MSYS\mingw64\bin")]:
        for name in ["verilator.exe", "verilator_bin.exe"]:
            p = msys_bin / name
            if p.exists():
                p.unlink()
                print(f"[OK] Removed: {p}")
    print("[2/2] Verifying removal...")
    exe, _ = find_verilator(None)
    if not exe:
        print("[OK] Verilator uninstalled")
        print_status("not_installed", "none", "none")
    else:
        print_status("uninstall_failed", "still_found", "none")


TOOLS = {
    "chocolatey": (check_chocolatey, install_chocolatey, None),
    "esim":       (check_esim,       install_esim,       uninstall_esim),
    "kicad":      (check_kicad,      install_kicad,      uninstall_kicad),
    "ngspice":    (check_ngspice,    install_ngspice,    uninstall_ngspice),
    "llvm":       (check_llvm,       install_llvm,       uninstall_llvm),
    "verilator":  (check_verilator_tool, install_verilator, uninstall_verilator),
    "ghdl":       (check_ghdl_tool,  install_ghdl,       uninstall_ghdl),
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="COMPLETE Tool Manager - All Tools in One",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
IMPROVED VERSION - Better Version Support and Updates:

Available tools and versions:
  chocolatey: latest
  kicad: 6, 7, 8, 9, latest (Note: KiCad 6 may use direct download if Chocolatey fails)
  ngspice: 35, 36, 37, 38, 39, 40, 41, 42, latest
  llvm: 13, 14, 15, 16, 17, 18, 19, latest
  python-pyqt5: 5.15.9, 5.15.10, 6.5.0, 6.6.0, latest
  ghdl: 4.0.0, 5.1.1, latest
  verilator: latest (via MSYS2)

Examples:
  # Check current installation
  python tool_manager_windows.py check kicad none
  
  # Install specific version
  python tool_manager_windows.py install ngspice 38
  python tool_manager_windows.py install llvm 17
  python tool_manager_windows.py install kicad 6
  
  # Update to specific version (from any version)
  python tool_manager_windows.py update ngspice 40  
  python tool_manager_windows.py update llvm 19     
  python tool_manager_windows.py update kicad 7    
  
  # Update to latest
  python tool_manager_windows.py update kicad latest

Note: If KiCad 6 installation via Chocolatey fails, the script will automatically
      attempt a direct download from KiCad's official releases.
        """
    )
    
    parser.add_argument("cmd", choices=["check", "install", "update", "uninstall"])
    parser.add_argument("tool")
    parser.add_argument("version")
    
    args = parser.parse_args()
    
    if args.tool not in TOOLS:
        print("not_supported|none|none")
        sys.exit(0)
    
    check_fn, install_fn, uninstall_fn = TOOLS[args.tool]

    if args.cmd == "check":
        check_fn(args.version)
    elif args.cmd == "install":
        install_fn(args.version, upgrade=False)
    elif args.cmd == "update":
        install_fn(args.version, upgrade=True)
    elif args.cmd == "uninstall":
        if uninstall_fn:
            uninstall_fn(args.version)
        else:
            print_status("not_supported", "none", "none")