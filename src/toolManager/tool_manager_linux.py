#!/usr/bin/env python3
"""
tool_manager_linux.py — Linux backend for eSim Tool Manager.
"""

import sys
import os
import shutil
import subprocess
import argparse
import contextlib
from pathlib import Path

_local = str(Path(__file__).resolve().parent)
if _local not in sys.path:
    sys.path.insert(0, _local)

from platform_utils import detect_package_manager

BASE_DIR   = Path(__file__).resolve().parent
INSTALL_SH = BASE_DIR / "install-eSim.sh"

# ── Package names per package manager ────────────────────────────────────────
PACKAGE_MAP = {
    "apt": {
        "kicad":     ["kicad", "kicad-footprints", "kicad-libraries",
                      "kicad-symbols", "kicad-templates"],
        "ngspice":   ["ngspice"],
        "ghdl":      ["ghdl"],
        "verilator": ["verilator"],
        "llvm":      ["clang", "llvm"],
        "esim":      [],    
    },
    "dnf": {
        "kicad":     ["kicad"],
        "ngspice":   ["ngspice"],
        "ghdl":      ["ghdl"],
        "verilator": ["verilator"],
        "llvm":      ["clang", "llvm-devel"],
        "esim":      [],
    },
    "yum": {
        "kicad":     ["kicad"],
        "ngspice":   ["ngspice"],
        "ghdl":      [],    # not in yum repos
        "verilator": [],    # not in yum repos
        "llvm":      ["clang"],
        "esim":      [],
    },
    "pacman": {
        "kicad":     ["kicad", "kicad-library", "kicad-library-3d"],
        "ngspice":   ["ngspice"],
        "ghdl":      ["ghdl"],
        "verilator": ["verilator"],
        "llvm":      ["clang", "llvm"],
        "esim":      [],
    },
    "zypper": {
        "kicad":     ["kicad"],
        "ngspice":   ["ngspice"],
        "ghdl":      ["ghdl"],
        "verilator": ["verilator"],
        "llvm":      ["clang", "llvm-devel"],
        "esim":      [],
    },
}

INSTALL_CMD = {
    "apt":    ["apt-get", "install", "-y"],
    "dnf":    ["dnf",     "install", "-y"],
    "yum":    ["yum",     "install", "-y"],
    "pacman": ["pacman",  "-S", "--noconfirm"],
    "zypper": ["zypper",  "install", "--non-interactive"],
}

UNINSTALL_CMD = {
    "apt":    ["apt-get", "remove", "-y", "--autoremove"],
    "dnf":    ["dnf",     "remove", "-y"],
    "yum":    ["yum",     "remove", "-y"],
    "pacman": ["pacman",  "-Rs", "--noconfirm"],
    "zypper": ["zypper",  "remove", "--non-interactive", "--clean-deps"],
}


_BINARY_CHECK = {
    "kicad":     ["kicad"],
    "ngspice":   ["ngspice"],
    "ghdl":      ["ghdl"],
    "verilator": ["verilator"],
    "llvm":      ["clang", "clang++", "llvm-config"],
    "esim":      ["esim"],
}

# ── WSL detection ─────────────────────────────────────────────────────────────
def _detect_wsl() -> bool:
    """Return True when running inside Windows Subsystem for Linux."""
    if os.environ.get("WSL_DISTRO_NAME"):
        return True
    try:
        with open("/proc/version") as _f:
            if "microsoft" in _f.read().lower():
                return True
    except OSError:
        pass
    return False
 
 
_IS_WSL: bool = _detect_wsl()
 
def _pkexec_usable() -> bool:
    """
    pkexec requires:
      1. A running polkit daemon — absent in WSL (no D-Bus system bus).
      2. A graphical session so the polkit agent can show its dialog.
    """
    if _IS_WSL:
        return False
    
    if not (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")):
        return False
    return True


# ────────────────────────────────────────────────────────
def _run_elevated(args: list) -> int:
    pkexec = shutil.which("pkexec")
    if pkexec and _pkexec_usable():
        print("[INFO] Using pkexec for elevation.", flush=True)
        return _stream([pkexec] + args)

    sudo = shutil.which("sudo")
    if sudo:
        print("[INFO] Using sudo -S for elevation (password via stdin).", flush=True)
        return _stream([sudo, "-S"] + args)

    print("[WARN] Neither pkexec nor sudo found — attempting without elevation.", flush=True)
    return _stream(args)


def _stream(args: list) -> int:
    """Run a command and stream its stdout line by line to our stdout."""
    try:
        proc = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="ignore",
        )
        for line in proc.stdout:
            line = line.rstrip()
            if line:
                print(line, flush=True)
        proc.wait()
        return proc.returncode
    except FileNotFoundError:
        print(f"[ERROR] Command not found: {args[0]}", flush=True)
        return 1

