"""
esim_tool_manager.core
-----------------------
Core engine for the eSim Automated Tool Manager.

Responsibilities covered here (mapped to task requirements):
  1. Tool Installation Management   -> ToolManager.install()
  2. Update/Upgrade System          -> ToolManager.check_updates() / update()
  3. Configuration Handling         -> ConfigStore, ToolManager.configure()
  4. Dependency Checker             -> DependencyChecker
  5. Logging / feedback to user     -> Logger (used by everything)
"""

import json
import logging
import os
import platform
import re
import shutil
import subprocess
import sys
import urllib.request
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional


# --------------------------------------------------------------------------- #
# Paths & Logging
# --------------------------------------------------------------------------- #

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
LOG_DIR = BASE_DIR / "logs"
REGISTRY_FILE = CONFIG_DIR / "tool_registry.json"   # what tools/versions are known
STATE_FILE = CONFIG_DIR / "installed_state.json"    # what's installed on this machine
USER_CONFIG_FILE = CONFIG_DIR / "user_config.json"  # user-specific settings/paths

CONFIG_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("esim_tool_manager")
logger.setLevel(logging.DEBUG)

_fmt = logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s", "%Y-%m-%d %H:%M:%S")

_file_handler = logging.FileHandler(LOG_DIR / "tool_manager.log")
_file_handler.setFormatter(_fmt)
_file_handler.setLevel(logging.DEBUG)

_console_handler = logging.StreamHandler(sys.stdout)
_console_handler.setFormatter(_fmt)
_console_handler.setLevel(logging.INFO)

if not logger.handlers:
    logger.addHandler(_file_handler)
    logger.addHandler(_console_handler)


# --------------------------------------------------------------------------- #
# Data model
# --------------------------------------------------------------------------- #

@dataclass
class ToolSpec:
    """Static, known-good definition of a tool the manager can handle."""
    name: str
    version_check_cmd: list          # e.g. ["ngspice", "-v"]
    version_regex: str               # regex with one capturing group for the version
    latest_known_version: str
    apt_package: Optional[str] = None
    brew_package: Optional[str] = None
    choco_package: Optional[str] = None
    # Dependencies needed only if building from source (not for prebuilt
    # package-manager installs). Checked and reported, but do NOT block
    # a package-manager install.
    build_dependencies: list = field(default_factory=list)
    # Dependencies required at runtime regardless of install method.
    # Checked BEFORE installation and will block install if missing.
    runtime_dependencies: list = field(default_factory=list)


@dataclass
class InstalledRecord:
    name: str
    version: str
    install_path: str
    installed_via: str    # "apt" | "brew" | "choco" | "manual" | "detected"


# --------------------------------------------------------------------------- #
# Registry: default known tools (eSim's key external dependencies)
# --------------------------------------------------------------------------- #

DEFAULT_REGISTRY = {
    "ngspice": asdict(ToolSpec(
        name="ngspice",
        version_check_cmd=["ngspice", "-v"],
        # Matches "ngspice-42", "ngspice-42.1", "ngspice version 42", etc.
        version_regex=r"ngspice[- ](?:version )?(\d+(?:\.\d+)*)",
        latest_known_version="42",
        apt_package="ngspice",
        brew_package="ngspice",
        choco_package="ngspice",
        # gcc/make are only needed if compiling ngspice from source.
        # A prebuilt apt/brew/choco package does NOT require them.
        build_dependencies=["gcc", "make"],
        runtime_dependencies=[],
    )),
    "kicad": asdict(ToolSpec(
        name="kicad",
        version_check_cmd=["kicad-cli", "version"],
        version_regex=r"(\d+\.\d+(?:\.\d+)?)",
        latest_known_version="8.0.0",
        apt_package="kicad",
        brew_package="kicad",
        choco_package="kicad",
        build_dependencies=[],
        runtime_dependencies=[],
    )),
    "ghdl": asdict(ToolSpec(
        name="ghdl",
        version_check_cmd=["ghdl", "--version"],
        version_regex=r"GHDL (\d+(?:\.\d+)*)",
        latest_known_version="4.1.0",
        apt_package="ghdl",
        brew_package="ghdl",
        build_dependencies=["gcc"],
        runtime_dependencies=[],
    )),
}


