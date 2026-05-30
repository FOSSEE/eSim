import os
import re
import shutil
import subprocess
import sys
import platform
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import yaml


# =========================
# 📁 PATHS
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

VENV_NAME = "toolmanagervenv"
VENV_PATH = os.path.join(BASE_DIR, VENV_NAME)

TOOLS_FILE = os.path.join(BASE_DIR, "tools.yml")
INSTALL_DETAILS_YML = os.path.join(BASE_DIR, "install_details.yml")


# =========================
# 🖥️ OS DETECTION
# =========================
def get_os():
    system = platform.system().lower()
    if "windows" in system:
        return "windows"
    if "linux" in system:
        return "linux"
    if "darwin" in system:
        return "mac"
    return None


# =========================
# ⚙️ COMMAND RUNNER
# =========================
def run(cmd, log=print, cwd=None):
    display_cmd = cmd if isinstance(cmd, str) else " ".join(cmd)
    log(f"> {display_cmd}")

    p = subprocess.Popen(
        cmd,
        shell=isinstance(cmd, str),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        cwd=cwd,
    )

    output = []

    if p.stdout:
        for line in iter(p.stdout.readline, ""):
            if not line:
                break
            line = line.rstrip()
            output.append(line)
            log(line)

    p.wait()
    if p.returncode != 0:
        raise RuntimeError(f"Command failed: {display_cmd}\n" + "\n".join(output))

    return "\n".join(output)


