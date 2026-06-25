from platform_utils import IS_LINUX
from registry import SCRIPT_MAPPING, TOOLS as REG_TOOLS
from registry import KICAD_VERSIONS, NGSPICE_VERSIONS, LLVM_VERSIONS, VERILATOR_VERSIONS

import os, re, time, shutil, json, subprocess, urllib.request, zipfile
from pathlib import Path
from datetime import datetime

_ESIM_DIR = Path(r"C:\FOSSEE\eSim")

def _linux_install(version, backend, script_name=None, package=None):
    if script_name:
        ok = backend.run_bash_script(script_name, version)
    elif package:
        ok = backend.install_package(package, version)
    else:
        ok = False
    backend.print_status("installed" if ok else "install_failed",
        version if ok else ("script_failed" if script_name else "package_manager_failed"), version)

def _linux_uninstall(version, backend, package):
    ok = backend.uninstall_package(package, version)
    backend.print_status("not_installed" if ok else "uninstall_failed",
        "none" if ok else "still_found", "none")

def _default_check(version, backend, tool_id, match_fn):
    exe, found = backend.find_executable_with_version(tool_id, None if version == "none" else version)
    if version == "none":
        backend.print_status("installed" if exe else "not_installed", found or "none", "latest"); return
    if exe:
        if version == "latest":
            backend.print_status("installed", found or "unknown", version)
        elif found and found != "unknown" and match_fn and match_fn(version, found):
            backend.print_status("installed", found, version)
        else:
            backend.print_status("wrong_version" if found else "installed", found or "unknown", version)
    else:
        backend.print_status("not_installed", "none", version)

def _choco_verification(rc, out, version, backend, tool_id):
    if rc == 0:
        time.sleep(2 if tool_id == "ngspice" else 3)
        exe, found = backend.find_executable_with_version(tool_id, "none")
        if exe:
            backend.print_status("installed", found or "unknown", version)
        else:
            backend.print_status("install_failed", "not_found", version)
    else:
        backend.print_status("install_failed",
            (out[-50:].replace('\n', ' ').replace('|', '_') if out else "choco_error"), version)

def _choco_precheck(backend, version):
    if not backend.find_executable("chocolatey", "none"):
        backend.print_status("install_failed", "choco_missing", version)
        return False
    return True

# ═══════════════════════════════════════════════════════════════════════
# eSim
# ═══════════════════════════════════════════════════════════════════════

