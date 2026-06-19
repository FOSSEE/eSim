"""
Ngspice — check, install, uninstall (via Chocolatey on Windows).
"""

import time

from pm_platform import IS_LINUX
from registry import NGSPICE_VERSIONS, SCRIPT_MAPPING


def check(version: str, backend) -> None:
    """Check if Ngspice is installed."""
    exe, found_ver = backend.find_executable_with_version("ngspice", version)

    if version == "none":
        backend.print_status(
            "installed" if exe else "not_installed",
            found_ver or "none", "latest")
        return

    if exe:
        if version == "latest":
            backend.print_status("installed", found_ver or "unknown", version)
        elif found_ver == "unknown":
            backend.print_status("installed", "unknown", version)
        elif found_ver == version or (
                found_ver and found_ver.startswith(str(version))):
            backend.print_status("installed", found_ver, version)
        else:
            backend.print_status(
                "wrong_version", found_ver or "unknown", version)
    else:
        backend.print_status("not_installed", "none", version)


def install(version: str, upgrade: bool, backend) -> None:
    """Install Ngspice via Chocolatey."""
    if IS_LINUX:
        script = SCRIPT_MAPPING.get("Ngspice")
        if script:
            ok = backend.run_bash_script(script, version)
            backend.print_status(
                "installed" if ok else "install_failed",
                version if ok else "script_failed",
                version)
        else:
            ok = backend.install_package("ngspice", version)
            backend.print_status(
                "installed" if ok else "install_failed",
                version if ok else "package_manager_failed",
                version)
        return

    choco_exe = backend.find_executable("chocolatey", "none")
    if not choco_exe:
        backend.print_status("install_failed", "choco_missing", version)
        return

    exact_version = NGSPICE_VERSIONS.get(version, version)

    print("Uninstalling existing ngspice...")
    backend.run_cmd(
        ["choco", "uninstall", "ngspice", "-y",
         "--force-dependencies", "--no-progress"],
        timeout=180)

    print(f"[1/3] Removing existing ngspice...")
    print(f"[2/3] Installing ngspice {version} via Chocolatey...")

    if version == "latest":
        cmd = ["choco", "install", "ngspice", "-y", "--no-progress"]
    else:
        cmd = ["choco", "install", "ngspice", "--version", exact_version,
               "-y", "--no-progress", "--allow-downgrade", "--force"]

    rc, out = backend.run_stream(cmd, timeout=300)

    if rc == 0:
        print("[3/3] Verifying installation...")
        time.sleep(2)
        exe, installed_version = backend.find_executable_with_version(
            "ngspice", "none")
        if exe:
            print(f"[OK] ngspice {installed_version or 'unknown'} "
                  f"installed successfully")
            backend.print_status(
                "installed", installed_version or "unknown", version)
        else:
            backend.print_status("install_failed", "not_found", version)
    else:
        backend.print_status(
            "install_failed",
            (out[-50:].replace('\n', ' ').replace('|', '_')
             if out else "unknown_error"),
            version)


def uninstall(version: str, backend) -> None:
    """Uninstall Ngspice via Chocolatey."""
    if IS_LINUX:
        ok = backend.uninstall_package("ngspice", version)
        backend.print_status(
            "not_installed" if ok else "uninstall_failed",
            "none" if ok else "still_found",
            "none")
        return

    print("[1/2] Uninstalling ngspice...")
    choco = backend.which("choco") or backend.which("choco.exe")
    if choco:
        backend.run_stream(
            [choco, "uninstall", "ngspice", "-y",
             "--force-dependencies", "--no-progress"],
            timeout=180)
    else:
        ps = (r'@("C:\Program Files\ngspice",'
              r'"C:\Program Files (x86)\ngspice") | '
              r'ForEach-Object { if (Test-Path $_) { '
              r'Remove-Item $_ -Recurse -Force -EA SilentlyContinue } }')
        backend.run_cmd(["powershell", "-Command", ps], timeout=60)

    print("[2/2] Verifying removal...")
    exe = backend.find_executable("ngspice", "none")
    if not exe:
        print("[OK] Ngspice uninstalled")
        backend.print_status("not_installed", "none", "none")
    else:
        backend.print_status("uninstall_failed", "still_found", "none")