# =========================
# 📄 YAML TRACKING
# =========================
def _load_install_details_yml():
    if not os.path.exists(INSTALL_DETAILS_YML):
        return {"important_packages": []}

    with open(INSTALL_DETAILS_YML, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    data.setdefault("important_packages", [])
    return data


def _save_install_details_yml(data):
    with open(INSTALL_DETAILS_YML, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False)


def _upsert_install_details(package_name, installed, version, install_directory):
    data = _load_install_details_yml()
    pkgs = data["important_packages"]

    entry = next((p for p in pkgs if p["package_name"].lower() == package_name.lower()), None)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    payload = {
        "package_name": package_name,
        "version": version if installed else "-",
        "installed": "Yes" if installed else "No",
        "installed_date": now if installed else "-",
        "install_directory": install_directory if installed else "-",
    }

    if entry:
        entry.update(payload)
    else:
        pkgs.append(payload)

    _save_install_details_yml(data)


# =========================
# 📦 LOAD CONFIG
# =========================
def _load_python_section():
    if not os.path.exists(TOOLS_FILE):
        return [], []

    with open(TOOLS_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    python_tool = data.get("tools", {}).get("Python", {})

    return python_tool.get("pip_packages", []), python_tool.get("dependencies", [])


# =========================
# 🧱 SYSTEM DEPENDENCIES
# =========================
def _is_installed_cmd(cmd):
    return shutil.which(cmd) is not None


def _install_system_package(pkg, log):
    os_type = get_os()

    try:
        if os_type == "linux":
            run(["sudo", "apt-get", "install", "-y", pkg], log)
        elif os_type == "mac":
            run(["brew", "install", pkg], log)
        elif os_type == "windows":
            run(["winget", "install", "--id", pkg, "-e", "--silent"], log)
        else:
            raise RuntimeError("Unsupported OS")

        _upsert_install_details(pkg, True, "-", "/usr/bin")
        return True

    except Exception as e:
        log(f"[ERROR] {pkg} failed: {e}")
        _upsert_install_details(pkg, False, "-", "-")
        return False


def _handle_system_dependencies(deps, log=print):
    missing = []

    for dep in deps:
        if _is_installed_cmd(dep):
            log(f"[OK] {dep} already installed")
            _upsert_install_details(dep, True, "-", "/usr/bin")
        else:
            missing.append(dep)

    if not missing:
        return

    log(f"Installing {len(missing)} system packages...")

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(_install_system_package, pkg, log) for pkg in missing]
        for f in as_completed(futures):
            f.result()


def _update_system_packages(log=print):
    os_type = get_os()

    try:
        if os_type == "linux":
            run(["sudo", "apt-get", "update"], log)
            run(["sudo", "apt-get", "upgrade", "-y"], log)
        elif os_type == "mac":
            run(["brew", "update"], log)
            run(["brew", "upgrade"], log)
        elif os_type == "windows":
            run(["winget", "upgrade", "--all"], log)
    except Exception as e:
        log(f"[ERROR] System update failed: {e}")


# =========================
# 🐍 VENV + PIP
# =========================
def _venv_python():
    if get_os() == "windows":
        return os.path.join(VENV_PATH, "Scripts", "python.exe")
    return os.path.join(VENV_PATH, "bin", "python")


def _ensure_venv(log=print):
    if not os.path.exists(_venv_python()):
        log("Creating virtual environment...")
        run([sys.executable, "-m", "venv", VENV_PATH], log)


def _ensure_pip(log=print):
    py = _venv_python()
    run([py, "-m", "ensurepip", "--upgrade"], log)
    run([py, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"], log)


# =========================
# 📦 VERSION HANDLING
# =========================
def _get_pip_version(pkg):
    py = _venv_python()
    name = pkg.split("==")[0]

    try:
        out = subprocess.check_output([py, "-m", "pip", "show", name], text=True)
        for line in out.splitlines():
            if line.startswith("Version:"):
                return line.split(":")[1].strip()
    except Exception:
        return None


def _get_latest_pip_version(pkg):
    py = _venv_python()
    name = pkg.split("==")[0]

    try:
        out = subprocess.check_output([py, "-m", "pip", "index", "versions", name], text=True)
        match = re.search(r"Available versions:\s*(.*)", out)
        if match:
            return match.group(1).split(",")[0].strip()
    except Exception:
        return None


def _pip_installed(pkg):
    return _get_pip_version(pkg) is not None


# =========================
# 📦 PIP INSTALL (PARALLEL)
# =========================
def _pip_install(packages, log=print):
    py = _venv_python()

    def install(pkg):
        for i in range(3):
            try:
                log(f"Installing {pkg} (attempt {i+1})")
                run([py, "-m", "pip", "install", pkg], log)

                version = _get_pip_version(pkg)
                _upsert_install_details(pkg, True, version, VENV_PATH)
                return
            except Exception as e:
                log(f"[RETRY] {pkg}: {e}")

        _upsert_install_details(pkg, False, "-", "-")

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(install, pkg) for pkg in packages]
        for f in as_completed(futures):
            f.result()


# =========================
# 🔄 UPDATE PIP PACKAGES
# =========================
def _update_pip_packages(packages, log=print):
    py = _venv_python()

    for pkg in packages:
        name = pkg.split("==")[0]

        current = _get_pip_version(pkg)
        latest = _get_latest_pip_version(pkg)

        if not current or not latest:
            log(f"[SKIP] {name} version check failed")
            continue

        if current == latest:
            log(f"[OK] {name} already latest ({current})")
            continue

        log(f"[UPDATE] {name}: {current} → {latest}")

        try:
            run([py, "-m", "pip", "install", "--upgrade", name], log)

            new_version = _get_pip_version(pkg)
            _upsert_install_details(name, True, new_version, VENV_PATH)

        except Exception as e:
            log(f"[ERROR] {name} update failed: {e}")


# =========================
# 🚀 INSTALL
# =========================
def install_python(log=print):

    _ensure_venv(log)
    _ensure_pip(log)

    pip_packages, dependencies = _load_python_section()

    _handle_system_dependencies(dependencies, log)

    missing = [p for p in pip_packages if not _pip_installed(p)]

    if missing:
        log(f"Installing {len(missing)} pip packages...")
        _pip_install(missing, log)

    failed = [p for p in pip_packages if not _pip_installed(p)]

    if failed:
        raise RuntimeError(f"Failed packages: {', '.join(failed)}")

    py_ver = subprocess.check_output([sys.executable, "--version"], text=True).strip()
    _upsert_install_details("python", True, py_ver, sys.executable)

    log("✅ INSTALL COMPLETE")


# =========================
# 🔄 UPDATE (BUTTON LOGIC)
# =========================
def update_python(log=print):

    log("🔄 Checking for updates...")

    pip_packages, dependencies = _load_python_section()

    _update_pip_packages(pip_packages, log)
    _update_system_packages(log)

    log("✅ UPDATE COMPLETE")

# =========================
# 🧹 UNINSTALL
# =========================
def _pip_uninstall(packages, log=print):
    py = _venv_python()

    def uninstall(pkg):
        name = pkg.split("==")[0]
        try:
            if _pip_installed(pkg):
                log(f"Uninstalling {name}...")
                run([py, "-m", "pip", "uninstall", "-y", name], log)
                _upsert_install_details(name, False, "-", "-")
            else:
                log(f"[SKIP] {name} not installed")
        except Exception as e:
            log(f"[ERROR] Failed to uninstall {name}: {e}")
            _upsert_install_details(name, False, "-", "-")

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(uninstall, pkg) for pkg in packages]
        for f in as_completed(futures):
            f.result()

## UNINSTALL 

def _uninstall_system_package(pkg, log=print):
    os_type = get_os()

    try:
        if os_type == "linux":
            run(["sudo", "apt-get", "remove", "-y", pkg], log)
        elif os_type == "mac":
            run(["brew", "uninstall", pkg], log)
        elif os_type == "windows":
            run(["winget", "uninstall", "--id", pkg, "-e", "--silent"], log)
        else:
            raise RuntimeError("Unsupported OS")

        _upsert_install_details(pkg, False, "-", "-")
        return True

    except Exception as e:
        log(f"[ERROR] {pkg} uninstall failed: {e}")
        return False


def _handle_uninstall_system_dependencies(deps, log=print):
    log(f"Uninstalling {len(deps)} system packages...")

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(_uninstall_system_package, pkg, log) for pkg in deps]
        for f in as_completed(futures):
            f.result()


def _remove_venv(log=print):
    if os.path.exists(VENV_PATH):
        log("Removing virtual environment...")
        try:
            shutil.rmtree(VENV_PATH)
            log("Venv removed")
        except Exception as e:
            log(f"[ERROR] Failed to remove venv: {e}")
    else:
        log("[SKIP] No virtual environment found")


# =========================
# 🧨 MAIN UNINSTALL FUNCTION
# =========================
def uninstall_python(log=print):

    log("🧹 Starting full uninstall...")

    pip_packages, dependencies = _load_python_section()

    # 1️⃣ Uninstall pip packages
    if os.path.exists(_venv_python()):
        _pip_uninstall(pip_packages, log)
    else:
        log("[SKIP] Venv not found, skipping pip uninstall")

    # 2️⃣ Remove system dependencies
    if dependencies:
        _handle_uninstall_system_dependencies(dependencies, log)

    # 3️⃣ Remove virtual environment
    _remove_venv(log)

    # 4️⃣ Mark python as uninstalled
    _upsert_install_details("python", False, "-", "-")

    log("✅ UNINSTALL COMPLETE")