def _esim_state(pkg_name, version, backend, write=False):
    path = backend.base_dir / "information.json"
    data = {"important_packages": []}
    if path.exists():
        try:
            with open(path) as f: data = json.load(f)
        except: pass
    if write:
        for pkg in data["important_packages"]:
            if pkg["package_name"] == pkg_name:
                pkg["version"] = version
                pkg["installed_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open(path, "w") as f: json.dump(data, f, indent=4)
                return
        data["important_packages"].append({"package_name": pkg_name, "version": version,
            "installed_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        with open(path, "w") as f: json.dump(data, f, indent=4)
        return
    for pkg in data["important_packages"]:
        if pkg["package_name"] == pkg_name: return pkg.get("version")
    return None

def check_esim(version, backend):
    indicators = [backend.base_dir / "eSim.bat", backend.base_dir / "src" / "frontEnd" / "Application.py",
        _ESIM_DIR / "eSim.bat", _ESIM_DIR / "uninst-eSim.exe", _ESIM_DIR / "src" / "frontEnd" / "Application.py"]
    for p in indicators:
        if p.exists():
            ver = _esim_state("esim", None, backend) or "unknown"
            tv = version if version != "none" else "latest"
            backend.print_status("installed" if tv in ("latest", "none") or tv == ver else "wrong_version", ver, tv)
            return
    backend.print_status("not_installed", "none", version if version != "none" else "latest")

def install_esim(version, upgrade, backend):
    if IS_LINUX:
        ok = backend.run_bash_script("install-eSim.sh", "--install")
        backend.print_status("installed" if ok else "install_failed", version if ok else "script_failed", version)
        return
    spec = REG_TOOLS.get("esim")
    ver_key = version if version in (spec.download_urls if spec else {}) else "latest"
    url = spec.get_download_url(ver_key) if spec else None
    display_ver = version if version != "latest" else "2.4"
    installer = backend.download_file(url, f"eSim-{display_ver}_installer.exe") if url else None
    if not installer:
        for pat in ["eSim*installer*.exe", "eSim*.exe", "esim*.exe"]:
            matches = list(backend.download_dir.glob(pat))
            if matches: installer = matches[0]; break
    if not installer:
        backend.print_status("install_failed", "installer_not_found", version); return
    try:
        subprocess.run([str(installer), "/S"], timeout=1800)
        time.sleep(20)
        for p in [backend.base_dir / "eSim.bat", backend.base_dir / "src" / "frontEnd" / "Application.py",
                  _ESIM_DIR / "eSim.bat", _ESIM_DIR / "uninst-eSim.exe"]:
            if p.exists():
                _esim_state("esim", display_ver, backend, write=True)
                backend.print_status("installed", display_ver, version); return
        backend.print_status("install_failed", "verification_failed", version)
    except subprocess.TimeoutExpired:
        backend.print_status("install_failed", "timeout", version)
    except Exception as e:
        backend.print_status("install_failed", str(e)[:50], version)

def uninstall_esim(version, backend):
    if IS_LINUX:
        _linux_uninstall(version, backend, None) if False else None
        ok = backend.run_bash_script("install-eSim.sh", "--uninstall")
        backend.print_status("not_installed" if ok else "uninstall_failed", "none" if ok else "still_found", "none")
        return
    uninst = _ESIM_DIR / "uninst-eSim.exe"
    if uninst.exists():
        try: subprocess.run([str(uninst), "/S"], timeout=600); time.sleep(10)
        except: pass
    else:
        backend.run_cmd(["powershell", "-Command",
            r'@("C:\FOSSEE\eSim") | ForEach-Object { if (Test-Path $_) { Remove-Item $_ -Recurse -Force -EA SilentlyContinue } }'], timeout=120)
    backend.print_status("not_installed" if not (_ESIM_DIR / "eSim.bat").exists() else "uninstall_failed",
        "none" if not (_ESIM_DIR / "eSim.bat").exists() else "still_found", "none")

# ═══════════════════════════════════════════════════════════════════════
# KiCad
# ═══════════════════════════════════════════════════════════════════════

def check_kicad(version, backend):
    exe, found = backend.find_executable_with_version("kicad", None)
    if version == "none":
        backend.print_status("installed" if exe else "not_installed", found or "none", "latest"); return
    if exe:
        if version == "latest":
            backend.print_status("installed", found or "unknown", version)
        elif found in (None, "unknown"):
            backend.print_status("installed", "unknown", version)
        elif found.startswith(f"{version}.") or found.startswith(f"{version}x"):
            backend.print_status("installed", found, version)
        else:
            backend.print_status("wrong_version", found, version)
    else:
        backend.print_status("not_installed", "none", version)

def _kicad_cleanup(backend):
    backend.run_cmd(["choco", "uninstall", "kicad", "-y", "--force-dependencies", "--remove-dependencies", "--no-progress"], timeout=180)
    ps = r"""Get-Process -Name "*kicad*" -EA SilentlyContinue | Stop-Process -Force -EA SilentlyContinue
Start-Sleep -Seconds 2
$paths = @("C:\Program Files\KiCad","C:\Program Files\KiCad 9.0","C:\Program Files\KiCad 8.0","C:\Program Files\KiCad 7.0","C:\Program Files\KiCad 6.0","C:\Program Files (x86)\KiCad","$env:LOCALAPPDATA\KiCad","$env:APPDATA\kicad")
foreach ($path in $paths) { if (Test-Path $path) { Write-Host "Removing: $path"; Remove-Item -Path $path -Recurse -Force -EA SilentlyContinue; Start-Sleep -Milliseconds 500 } }"""
    backend.run_cmd(["powershell", "-Command", ps], timeout=180)
    backend.run_cmd(["choco", "cache", "remove", "--expired", "-y"], timeout=60)

def _kicad_direct_install(ver_str, backend):
    spec = REG_TOOLS.get("kicad")
    url = spec.get_download_url(ver_str) if spec else None
    if not url: return False
    import tempfile
    installer = Path(tempfile.gettempdir()) / f"kicad-{ver_str}-installer.exe"
    try:
        def hook(n, bs, total):
            if total > 0 and n % 50 == 0:
                pct = min(n * bs * 100 / total, 100); mb = min(n * bs, total) / (1024 * 1024)
                print(f"[DOWNLOAD] {pct:.1f}% ({mb:.1f} MB / {total / (1024 * 1024):.1f} MB)", flush=True)
        urllib.request.urlretrieve(url, installer, hook)
        if not installer.exists() or installer.stat().st_size < 100 * 1024 * 1024: return False
        subprocess.run([str(installer), "/S", "/NCRC"], timeout=900)
        time.sleep(10)
        exe, iv = backend.find_executable_with_version("kicad", "none")
        if exe: backend.print_status("installed", iv or ver_str, "6"); return True
        if os.path.exists(r"C:\Program Files\KiCad\6.0\bin\kicad.exe"):
            backend.print_status("installed", ver_str, "6"); return True
        return False
    except: return False
    finally:
        if installer.exists():
            try: installer.unlink()
            except: pass

def install_kicad(version, upgrade, backend):
    if IS_LINUX:
        _linux_install(version, backend, script_name=SCRIPT_MAPPING.get("KiCad"), package="kicad"); return
    if not _choco_precheck(backend, version): return
    if version == "6":
        _kicad_cleanup(backend)
        for v in ["6.0.11", "6.0.10", "6.0.9"]:
            if _kicad_direct_install(v, backend): return
        backend.print_status("install_failed", "direct_download_failed", version); return
    candidates = KICAD_VERSIONS.get(version, version)
    if not isinstance(candidates, list): candidates = [candidates] if candidates else [None]
    _kicad_cleanup(backend); time.sleep(2)
    for exact in candidates:
        if exact is None:
            cmd = ["choco", "install", "kicad", "-y", "--no-progress", "--ignore-checksums"]
        else:
            cmd = ["choco", "install", "kicad", "--version", exact, "-y", "--no-progress", "--force",
                   "--allow-downgrade", "--ignore-checksums", "--execution-timeout", "600"]
        rc, out = backend.run_stream(cmd, timeout=1500)
        if rc != 0:
            low = (out or "").lower()
            if "osdn.net" in low or "404" in low: break
            continue
        time.sleep(3)
        exe, iv = backend.find_executable_with_version("kicad", "none")
        if exe:
            backend.print_status("installed", iv, version); return
        check_paths = [(r"C:\Program Files\KiCad\9.0\bin\kicad.exe", "9"),
            (r"C:\Program Files\KiCad\8.0\bin\kicad.exe", "8"),
            (r"C:\Program Files\KiCad\7.0\bin\kicad.exe", "7"),
            (r"C:\Program Files\KiCad\6.0\bin\kicad.exe", "6")]
        for path, ver in check_paths:
            if os.path.exists(path):
                backend.print_status("installed", f"{ver}.x", version); return
    backend.print_status("install_failed", "installation_failed", version)

def uninstall_kicad(version, backend):
    if IS_LINUX:
        _linux_uninstall(version, backend, "kicad"); return
    backend.run_stream(["powershell", "-Command",
        "Get-Process -Name '*kicad*' -EA SilentlyContinue | Stop-Process -Force -EA SilentlyContinue"], timeout=30)
    choco = backend.which("choco") or backend.which("choco.exe")
    if choco:
        backend.run_stream([choco, "uninstall", "kicad", "-y", "--force-dependencies", "--no-progress"], timeout=300)
    ps = r'@("C:\Program Files\KiCad","C:\Program Files (x86)\KiCad") | ForEach-Object { if (Test-Path $_) { Remove-Item $_ -Recurse -Force -EA SilentlyContinue; Write-Host "Removed: $_" } }'
    backend.run_stream(["powershell", "-Command", ps], timeout=120)
    backend.print_status("not_installed" if not backend.find_executable("kicad", "none") else "uninstall_failed",
        "none" if not backend.find_executable("kicad", "none") else "still_found", "none")

# ═══════════════════════════════════════════════════════════════════════
# Ngspice
# ═══════════════════════════════════════════════════════════════════════

def check_ngspice(version, backend):
    _default_check(version, backend, "ngspice", lambda v, f: f == str(v) or f.startswith(str(v)))

def install_ngspice(version, upgrade, backend):
    if IS_LINUX:
        _linux_install(version, backend, script_name=SCRIPT_MAPPING.get("Ngspice"), package="ngspice"); return
    if not _choco_precheck(backend, version): return
    exact = NGSPICE_VERSIONS.get(version, version)
    backend.run_cmd(["choco", "uninstall", "ngspice", "-y", "--force-dependencies", "--no-progress"], timeout=180)
    cmd = (["choco", "install", "ngspice", "-y", "--no-progress"] if version == "latest"
           else ["choco", "install", "ngspice", "--version", exact, "-y", "--no-progress", "--allow-downgrade", "--force"])
    rc, out = backend.run_stream(cmd, timeout=300)
    _choco_verification(rc, out, version, backend, "ngspice")

def uninstall_ngspice(version, backend):
    if IS_LINUX:
        _linux_uninstall(version, backend, "ngspice"); return
    choco = backend.which("choco") or backend.which("choco.exe")
    if choco:
        backend.run_stream([choco, "uninstall", "ngspice", "-y", "--force-dependencies", "--no-progress"], timeout=180)
    else:
        backend.run_cmd(["powershell", "-Command",
            r'@("C:\Program Files\ngspice","C:\Program Files (x86)\ngspice") | ForEach-Object { if (Test-Path $_) { Remove-Item $_ -Recurse -Force -EA SilentlyContinue } }'], timeout=60)
    backend.print_status("not_installed" if not backend.find_executable("ngspice", "none") else "uninstall_failed",
        "none" if not backend.find_executable("ngspice", "none") else "still_found", "none")

# ═══════════════════════════════════════════════════════════════════════
# GHDL
# ═══════════════════════════════════════════════════════════════════════

def check_ghdl(version, backend):
    _default_check(version, backend, "ghdl", lambda v, f: f.startswith(v))

def install_ghdl(version, upgrade, backend):
    if IS_LINUX:
        _linux_install(version, backend, script_name=SCRIPT_MAPPING.get("GHDL"), package="ghdl"); return
    spec = REG_TOOLS.get("ghdl")
    url = spec.get_download_url(version) if spec else None
    if not url: backend.print_status("not_supported", "none", version); return
    install_dir = backend.base_dir / "ghdl" / version
    if upgrade and install_dir.exists(): shutil.rmtree(install_dir, ignore_errors=True)
    install_dir.mkdir(parents=True, exist_ok=True)
    zip_file = install_dir / "download.zip"
    try:
        def hook(n, bs, total):
            if total > 0 and n % 50 == 0:
                pct = min(n * bs * 100 / total, 100)
                mb = min(n * bs, total) / (1024 * 1024)
                print(f"[DOWNLOAD] {pct:.1f}% ({mb:.1f} MB / {total / (1024 * 1024):.1f} MB)", flush=True)
        urllib.request.urlretrieve(url, zip_file, hook)
    except:
        backend.print_status("install_failed", "download_error", version); return
    try:
        with zipfile.ZipFile(zip_file, 'r') as zf: zf.extractall(install_dir)
    except:
        backend.print_status("install_failed", "extract_error", version); return
    finally:
        if zip_file.exists(): zip_file.unlink()
    ghdl_exe = next((Path(r) / f for r, _, fs in os.walk(install_dir) for f in fs if f.lower() == "ghdl.exe"), None)
    if ghdl_exe:
        bin_dir = backend.base_dir / "bin"; bin_dir.mkdir(exist_ok=True)
        dest = bin_dir / "ghdl.exe"; shutil.copy2(ghdl_exe, dest)
        result = backend.run_cmd([str(dest), "--version"])
        if result and result.returncode == 0:
            m = re.search(r'GHDL\s+(\d+\.\d+(?:\.\d+)?)', result.stdout)
            ver = m.group(1) if m else "unknown"
            backend.print_status("installed", ver, version)
        else:
            backend.print_status("installed", version, version)
    else:
        backend.print_status("install_failed", "no_exe", version)

def uninstall_ghdl(version, backend):
    if IS_LINUX:
        _linux_uninstall(version, backend, "ghdl"); return
    for p in [backend.base_dir / "bin" / "ghdl.exe",
              backend.msys2_mingw_bin.parent / "ghdl.exe" if backend.msys2_mingw_bin else None,
              Path(r"C:\FOSSEE\MSYS\mingw64\bin\ghdl.exe")]:
        if p and p.exists(): p.unlink()
    ghdl_dir = backend.base_dir / "ghdl"
    if ghdl_dir.exists(): shutil.rmtree(ghdl_dir, ignore_errors=True)
    backend.print_status("not_installed" if not backend.find_executable("ghdl", "none") else "uninstall_failed",
        "none" if not backend.find_executable("ghdl", "none") else "still_found", "none")

# ═══════════════════════════════════════════════════════════════════════
# Verilator
# ═══════════════════════════════════════════════════════════════════════

def check_verilator(version, backend):
    exe, found = backend.find_executable_with_version("verilator", None if version == "none" else version)
    if version == "none":
        backend.print_status("installed" if exe else "not_installed", found or "none", "latest"); return
    if exe and found:
        if version == "latest":
            backend.print_status("installed", found, version)
        elif found == version or version in found:
            backend.print_status("installed", found, version)
        else:
            backend.print_status("wrong_version", found, version)
    else:
        backend.print_status("not_installed", "none", version)

def _msys2_run(backend, cmd, timeout=300):
    bash = backend.msys2_bash
    if not bash: print("[ERROR] MSYS2 not found"); return None
    try:
        rc, out = backend.run_stream([str(bash), "-lc", cmd], timeout)
        r = type("R", (), {"returncode": rc, "stdout": out, "stderr": ""})()
        return r
    except: return None

def _extract_verilator_7z(archive, version, backend):
    try: import py7zr
    except ImportError:
        backend.print_status("install_failed", "py7zr_missing", version); return False
    extract_dir = backend.download_dir / "verilator_extract"
    if extract_dir.exists(): shutil.rmtree(extract_dir, ignore_errors=True)
    extract_dir.mkdir(parents=True, exist_ok=True)
    try:
        with py7zr.SevenZipFile(archive, mode='r') as z: z.extractall(extract_dir)
    except:
        backend.print_status("install_failed", "extract_error", version); return False
    dest = backend.msys2_mingw_root
    if not dest:
        backend.print_status("install_failed", "msys2_missing", version); return False
    extracted = extract_dir / "verilator"
    if not extracted.exists():
        subs = [d for d in extract_dir.iterdir() if d.is_dir()]
        extracted = subs[0] if subs else extract_dir
    try:
        for sub in ["bin", "share", "include"]:
            src = extracted / sub
            if src.exists(): shutil.copytree(str(src), str(dest / sub), dirs_exist_ok=True)
        pkg = extracted / "share" / "pkgconfig"
        if pkg.exists(): shutil.copytree(str(pkg), str(dest / "pkgconfig"), dirs_exist_ok=True)
        shutil.rmtree(extract_dir, ignore_errors=True)
    except:
        backend.print_status("install_failed", "copy_error", version); return False
    return True

def install_verilator(version, upgrade, backend):
    if IS_LINUX:
        _linux_install(version, backend, script_name=SCRIPT_MAPPING.get("Verilator"), package="verilator"); return
    if version != "latest" and version in VERILATOR_VERSIONS:
        fname = VERILATOR_VERSIONS[version]
        if fname:
            archive = backend.download_dir / fname
            if archive.exists() and _extract_verilator_7z(archive, version, backend):
                exe, iv = backend.find_executable_with_version("verilator", "none")
                backend.print_status("installed", iv or version, version)
                return
    bash = backend.msys2_bash
    if not bash: backend.print_status("install_failed", "msys2_missing", version); return
    try:
        _msys2_run(backend, "pacman -Syu --noconfirm 2>&1 || true")
        if upgrade:
            _msys2_run(backend, "pacman -R --noconfirm mingw-w64-x86_64-verilator 2>/dev/null || true")
        result = _msys2_run(backend, "pacman -S --noconfirm mingw-w64-x86_64-verilator")
        if result and result.returncode == 0:
            time.sleep(5)
            exe, iv = backend.find_executable_with_version("verilator", "none")
            if not exe: time.sleep(3); exe, iv = backend.find_executable_with_version("verilator", "none")
            if exe:
                if version == "latest" or (iv and version in iv):
                    backend.print_status("installed", iv or "unknown", version)
                else:
                    backend.print_status("installed", iv or "unknown", version)
            else:
                backend.print_status("install_failed", "not_found_after_install", version)
        else:
            err = (result.stderr[:100].replace('\n', ' ').replace('|', '_') if result and result.stderr else "msys2_failed")
            backend.print_status("install_failed", err, version)
    except:
        backend.print_status("install_failed", "msys2_error", version)

def uninstall_verilator(version, backend):
    if IS_LINUX:
        _linux_uninstall(version, backend, "verilator"); return
    bash = backend.msys2_bash
    if bash:
        backend.run_stream([str(bash), "-lc", "pacman -R --noconfirm mingw-w64-x86_64-verilator 2>&1 || true"], timeout=120)
    msys_bin = backend.msys2_mingw_bin
    if msys_bin:
        for name in ["verilator.exe", "verilator_bin.exe"]:
            p = msys_bin / name
            if p.exists(): p.unlink()
    fossee = Path(r"C:\FOSSEE\MSYS\mingw64\bin")
    if fossee.exists():
        for name in ["verilator.exe", "verilator_bin.exe"]:
            p = fossee / name
            if p.exists(): p.unlink()
    backend.print_status("not_installed" if not backend.find_executable("verilator", "none") else "uninstall_failed",
        "none" if not backend.find_executable("verilator", "none") else "still_found", "none")

# ═══════════════════════════════════════════════════════════════════════
# LLVM / Clang
# ═══════════════════════════════════════════════════════════════════════

def check_llvm(version, backend):
    _default_check(version, backend, "llvm", lambda v, f: f == v)

def install_llvm(version, upgrade, backend):
    if IS_LINUX:
        _linux_install(version, backend, package="llvm"); return
    if not _choco_precheck(backend, version): return
    exact = LLVM_VERSIONS.get(version, version)
    backend.run_stream(["choco", "uninstall", "llvm", "-y", "--no-progress"], timeout=180)
    cmd = (["choco", "install", "llvm", "-y", "--no-progress"] if version == "latest"
           else ["choco", "install", "llvm", "--version", exact, "-y", "--no-progress", "--allow-downgrade", "--force"])
    rc, out = backend.run_stream(cmd, timeout=300)
    if rc == 0:
        time.sleep(3)
        for path in [r"C:\Program Files\LLVM\bin\clang.exe", r"C:\Program Files (x86)\LLVM\bin\clang.exe"]:
            if os.path.exists(path):
                result = backend.run_cmd([path, "--version"], timeout=10)
                if result and result.returncode == 0:
                    m = re.search(r'clang version (\d+)\.', result.stdout)
                    if m: backend.print_status("installed", m.group(1), version); return
                backend.print_status("installed", exact or version, version); return
        backend.print_status("install_failed", "verification_failed", version)
    else:
        backend.print_status("install_failed",
            (out[-50:].replace('\n', ' ').replace('|', '_') if out else "choco_error"), version)

def uninstall_llvm(version, backend):
    if IS_LINUX:
        _linux_uninstall(version, backend, "llvm"); return
    choco = backend.which("choco") or backend.which("choco.exe")
    if choco:
        backend.run_stream([choco, "uninstall", "llvm", "-y", "--no-progress"], timeout=180)
    else:
        backend.run_cmd(["powershell", "-Command",
            r'@("C:\Program Files\LLVM","C:\Program Files (x86)\LLVM") | ForEach-Object { if (Test-Path $_) { Remove-Item $_ -Recurse -Force -EA SilentlyContinue } }'], timeout=60)
    backend.print_status("not_installed" if not backend.find_executable("llvm", "none") else "uninstall_failed",
        "none" if not backend.find_executable("llvm", "none") else "still_found", "none")

# ═══════════════════════════════════════════════════════════════════════
# Chocolatey
# ═══════════════════════════════════════════════════════════════════════

def check_chocolatey(version, backend):
    _default_check(version, backend, "chocolatey", lambda v, f: f == v)

def install_chocolatey(version, upgrade, backend):
    exe, cv = backend.find_executable_with_version("chocolatey", version)
    if exe and not upgrade:
        check_chocolatey(version, backend); return
    result = backend.run_cmd(["powershell", "-Command",
        "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"], timeout=600)
    if result and result.returncode == 0:
        exe, iv = backend.find_executable_with_version("chocolatey", "none")
        backend.print_status("installed" if exe else "install_failed", iv or "unknown" if exe else "not_found", version)
    else:
        backend.print_status("install_failed", "choco_error", version)

# ═══════════════════════════════════════════════════════════════════════
# Tool function registry — dispatch dict indexed by tool_id
# ═══════════════════════════════════════════════════════════════════════

TOOL_FUNCS = {
    "esim": {"check": check_esim, "install": install_esim, "uninstall": uninstall_esim},
    "kicad": {"check": check_kicad, "install": install_kicad, "uninstall": uninstall_kicad},
    "ngspice": {"check": check_ngspice, "install": install_ngspice, "uninstall": uninstall_ngspice},
    "ghdl": {"check": check_ghdl, "install": install_ghdl, "uninstall": uninstall_ghdl},
    "verilator": {"check": check_verilator, "install": install_verilator, "uninstall": uninstall_verilator},
    "llvm": {"check": check_llvm, "install": install_llvm, "uninstall": uninstall_llvm},
    "chocolatey": {"check": check_chocolatey, "install": install_chocolatey},
}
