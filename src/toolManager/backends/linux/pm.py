import os
from typing import Callable, Optional

_PM_COMMANDS = {
    "apt": {"check":"apt-get","install":["apt-get","install","-y"],"uninstall":["apt-get","autoremove","-y","--purge"],
            "search":"apt-cache search {pkg}","update":["apt-get","update"],"version_parse":""},
    "dnf": {"check":"dnf","install":["dnf","install","-y"],"uninstall":["dnf","remove","-y"],
            "search":"dnf search {pkg}","update":["dnf","check-update"],"version_parse":""},
    "yum": {"check":"yum","install":["yum","install","-y"],"uninstall":["yum","remove","-y"],
            "search":"yum search {pkg}","update":["yum","check-update"],"version_parse":""},
    "pacman": {"check":"pacman","install":["pacman","-S","--noconfirm"],"uninstall":["pacman","-R","--noconfirm"],
               "search":"pacman -Ss {pkg}","update":["pacman","-Sy"],"version_parse":""},
    "zypper": {"check":"zypper","install":["zypper","install","-y"],"uninstall":["zypper","remove","-y"],
               "search":"zypper search {pkg}","update":["zypper","refresh"],"version_parse":""},
    "pkg": {"check":"pkg","install":["pkg","install","-y"],"uninstall":["pkg","delete","-y"],
            "search":"pkg search {pkg}","update":["pkg","update"],"version_parse":""},
    "xbps": {"check":"xbps-install","install":["xbps-install","-y"],"uninstall":["xbps-remove","-y"],
             "search":"xbps-query -Rs {pkg}","update":["xbps-install","-Su"],"version_parse":""},
}

def _sudo_prefix(cmd):
    return cmd if os.geteuid() == 0 else ["sudo"] + cmd

def pm_install(pm_name, package, run_cmd, use_sudo=True, timeout=120):
    if pm_name not in _PM_COMMANDS: return False
    cmd = _PM_COMMANDS[pm_name]["install"] + [package]
    if use_sudo: cmd = _sudo_prefix(cmd)
    result = run_cmd(cmd, timeout=timeout)
    return result is not None and result.returncode == 0

def pm_uninstall(pm_name, package, run_cmd, use_sudo=True, timeout=120):
    if pm_name not in _PM_COMMANDS: return False
    cmd = _PM_COMMANDS[pm_name]["uninstall"] + [package]
    if use_sudo: cmd = _sudo_prefix(cmd)
    result = run_cmd(cmd, timeout=timeout)
    return result is not None and result.returncode == 0

def pm_list_installed(pm_name, run_cmd, use_sudo=False, timeout=30):
    if pm_name not in _PM_COMMANDS or "list" not in _PM_COMMANDS[pm_name]: return None
    cmd = _PM_COMMANDS[pm_name].get("list", [f"{_PM_COMMANDS[pm_name]['check']} list --installed"])
    if use_sudo: cmd = _sudo_prefix(cmd)
    result = run_cmd(cmd if isinstance(cmd, list) else cmd.split(), timeout=timeout)
    return result.stdout.split("\n") if result and result.returncode == 0 else None

def pm_search(pm_name, package, run_cmd, timeout=30):
    if pm_name not in _PM_COMMANDS: return False
    result = run_cmd(_PM_COMMANDS[pm_name]["search"].format(pkg=package).split(), timeout=timeout)
    return result is not None and result.returncode == 0

def pm_update_index(pm_name, run_cmd, use_sudo=True, timeout=120):
    if pm_name not in _PM_COMMANDS: return False
    cmd = _PM_COMMANDS[pm_name]["update"]
    if use_sudo: cmd = _sudo_prefix(cmd)
    result = run_cmd(cmd, timeout=timeout)
    return result is not None and result.returncode == 0
