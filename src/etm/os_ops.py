import platform, shutil, subprocess
from typing import Tuple, List

def current_os() -> str:
    s = platform.system().lower()
    if s.startswith("linux"):
        return "linux"
    if s.startswith("darwin"):
        return "mac"
    if s.startswith("windows"):
        return "windows"
    return s

def which(cmd: str) -> str:
    return shutil.which(cmd) or ""

def run_cmd(cmd: List[str]) -> Tuple[int, str, str]:
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out, err = p.communicate()
        return p.returncode, out.strip(), err.strip()
    except FileNotFoundError as e:
        return 127, "", str(e)

def pkg_manager() -> str:
    osid = current_os()
    if osid == "linux" and which("apt-get"):
        return "apt"
    if osid == "mac" and which("brew"):
        return "brew"
    if osid == "windows" and which("choco"):
        return "choco"
    return ""

def prefix_sudo(cmd: List[str]) -> List[str]:
    osid = current_os()
    if osid in ("linux","mac"):
        return ["sudo"] + cmd
    return cmd

def suggest_pkgmgr_install() -> str:
    osid = current_os()
    if osid == "linux":
        return "Install apt (Debian/Ubuntu) or use your distro package manager."
    if osid == "mac":
        return "Install Homebrew: /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    if osid == "windows":
        return "Install Chocolatey in an elevated PowerShell: Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
    return "Unsupported OS."
