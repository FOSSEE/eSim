#!/usr/bin/env python3
"""
tool_manager_linux.py — Linux backend for eSim Tool Manager.

Exit codes for install / update / uninstall
-------------------------------------------
0  success                         (status line: installed|... or not_installed|...)
1  attempted, but failed           (install_failed|...  or uninstall_failed|...)
3  not supported on this system    (not_supported|...)

``check`` keeps its own convention: 0 = installed, 1 = not installed.
(2 is left to argparse, which uses it for command-line errors.)
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

EXIT_OK          = 0
EXIT_FAILED      = 1
EXIT_UNSUPPORTED = 3

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
def _find_installed(tool: str):
    """Return where *tool* is installed (a binary path or "dpkg"), or None."""
    binaries = _BINARY_CHECK.get(tool, [tool])
    for binary in binaries:
        path = _which_native(binary)
        if path:
            return path

    # Fallback: dpkg status check on apt distros
    if detect_package_manager() == "apt":
        try:
            r = subprocess.run(
                ["dpkg", "-s", tool],
                capture_output=True, text=True
            )
        except OSError:
            return None
        if r.returncode == 0 and "Status: install ok installed" in r.stdout:
            return "dpkg"
    return None


def check_tool(tool: str, version: str) -> int:
    """Check if a tool binary exists in PATH. Returns 0 if found, 1 if not."""
    where = _find_installed(tool)
    if where:
        print(f"installed|{tool}|{where}", flush=True)
        return 0
    print(f"not_installed|{tool}|none", flush=True)
    return 1


def _unsupported(tool: str, pm, reason: str) -> int:
    print(f"[INFO] {reason}", flush=True)
    print(f"not_supported|{tool}|{pm or 'none'}", flush=True)
    return EXIT_UNSUPPORTED


# ── install ───────────────────────────────────────────────────────────────────
def install_tool(tool: str, version: str, upgrade: bool = False) -> int:
    pm = detect_package_manager()
    if not pm:
        print("[ERROR] No supported package manager found.", flush=True)
        print(f"not_supported|{tool}|none", flush=True)
        return EXIT_UNSUPPORTED

    # Ubuntu/Debian + esim → delegate to the maintained shell script
    if pm == "apt" and tool == "esim":
        if not INSTALL_SH.exists():
            print(f"[ERROR] install-eSim.sh not found at {INSTALL_SH}", flush=True)
            print("install_failed|esim|script_missing", flush=True)
            return EXIT_FAILED
        flag = "--upgrade" if upgrade else "--install"
        rc = _stream(["bash", str(INSTALL_SH), flag])
        if rc != 0:
            print(f"install_failed|esim|exit_{rc}", flush=True)
            return EXIT_FAILED
        return EXIT_OK

    if tool == "esim":
        print(f"[INFO] eSim has no native package for {pm}.", flush=True)
        return _unsupported(tool, pm, "Please visit https://esim.fossee.in "
                                      "for installation options.")

    packages = PACKAGE_MAP.get(pm, {}).get(tool)
    if packages is None:
        return _unsupported(tool, pm, f"'{tool}' is not supported with {pm}.")
    if not packages:
        return _unsupported(tool, pm, f"'{tool}' has no individual package on {pm}.")

    cmd_base = INSTALL_CMD.get(pm)
    if not cmd_base:
        print(f"[ERROR] No install command defined for '{pm}'.", flush=True)
        print(f"install_failed|{tool}|no_command", flush=True)
        return EXIT_FAILED

    action = "Upgrading" if upgrade else "Installing"
    print(f"[Linux/{pm}] {action} {tool}: {' '.join(packages)} ...", flush=True)
    with _apt_lock(pm):
        rc = _run_elevated(cmd_base + packages)

    if rc != 0:
        print(f"install_failed|{tool}|exit_{rc}", flush=True)
        return EXIT_FAILED
    where = _find_installed(tool)
    if not where:
        print(f"install_failed|{tool}|not_found", flush=True)
        return EXIT_FAILED
    print(f"installed|{tool}|{where}", flush=True)
    return EXIT_OK


# ── uninstall ─────────────────────────────────────────────────────────────────
def uninstall_tool(tool: str, version: str) -> int:
    pm = detect_package_manager()
    if not pm:
        print("[ERROR] No supported package manager found.", flush=True)
        print(f"not_supported|{tool}|none", flush=True)
        return EXIT_UNSUPPORTED

    if pm == "apt" and tool == "esim":
        if not INSTALL_SH.exists():
            print(f"[ERROR] install-eSim.sh not found at {INSTALL_SH}", flush=True)
            print("uninstall_failed|esim|script_missing", flush=True)
            return EXIT_FAILED
        rc = _stream(["bash", str(INSTALL_SH), "--uninstall"])
        if rc != 0:
            print(f"uninstall_failed|esim|exit_{rc}", flush=True)
            return EXIT_FAILED
        return EXIT_OK

    packages = PACKAGE_MAP.get(pm, {}).get(tool)
    if not packages:
        # Nothing this backend could have installed. That is only a success
        # if the tool really is absent; otherwise we cannot remove it.
        where = _find_installed(tool)
        if not where:
            print(f"[INFO] '{tool}' is not installed.", flush=True)
            print(f"not_installed|{tool}|none", flush=True)
            return EXIT_OK
        return _unsupported(tool, pm,
                            f"'{tool}' ({where}) was not installed by {pm}; "
                            "remove it manually.")

    cmd_base = UNINSTALL_CMD.get(pm)
    if not cmd_base:
        print(f"[ERROR] No uninstall command defined for '{pm}'.", flush=True)
        print(f"uninstall_failed|{tool}|no_command", flush=True)
        return EXIT_FAILED

    print(f"[Linux/{pm}] Uninstalling {tool}: {' '.join(packages)} ...", flush=True)
    with _apt_lock(pm):
        rc = _run_elevated(cmd_base + packages)

    if rc != 0:
        print(f"uninstall_failed|{tool}|exit_{rc}", flush=True)
        return EXIT_FAILED
    if _find_installed(tool):
        print(f"uninstall_failed|{tool}|still_found", flush=True)
        return EXIT_FAILED
    print(f"not_installed|{tool}|none", flush=True)
    return EXIT_OK

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