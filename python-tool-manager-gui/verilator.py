import os
import re
import shutil
import subprocess
import platform
import tempfile
from datetime import datetime
import logging
import yaml

BASE_DIR = os.path.dirname(__file__)
TOOLS_FILE = os.path.join(BASE_DIR, "tools.yml")
INSTALL_DETAILS_FILE = os.path.join(BASE_DIR, "install_details.yml")

# ---------------- LOGGING ---------------- #

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("verilator")

# ---------------- OS ---------------- #

def get_os():
    s = platform.system().lower()
    if "windows" in s:
        return "windows"
    if "linux" in s:
        return "linux"
    if "darwin" in s:
        return "mac"
    return None


def tool_exists(name):
    return shutil.which(name) is not None


# ---------------- RUN ---------------- #

def run(cmd, log=logger.info, cwd=None, retry=0, dry_run=False, env=None):
    display = cmd if isinstance(cmd, str) else " ".join(cmd)

    if dry_run:
        log(f"[DRY RUN] {display}")
        return

    for attempt in range(retry + 1):
        try:
            log(f"> {display}")

            p = subprocess.Popen(
                cmd,
                shell=isinstance(cmd, str),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=cwd,
                env=env
            )

            if p.stdout:
                for line in iter(p.stdout.readline, ""):
                    log(line.rstrip())

            p.wait(timeout=300)

            if p.returncode != 0:
                raise RuntimeError(f"Command failed: {display}")

            return

        except Exception as e:
            if attempt == retry:
                raise
            log(f"Retrying... ({attempt + 1})")


# ---------------- YAML ---------------- #

def load_cfg():
    with open(TOOLS_FILE) as f:
        data = yaml.safe_load(f) or {}
    return data.get("tools", {}).get("Verilator")


# ---------------- INSTALL DETAILS ---------------- #

def _load():
    if not os.path.exists(INSTALL_DETAILS_FILE):
        return {"important_packages": []}
    with open(INSTALL_DETAILS_FILE) as f:
        return yaml.safe_load(f) or {"important_packages": []}


def _save(d):
    with open(INSTALL_DETAILS_FILE, "w") as f:
        yaml.safe_dump(d, f, sort_keys=False)


def get_install_entry(name):
    data = _load()
    return next(
        (p for p in data.get("important_packages", []) if p["package_name"] == name),
        None
    )


def get_install_type(name):
    entry = get_install_entry(name)
    return entry.get("install_type") if entry else "unknown"


def _upsert(name, installed, version, path, install_type=None):
    data = _load()
    pkgs = data.setdefault("important_packages", [])

    entry = next((p for p in pkgs if p.get("package_name") == name), None)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # preserve install_type if not provided
    if not install_type and entry:
        install_type = entry.get("install_type")

    payload = {
        "package_name": name,
        "version": version if installed else "-",
        "installed": "Yes" if installed else "No",
        "installed_date": now if installed else "-",
        "install_directory": path if installed else "-",
        "install_type": install_type if installed else "-"
    }

    if entry:
        entry.update(payload)
    else:
        pkgs.append(payload)

    _save(data)


# ---------------- VERSION ---------------- #

def detect_version():
    if not tool_exists("verilator"):
        return None
    try:
        out = subprocess.check_output(["verilator", "--version"], text=True)
        m = re.search(r"verilator\s+([\d\.]+)", out, re.IGNORECASE)
        return m.group(1) if m else None
    except subprocess.CalledProcessError:
        return None


def validate_version(version, cfg):
    versions = cfg.get("versions", [])
    if version != "latest" and version not in versions:
        raise ValueError(f"Invalid version: {version}")


# ---------------- INSTALL ---------------- #

def _check_dependencies(tools):
    for t in tools:
        if not tool_exists(t):
            raise RuntimeError(f"Missing dependency: {t}")


