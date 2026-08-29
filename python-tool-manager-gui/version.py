import subprocess
import re
from packaging import version as vparse


# ----------- VERSION UTILS -----------

def parse_version(v):
    return tuple(map(int, v.split(".")))


def max_version(versions):
    if not versions:
        return None

    parsed = []
    for item in versions:
        if not isinstance(item, str):
            continue

        s = item.strip()
        if not s:
            continue

        try:
            parsed.append((vparse.parse(s), s))
        except Exception:
            continue

    if not parsed:
        return None

    parsed.sort(key=lambda t: t[0], reverse=True)
    return parsed[0][1]


def compare_versions(installed, target):
    try:
        i = vparse.parse(installed)
        t = vparse.parse(target)

        if i < t:
            return -1
        elif i > t:
            return 1
        else:
            return 0
    except Exception:
        return None


# ----------- VERSION DETECTION -----------

def get_version(commands):
    """
    Robust version detection:
    Supports:
    - 46
    - 46.1
    - 3.3.10
    - mixed stdout/stderr
    """

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
            if not output:
                continue

            # 🔥 supports ALL formats
            match = re.search(r"(\d+(\.\d+)+|\d+)", output)
            if match:
                return match.group(1)

        except Exception:
            continue

    return None


# ----------- STATUS CHECK -----------

def check_tool_version(tool_cfg):
    installed = get_version(tool_cfg.get("version_cmd"))

    if not installed:
        return "not_installed"

    min_v = tool_cfg.get("min_version")
    rec_v = tool_cfg.get("recommended_version")

    if min_v and compare_versions(installed, min_v) == -1:
        return "too_old"

    if rec_v:
        cmp = compare_versions(installed, rec_v)
        if cmp == -1:
            return "outdated"
        return "up_to_date"

    return "up_to_date"