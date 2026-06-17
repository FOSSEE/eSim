"""
Verilator — check, install, uninstall (via MSYS2 or 7z archive on Windows).
"""

import shutil
import time
from pathlib import Path

from registry import VERILATOR_VERSIONS


def _run_msys2_cmd(backend, cmd, timeout=300):
    """Run a command inside MSYS2 bash."""
    bash_exe = backend.msys2_bash
    if not bash_exe:
        print("[ERROR] MSYS2 not found")
        return None

    full_cmd = [str(bash_exe), "-lc", cmd]
    try:
        rc, out = backend.run_stream(full_cmd, timeout)
        class _R:
            def __init__(self, rc, out):
                self.returncode = rc
                self.stdout = out
                self.stderr = ""
        return _R(rc, out)
    except Exception as e:
        print(f"[ERROR] MSYS2 command failed: {e}")
        return None


def _extract_verilator_7z(archive_path, version, backend):
    """Extract a pre-built Verilator 7z archive into MSYS2."""
    try:
        import py7zr
    except ImportError:
        print("[ERROR] py7zr not installed. Run: pip install py7zr")
        backend.print_status("install_failed", "py7zr_missing", version)
        return False

    extract_dir = backend.download_dir / "verilator_extract"
    if extract_dir.exists():
        shutil.rmtree(extract_dir, ignore_errors=True)
    extract_dir.mkdir(parents=True, exist_ok=True)

    print(f"[1/3] Extracting {archive_path.name}... "
          "This may take several minutes.", flush=True)
    try:
        with py7zr.SevenZipFile(archive_path, mode='r') as archive:
            archive.extractall(extract_dir)
        print("[1/3] Extraction complete")
    except Exception as e:
        print(f"[ERROR] Extraction failed: {e}")
        backend.print_status("install_failed", "extract_error", version)
        return False

    dest_msys = backend.msys2_mingw_root
    if not dest_msys:
        print("[ERROR] MSYS2 not found. "
              "Install MSYS2 at C:\\msys64 first.")
        backend.print_status("install_failed", "msys2_missing", version)
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
                shutil.copytree(
                    str(src), str(dest_msys / sub), dirs_exist_ok=True)

        pkgconfig = extracted / "share" / "pkgconfig"
        if pkgconfig.exists():
            shutil.copytree(
                str(pkgconfig), str(dest_msys / "pkgconfig"),
                dirs_exist_ok=True)

        shutil.rmtree(extract_dir, ignore_errors=True)
        print("[2/3] Files copied successfully")
    except Exception as e:
        print(f"[ERROR] Copy failed: {e}")
        backend.print_status("install_failed", "copy_error", version)
        return False

    print("[3/3] Verifying installation...")
    time.sleep(2)
    exe, installed_ver = backend.find_executable_with_version(
        "verilator", "none")
    if exe:
        print(f"[OK] Verilator {installed_ver or version} is ready")
        return True
    else:
        print("[WARNING] Files copied but could not verify version")
        return True


# ── Tool functions ───────────────────────────────────────────────────

def check(version: str, backend) -> None:
    """Check if Verilator is installed."""
    if version == "none":
        exe, found_ver = backend.find_executable_with_version(
            "verilator", None)
        if exe:
            backend.print_status(
                "installed", found_ver or "unknown", "latest")
        else:
            backend.print_status("not_installed", "none", "latest")
        return

    exe, found_ver = backend.find_executable_with_version(
        "verilator", version)

    if exe and found_ver:
        if version == "latest":
            backend.print_status("installed", found_ver, version)
        elif found_ver == version or version in found_ver:
            backend.print_status("installed", found_ver, version)
        else:
            backend.print_status("wrong_version", found_ver, version)
    else:
        backend.print_status("not_installed", "none", version)


