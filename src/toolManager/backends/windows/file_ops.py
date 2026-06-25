import os, urllib.request, zipfile
from pathlib import Path
from typing import Callable, Optional

def download_file(url, filename, download_dir, print_fn=None):
    print_fn = print_fn or print
    dest = download_dir / filename
    if dest.exists(): print_fn(f"[LOCAL] Using cached: {filename}"); return dest
    def hook(n, bs, total):
        if total > 0 and n % 50 == 0:
            pct = min(n * bs * 100 / total, 100)
            mb = min(n * bs, total) / (1024 * 1024)
            print_fn(f"[DOWNLOAD] {pct:.1f}% ({mb:.1f}/{total / (1024 * 1024):.1f} MB)", flush=True)
    try:
        urllib.request.urlretrieve(url, dest, hook)
        return dest
    except: return None

def extract_zip(archive, dest_dir, print_fn=None):
    print_fn = print_fn or print
    try:
        with zipfile.ZipFile(archive, 'r') as zf:
            print_fn(f"Extracting {archive.name}...", flush=True)
            zf.extractall(dest_dir)
        return True
    except: return False

def extract_7z(archive, dest_dir, run_cmd, print_fn=None):
    print_fn = print_fn or print
    for c in [r"C:\Program Files\7-Zip\7z.exe", r"C:\Program Files (x86)\7-Zip\7z.exe"]:
        if os.path.exists(c):
            print_fn(f"Extracting {archive.name}...", flush=True)
            result = run_cmd([c, "x", str(archive), f"-o{dest_dir}", "-y"], timeout=300)
            return result is not None and result.returncode == 0
    import shutil
    for p in [shutil.which("7z"), shutil.which("7z.exe")]:
        if p:
            result = run_cmd([p, "x", str(archive), f"-o{dest_dir}", "-y"], timeout=300)
            return result is not None and result.returncode == 0
    print_fn("[ERROR] 7-Zip not found"); return False

def run_installer(exe_path, args, run_cmd, print_fn=None):
    print_fn = print_fn or print
    print_fn(f"Running installer: {exe_path}...", flush=True)
    result = run_cmd([exe_path] + args, timeout=900)
    return result is not None and result.returncode == 0
