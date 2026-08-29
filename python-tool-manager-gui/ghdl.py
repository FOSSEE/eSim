import os
import yaml
import shutil
import subprocess
import platform
import urllib.request
import json
import tarfile
from datetime import datetime

TOOLS_DIR = os.path.expanduser("~/esim-tools-bin")
os.makedirs(TOOLS_DIR, exist_ok=True)

INSTALL_DETAILS_FILE = "install_details.yml"


# -------------------- BASIC UTILS --------------------

def get_os():
    system = platform.system().lower()
    if "windows" in system:
        return "windows"
    if "linux" in system:
        return "linux"
    if "darwin" in system:
        return "mac"
    return None


def run(cmd, log=print, cwd=None):
    log("> " + (cmd if isinstance(cmd, str) else " ".join(cmd)))
    p = subprocess.Popen(
        cmd,
        shell=isinstance(cmd, str),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        cwd=cwd,
    )

    for line in iter(p.stdout.readline, ""):
        if not line:
            break
        log(line.strip())

    p.wait()
    if p.returncode != 0:
        raise RuntimeError("Command failed")


def tool_exists(name):
    return shutil.which(name) is not None


def get_tool_cfg(tool_name):
    with open("tools.yml", "r") as f:
        data = yaml.safe_load(f)
    return data["tools"][tool_name]


# -------------------- VERSION VALIDATION --------------------

def validate_version(cfg, version):
    if version in ("", "latest"):
        return

    valid_versions = cfg.get("versions", [])
    if version not in valid_versions:
        raise ValueError(f"Invalid version '{version}'. Allowed: {', '.join(valid_versions)}")


# -------------------- INSTALL DETAILS --------------------

def _load_install_details():
    if not os.path.exists(INSTALL_DETAILS_FILE):
        return {"important_packages": []}

    with open(INSTALL_DETAILS_FILE, "r") as f:
        return yaml.safe_load(f) or {"important_packages": []}


def _save_install_details(data):
    with open(INSTALL_DETAILS_FILE, "w") as f:
        yaml.safe_dump(data, f)


def _upsert(package, installed, version, path):
    data = _load_install_details()
    pkgs = data.setdefault("important_packages", [])

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = next((p for p in pkgs if p["package_name"] == package), None)

    payload = {
        "package_name": package,
        "version": version if installed else "-",
        "installed": "Yes" if installed else "No",
        "installed_date": now if installed else "-",
        "install_directory": path if installed else {}
    }

    if entry:
        entry.update(payload)
    else:
        pkgs.append(payload)

    _save_install_details(data)


def _get_installed_entry(package):
    data = _load_install_details()
    for p in data.get("important_packages", []):
        if p.get("package_name") == package:
            return p
    return None


# -------------------- NETWORK --------------------

def _http_get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "tool-manager"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def _download(url, dest, log=print):
    try:
        log(f"Downloading {url}")
        with urllib.request.urlopen(url, timeout=60) as r:
            with open(dest, "wb") as f:
                f.write(r.read())
    except Exception as e:
        raise RuntimeError(f"Download failed: {e}")


# -------------------- GITHUB --------------------

def _fetch_release(cfg, version):
    if version in ("", "latest"):
        url = cfg["github"]["latest_api"]
    else:
        tag = version if version.startswith("v") else f"v{version}"
        url = cfg["github"]["tag_api"].format(tag=tag)

    data = _http_get_json(url)
    return data.get("tag_name"), data.get("assets", [])


def _pick_windows_asset(assets):
    keywords = ["windows", "win64", "mingw"]

    for a in assets:
        name = a.get("name", "").lower()
        url = a.get("browser_download_url", "")
        if url.endswith(".zip") and any(k in name for k in keywords):
            return url

    return None


# -------------------- INSTALL --------------------

def install_ghdl(version="latest", log=print):
    cfg = get_tool_cfg("GHDL")
    os_type = get_os()

    validate_version(cfg, version)


    if tool_exists(cfg["check"]):
        log("GHDL already installed")
        return

    if os_type == "windows":
        tag, assets = _fetch_release(cfg, version)
        url = _pick_windows_asset(assets)

        if not url:
            raise RuntimeError("No Windows build found")

        zip_path = os.path.join(TOOLS_DIR, "ghdl.zip")
        out_dir = os.path.join(TOOLS_DIR, "ghdl")

        _download(url, zip_path, log)

        import zipfile
        with zipfile.ZipFile(zip_path) as z:
            z.extractall(out_dir)

        os.remove(zip_path)

        log(f"⚠️ Add {out_dir}/bin to PATH")

        _upsert("ghdl", True, tag, {"root": out_dir})
        log("Installed GHDL (Windows)")

    elif os_type == "linux":
        deps = cfg.get("linux", {}).get("deps", [])
        if deps:
            run(["sudo", "apt-get", "install", "-y"] + deps, log)

        _install_from_source(cfg, version, log)

    elif os_type == "mac":
        if tool_exists("brew"):
            run(["brew", "install"] + cfg.get("mac", {}).get("deps", []), log)

        _install_from_source(cfg, version, log)


def _install_from_source(cfg, version, log):
    if version in ("", "latest"):
        version = cfg["recommended_version"]

    tarballs = cfg.get("source_tarballs", {})
    if version not in tarballs:
        raise RuntimeError("Version not supported")

    url = tarballs[version]

    work = os.path.join(TOOLS_DIR, "ghdl-src")
    os.makedirs(work, exist_ok=True)

    tar_path = os.path.join(work, "ghdl.tar.gz")
    _download(url, tar_path, log)

    with tarfile.open(tar_path) as tar:
        tar.extractall(work)

    dirs = [d for d in os.listdir(work) if os.path.isdir(os.path.join(work, d))]
    src = next((os.path.join(work, d) for d in dirs if "ghdl" in d.lower()), None)

    if not src:
        raise RuntimeError("GHDL source dir not found")

    try:
        run(["./configure"], log, cwd=src)
        run(["make"], log, cwd=src)
        run(["sudo", "make", "install"], log, cwd=src)
    except Exception as e:
        shutil.rmtree(work, ignore_errors=True)
        raise e

    shutil.rmtree(work, ignore_errors=True)

    install_paths = {
        "bin": shutil.which("ghdl") or "/usr/local/bin/ghdl",
        "lib": "/usr/local/lib/ghdl",
        "root": "/usr/local"
    }

    _upsert("ghdl", True, version, install_paths)
    log("Installed GHDL from source")


# -------------------- UNINSTALL --------------------

def uninstall_ghdl(log=print):
    os_type = get_os()

    log("=== UNINSTALLING GHDL ===")

    entry = _get_installed_entry("ghdl")

    if not entry or entry.get("installed") != "Yes":
        log("GHDL is not installed")
        return

    paths = entry.get("install_directory", {})

    if os_type == "windows":
        root = paths.get("root")
        if root and os.path.exists(root):
            shutil.rmtree(root)
            log("Removed GHDL directory")

    elif os_type == "linux":
        for key, p in paths.items():
            if p and os.path.exists(p):
                run(["sudo", "rm", "-rf", p], log)
                log(f"Removed {key}: {p}")

    elif os_type == "mac":
        if tool_exists("brew"):
            run(["brew", "uninstall", "ghdl"], log)
        else:
            for key, p in paths.items():
                if p and os.path.exists(p):
                    run(["sudo", "rm", "-rf", p], log)

    _upsert("ghdl", False, "-", {})
    log("GHDL uninstalled successfully")


