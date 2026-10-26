import yaml
import shutil
import os

try:
    from tool_manager_gui.version import get_version, compare_versions, max_version
except ImportError:
    from version import get_version, compare_versions, max_version


# ---------- LOAD TOOLS ----------
def load_tools():
    base_dir = os.path.dirname(__file__)
    tools_path = os.path.join(base_dir, "tools.yml")

    with open(tools_path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    return data.get("tools", {}) 


# ---------- CHECK HELPERS ----------
def check_executable(names):
    if isinstance(names, str):
        names = [names]
    return any(shutil.which(name) for name in names)


def check_directory(path):
    return os.path.exists(path)

def is_installed(info):
    ttype = (info or {}).get("type")
    if ttype == "executable":
        return check_executable((info or {}).get("check"))
    if ttype == "directory":
        return check_directory((info or {}).get("path"))
    return False


def get_installed_version(info):
    """
    Best-effort: only meaningful for executable tools.
    Returns version string or None.
    """
    if (info or {}).get("type") != "executable":
        return None
    if not check_executable((info or {}).get("check")):
        return None
    cmd = (info or {}).get("version_cmd")
    return get_version(cmd)


def get_latest_target_version(info):
    """
    Defines what "latest" means for update checks.
    Priority:
    - recommended_version
    - highest item in versions list
    - min_version (as a fallback target)
    """
    if not isinstance(info, dict):
        return None
    rec = info.get("recommended_version")
    if isinstance(rec, str) and rec.strip():
        return rec.strip()
    versions = info.get("versions")
    if isinstance(versions, list):
        mv = max_version(versions)
        if mv:
            return mv
    min_v = info.get("min_version")
    if isinstance(min_v, str) and min_v.strip():
        return min_v.strip()
    return None


# ---------- TABLE VIEW (list / check) ----------
def check_dependencies():
    tools = load_tools()
    results = []

    for tool, info in tools.items():
        # Defensive: ignore malformed tool entries in tools.yml (e.g. nested "tools:" key)
        if not isinstance(info, dict):
            continue
        ttype = info.get("type")
        status = "not installed"
        version = "-"

        if ttype == "executable":
            found = check_executable(info.get("check"))

            if found:
                status = "installed"
                if "version_cmd" in info:
                    version = get_version(info["version_cmd"]) or "-"

        elif ttype == "directory":
            found = check_directory(info.get("path"))
            if found:
                status = "installed"

        results.append((tool.lower(), status, version))
    return results


def print_dependency_table(results):
    print(f"{'Tool':<12} {'Status':<14} Version")
    print("-" * 38)

    for tool, status, version in results:
        print(f"{tool:<12} {status:<14} {version}")


# ---------- DOCTOR COMMAND ----------
def run_doctor():
    print("🔍 System Diagnostics\n")

    tools = load_tools()
    system_ready = True

    for tool, info in tools.items():
        tool_name = tool.lower()

        if info.get("type") != "executable":
            continue

        found = check_executable(info.get("check"))

        if not found:
            print(f"✖ {tool_name} missing")
            system_ready = False
            continue

        # Tools without version rules are still required, just not version-gated.
        if (
            "min_version" not in info
            and "recommended_version" not in info
        ):
            print(f"✔ {tool_name} found")
            continue

        installed_version = None
        if "version_cmd" in info:
            installed_version = get_version(info["version_cmd"])

        if installed_version and "min_version" in info:
            cmp = compare_versions(installed_version, info["min_version"])
            if cmp == -1:
                print(
                    f"⚠ {tool_name} version outdated "
                    f"({installed_version} < {info['min_version']})"
                )
                system_ready = False
                continue

        if installed_version and "recommended_version" in info:
            cmp = compare_versions(installed_version, info["recommended_version"])
            if cmp == -1:
                print(
                    f"ℹ {tool_name} update recommended "
                    f"(v{installed_version} < {info['recommended_version']})"
                )
                continue

        if installed_version:
            print(f"✔ {tool_name} found (v{installed_version})")
        else:
            print(f"✔ {tool_name} found")

    print("\nStatus:", end=" ")
    if system_ready:
        print("✅ System ready")
    else:
        print("❌ System not ready")


#-----------------Update---------------
def needs_update(tool_name, info):
    """
    Returns True only if:
    - tool is executable
    - tool is installed
    - AND version rules are defined
    - AND installed version is outdated
    """

    # Only executables can be updated
    if info.get("type") != "executable":
        return False

    # 🔑 KEY RULE: no known target → no update
    target = get_latest_target_version(info)
    if not target:
        return False

    # Tool must be installed
    if not check_executable(info.get("check")):
        return False

    # Detect version
    installed_version = None
    if "version_cmd" in info:
        installed_version = get_version(info["version_cmd"])

    if not installed_version:
        return False

    return compare_versions(installed_version, target) == -1
