"""
eSim — check, install, uninstall.

Uses direct-download .exe installer.  Tracks version in information.json.
"""

import json
import subprocess
import time
from datetime import datetime
from pathlib import Path

from registry import TOOLS


# ── State helpers (information.json) ─────────────────────────────────

def _read_state(backend):
    path = backend.base_dir / "information.json"
    if path.exists():
        try:
            with open(path) as f:
                return json.load(f)
        except Exception:
            pass
    return {"important_packages": []}


def _write_state(data, backend):
    path = backend.base_dir / "information.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def _update_state(package_name, version, backend):
    data = _read_state(backend)
    for pkg in data["important_packages"]:
        if pkg["package_name"] == package_name:
            pkg["version"] = version
            pkg["installed_date"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S")
            _write_state(data, backend)
            return
    data["important_packages"].append({
        "package_name": package_name,
        "version": version,
        "installed_date": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"),
    })
    _write_state(data, backend)


def _get_state_version(package_name, backend):
    data = _read_state(backend)
    for pkg in data["important_packages"]:
        if pkg["package_name"] == package_name:
            return pkg.get("version")
    return None


# ── Default install path (Windows) ───────────────────────────────────

_ESIM_DIR = Path(r"C:\FOSSEE\eSim")


# ── Tool functions ───────────────────────────────────────────────────

def check(version: str, backend) -> None:
    """Check if eSim is installed by looking for indicator files."""
    indicators = [
        backend.base_dir / "eSim.bat",
        backend.base_dir / "src" / "frontEnd" / "Application.py",
        _ESIM_DIR / "eSim.bat",
        _ESIM_DIR / "uninst-eSim.exe",
        _ESIM_DIR / "src" / "frontEnd" / "Application.py",
    ]
    for p in indicators:
        if p.exists():
            ver = _get_state_version("esim", backend) or "unknown"
            tv = version if version != "none" else "latest"
            if tv in ("latest", "none") or tv == ver:
                backend.print_status("installed", ver, tv)
            else:
                backend.print_status("wrong_version", ver, tv)
            return
    tv = version if version != "none" else "latest"
    backend.print_status("not_installed", "none", tv)


def install(version: str, upgrade: bool, backend) -> None:
    """Download and run the eSim installer."""
    spec = TOOLS.get("esim")
    ver_key = version if version in (spec.download_urls if spec else {}) \
              else "latest"
    url = spec.get_download_url(ver_key) if spec else None
    display_ver = version if version != "latest" else "2.4"
    fname = f"eSim-{display_ver}_installer.exe"

    print(f"[INFO] Installing eSim {display_ver}...")
    print("[INFO] Large file (~400MB) - may take several minutes.")

    installer = backend.download_file(url, fname) if url else None
    if not installer:
        # Fallback: glob for any eSim installer already present
        from pathlib import Path
        for pattern in ["eSim*installer*.exe", "eSim*.exe", "esim*.exe"]:
            matches = list(backend.download_dir.glob(pattern))
            if matches:
                installer = matches[0]
                break
    if not installer:
        print("[ERROR] eSim installer not found. "
              f"Place it in {backend.download_dir}")
        backend.print_status("install_failed", "installer_not_found", version)
        return

    print(f"[INFO] Running installer: {installer.name}")
    print("[INFO] Silent install in progress (10-20 min). Please wait...")
    try:
        subprocess.run([str(installer), "/S"], timeout=1800)
        time.sleep(20)
        for p in [
            backend.base_dir / "eSim.bat",
            backend.base_dir / "src" / "frontEnd" / "Application.py",
            _ESIM_DIR / "eSim.bat",
            _ESIM_DIR / "uninst-eSim.exe",
        ]:
            if p.exists():
                _update_state("esim", display_ver, backend)
                print(f"[OK] eSim {display_ver} installed")
                backend.print_status("installed", display_ver, version)
                return
        print("[ERROR] eSim installed but could not verify")
        backend.print_status("install_failed", "verification_failed", version)
    except subprocess.TimeoutExpired:
        backend.print_status("install_failed", "timeout", version)
    except Exception as e:
        print(f"[ERROR] {e}")
        backend.print_status("install_failed", str(e)[:50], version)


def uninstall(version: str, backend) -> None:
    """Uninstall eSim."""
    uninst = _ESIM_DIR / "uninst-eSim.exe"
    if uninst.exists():
        print("[1/2] Running eSim uninstaller...")
        try:
            subprocess.run([str(uninst), "/S"], timeout=600)
            time.sleep(10)
        except Exception as e:
            print(f"[WARNING] {e}")
    else:
        print("[WARNING] Uninstaller not found - removing folder...")
        ps = (r'@("C:\FOSSEE\eSim") | '
              r'ForEach-Object { if (Test-Path $_) { '
              r'Remove-Item $_ -Recurse -Force -EA SilentlyContinue } }')
        backend.run_cmd(["powershell", "-Command", ps], timeout=120)
    print("[2/2] Verifying removal...")
    if not (_ESIM_DIR / "eSim.bat").exists():
        print("[OK] eSim uninstalled")
        backend.print_status("not_installed", "none", "none")
    else:
        backend.print_status("uninstall_failed", "still_found", "none")
