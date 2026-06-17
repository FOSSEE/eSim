"""
Windows file operations: download with caching, 7z extraction, installer execution.
"""

import os
import urllib.request
import zipfile
from pathlib import Path
from typing import Callable, Optional


def download_file(url: str, filename: str, download_dir: Path,
                  print_fn: Callable = None) -> Optional[Path]:
    """Download *url* to *download_dir* / *filename* with caching and progress.

    If the file already exists it is returned immediately (cached).
    *print_fn* defaults to ``print`` and is used for status messages.
    Returns the local path on success, or None on failure.
    """
    if print_fn is None:
        print_fn = print

    local = download_dir / filename
    if local.exists():
        print_fn(f"[LOCAL] Using cached: {filename}")
        return local

    dest = download_dir / filename
    print_fn(f"[DOWNLOAD] {filename}")
    try:
        def _hook(n, bs, total):
            if total > 0 and n % 50 == 0:
                pct = min(n * bs * 100 / total, 100)
                mb = min(n * bs, total) / (1024 * 1024)
                tot = total / (1024 * 1024)
                print_fn(f"[DOWNLOAD] {pct:.1f}% ({mb:.1f}/{tot:.1f} MB)")

        urllib.request.urlretrieve(url, dest, _hook)
        print_fn("[OK] Download complete")
        return dest
    except Exception as e:
        print_fn(f"[ERROR] Download failed: {e}")
        if dest.exists():
            dest.unlink()
        return None


def extract_zip(archive: Path, dest_dir: Path,
                print_fn: Callable = None) -> bool:
    """Extract a .zip archive to *dest_dir*."""
    if print_fn is None:
        print_fn = print
    try:
        with zipfile.ZipFile(archive) as zf:
            zf.extractall(dest_dir)
        print_fn(f"[OK] Extracted {archive.name} to {dest_dir}")
        return True
    except Exception as e:
        print_fn(f"[ERROR] Zip extraction failed: {e}")
        return False


def extract_7z(archive: Path, dest_dir: Path, seven_zip_path: str = None,
               run_cmd: Callable = None, print_fn: Callable = None) -> bool:
    """Extract a .7z archive using 7-Zip.

    *seven_zip_path* is the path to 7z.exe (or None to search).
    *run_cmd* must be a callable accepting a command list.
    """
    if print_fn is None:
        print_fn = print

    if seven_zip_path is None:
        seven_zip_path = _find_7z()

    if not seven_zip_path:
        print_fn("[ERROR] 7-Zip not found. Install 7-Zip to handle .7z files.")
        return False

    try:
        result = run_cmd(
            [seven_zip_path, "x", str(archive),
             f"-o{dest_dir}", "-y"],
            timeout=300,
        )
        if result and result.returncode == 0:
            print_fn(f"[OK] Extracted {archive.name} to {dest_dir}")
            return True
        print_fn(f"[ERROR] 7z extraction failed (exit {result.returncode})")
        return False
    except Exception as e:
        print_fn(f"[ERROR] 7z extraction error: {e}")
        return False


def _find_7z() -> Optional[str]:
    """Locate 7z.exe on the system."""
    import shutil
    candidates = [
        r"C:\Program Files\7-Zip\7z.exe",
        r"C:\Program Files (x86)\7-Zip\7z.exe",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return shutil.which("7z") or shutil.which("7z.exe")


def run_installer(exe_path: str, args: list = None,
                  run_cmd: Callable = None,
                  print_fn: Callable = None) -> bool:
    """Run an executable installer (.exe / .msi) and wait for completion.

    *args* are additional command-line arguments.
    *run_cmd* must be a callable accepting a command list.
    """
    if print_fn is None:
        print_fn = print

    cmd = [exe_path]
    if args:
        cmd.extend(args)

    print_fn(f"[INSTALL] Running: {' '.join(cmd)}")
    try:
        result = run_cmd(cmd, timeout=600)
        if result and result.returncode == 0:
            print_fn("[OK] Installer completed successfully")
            return True
        print_fn(f"[ERROR] Installer failed (exit {result.returncode})")
        return False
    except Exception as e:
        print_fn(f"[ERROR] Installer error: {e}")
        return False
