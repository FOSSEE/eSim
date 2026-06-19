"""
GHDL — check, install, uninstall (direct download + extract on Windows).
"""

import os
import re
import shutil
from pathlib import Path

from pm_platform import IS_LINUX
from registry import SCRIPT_MAPPING, TOOLS


def check(version: str, backend) -> None:
    """Check if GHDL is installed."""
    if version == "none":
        exe, found_ver = backend.find_executable_with_version("ghdl", None)
        if exe:
            backend.print_status(
                "installed", found_ver or "unknown", "latest")
        else:
            backend.print_status("not_installed", "none", "latest")
        return

    exe, found_ver = backend.find_executable_with_version("ghdl", version)

    if exe and found_ver:
        if version == "latest":
            backend.print_status("installed", found_ver, version)
        elif found_ver.startswith(version):
            backend.print_status("installed", found_ver, version)
        else:
            backend.print_status("wrong_version", found_ver, version)
    else:
        backend.print_status("not_installed", "none", version)


def install(version: str, upgrade: bool, backend) -> None:
    """Download GHDL zip, extract, and copy ghdl.exe to toolManager/bin/."""
    if IS_LINUX:
        script = SCRIPT_MAPPING.get("GHDL")
        if script:
            ok = backend.run_bash_script(script, version)
            backend.print_status(
                "installed" if ok else "install_failed",
                version if ok else "script_failed",
                version)
        else:
            ok = backend.install_package("ghdl", version)
            backend.print_status(
                "installed" if ok else "install_failed",
                version if ok else "package_manager_failed",
                version)
        return

    spec = TOOLS.get("ghdl")
    url = spec.get_download_url(version) if spec else None
    if not url:
        backend.print_status("not_supported", "none", version)
        return

    print(f"Installing GHDL {version} from: {url}")

    install_dir = backend.base_dir / "ghdl" / version
    if upgrade and install_dir.exists():
        shutil.rmtree(install_dir, ignore_errors=True)

    install_dir.mkdir(parents=True, exist_ok=True)
    zip_file = install_dir / "download.zip"

    try:
        def _hook(n, bs, total):
            if total > 0 and n % 50 == 0:
                pct = min(n * bs * 100 / total, 100)
                mb_done = min(n * bs, total) / (1024 * 1024)
                mb_total = total / (1024 * 1024)
                print(f"[DOWNLOAD] {pct:.1f}% "
                      f"({mb_done:.1f} MB / {mb_total:.1f} MB)",
                      flush=True)

        import urllib.request
        urllib.request.urlretrieve(url, zip_file, _hook)
        print("[OK] Download complete")
    except Exception as e:
        print(f"[ERROR] Download failed: {e}")
        backend.print_status("install_failed", "download_error", version)
        return

    try:
        import zipfile
        with zipfile.ZipFile(zip_file, 'r') as zf:
            files = zf.namelist()
            print(f"Archive contains {len(files)} files")
            print("[INFO] Extracting package... "
                  "This may take several minutes.", flush=True)
            zf.extractall(install_dir)
            print("[OK] Extraction complete")
    except Exception as e:
        print(f"[ERROR] Extraction failed: {e}")
        backend.print_status("install_failed", "extract_error", version)
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
        bin_dir = backend.base_dir / "bin"
        bin_dir.mkdir(exist_ok=True)
        dest_exe = bin_dir / "ghdl.exe"

        shutil.copy2(ghdl_exe, dest_exe)
        print(f"[OK] Installed to: {dest_exe}")

        result = backend.run_cmd([str(dest_exe), "--version"])
        if result and result.returncode == 0:
            m = re.search(r'GHDL\s+(\d+\.\d+(?:\.\d+)?)', result.stdout)
            ghdl_ver = m.group(1) if m else "unknown"
            print(f"[OK] GHDL {ghdl_ver} ready to use")
            backend.print_status("installed", ghdl_ver, version)
        else:
            print("[WARNING] Version check failed")
            backend.print_status("installed", version, version)
    else:
        print("[ERROR] No ghdl.exe found in archive")
        backend.print_status("install_failed", "no_exe", version)


def uninstall(version: str, backend) -> None:
    """Remove GHDL files."""
    if IS_LINUX:
        ok = backend.uninstall_package("ghdl", version)
        backend.print_status(
            "not_installed" if ok else "uninstall_failed",
            "none" if ok else "still_found",
            "none")
        return

    print("[1/2] Removing GHDL files...")
    for p in [
        backend.base_dir / "bin" / "ghdl.exe",
        backend.msys2_mingw_bin.parent / "ghdl.exe"
        if backend.msys2_mingw_bin else None,
        Path(r"C:\FOSSEE\MSYS\mingw64\bin\ghdl.exe"),
    ]:
        if p and p.exists():
            p.unlink()
            print(f"[OK] Removed: {p}")

    ghdl_dir = backend.base_dir / "ghdl"
    if ghdl_dir.exists():
        shutil.rmtree(ghdl_dir, ignore_errors=True)

    print("[2/2] Verifying removal...")
    exe = backend.find_executable("ghdl", "none")
    if not exe:
        print("[OK] GHDL uninstalled")
        backend.print_status("not_installed", "none", "none")
    else:
        backend.print_status("uninstall_failed", "still_found", "none")
