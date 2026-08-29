import os
import platform
import shutil
from pathlib import Path

try:
    from .dependency import load_tools, needs_update
    from .ghdl import install_ghdl
    from .kicad import install_kicad
    from .llmv import install_llvm
    from .ngspice import install_ngspice
    from .python import install_python
    from .verilator import install_verilator
except ImportError:
    from dependency import load_tools, needs_update
    from ghdl import install_ghdl
    from kicad import install_kicad
    from llmv import install_llvm
    from ngspice import install_ngspice
    from python import install_python
    from verilator import install_verilator

TOOLS_DIR = os.path.expanduser("~/esim-tools-bin")
os.makedirs(TOOLS_DIR, exist_ok=True)

INSTALLERS = {
    "ngspice": install_ngspice,
    "kicad": install_kicad,
    "ghdl": install_ghdl,
    "llvm": install_llvm,
    "verilator": install_verilator,
    "python": install_python,
}


def _platform_name():
    system = platform.system().lower()
    if "windows" in system:
        return "windows"
    if "darwin" in system:
        return "mac"
    if "linux" in system:
        return "linux"
    return "unknown"


def normalize_tool_name(tool_name):
    if not tool_name:
        return ""
    return str(tool_name).strip().lower()
        

def get_supported_tools():
    return list(INSTALLERS.keys())


def _display_name(tool_name):
    tools = load_tools()
    canonical = normalize_tool_name(tool_name)
    for raw_name in tools:
        if normalize_tool_name(raw_name) == canonical:
            return raw_name
    return canonical


def _run_shell_command(command, log=print):
    log(f"> {command}")
    result = os.system(command)
    if result != 0:
        raise RuntimeError(f"Command failed with exit status {result}: {command}")


def _uninstall_python(log=print):
    venv_path = Path.cwd() / "toolmanagervenv"
    if not venv_path.exists():
        log("Python virtual environment is not present.")
        return
    shutil.rmtree(venv_path)
    log(f"Removed virtual environment at {venv_path}")


def uninstall_tool(tool_name, log=print):
    canonical = normalize_tool_name(tool_name)
    if canonical not in INSTALLERS:
        raise ValueError(f"Unknown tool: {tool_name}")

    if canonical == "python":
        _uninstall_python(log)
        return

    os_type = _platform_name()
    package_name = canonical

    if os_type == "linux":
        if canonical == "llvm":
            _run_shell_command("sudo apt-get remove -y llvm clang", log)
        else:
            _run_shell_command(f"sudo apt-get remove -y {package_name}", log)
        return

    if os_type == "mac":
        if canonical == "kicad":
            _run_shell_command("brew uninstall --cask kicad", log)
        else:
            _run_shell_command(f"brew uninstall {package_name}", log)
        return

    if os_type == "windows":
        _run_shell_command(f"choco uninstall -y {package_name}", log)
        return

    raise RuntimeError("Unsupported OS")


def install_tool(tool_name, version="latest", log=print):
    canonical = normalize_tool_name(tool_name)
    if canonical not in INSTALLERS:
        raise ValueError(f"Unknown tool: {tool_name}")

    display_name = _display_name(canonical)
    log(f"Installing {display_name} ({version})...")
    INSTALLERS[canonical](version=version, log=log)
    log(f"{display_name} install complete")


def update_tool(tool_name=None, version="latest", log=print):
    tools = load_tools()

    if tool_name:
        canonical = normalize_tool_name(tool_name)
        info = None
        for raw_name, raw_info in tools.items():
            if normalize_tool_name(raw_name) == canonical:
                info = raw_info
                break

        if canonical not in INSTALLERS:
            raise ValueError(f"Unknown tool: {tool_name}")

        if info and not needs_update(canonical, info):
            log(f"{_display_name(canonical)} is already up to date or has no managed update policy.")
            return

        install_tool(canonical, version=version, log=log)
        return

    update_all(log=log)


def update_all(log=print):
    tools = load_tools()
    updated_any = False

    for raw_name, info in tools.items():
        canonical = normalize_tool_name(raw_name)

        if canonical not in INSTALLERS:
            if needs_update(canonical, info):
                log(f"{raw_name} has an update recommendation but is not managed automatically.")
            continue

        if needs_update(canonical, info):
            log(f"Updating {raw_name}...")
            install_tool(canonical, log=log)
            updated_any = True

    if not updated_any:
        log("All managed tools are already up to date.")


def install_all(log=print):
    tools = load_tools()
    log("Installing all managed tools...")

    for raw_name in tools:
        canonical = normalize_tool_name(raw_name)
        if canonical in INSTALLERS:
            install_tool(canonical, log=log)

    log("All managed tool install steps completed.")
