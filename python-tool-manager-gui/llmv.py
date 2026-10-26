import os
import re
import shutil
import subprocess
import platform
from datetime import datetime
import yaml


INSTALL_DETAILS_FILE = os.path.join(os.path.dirname(__file__), "install_details.yml")


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


def tool_exists(name):
    return shutil.which(name) is not None


# ---------------- RUN ---------------- #

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
        for line in p.stdout:
            log(line.rstrip())

    p.wait()
    if p.returncode != 0:
        raise RuntimeError(f"Command failed: {display}")


# ---------------- VERSION DETECTION ---------------- #

def detect_llvm_version():
    """
    Primary: llvm-config (REAL LLVM)
    Fallback: clang ONLY if it's from brew/apt/choco (not system clang)
    """

    # ✅ Primary check
    try:
        path = shutil.which("llvm-config")
        if path:
            return subprocess.check_output(
                ["llvm-config", "--version"], text=True
            ).strip()
    except:
        pass

    # ⚠️ Fallback (only if not system clang)
    try:
        clang_path = shutil.which("clang")
        if clang_path and "homebrew" in clang_path.lower() or "llvm" in clang_path.lower():
            out = subprocess.check_output(["clang", "--version"], text=True)
            m = re.search(r"clang version\s+(\d+(\.\d+){0,2})", out, re.IGNORECASE)
            if m:
                return m.group(1)
    except:
        pass

    return None


def is_llvm_installed():
    """
    True only if REAL LLVM is installed (not system clang)
    """
    return shutil.which("llvm-config") is not None


# ---------------- INSTALL DETAILS ---------------- #

def _load():
    if not os.path.exists(INSTALL_DETAILS_FILE):
        return {"important_packages": []}
    with open(INSTALL_DETAILS_FILE) as f:
        return yaml.safe_load(f) or {"important_packages": []}


def _save(data):
    with open(INSTALL_DETAILS_FILE, "w") as f:
        yaml.safe_dump(data, f, sort_keys=False)


def _upsert(name, installed, version, path):
    data = _load()
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

    _save(data)


# ---------------- WINDOWS VERSION SUPPORT ---------------- #

def _choco_versions(log):
    try:
        result = subprocess.run(
            "choco search llvm --exact --all-versions",
            shell=True,
            capture_output=True,
            text=True
        )
        versions = []
        for line in result.stdout.splitlines():
            if line.lower().startswith("llvm "):
                versions.append(line.split()[1])
        return versions
    except Exception as e:
        log(f"Failed to fetch versions: {e}")
        return []


def _pick_version(requested, versions):
    if requested in ("", "latest"):
        return sorted(versions, reverse=True)[0] if versions else "latest"

    if requested in versions:
        return requested

    prefix = requested + "."
    matches = [v for v in versions if v.startswith(prefix)]

    return sorted(matches, reverse=True)[0] if matches else None


# ---------------- INSTALL ---------------- #

def install_llvm(version="latest", log=print):
    log("=== INSTALLING LLVM ===")

    os_type = get_os()

    # ✅ Correct check
    if is_llvm_installed():
        v = detect_llvm_version() or "-"
        log(f"LLVM already installed ({v})")
        _upsert("llvm", True, v, shutil.which("llvm-config"))
        return

    if os_type == "windows":
        if not tool_exists("choco"):
            raise RuntimeError("Chocolatey not installed")

        versions = _choco_versions(log)
        chosen = _pick_version(version, versions)

        if chosen == "latest":
            run("choco install -y llvm", log)
        elif chosen:
            run(f"choco install -y llvm --version={chosen}", log)
        else:
            raise RuntimeError(f"Version {version} not found")

    elif os_type == "mac":
        if not tool_exists("brew"):
            raise RuntimeError("Homebrew not installed")

        run("brew install llvm", log)

        # 🔥 fix PATH (important for detection)
        try:
            prefix = subprocess.check_output(["brew", "--prefix", "llvm"], text=True).strip()
            os.environ["PATH"] += os.pathsep + os.path.join(prefix, "bin")
        except:
            pass

    elif os_type == "linux":
        run("sudo apt-get update", log)
        run("sudo apt-get install -y llvm clang", log)

    else:
        log("Unsupported OS")
        return

    v = detect_llvm_version() or version
    _upsert("llvm", True, v, shutil.which("llvm-config"))

    log(f"=== INSTALLED LLVM {v} ===")


# ---------------- UNINSTALL ---------------- #

def uninstall_llvm(log=print):
    log("=== UNINSTALLING LLVM ===")

    os_type = get_os()

    if not is_llvm_installed():
        log("LLVM not installed (real LLVM not found)")
        _upsert("llvm", False, "-", "-")
        return

    try:
        if os_type == "windows":
            run("choco uninstall -y llvm", log)

        elif os_type == "mac":
            # try both
            try:
                run("brew uninstall llvm", log)
            except:
                log("[INFO] llvm not found in brew")

            run("brew cleanup", log)

        elif os_type == "linux":
            run("sudo apt-get remove -y llvm clang", log)
            run("sudo apt-get autoremove -y", log)

        else:
            log("Unsupported OS")
            return

    except Exception as e:
        log(f"[ERROR] {e}")
        return

    _upsert("llvm", False, "-", "-")
    log("=== LLVM REMOVED ===")