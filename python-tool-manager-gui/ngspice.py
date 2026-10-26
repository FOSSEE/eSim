import os
import re
import shutil
import subprocess
import tarfile
import platform
import urllib.request
import tempfile
from datetime import datetime

import yaml


BASE_DIR = os.path.dirname(__file__)
TOOLS_FILE = os.path.join(BASE_DIR, "tools.yml")
INSTALL_DETAILS_FILE = os.path.join(BASE_DIR, "install_details.yml")


# ---------------- OS ---------------- #

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
    display = cmd if isinstance(cmd, str) else " ".join(cmd)
    log(f"> {display}")

    p = subprocess.Popen(
        cmd,
        shell=isinstance(cmd, str),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        cwd=cwd,
    )

    if p.stdout:
        for line in iter(p.stdout.readline, ""):
            log(line.rstrip())

    p.wait()
    if p.returncode != 0:
        log(f"Command failed: {display}")
        return   #  don't crash whole app


# ---------------- YAML ---------------- #

def load_ngspice_config():
    try:
        with open(TOOLS_FILE, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except Exception as e:
        raise RuntimeError(f"Failed to load tools.yml: {e}")

    tools = data.get("tools", {})
    if "ngspice" not in tools:
        raise RuntimeError("ngspice config not found in tools.yml")

    return tools["ngspice"]


# ---------------- INSTALL DETAILS ---------------- #

def _load_install_details():
    if not os.path.exists(INSTALL_DETAILS_FILE):
        return {"important_packages": []}
    with open(INSTALL_DETAILS_FILE) as f:
        return yaml.safe_load(f) or {"important_packages": []}


def _save_install_details(data):
    with open(INSTALL_DETAILS_FILE, "w") as f:
        yaml.safe_dump(data, f, sort_keys=False)


def _upsert(name, installed, version, path):
    data = _load_install_details()
    pkgs = data.setdefault("important_packages", [])

    entry = next((p for p in pkgs if p.get("package_name") == name), None)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    payload = {
        "package_name": name,
        "version": version if installed else "-",
        "installed": "Yes" if installed else "No",
        "installed_date": now if installed else "-",
        "install_directory": path if installed else "-",
    }

    if entry:
        entry.update(payload)
    else:
        pkgs.append(payload)

    _save_install_details(data)


# ---------------- VERSION ---------------- #

def tool_exists(name):
    return shutil.which(name) is not None


def _extract_version(output):
    patterns = [
        r"ngspice[-\s]*([\d\.]+)",
        r"(\d+\.\d+(\.\d+)?)"
    ]

    for p in patterns:
        match = re.search(p, output, re.IGNORECASE)
        if match:
            return match.group(1)

    return None


def detect_version(cfg):
    if not tool_exists(cfg.get("check")):
        return None

    commands = cfg.get("version_cmd")
    if not commands:
        return None

    if isinstance(commands, str):
        commands = [commands]

    for cmd in commands:
        try:
            result = subprocess.run(
                cmd.split(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            output = (result.stdout or "") + (result.stderr or "")
            version = _extract_version(output)

            if version:
                return version

        except Exception:
            continue

    return None


def resolve_version(requested, available):
    requested = (requested or "").strip()

    if requested in ("", "latest"):
        return available[0]

    if requested in available:
        return requested

    prefix = requested + "."
    matches = [v for v in available if v.startswith(prefix)]

    if matches:
        return sorted(matches, reverse=True)[0]

    return requested


# ---------------- DOWNLOAD ---------------- #

def _download(url, dest, log):
    log(f"Downloading: {url}")
    with urllib.request.urlopen(url) as r, open(dest, "wb") as f:
        shutil.copyfileobj(r, f)


# ---------------- INSTALL ---------------- #

def install_linux(version, cfg, log):
    linux_cfg = cfg["install"]["linux"]

    run("sudo apt-get update", log)

    deps = linux_cfg.get("deps", [])
    if deps:
        run(["sudo", "apt-get", "install", "-y"] + deps, log)

    url = linux_cfg["url_template"].format(version=version)

    with tempfile.TemporaryDirectory() as tmp:
        archive = os.path.join(tmp, "ngspice.tar.gz")
        _download(url, archive, log)

        with tarfile.open(archive) as tar:
            tar.extractall(tmp)

        src = next(
            (os.path.join(tmp, d) for d in os.listdir(tmp) if d.startswith("ngspice-")),
            None,
        )

        if not src:
            raise RuntimeError("Source folder not found")

        for cmd in linux_cfg.get("build", []):
            run(cmd, log, cwd=src)


def install_windows(version, cfg, log):
    win_cfg = cfg["install"]["windows"]

    base_dir = os.path.join(os.getcwd(), "tools")
    os.makedirs(base_dir, exist_ok=True)

    archive = os.path.join(base_dir, win_cfg["archive_name"].format(version=version))
    out_folder = os.path.join(base_dir, win_cfg["extract_folder"].format(version=version))

    url = win_cfg["url_template"].format(version=version)
    fallback = win_cfg["fallback_url_template"].format(version=version)

    # -------- Download with fallback -------- #
    try:
        _download(url, archive, log)
    except Exception:
        log("Main URL failed, trying fallback...")
        try:
            _download(fallback, archive, log)
        except Exception:
            raise RuntimeError(f"❌ Failed to download ngspice {version}")

    os.makedirs(out_folder, exist_ok=True)

    # -------- 7z check -------- #
    if not tool_exists("7z"):
        raise RuntimeError("❌ 7-Zip not found. Install it first.")

    run(f'7z x "{archive}" -o"{out_folder}"', log)

    log(f"✅ Ngspice {version} installed at {out_folder}")
    log(f"👉 Add to PATH: {out_folder}")


def install_mac(cfg, log):
    if not tool_exists("brew"):
        raise RuntimeError("brew not installed")

    pkg = cfg["install"]["mac"].get("package", "ngspice")
    run(f"brew install {pkg}", log)


def install_ngspice(version="latest", log=print):
    log("=== INSTALLING NGSPICE ===")

    cfg = load_ngspice_config()
    os_type = get_os()

    if tool_exists(cfg.get("check")):
        v = detect_version(cfg) or "-"
        log(f"Already installed ({v})")
        _upsert("ngspice", True, v, shutil.which("ngspice"))
        return

    available = cfg.get("versions", [])
    version = resolve_version(version, available)

    log(f"Requested: {version}")

    if os_type == "linux":
        install_linux(version, cfg, log)

    elif os_type == "windows":
        install_windows(version, cfg, log)

    elif os_type == "mac":
        install_mac(cfg, log)

    else:
        raise RuntimeError("Unsupported OS")

    v = detect_version(cfg) or version
    _upsert("ngspice", True, v, shutil.which("ngspice") or "-")

    log(f"=== INSTALLED NGSPICE {v} ===")


# ---------------- UNINSTALL ---------------- #

def _cleanup(log=print):
    paths = [
        os.path.expanduser("~/.ngspice"),
        os.path.expanduser("~/.cache/ngspice"),
    ]

    for p in paths:
        if os.path.exists(p):
            shutil.rmtree(p, ignore_errors=True)
            log(f"Removed {p}")


def uninstall_ngspice(log=print):
    log("=== UNINSTALLING NGSPICE ===")

    cfg = load_ngspice_config()
    os_type = get_os()

    if not tool_exists(cfg.get("check")):
        log("Not installed")
        _upsert("ngspice", False, "-", "-")
        return

    try:
        if os_type == "linux":
            run(["sudo", "apt-get", "remove", "-y", "ngspice"], log)
            run(["sudo", "apt-get", "autoremove", "-y"], log)

        elif os_type == "windows":
            run("choco uninstall -y ngspice", log)

        elif os_type == "mac":
            run("brew uninstall ngspice", log)

        _cleanup(log)

        _upsert("ngspice", False, "-", "-")

        log("=== NGSPICE FULLY REMOVED ===")

    except Exception as e:
        log(f"[ERROR] {e}")
        return

