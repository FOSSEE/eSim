"""
LLVM / Clang — check, install, uninstall (via Chocolatey on Windows).
"""

import os
import re
import time

from pm_platform import IS_LINUX
from registry import LLVM_VERSIONS


def check(version: str, backend) -> None:
    """Check if LLVM/Clang is installed."""
    if version == "none":
        exe, found_ver = backend.find_executable_with_version("llvm", None)
        if exe:
            backend.print_status(
                "installed", found_ver or "unknown", "latest")
        else:
            backend.print_status("not_installed", "none", "latest")
        return

    exe, found_ver = backend.find_executable_with_version("llvm", version)

    if exe and found_ver:
        if version == "latest" or found_ver == version:
            backend.print_status("installed", found_ver, version)
        else:
            backend.print_status("wrong_version", found_ver, version)
    else:
        backend.print_status("not_installed", "none", version)


def install(version: str, upgrade: bool, backend) -> None:
    """Install LLVM via Chocolatey."""
    if IS_LINUX:
        ok = backend.install_package("llvm", version)
        backend.print_status(
            "installed" if ok else "install_failed",
            version if ok else "package_manager_failed",
            version)
        return

    choco_exe = backend.find_executable("chocolatey", "none")
    if not choco_exe:
        backend.print_status("install_failed", "choco_missing", version)
        return

    exact_version = LLVM_VERSIONS.get(version, version)

    print("[1/3] Removing existing LLVM...")
    backend.run_stream(
        ["choco", "uninstall", "llvm", "-y", "--no-progress"],
        timeout=180)

    print(f"[2/3] Installing LLVM {version} ({exact_version}) "
          f"via Chocolatey...")

    if version == "latest":
        cmd = ["choco", "install", "llvm", "-y", "--no-progress"]
    else:
        cmd = ["choco", "install", "llvm", "--version", exact_version,
               "-y", "--no-progress", "--allow-downgrade", "--force"]

    rc, out = backend.run_stream(cmd, timeout=300)

    if rc == 0:
        print("[3/3] Verifying LLVM installation...")
        time.sleep(3)

        common_paths = [
            r"C:\Program Files\LLVM\bin\clang.exe",
            r"C:\Program Files (x86)\LLVM\bin\clang.exe",
        ]
        for path in common_paths:
            if os.path.exists(path):
                result = backend.run_cmd([path, "--version"], timeout=10)
                if result and result.returncode == 0:
                    m = re.search(r'clang version (\d+)\.', result.stdout)
                    if m:
                        found_ver = m.group(1)
                        print(f"[SUCCESS] LLVM {found_ver} installed at "
                              f"{path}")
                        backend.print_status(
                            "installed", found_ver, version)
                        return
                print(f"[SUCCESS] LLVM installed at {path}")
                backend.print_status(
                    "installed", exact_version or version, version)
                return

        print("[ERROR] LLVM verification failed - exe not found after "
              "install")
        backend.print_status(
            "install_failed", "verification_failed", version)
    else:
        backend.print_status(
            "install_failed",
            (out[-50:].replace('\n', ' ').replace('|', '_')
             if out else "choco_error"),
            version)


def uninstall(version: str, backend) -> None:
    """Uninstall LLVM via Chocolatey."""
    if IS_LINUX:
        ok = backend.uninstall_package("llvm", version)
        backend.print_status(
            "not_installed" if ok else "uninstall_failed",
            "none" if ok else "still_found",
            "none")
        return

    print("[1/2] Uninstalling LLVM...")
    choco = backend.which("choco") or backend.which("choco.exe")
    if choco:
        backend.run_stream(
            [choco, "uninstall", "llvm", "-y", "--no-progress"],
            timeout=180)
    else:
        ps = (r'@("C:\Program Files\LLVM",'
              r'"C:\Program Files (x86)\LLVM") | '
              r'ForEach-Object { if (Test-Path $_) { '
              r'Remove-Item $_ -Recurse -Force -EA SilentlyContinue } }')
        backend.run_cmd(["powershell", "-Command", ps], timeout=60)

    print("[2/2] Verifying removal...")
    exe = backend.find_executable("llvm", "none")
    if not exe:
        print("[OK] LLVM uninstalled")
        backend.print_status("not_installed", "none", "none")
    else:
        backend.print_status("uninstall_failed", "still_found", "none")
