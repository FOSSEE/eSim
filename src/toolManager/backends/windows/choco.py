from typing import Optional
import re

def choco_install(package, version, run_cmd):
    cmd = ["choco", "install", package, "-y", "--no-progress"]
    if version and version != "latest": cmd.extend(["--version", version, "--allow-downgrade", "--force"])
    result = run_cmd(cmd, timeout=300)
    return result is not None and result.returncode == 0

def choco_uninstall(package, version, run_cmd):
    result = run_cmd(["choco", "uninstall", package, "-y", "--force-dependencies", "--no-progress"], timeout=180)
    return result is not None and result.returncode == 0

def choco_list(package, run_cmd):
    for cmd in [["choco", "list", "--exact", package],
                ["choco", "list", "--local-only", "--exact", package]]:
        result = run_cmd(cmd, timeout=30)
        if result and result.returncode == 0:
            m = re.search(rf'{re.escape(package)}\s+(\S+)', result.stdout)
            if m: return m.group(1)
    return None