def install(version: str, upgrade: bool, backend) -> None:
    """Install Verilator (from 7z archive or via MSYS2 pacman)."""
    print(f"[INFO] {'Upgrading' if upgrade else 'Installing'} "
          f"Verilator {version}...")

    # Try local 7z archive first
    if version != "latest" and version in VERILATOR_VERSIONS:
        fname = VERILATOR_VERSIONS[version]
        if fname:
            archive = backend.download_dir / fname
            if archive.exists():
                print(f"[INFO] Using local archive: {fname}")
                if _extract_verilator_7z(archive, version, backend):
                    exe, installed_ver = \
                        backend.find_executable_with_version(
                            "verilator", "none")
                    backend.print_status(
                        "installed", installed_ver or version, version)
                return
            else:
                print(f"[INFO] Archive not found: {archive}")
                print(f"[INFO] Falling back to latest via MSYS2...")

    # MSYS2 pacman install
    bash_exe = backend.msys2_bash
    if not bash_exe:
        backend.print_status("install_failed", "msys2_missing", version)
        return

    try:
        print("[MSYS2] Step 1/3: Updating package database...")
        _run_msys2_cmd(backend,
                       "pacman -Syu --noconfirm 2>&1 || true")

        if upgrade:
            print("[MSYS2] Step 2/3: Removing existing Verilator...")
            _run_msys2_cmd(
                backend,
                "pacman -R --noconfirm "
                "mingw-w64-x86_64-verilator 2>/dev/null || true")
        else:
            print("[MSYS2] Step 2/3: Preparing...")

        print("[MSYS2] Step 3/3: Installing Verilator "
              "(may take a few minutes)...")
        result = _run_msys2_cmd(
            backend,
            "pacman -S --noconfirm mingw-w64-x86_64-verilator")

        if result and result.returncode == 0:
            print("[MSYS2] Waiting for installation to settle...")
            time.sleep(5)
            exe, installed_version = \
                backend.find_executable_with_version("verilator", "none")
            if not exe:
                time.sleep(3)
                exe, installed_version = \
                    backend.find_executable_with_version(
                        "verilator", "none")
            if exe:
                if version == "latest":
                    backend.print_status(
                        "installed", installed_version or "unknown",
                        "latest")
                elif installed_version and version in installed_version:
                    backend.print_status(
                        "installed", installed_version, version)
                else:
                    backend.print_status(
                        "installed", installed_version or "unknown",
                        version)
            else:
                backend.print_status(
                    "install_failed", "not_found_after_install", version)
        else:
            error_msg = "msys2_install_failed"
            if result and result.stderr:
                error_msg = (
                    result.stderr[:100]
                    .replace('\n', ' ')
                    .replace('|', '_'))
            backend.print_status("install_failed", error_msg, version)

    except Exception as e:
        backend.print_status("install_failed", str(e)[:50], version)


def uninstall(version: str, backend) -> None:
    """Remove Verilator via MSYS2 pacman and delete any leftover files."""
    print("[1/2] Removing Verilator...")
    bash_exe = backend.msys2_bash
    if bash_exe:
        backend.run_stream(
            [str(bash_exe), "-lc",
             "pacman -R --noconfirm "
             "mingw-w64-x86_64-verilator 2>&1 || true"],
            timeout=120)

    msys_bin = backend.msys2_mingw_bin
    if msys_bin:
        for name in ["verilator.exe", "verilator_bin.exe"]:
            p = msys_bin / name
            if p.exists():
                p.unlink()
                print(f"[OK] Removed: {p}")

    # Also check FOSSEE MSYS path
    fossee_path = Path(r"C:\FOSSEE\MSYS\mingw64\bin")
    if fossee_path.exists():
        for name in ["verilator.exe", "verilator_bin.exe"]:
            p = fossee_path / name
            if p.exists():
                p.unlink()
                print(f"[OK] Removed: {p}")

    print("[2/2] Verifying removal...")
    exe = backend.find_executable("verilator", "none")
    if not exe:
        print("[OK] Verilator uninstalled")
        backend.print_status("not_installed", "none", "none")
    else:
        backend.print_status("uninstall_failed", "still_found", "none")
