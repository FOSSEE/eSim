"""backends/linux/file_ops.py — Linux file operations.

Download, archive extraction, and installer running for Linux systems.
Follows the same pattern as backends/windows/file_ops.py.
"""

import os
import subprocess
import urllib.request
from pathlib import Path
from typing import Callable, Optional


def download_file(
    url: str,
    filename: str,
    download_dir: Path,
    print_fn: Optional[Callable] = None,
) -> Optional[Path]:
    """Download *url* to *download_dir* / *filename*.

    If the file already exists, return it immediately (cached).
    Returns the local Path on success, None on failure.
    """
    dest = download_dir / filename
    if dest.exists():
        return dest

    if print_fn is None:
        print_fn = print

    download_dir.mkdir(parents=True, exist_ok=True)

    def _reporthook(block, blocksize, totalsize):
        if totalsize > 0 and block % 50 == 0:
            pct = min(100, int(block * blocksize * 100 / totalsize))
            print_fn(f"\r  Downloading {filename} ... {pct}%", end="")

    try:
        urllib.request.urlretrieve(url, str(dest), _reporthook)
        print_fn("")
        return dest
    except Exception as exc:
        print_fn(f"[ERROR] Download failed: {exc}")
        if dest.exists():
            dest.unlink()
        return None


def extract_zip(
    archive: Path,
    dest_dir: Path,
    print_fn: Optional[Callable] = None,
) -> bool:
    """Extract a .zip archive to *dest_dir*."""
    import zipfile
    try:
        dest_dir.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(archive) as zf:
            zf.extractall(dest_dir)
        if print_fn:
            print_fn(f"  Extracted {archive.name} to {dest_dir}")
        return True
    except Exception as exc:
        if print_fn:
            print_fn(f"[ERROR] Extract failed: {exc}")
        return False


def extract_tar(
    archive: Path,
    dest_dir: Path,
    run_cmd: Optional[Callable] = None,
    print_fn: Optional[Callable] = None,
) -> bool:
    """Extract a .tar.* archive to *dest_dir* using system ``tar``."""
    if print_fn is None:
        print_fn = print
    dest_dir.mkdir(parents=True, exist_ok=True)
    cmd = ["tar", "xf", str(archive), "-C", str(dest_dir)]
    try:
        if run_cmd:
            result = run_cmd(cmd, timeout=300)
            ok = result is not None and result.returncode == 0
        else:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            ok = result.returncode == 0
        if ok:
            print_fn(f"  Extracted {archive.name} to {dest_dir}")
        else:
            print_fn(f"[ERROR] tar extract failed: {result.stderr.strip()}")
        return ok
    except Exception as exc:
        print_fn(f"[ERROR] tar extract failed: {exc}")
        return False


def extract_7z(
    archive: Path,
    dest_dir: Path,
    run_cmd: Optional[Callable] = None,
    print_fn: Optional[Callable] = None,
) -> bool:
    """Extract a .7z archive using system ``7z`` or ``p7zip``."""
    if print_fn is None:
        print_fn = print

    # Find a 7z-capable extractor
    extractor = None
    for cmd in ("7z", "7za", "7zr", "p7zip"):
        if Path(cmd).exists() or os.access(f"/usr/bin/{cmd}", os.X_OK):
            extractor = cmd
            break
    if extractor is None:
        # Fall back to shutil.which
        import shutil
        for cmd in ("7z", "7za", "7zr", "p7zip"):
            if shutil.which(cmd):
                extractor = cmd
                break

    if extractor is None:
        print_fn("[ERROR] No 7z extractor found (install p7zip or 7zip)")
        return False

    dest_dir.mkdir(parents=True, exist_ok=True)
    cmd = [extractor, "x", str(archive), f"-o{dest_dir}", "-y"]
    try:
        if run_cmd:
            result = run_cmd(cmd, timeout=300)
            ok = result is not None and result.returncode == 0
        else:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            ok = result.returncode == 0
        if ok:
            print_fn(f"  Extracted {archive.name} to {dest_dir}")
        else:
            print_fn(f"[ERROR] {extractor} extract failed")
        return ok
    except Exception as exc:
        print_fn(f"[ERROR] {extractor} extract failed: {exc}")
        return False


def run_installer(
    exe_path: str,
    args: Optional[list[str]] = None,
    run_cmd: Optional[Callable] = None,
    print_fn: Optional[Callable] = None,
) -> bool:
    """Run a Linux installer script (.sh, .run) or AppImage.

    The *exe_path* is made executable and then executed.  If *run_cmd*
    is provided it is used; otherwise a plain subprocess call is made.
    """
    if print_fn is None:
        print_fn = print

    try:
        os.chmod(exe_path, os.stat(exe_path).st_mode | 0o111)
    except OSError as exc:
        print_fn(f"[ERROR] Failed to chmod {exe_path}: {exc}")
        return False

    cmd = [exe_path]
    if args:
        cmd.extend(args)

    try:
        if run_cmd:
            result = run_cmd(cmd, timeout=600)
            ok = result is not None and result.returncode == 0
        else:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            ok = result.returncode == 0
        if ok:
            print_fn(f"  Installer {Path(exe_path).name} completed")
        else:
            print_fn(f"[ERROR] Installer {Path(exe_path).name} failed")
        return ok
    except subprocess.TimeoutExpired:
        print_fn(f"[ERROR] Installer {Path(exe_path).name} timed out")
        return False
    except Exception as exc:
        print_fn(f"[ERROR] Installer failed: {exc}")
        return False
