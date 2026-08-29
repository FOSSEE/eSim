import json
import os
import platform
import re
import shutil
import subprocess
import urllib.error
import urllib.request
import time
from datetime import datetime

import yaml

try:
    from .version import get_version
except ImportError:
    from version import get_version


TOOLS_DIR = os.path.expanduser("~/esim-tools-bin")
os.makedirs(TOOLS_DIR, exist_ok=True)

BASE_DIR = os.path.dirname(__file__)
TOOLS_FILE = os.path.join(BASE_DIR, "tools.yml")
INSTALL_DETAILS_FILE = os.path.join(BASE_DIR, "install_details.yml")

KICAD_RELEASES_API = (
    "https://api.github.com/repos/KiCad/kicad-source-mirror/releases?per_page=100"
)



def get_os():
    # Keep OS naming aligned with the rest of the tool manager modules.
    system = platform.system().lower()
    if "windows" in system:
        return "windows"
    if "linux" in system:
        return "linux"
    if "darwin" in system:
        return "mac"
    return None


def run(cmd, log=print, cwd=None):
    display_cmd = cmd if isinstance(cmd, str) else " ".join(cmd)
    log(f"> {display_cmd}")

    try:
        process = subprocess.Popen(
            cmd,
            shell=isinstance(cmd, str),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=cwd,
        )

        for line in iter(process.stdout.readline, ""):
            if not line:
                break
            log(line.rstrip())

        process.wait()

        if process.returncode != 0:
            log(f"[ERROR] Command failed: {display_cmd}")
            return False

        return True

    except Exception as e:
        log(f"[ERROR] {e}")
        return False