def _install_linux(version, cfg, log, dry_run):
    linux = cfg["install"]["linux"]

    run("sudo apt-get update", log, dry_run=dry_run)

    deps = linux.get("deps", [])
    if deps:
        run(["sudo", "apt-get", "install", "-y"] + deps, log, dry_run=dry_run)

    _check_dependencies(["git", "make", "gcc"])

    repo = linux.get("repo")

    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, "verilator")

        run(["git", "clone", repo, src], log, dry_run=dry_run)

        if version.lower() != "latest":
            run(["git", "checkout", f"v{version}"], log, cwd=src, dry_run=dry_run)

        env = os.environ.copy()
        env["MAKEFLAGS"] = f"-j{os.cpu_count() or 2}"

        for cmd in linux.get("build", []):
            run(cmd, log, cwd=src, env=env, dry_run=dry_run)


def _install_windows(version, cfg, log, dry_run):
    pkg = cfg["install"]["windows"]["package"]

    if version == "latest":
        run(f"choco install -y {pkg}", log, dry_run=dry_run)
    else:
        run(f"choco install -y {pkg} --version={version}", log, dry_run=dry_run)


def _install_mac(cfg, log, dry_run):
    pkg = cfg["install"]["mac"]["package"]
    run(f"brew install {pkg}", log, dry_run=dry_run)


def install_verilator(version="latest", log=logger.info, dry_run=False):
    log("=== INSTALLING VERILATOR ===")

    cfg = load_cfg()
    if not cfg:
        raise RuntimeError("Verilator config missing in tools.yml")

    validate_version(version, cfg)

    os_type = get_os()
    installed_v = detect_version()

    if installed_v:
        if version == "latest" or installed_v == version:
            log(f"Already installed ({installed_v})")

            _upsert(
                "verilator",
                True,
                installed_v,
                shutil.which("verilator"),
                get_install_type("verilator")
            )
            return
        else:
            log(f"Different version detected ({installed_v}) → reinstalling")
            uninstall_verilator(log)

    if os_type == "linux":
        _install_linux(version, cfg, log, dry_run)
        install_type = "source"

    elif os_type == "windows":
        _install_windows(version, cfg, log, dry_run)
        install_type = "package"

    elif os_type == "mac":
        _install_mac(cfg, log, dry_run)
        install_type = "package"

    else:
        raise RuntimeError("Unsupported OS")

    v = detect_version()
    if not v:
        raise RuntimeError("Installation failed: version not detected")

    _upsert("verilator", True, v, shutil.which("verilator"), install_type)

    log(f"Installed Verilator {v}")


# ---------------- UNINSTALL ---------------- #

def _cleanup(log):
    paths = [
        os.path.expanduser("~/.cache/verilator"),
        os.path.expanduser("~/.verilator"),
    ]
    for p in paths:
        if os.path.exists(p):
            shutil.rmtree(p, ignore_errors=True)
            log(f"Removed {p}")


def uninstall_verilator(log=logger.info):
    log("=== UNINSTALLING VERILATOR ===")

    cfg = load_cfg()
    os_type = get_os()

    if not tool_exists(cfg["check"]):
        log("Not installed")
        _upsert("verilator", False, "-", "-", "-")
        return

    install_type = get_install_type("verilator")

    try:
        if os_type == "linux":
            if install_type == "source":
                log("Removing source installation safely")

                paths = [
                    "/usr/local/bin/verilator",
                    "/usr/local/share/verilator",
                    "/usr/local/include/verilator",
                ]

                for p in paths:
                    if os.path.exists(p):
                        run(["sudo", "rm", "-rf", p], log)

            else:
                run(["sudo", "apt-get", "purge", "-y", "verilator"], log)
                run(["sudo", "apt-get", "autoremove", "-y"], log)

        elif os_type == "windows":
            run("choco uninstall -y verilator", log)

        elif os_type == "mac":
            run("brew uninstall verilator", log)

        _cleanup(log)

        _upsert("verilator", False, "-", "-", "-")

        log("=== VERILATOR FULLY REMOVED ===")

    except Exception as e:
        log(f"[ERROR] {e}")
        raise