"""
KiCad — check, install, uninstall.

Install via Chocolatey with version fallback chain.
Version 6 falls back to direct download from GitHub when Chocolatey's
osdn.net links are broken.
"""

import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

from registry import KICAD_VERSIONS, TOOLS


# ── Internal helpers ─────────────────────────────────────────────────

def _cleanup(backend):
    """Clean up KiCad before (re)install."""
    print("Step 1/3: Chocolatey uninstall...")
    backend.run_cmd(
        ["choco", "uninstall", "kicad", "-y",
         "--force-dependencies", "--remove-dependencies",
         "--no-progress"],
        timeout=180)

    print("Step 2/3: Manual file cleanup...")
    ps_cleanup = r"""
    Get-Process -Name "*kicad*" -ErrorAction SilentlyContinue |
        Stop-Process -Force -ErrorAction SilentlyContinue
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
            Remove-Item -Path $path -Recurse -Force -EA SilentlyContinue
            Start-Sleep -Milliseconds 500
        }
    }
    """
    backend.run_cmd(["powershell", "-Command", ps_cleanup], timeout=180)

    print("Step 3/3: Clearing Chocolatey cache...")
    backend.run_cmd(
        ["choco", "cache", "remove", "--expired", "-y"],
        timeout=60)


def _direct_install(version_str, backend):
    """Install KiCad via direct download (fallback, v6 only)."""
    spec = TOOLS.get("kicad")
    url = spec.get_download_url(version_str) if spec else None
    if not url:
        print(f"[ERROR] No direct download URL for version {version_str}")
        return False

    print(f"[INFO] Downloading KiCad {version_str} from GitHub...")
    print(f"[URL] {url}")

    import tempfile
    import urllib.request
    temp_dir = Path(tempfile.gettempdir())
    installer_path = temp_dir / f"kicad-{version_str}-installer.exe"

    try:
        print("[INFO] Downloading... "
              "(this may take 5-10 minutes, file is ~800MB)")

        def reporthook(blocknum, blocksize, totalsize):
            if totalsize > 0:
                percent = min(
                    blocknum * blocksize * 100 / totalsize, 100)
                if blocknum % 50 == 0:
                    mb_done = min(
                        blocknum * blocksize, totalsize) / (1024 * 1024)
                    mb_total = totalsize / (1024 * 1024)
                    print(f"[DOWNLOAD] {percent:.1f}% "
                          f"({mb_done:.1f} MB / {mb_total:.1f} MB)",
                          flush=True)

        urllib.request.urlretrieve(
            url, installer_path, reporthook=reporthook)
        print(f"\n[OK] Downloaded to: {installer_path}")

        if not installer_path.exists():
            print("[ERROR] Download failed - file not found")
            return False

        file_size_mb = installer_path.stat().st_size / (1024 * 1024)
        print(f"[INFO] Downloaded file size: {file_size_mb:.1f} MB")

        if file_size_mb < 100:
            print("[ERROR] Downloaded file is too small - "
                  "likely corrupted")
            return False

        print("[INFO] Running silent installation...")
        print("[NOTE] This may take 5-10 minutes...")

        import subprocess
        subprocess.run(
            [str(installer_path), "/S", "/NCRC"], timeout=900)

        print("[INFO] Waiting for installation to complete...")
        time.sleep(10)

        exe, installed_version = \
            backend.find_executable_with_version("kicad", "none")
        if exe:
            print(f"[SUCCESS] KiCad {installed_version} "
                  f"installed successfully!")
            backend.print_status(
                "installed", installed_version or version_str, "6")
            return True

        for path in [r"C:\Program Files\KiCad\6.0\bin\kicad.exe"]:
            if os.path.exists(path):
                print(f"[SUCCESS] KiCad installed at: {path}")
                backend.print_status("installed", version_str, "6")
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
            except Exception:
                pass



# ── Tool functions ───────────────────────────────────────────────────

def check(version: str, backend) -> None:
    """Check if KiCad is installed."""
    exe, found_ver = backend.find_executable_with_version("kicad", None)

    if version == "none":
        backend.print_status(
            "installed" if exe else "not_installed",
            found_ver or "none", "latest")
        return

    if exe:
        if version == "latest":
            backend.print_status(
                "installed", found_ver or "unknown", version)
        elif found_ver in (None, "unknown"):
            backend.print_status("installed", "unknown", version)
        elif (found_ver.startswith(f"{version}.")
              or found_ver.startswith(f"{version}x")):
            backend.print_status("installed", found_ver, version)
        else:
            backend.print_status("wrong_version", found_ver, version)
    else:
        backend.print_status("not_installed", "none", version)