def _load_json(path: Path, default):
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return default


def _save_json(path: Path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


class ConfigStore:
    """Handles persisted registry, installed-state and user configuration."""

    def __init__(self):
        self.registry = _load_json(REGISTRY_FILE, DEFAULT_REGISTRY)
        if not REGISTRY_FILE.exists():
            _save_json(REGISTRY_FILE, self.registry)

        self.state = _load_json(STATE_FILE, {})       # name -> InstalledRecord dict
        self.user_config = _load_json(USER_CONFIG_FILE, {
            "esim_home": str(Path.home() / ".esim"),
            "tool_paths": {},          # name -> resolved install/binary path
            "preferred_package_manager": None,   # auto-detected if None
        })

    def save_state(self):
        _save_json(STATE_FILE, self.state)

    def save_user_config(self):
        _save_json(USER_CONFIG_FILE, self.user_config)


# --------------------------------------------------------------------------- #
# Platform detection
# --------------------------------------------------------------------------- #

class PlatformInfo:
    def __init__(self):
        self.system = platform.system()          # "Linux", "Windows", "Darwin"
        self.is_linux = self.system == "Linux"
        self.is_windows = self.system == "Windows"
        self.is_mac = self.system == "Darwin"
        self.package_manager = self._detect_package_manager()

    def _detect_package_manager(self) -> Optional[str]:
        if self.is_linux and shutil.which("apt"):
            return "apt"
        if self.is_mac and shutil.which("brew"):
            return "brew"
        if self.is_windows and shutil.which("choco"):
            return "choco"
        return None

    def __str__(self):
        return f"{self.system} (package manager: {self.package_manager or 'none detected'})"


# --------------------------------------------------------------------------- #
# Dependency checker
# --------------------------------------------------------------------------- #

class DependencyChecker:
    def __init__(self, platform_info: PlatformInfo):
        self.platform_info = platform_info

    def check_system_deps(self, deps: list) -> dict:
        """Return {dep_name: bool_found} for a list of required system binaries."""
        result = {}
        for dep in deps:
            found = shutil.which(dep) is not None
            result[dep] = found
            level = logging.DEBUG if found else logging.WARNING
            logger.log(level, f"Dependency check: '{dep}' {'FOUND' if found else 'MISSING'}")
        return result

    def report(self, tool_name: str, deps: list, label: str = "dependencies") -> bool:
        if not deps:
            logger.info(f"[{tool_name}] No {label} required.")
            return True
        results = self.check_system_deps(deps)
        missing = [d for d, ok in results.items() if not ok]
        if missing:
            logger.warning(
                f"[{tool_name}] Missing {label}: {', '.join(missing)}. "
                f"Install them first (e.g. 'sudo apt install {' '.join(missing)}')."
            )
            return False
        logger.info(f"[{tool_name}] All {label} satisfied.")
        return True


# --------------------------------------------------------------------------- #
# Version detection
# --------------------------------------------------------------------------- #

class VersionDetector:
    @staticmethod
    def get_installed_version(spec: ToolSpec) -> Optional[str]:
        binary = spec.version_check_cmd[0]
        if shutil.which(binary) is None:
            return None
        try:
            out = subprocess.run(
                spec.version_check_cmd,
                capture_output=True, text=True, timeout=10
            )
            text = out.stdout + out.stderr
            match = re.search(spec.version_regex, text)
            return match.group(1) if match else "unknown"
        except Exception as e:
            logger.error(f"Could not determine version for {spec.name}: {e}")
            return None


# --------------------------------------------------------------------------- #
# Tool Manager (orchestrator)
# --------------------------------------------------------------------------- #

class ToolManager:
    def __init__(self):
        self.config = ConfigStore()
        self.platform_info = PlatformInfo()
        self.dep_checker = DependencyChecker(self.platform_info)
        logger.info(f"Initialized ToolManager on {self.platform_info}")

    # ---------- Listing / status ---------- #

    def list_tools(self):
        rows = []
        for name, spec_dict in self.config.registry.items():
            spec = ToolSpec(**spec_dict)
            installed_version = VersionDetector.get_installed_version(spec)
            status = "not installed" if installed_version is None else installed_version
            update_available = (
                installed_version not in (None, "unknown")
                and installed_version != spec.latest_known_version
            )
            rows.append({
                "name": name,
                "installed_version": status,
                "latest_known_version": spec.latest_known_version,
                "update_available": update_available,
            })
        return rows

    # ---------- Dependency check ---------- #

    def check_dependencies(self, tool_name: str) -> bool:
        """
        Checks BOTH runtime and build dependencies and reports on each,
        but only runtime dependencies can block an install. Build
        dependencies (e.g. gcc/make) are only relevant if the tool were
        being compiled from source, not for a prebuilt package-manager
        install, so they are reported as informational warnings only.
        """
        spec = self._get_spec(tool_name)
        runtime_ok = self.dep_checker.report(
            tool_name, spec.runtime_dependencies, label="runtime dependencies"
        )
        # Build deps are informational only - never block installation
        # via a package manager.
        self.dep_checker.report(
            tool_name, spec.build_dependencies, label="build dependencies (only needed if compiling from source)"
        )
        return runtime_ok

    # ---------- Install ---------- #

    def install(self, tool_name: str, dry_run: bool = False) -> bool:
        spec = self._get_spec(tool_name)
        logger.info(f"Starting installation for '{tool_name}' on {self.platform_info.system}")

        if not self.check_dependencies(tool_name):
            logger.error(f"Aborting install of {tool_name}: unmet runtime dependencies.")
            return False

        existing = VersionDetector.get_installed_version(spec)
        if existing:
            logger.info(f"'{tool_name}' already installed (version {existing}). Skipping install.")
            self._record_installed(spec, existing, "detected")
            return True

        cmd = self._build_install_command(spec)
        if cmd is None:
            logger.error(
                f"No installation method available for '{tool_name}' on "
                f"{self.platform_info.system}. Please install manually."
            )
            return False

        logger.info(f"Running: {' '.join(cmd)}")
        if dry_run:
            logger.info("[dry-run] Skipping actual execution.")
            return True

        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Installation of {tool_name} failed: {e}")
            return False
        except FileNotFoundError as e:
            logger.error(
                f"Could not execute '{cmd[0]}' ({e}). Either the package "
                f"manager '{self.platform_info.package_manager}' or a "
                f"required helper binary (e.g. 'sudo') is not on PATH."
            )
            return False

        new_version = VersionDetector.get_installed_version(spec) or "unknown"
        self._record_installed(spec, new_version, self.platform_info.package_manager or "manual")
        self.configure(tool_name)
        logger.info(f"'{tool_name}' installed successfully (version {new_version}).")
        return True

    def _sudo_prefix(self) -> list:
        """
        Returns ["sudo"] only when it's actually needed and available:
        not on Windows, not when already root (os.geteuid() == 0 - e.g.
        inside a root Docker container/CI runner), and only if a `sudo`
        binary actually exists on PATH. This avoids a misleading
        "package manager not found" error that would otherwise surface
        when subprocess fails to find a nonexistent `sudo` binary.
        """
        if self.platform_info.is_windows:
            return []
        if hasattr(os, "geteuid") and os.geteuid() == 0:
            return []
        if shutil.which("sudo") is None:
            logger.warning(
                "'sudo' not found on PATH; attempting to run the package "
                "manager directly. This will fail if elevated privileges "
                "are required."
            )
            return []
        return ["sudo"]

    def _build_install_command(self, spec: ToolSpec) -> Optional[list]:
        pm = self.platform_info.package_manager
        if pm == "apt" and spec.apt_package:
            return self._sudo_prefix() + ["apt", "install", "-y", spec.apt_package]
        if pm == "brew" and spec.brew_package:
            return ["brew", "install", spec.brew_package]
        if pm == "choco" and spec.choco_package:
            return ["choco", "install", spec.choco_package, "-y"]
        return None

    # ---------- Update ---------- #

    def check_updates(self) -> list:
        updates = []
        for row in self.list_tools():
            if row["update_available"]:
                updates.append(row)
        if updates:
            logger.info(f"Updates available for: {[u['name'] for u in updates]}")
        else:
            logger.info("All tools are up to date.")
        return updates

    def update(self, tool_name: str, dry_run: bool = False) -> bool:
        spec = self._get_spec(tool_name)
        pm = self.platform_info.package_manager
        cmd = None
        if pm == "apt":
            cmd = self._sudo_prefix() + ["apt", "install", "--only-upgrade", "-y", spec.apt_package]
        elif pm == "brew":
            cmd = ["brew", "upgrade", spec.brew_package]
        elif pm == "choco":
            cmd = ["choco", "upgrade", spec.choco_package, "-y"]

        if cmd is None:
            logger.error(f"No update method available for '{tool_name}' on this platform.")
            return False

        logger.info(f"Updating '{tool_name}': {' '.join(cmd)}")
        if dry_run:
            logger.info("[dry-run] Skipping actual execution.")
            return True

        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Update of {tool_name} failed: {e}")
            return False

        new_version = VersionDetector.get_installed_version(spec) or "unknown"
        self._record_installed(spec, new_version, pm)
        logger.info(f"'{tool_name}' updated to version {new_version}.")
        return True

    # ---------- Configuration ---------- #

    ESIM_MANIFEST_FILE = CONFIG_DIR / "esim_config.json"

    def configure(self, tool_name: str) -> bool:
        """
        Resolves the tool's binary path and writes it into two places:
          1. user_config.json  -> internal bookkeeping for this manager
          2. esim_config.json  -> an eSim-consumable configuration manifest
             (key/value map of tool -> absolute binary path) that eSim's
             own settings loader can read directly, e.g.:
                 { "ngspice_path": "/usr/bin/ngspice", ... }

        This is a deliberate, non-destructive alternative to editing the
        user's shell rc files or system-wide PATH/registry: it avoids
        mutating global environment state while still giving eSim (or any
        other consumer) a single authoritative file to read tool paths
        from.
        """
        spec = self._get_spec(tool_name)
        binary_path = shutil.which(spec.version_check_cmd[0])
        if not binary_path:
            logger.warning(f"Cannot configure '{tool_name}': binary not found on PATH.")
            return False

        self.config.user_config["tool_paths"][tool_name] = binary_path
        self.config.save_user_config()

        manifest = _load_json(self.ESIM_MANIFEST_FILE, {})
        manifest[f"{tool_name}_path"] = binary_path
        _save_json(self.ESIM_MANIFEST_FILE, manifest)

        logger.info(f"Configured '{tool_name}' -> {binary_path}")
        logger.info(f"eSim configuration manifest updated: {self.ESIM_MANIFEST_FILE}")

        install_dir = str(Path(binary_path).parent)
        if install_dir not in os.environ.get("PATH", ""):
            logger.info(
                f"Note: add '{install_dir}' to your PATH if a tool other than "
                f"eSim needs to locate '{tool_name}' via PATH directly."
            )
        return True

    # ---------- Helpers ---------- #

    def _get_spec(self, tool_name: str) -> ToolSpec:
        if tool_name not in self.config.registry:
            raise ValueError(f"Unknown tool '{tool_name}'. Known tools: {list(self.config.registry)}")
        return ToolSpec(**self.config.registry[tool_name])

    def _record_installed(self, spec: ToolSpec, version: str, via: str):
        record = InstalledRecord(
            name=spec.name,
            version=version,
            install_path=shutil.which(spec.version_check_cmd[0]) or "unknown",
            installed_via=via,
        )
        self.config.state[spec.name] = asdict(record)
        self.config.save_state()
