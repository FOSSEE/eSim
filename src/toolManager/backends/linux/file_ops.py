import os, shutil, subprocess, urllib.request
from pathlib import Path
from typing import Callable, Optional

def download_file(url, filename, download_dir, print_fn=None):
    print_fn = print_fn or print
    dest = download_dir / filename
    if dest.exists(): print_fn(f"[LOCAL] Using cached: {filename}"); return dest
    def hook(n, bs, total):
        if total > 0:
            pct = min(n * bs * 100 / total, 100)
            mb = min(n * bs, total) / (1024 * 1024)
            if n % 50 == 0: print_fn(f"[DOWNLOAD] {pct:.1f}% ({mb:.1f} MB / {total / (1024 * 1024):.1f} MB)", flush=True)
    try:
        urllib.request.urlretrieve(url, dest, hook)
        return dest
    except: return None

def extract_zip(archive, dest_dir, print_fn=None):
    print_fn = print_fn or print
    import zipfile
    try:
        with zipfile.ZipFile(archive, 'r') as zf:
            print_fn(f"Extracting {archive.name}...", flush=True)
            zf.extractall(dest_dir)
        return True
    except: return False

def extract_7z(archive, dest_dir, run_cmd, print_fn=None):
    print_fn = print_fn or print
    for cmd in ["7z", "7za", "7zr", "p7zip"]:
        if Path(cmd).exists() or os.access(f"/usr/bin/{cmd}", os.X_OK) or shutil.which(cmd):
            print_fn(f"Extracting {archive.name}...", flush=True)
            result = run_cmd([cmd, "x", str(archive), f"-o{dest_dir}", "-y"], timeout=300)
            return result is not None and result.returncode == 0
    print_fn("[ERROR] No 7z extractor found"); return False

def run_installer(exe_path, args, run_cmd, print_fn=None):
    print_fn = print_fn or print
    try:
        os.chmod(exe_path, os.stat(exe_path).st_mode | 0o111)
    except OSError as e:
        print_fn(f"[ERROR] chmod failed: {e}"); return False
    print_fn(f"Running installer: {exe_path}...", flush=True)
    result = run_cmd([exe_path] + args, timeout=600)
    return result is not None and result.returncode == 0