def load_tools():
    # Parse and validate the shared tool manifest once per call.
    try:
        with open(TOOLS_FILE, "r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
    except Exception as exc:
        raise RuntimeError(f"Failed to load tools.yml: {exc}") from exc

    tools = data.get("tools", {})
    if not isinstance(tools, dict):
        raise RuntimeError("Invalid tools.yml: 'tools' must be a mapping")
    return tools


def get_kicad_config():
    # Match the tool by normalized name so YAML display casing does not matter.
    tools = load_tools()
    for name, config in tools.items():
        if str(name).strip().lower() == "kicad":
            if not isinstance(config, dict):
                raise RuntimeError("Invalid Kicad config in tools.yml")
            return config
    raise RuntimeError("Kicad config not found in tools.yml")


def tool_exists(names):
    if isinstance(names, str):
        names = [names]
    return any(shutil.which(name) for name in names)


def find_kicad_install_path(): 
   # KiCad is not always on PATH, especially for app-bundle installs on macOS.
    config = get_kicad_config()
    candidates = []

    for path in config.get("install_paths", []):
        if path == "auto":
            auto_path = shutil.which("kicad")
            if auto_path:
                candidates.append(auto_path)
        else:
            candidates.append(path)

    for path in candidates:
        if path and os.path.exists(path):
            return path

    return "-"


def detect_installed_kicad_version(config):
    # Prefer the configured version command, then fall back to path-based detection.
    version_cmd = config.get("version_cmd")
    version = get_version(version_cmd)
    if version:
        return version
    install_path = find_kicad_install_path()
    if install_path not in ("", "-"):
        return "installed"
    return None


def _load_install_details():
    try:
        if not os.path.exists(INSTALL_DETAILS_FILE):
            return {"important_packages": []}
        with open(INSTALL_DETAILS_FILE, "r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
        if not isinstance(data, dict):
            return {"important_packages": []}
        packages = data.get("important_packages")
        if not isinstance(packages, list):
            data["important_packages"] = []
        return data
    except Exception:
        return {"important_packages": []}


def _save_install_details(data):
    with open(INSTALL_DETAILS_FILE, "w", encoding="utf-8") as handle:
        yaml.safe_dump(data, handle, sort_keys=False) 


def _upsert_install_details(package_name, installed, version, install_directory):
    # Preserve other package entries while updating the current tool in place.
    data = _load_install_details()
    packages = data.setdefault("important_packages", [])

    entry = None
    for pkg in packages:
        if isinstance(pkg, dict) and str(pkg.get("package_name", "")).lower() == package_name.lower():
            entry = pkg
            break

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload = {
        "package_name": package_name,
        "version": version if installed else "-",
        "installed": "Yes" if installed else "No",
        "installed_date": now if installed else "-",
        "install_directory": install_directory if installed else "-",
    }

    if entry is None:
        packages.append(payload)
    else:
        entry.update(payload)

    _save_install_details(data)


def _fetch_release_assets(log=print):
    # Query release metadata so we can match real asset names instead of guessing URLs.
    req = urllib.request.Request(
        KICAD_RELEASES_API,
        headers={"User-Agent": "tool_manager_gui"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        log(f"Failed to query KiCad releases: {exc}")
        return []
    except Exception as exc:
        log(f"Failed to parse KiCad release data: {exc}")
        return []

    releases = []
    if not isinstance(payload, list):
        return releases

    for item in payload:
        if not isinstance(item, dict):
            continue
        tag_name = str(item.get("tag_name", "")).strip()
        assets = item.get("assets", [])
        if tag_name:
            releases.append({"tag_name": tag_name, "assets": assets if isinstance(assets, list) else []})
    return releases


def _release_sort_key(tag):
    # Stable releases sort ahead of prereleases with the same numeric version.
    match = re.match(r"^v?(\d+)\.(\d+)\.(\d+)(.*)$", tag)
    if not match:
        return (-1, -1, -1, -1, tag)
    major, minor, patch = (int(match.group(i)) for i in range(1, 4))
    suffix = (match.group(4) or "").lower()
    stable_bonus = 1 if not suffix else 0
    return (major, minor, patch, stable_bonus, suffix)


def resolve_requested_version(requested, available_versions):
    # Support "latest", exact versions, and short prefixes like "7" or "7.0".
    requested = (requested or "").strip()
    if not available_versions:
        return requested or "latest"
    if requested == "" or requested.lower() == "latest":
        return available_versions[0]
    if requested in available_versions:
        return requested

    prefix = requested
    if re.fullmatch(r"\d+\.\d+", requested):
        prefix = requested + "."
    elif re.fullmatch(r"\d+", requested):
        prefix = requested + "."

    matches = [version for version in available_versions if str(version).startswith(prefix)]
    if matches:
        return sorted(matches, key=_release_sort_key, reverse=True)[0]
    return requested


def _select_release_for_version(version, releases):
    # Normalize GitHub tags like "v8.0.0" against plain requested versions like "8.0.0".
    if not releases:
        return None

    tags = [release["tag_name"] for release in releases]
    target_tag = resolve_requested_version(version, tags)
    if target_tag.lower() == "latest":
        return releases[0]

    for release in releases:
        if release["tag_name"] == target_tag:
            return release

    normalized_target = target_tag.lstrip("v")
    for release in releases:
        if release["tag_name"].lstrip("v") == normalized_target:
            return release
    return None


def _find_asset_url(release, patterns):
    # Match assets by filename hints because KiCad release names vary across platforms.
    if not release:
        return None
    for asset in release.get("assets", []):
        if not isinstance(asset, dict):
            continue
        name = str(asset.get("name", "")).lower()
        url = str(asset.get("browser_download_url", "")).strip()
        if not url:
            continue
        if all(pattern in name for pattern in patterns):
            return url, asset.get("name") or os.path.basename(url)
    return None


def _download(url, dest_path, log=print, progress_cb=None):
    """
    Download file with real progress, speed, ETA.
    progress_cb(percent, speed_MBps, eta_sec) -> optional for GUI
    """

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    log(f"Downloading: {url}")

    req = urllib.request.Request(url, headers={"User-Agent": "tool_manager_gui"})

    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            total_size = int(response.getheader("Content-Length", 0))
            downloaded = 0
            chunk_size = 1024 * 1024  # 1 MB
            start_time = time.time()

            with open(dest_path, "wb") as f:
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break

                    f.write(chunk)
                    downloaded += len(chunk)

                    elapsed = time.time() - start_time
                    speed = downloaded / (1024 * 1024) / elapsed if elapsed > 0 else 0
                    remaining = total_size - downloaded
                    eta = (remaining / (1024 * 1024) / speed) if speed > 0 else 0

                    percent = (downloaded / total_size * 100) if total_size else 0

                    msg = f"{percent:.1f}% | {speed:.2f} MB/s | ETA: {eta:.1f}s"
                    log(msg)

                    if progress_cb:
                        progress_cb(percent, speed, eta)

    except Exception as e:
        raise RuntimeError(f"Download failed: {e}")

    log("Download complete ✅")
    return dest_path


def _choco_available():
    return tool_exists("choco")


def _choco_list_versions(log=print):
    # Chocolatey gives us the most reliable version-pinned install path on Windows.
    try:
        result = subprocess.run(
            "choco search kicad --exact --all-versions",
            shell=True,
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception as exc:
        log(f"Failed to fetch KiCad versions from Chocolatey: {exc}")
        return []

    versions = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line.lower().startswith("kicad "):
            continue
        parts = line.split()
        if len(parts) >= 2:
            versions.append(parts[1].strip())
    return versions


def _ppa_exists(ppa_keyword):
    """Check if a PPA is already added."""
    sources_dir = "/etc/apt/sources.list.d"
    if not os.path.exists(sources_dir):
        return False
    return any(ppa_keyword in fname for fname in os.listdir(sources_dir))


def install_kicad_linux(version, log=print):
    log(f"Installing KiCad on Linux ({version})")

    config = get_kicad_config()
    linux_config = config.get("linux", {})
    ppas = linux_config.get("ppas", {})

    version_str = str(version).lower()

    # 🧠 Find matching PPA
    selected_ppa = None
    for prefix, ppa_info in ppas.items():
        if version_str.startswith(prefix):
            selected_ppa = ppa_info
            break

    # ➕ Add PPA
    if selected_ppa:
        repo = selected_ppa.get("repo")
        key = selected_ppa.get("key")

        if repo and not _ppa_exists(key):
            log(f"Adding PPA: {repo}")
            run(["sudo", "add-apt-repository", "-y", repo], log)
        else:
            log("PPA already exists or invalid config, skipping...")

    # 🔄 Update
    run(["sudo", "apt-get", "update"], log)

    # 📦 Install
    if version_str == "latest":
        run(["sudo", "apt-get", "install", "-y", "kicad"], log)
    else:
        version_prefix = f"{version}*"
        run(["sudo", "apt-get", "install", "-y", f"kicad={version_prefix}"], log)


def install_kicad_windows(version, log=print):
    if _choco_available():
        available_versions = _choco_list_versions(log)
        chosen = resolve_requested_version(version, available_versions)
        if str(chosen).lower() == "latest":
            run("choco install -y kicad", log)
        elif chosen in available_versions:
            run(f"choco install -y kicad --version={chosen}", log)
        else:
            log("Requested version not found in Chocolatey. Falling back to official installer.")
            chosen = None

        if chosen is not None:
            return chosen, find_kicad_install_path()

    # Fall back to the official release artifact if Chocolatey is unavailable or insufficient.
    releases = _fetch_release_assets(log)
    release = _select_release_for_version(version, releases)
    asset = _find_asset_url(release, patterns=["x86_64", ".exe"])
    if asset is None:
        asset = _find_asset_url(release, patterns=[".exe"])
    if asset is None:
        raise RuntimeError("No suitable KiCad Windows installer asset found.")

    url, filename = asset
    installer_path = os.path.join(TOOLS_DIR, filename)
    _download(url, installer_path, log)
    run([installer_path, "/S"], log)

    installed_version = release["tag_name"].lstrip("v") if release else version
    return installed_version, find_kicad_install_path()



def install_kicad(version="latest", log=print, progress_cb=None):
    # The public entrypoint keeps policy decisions here and delegates OS details below.
    config = get_kicad_config()
    os_type = get_os()
    if os_type is None:
        raise RuntimeError("Unsupported OS")

    installed_version = detect_installed_kicad_version(config)
    if installed_version:
        install_path = find_kicad_install_path()
        log(f"KiCad already installed (version: {installed_version}). Skipping installation.")
        _upsert_install_details("kicad", True, installed_version, install_path)
        return

    available_versions = config.get("versions", [])
    selected_version = resolve_requested_version(version, available_versions)
    log(f"Requested KiCad version: {version}")
    log(f"Resolved KiCad version: {selected_version}")

    if os_type == "linux":
        install_kicad_linux(selected_version, log)
        final_version = detect_installed_kicad_version(config) or selected_version
        install_path = find_kicad_install_path()
    elif os_type == "windows":
        final_version, install_path = install_kicad_windows(selected_version, log)
    elif os_type == "mac":
        final_version, install_path = install_kicad_macos(selected_version, log)
    else:
        raise RuntimeError("Unsupported OS")

    _upsert_install_details("kicad", True, final_version, install_path)
    log(f"KiCad installation complete ({final_version})")

# =========================
# 🧹 FULL UNINSTALL HELPERS
# =========================

def _uninstall_kicad_linux(config, log=print):
    log("Removing KiCad (Linux)...")

    try:
        run(["sudo", "apt-get", "remove", "-y", "kicad"], log)
        run(["sudo", "apt-get", "purge", "-y", "kicad"], log)
        run(["sudo", "apt-get", "autoremove", "-y"], log)

        # 🔥 Remove PPAs from YAML
        linux_config = config.get("linux", {})
        ppas = linux_config.get("ppas", {})

        for _, ppa_info in ppas.items():
            repo = ppa_info.get("repo")
            if repo:
                log(f"Removing PPA: {repo}")
                try:
                    run(["sudo", "add-apt-repository", "--remove", "-y", repo], log)
                except Exception:
                    log(f"[WARN] Failed to remove PPA: {repo}")

    except Exception as e:
        log(f"[ERROR] Linux uninstall failed: {e}")
        raise


def _uninstall_kicad_windows(log=print):
    log("Removing KiCad (Windows)...")

    try:
        # 🔹 Try Chocolatey
        if _choco_available():
            run("choco uninstall -y kicad", log)
            return

        # 🔹 Try Winget
        try:
            run(["winget", "uninstall", "--id", "KiCad.KiCad", "-e", "--silent"], log)
            return
        except Exception:
            log("[WARN] Winget uninstall failed, trying manual removal...")

        # 🔹 Fallback: manual delete (SAFE)
        install_path = find_kicad_install_path()

        if install_path and os.path.exists(install_path):
            # Safety check
            if "kicad" in install_path.lower():
                shutil.rmtree(os.path.dirname(install_path), ignore_errors=True)
                log("Removed KiCad manually")
            else:
                log("[WARN] Install path does not look like KiCad. Skipping delete.")

    except Exception as e:
        log(f"[ERROR] Windows uninstall failed: {e}")
        raise



def install_kicad_macos(version, log=print, progress_cb=None):
    if tool_exists("brew") and str(version).lower() == "latest":
        log("Installing KiCad via Homebrew cask")
        run(["brew", "install", "--cask", "kicad"], log)
        return "latest", find_kicad_install_path()

    releases = _fetch_release_assets(log)
    release = _select_release_for_version(version, releases)

    asset = _find_asset_url(release, patterns=["unified", ".dmg"])
    if asset is None:
        asset = _find_asset_url(release, patterns=[".dmg"])

    if asset is None:
        raise RuntimeError("No suitable KiCad macOS DMG found.")

    url, filename = asset
    dmg_path = os.path.join(TOOLS_DIR, filename)

    # 🔥 FIXED DOWNLOAD
    _download(url, dmg_path, log, progress_cb)

    log("Mounting DMG...")

    attach_output = subprocess.check_output(
        ["hdiutil", "attach", dmg_path, "-nobrowse"],
        text=True,
    )

    mount_point = None
    for line in attach_output.splitlines():
        if "/Volumes/" in line:
            mount_point = line.split("\t")[-1].strip() if "\t" in line else line.split()[-1].strip()
            break

    if not mount_point or not os.path.exists(mount_point):
        raise RuntimeError("Failed to mount DMG")

    try:
        app_path = None
        for name in os.listdir(mount_point):
            if name.lower().endswith(".app"):
                app_path = os.path.join(mount_point, name)
                break

        if not app_path:
            raise RuntimeError("KiCad app not found in DMG")

        destination = os.path.join("/Applications", os.path.basename(app_path))

        if os.path.exists(destination):
            log("Removing old version...")
            shutil.rmtree(destination)

        log("Installing KiCad...")
        run(["ditto", app_path, destination], log)

    finally:
        subprocess.run(["hdiutil", "detach", mount_point, "-quiet"], check=False)

    installed_version = release["tag_name"].lstrip("v") if release else version
    log(f"Installed KiCad {installed_version} ✅")

    return installed_version, find_kicad_install_path()


def _cleanup_kicad_files(log=print):
    log("Cleaning up KiCad config & cache...")

    paths = [
        os.path.expanduser("~/.config/kicad"),
        os.path.expanduser("~/.cache/kicad"),
        os.path.expanduser("~/.local/share/kicad"),
    ]

    for path in paths:
        if os.path.exists(path):
            try:
                shutil.rmtree(path)
                log(f"Removed: {path}")
            except Exception as e:
                log(f"[WARN] Failed to remove {path}: {e}")


# =========================
# 🧹 MAIN UNINSTALL FUNCTION
# =========================

def uninstall_kicad(log=print):
    log("🧹 Starting KiCad FULL uninstall...")

    os_type = get_os()
    config = get_kicad_config()
    install_path = find_kicad_install_path()

    if install_path in ("", "-", None):
        log("[SKIP] KiCad not found")
        _upsert_install_details("kicad", False, "-", "-")
        return

    try:
        if os_type == "linux":
            _uninstall_kicad_linux(config, log)

        elif os_type == "windows":
            _uninstall_kicad_windows(log)

        elif os_type == "mac":
            _uninstall_kicad_macos(log)

        else:
            raise RuntimeError("Unsupported OS")

        # 🔥 Always cleanup
        _cleanup_kicad_files(log)

        _upsert_install_details("kicad", False, "-", "-")

        log("✅ KiCad fully removed (app + PPA + configs + cache)")

    except Exception as e:
        log(f"[ERROR] Uninstall failed: {e}")
        raise