def install(version: str, upgrade: bool, backend) -> None:
    """Install KiCad via Chocolatey (or direct download for v6)."""
    choco_exe = backend.find_executable("chocolatey", "none")
    if not choco_exe:
        backend.print_status("install_failed", "choco_missing", version)
        return

    print(f"{'Upgrading' if upgrade else 'Installing'} "
          f"KiCad {version}...")

    # Version 6: direct download (Chocolatey links are broken)
    if version == "6":
        print("[INFO] KiCad 6 detected - Chocolatey's download links "
              "are broken (osdn.net)")
        print("[INFO] Using direct download from GitHub instead...")

        print("Running KiCad cleanup...")
        _cleanup(backend)

        success = _direct_install("6.0.11", backend)
        if not success:
            success = _direct_install("6.0.10", backend)
        if not success:
            success = _direct_install("6.0.9", backend)

        if success:
            return
        else:
            backend.print_status(
                "install_failed", "direct_download_failed", version)
            return

    # Other versions: Chocolatey with fallback chain
    version_candidates = KICAD_VERSIONS.get(version, version)
    if not isinstance(version_candidates, list):
        version_candidates = [version_candidates] if version_candidates \
            else [None]

    _cleanup(backend)
    time.sleep(2)

    installation_success = False
    last_error = None

    for exact_version in version_candidates:
        if exact_version is None:
            print(f"[CHOCO] Attempting to install latest KiCad...")
            cmd = ["choco", "install", "kicad", "-y",
                   "--no-progress", "--ignore-checksums"]
        else:
            print(f"[CHOCO] Attempting to install "
                  f"KiCad {exact_version}...")
            cmd = [
                "choco", "install", "kicad",
                "--version", exact_version,
                "-y", "--no-progress", "--force",
                "--allow-downgrade", "--ignore-checksums",
                "--execution-timeout", "600",
            ]

        print(f"[CHOCO] Running: {' '.join(cmd)}")
        rc, out = backend.run_stream(cmd, timeout=1500)

        if rc != 0:
            out_lower = (out or "").lower()
            if "osdn.net" in out_lower or "404" in out_lower:
                print("[ERROR] Download URL is broken (osdn.net issue)")
                break
            elif "checksum" in out_lower:
                print("[ERROR] Checksum verification failed")
            elif "download" in out_lower and "failed" in out_lower:
                print("[ERROR] Download failed")
            continue

        print("[CHOCO] Verifying installation...")
        time.sleep(3)

        exe, installed_version = \
            backend.find_executable_with_version("kicad", "none")
        if exe:
            print(f"[SUCCESS] KiCad {installed_version} "
                  f"installed successfully!")
            backend.print_status(
                "installed", installed_version, version)
            installation_success = True
            break

        # Fallback path check
        check_paths = [
            (r"C:\Program Files\KiCad\9.0\bin\kicad.exe", "9"),
            (r"C:\Program Files\KiCad\8.0\bin\kicad.exe", "8"),
            (r"C:\Program Files\KiCad\7.0\bin\kicad.exe", "7"),
            (r"C:\Program Files\KiCad\6.0\bin\kicad.exe", "6"),
        ]
        for path, ver in check_paths:
            if os.path.exists(path):
                print(f"[SUCCESS] Found KiCad at: {path}")
                backend.print_status(
                    "installed", f"{ver}.x", version)
                installation_success = True
                break

        if installation_success:
            break

        last_error = out

    if not installation_success:
        print(f"[ERROR] All installation attempts failed for "
              f"KiCad {version}")
        error_msg = "installation_failed"
        if last_error:
            lower = (last_error or "").lower()
            if "osdn.net" in lower or "404" in lower:
                error_msg = "broken_download_url"
            elif "checksum" in lower:
                error_msg = "checksum_failed"
            elif "download" in lower:
                error_msg = "download_failed"
            else:
                error_msg = (last_error[:50]
                             .replace('\n', ' ')
                             .replace('|', '_'))
        backend.print_status("install_failed", error_msg, version)


def uninstall(version: str, backend) -> None:
    """Uninstall KiCad."""
    print("[1/3] Stopping KiCad processes...")
    backend.run_stream(
        ["powershell", "-Command",
         "Get-Process -Name '*kicad*' -EA SilentlyContinue | "
         "Stop-Process -Force -EA SilentlyContinue"],
        timeout=30)

    print("[2/3] Uninstalling via Chocolatey...")
    choco = backend.which("choco") or backend.which("choco.exe")
    if choco:
        backend.run_stream(
            [choco, "uninstall", "kicad", "-y",
             "--force-dependencies", "--no-progress"],
            timeout=300)

    print("[3/3] Removing leftover files...")
    ps = (r'@("C:\Program Files\KiCad",'
          r'"C:\Program Files (x86)\KiCad") | '
          r'ForEach-Object { if (Test-Path $_) { '
          r'Remove-Item $_ -Recurse -Force -EA SilentlyContinue; '
          r'Write-Host "Removed: $_" } }')
    backend.run_stream(["powershell", "-Command", ps], timeout=120)

    exe = backend.find_executable("kicad", "none")
    if not exe:
        print("[OK] KiCad uninstalled")
        backend.print_status("not_installed", "none", "none")
    else:
        backend.print_status("uninstall_failed", "still_found", "none")