def _which_native(binary: str):
    if not _IS_WSL:
        return shutil.which(binary)

    path_env = os.environ.get("PATH", "")
    for directory in path_env.split(os.pathsep):
        if directory.startswith("/mnt/"):
            continue
        candidate = Path(directory) / binary
        try:
            if candidate.is_file() and os.access(str(candidate), os.X_OK):
                return str(candidate)
        except OSError:
            continue
    return None


# ── apt serialisation lock ─────────────────────────────────────────────────────
_APT_LOCK_FILE = "/tmp/esim-apt-serial.lock"

@contextlib.contextmanager
def _apt_lock(pm: str = "apt"): 
    if pm != "apt":
        yield
        return

    import fcntl as _fcntl

    with open(_APT_LOCK_FILE, "w") as _lf:
        print("[INFO] Waiting for apt serial lock ...", flush=True)
        _fcntl.flock(_lf, _fcntl.LOCK_EX)
        try:
            yield
        finally:
            _fcntl.flock(_lf, _fcntl.LOCK_UN)


# ── check ─────────────────────────────────────────────────────────────────────
def check_tool(tool: str, version: str) -> int:
    """Check if a tool binary exists in PATH. Returns 0 if found, 1 if not."""
    binaries = _BINARY_CHECK.get(tool, [tool])
    for binary in binaries:
        path = _which_native(binary)
        if path:
            print(f"installed|{tool}|{path}", flush=True)
            return 0

    # Fallback: dpkg status check on apt distros
    pm = detect_package_manager()
    if pm == "apt":
        r = subprocess.run(
            ["dpkg", "-s", tool],
            capture_output=True, text=True
        )
        if r.returncode == 0 and "Status: install ok installed" in r.stdout:
            print(f"installed|{tool}|dpkg", flush=True)
            return 0

    print(f"not_installed|{tool}|none", flush=True)
    return 1


# ── install ───────────────────────────────────────────────────────────────────
def install_tool(tool: str, version: str, upgrade: bool = False) -> int:
    pm = detect_package_manager()
    if not pm:
        print("[ERROR] No supported package manager found.", flush=True)
        return 1

    # Ubuntu/Debian + esim → delegate to the maintained shell script
    if pm == "apt" and tool == "esim":
        if INSTALL_SH.exists():
            flag = "--upgrade" if upgrade else "--install"
            return _stream(["bash", str(INSTALL_SH), flag])
        else:
            print(f"[ERROR] install-eSim.sh not found at {INSTALL_SH}", flush=True)
            return 1

    if tool == "esim":
        print("[INFO] eSim has no native package for this distro.", flush=True)
        print("[INFO] Please visit https://esim.fossee.in for installation options.", flush=True)
        return 0

    packages = PACKAGE_MAP.get(pm, {}).get(tool)
    if packages is None:
        print(f"not_supported|{tool}|{pm}", flush=True)
        return 0
    if not packages:
        print(f"[INFO] '{tool}' has no individual package on {pm}.", flush=True)
        return 0

    cmd_base = INSTALL_CMD.get(pm)
    if not cmd_base:
        print(f"[ERROR] No install command defined for '{pm}'.", flush=True)
        return 1

    action = "Upgrading" if upgrade else "Installing"
    print(f"[Linux/{pm}] {action} {tool}: {' '.join(packages)} ...", flush=True)
    with _apt_lock(pm):
        rc = _run_elevated(cmd_base + packages)

    if check_tool(tool, version) != 0:
        print(f"install_failed|{tool}|none", flush=True)
    return rc


# ── uninstall ─────────────────────────────────────────────────────────────────
def uninstall_tool(tool: str, version: str) -> int:
    pm = detect_package_manager()
    if not pm:
        print("[ERROR] No supported package manager found.", flush=True)
        return 1


    if pm == "apt" and tool == "esim" and INSTALL_SH.exists():
        return _stream(["bash", str(INSTALL_SH), "--uninstall"])

    packages = PACKAGE_MAP.get(pm, {}).get(tool, [])
    if not packages:
        print(f"[INFO] Nothing to uninstall for '{tool}' on {pm}.", flush=True)
        print(f"not_installed|{tool}|none", flush=True)
        return 0

    cmd_base = UNINSTALL_CMD.get(pm, [])
    print(f"[Linux/{pm}] Uninstalling {tool}: {' '.join(packages)} ...", flush=True)
    with _apt_lock(pm):
        rc = _run_elevated(cmd_base + packages)
        
    if check_tool(tool, version) == 0:
        print(f"uninstall_failed|{tool}|none", flush=True)
    return rc

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="eSim Tool Manager — Linux Backend")
    parser.add_argument("cmd", choices=["check", "install", "update", "uninstall"])
    parser.add_argument("tool")
    parser.add_argument("version")
    args = parser.parse_args()

    if args.cmd == "check":
        sys.exit(check_tool(args.tool, args.version))
    elif args.cmd == "install":
        sys.exit(install_tool(args.tool, args.version, upgrade=False))
    elif args.cmd == "update":
        sys.exit(install_tool(args.tool, args.version, upgrade=True))
    elif args.cmd == "uninstall":
        sys.exit(uninstall_tool(args.tool, args.version))