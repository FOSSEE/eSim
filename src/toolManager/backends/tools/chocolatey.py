"""
Chocolatey package manager itself — check and install.
"""

def check(version: str, backend) -> None:
    """Check if Chocolatey is installed."""
    exe, found_ver = backend.find_executable_with_version("chocolatey", version)

    if version == "none":
        backend.print_status(
            "installed" if exe else "not_installed",
            found_ver or "none", "latest")
        return

    if exe:
        if version == "latest":
            backend.print_status("installed", found_ver, version)
        elif found_ver == version:
            backend.print_status("installed", found_ver, version)
        else:
            backend.print_status("wrong_version", found_ver, version)
    else:
        backend.print_status("not_installed", "none", version)


def install(version: str, upgrade: bool, backend) -> None:
    """Install or upgrade Chocolatey via the official PowerShell script."""
    exe, current_version = backend.find_executable_with_version(
        "chocolatey", version)
    if exe and not upgrade:
        check(version, backend)
        return

    print(f"{'Upgrading' if upgrade else 'Installing'} Chocolatey...")
    cmd = [
        "powershell", "-Command",
        "Set-ExecutionPolicy Bypass -Scope Process -Force; "
        "[System.Net.ServicePointManager]::SecurityProtocol = "
        "[System.Net.ServicePointManager]::SecurityProtocol -bor 3072; "
        "iex ((New-Object System.Net.WebClient).DownloadString("
        "'https://community.chocolatey.org/install.ps1'))"
    ]

    result = backend.run_cmd(cmd, timeout=600)
    if result and result.returncode == 0:
        exe, installed_version = backend.find_executable_with_version(
            "chocolatey", "none")
        if exe:
            backend.print_status(
                "installed", installed_version or "unknown", version)
        else:
            backend.print_status("install_failed", "not_found", version)
    else:
        backend.print_status("install_failed", "choco_error", version)
