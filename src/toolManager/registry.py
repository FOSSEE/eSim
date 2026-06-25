"""
Tool Metadata Registry for eSim Tool Manager.
Consolidates tool definitions, versions, platform support, download URLs,
install scripts, and search paths into a single source of truth.

All UI files currently duplicate subsets of this data.  This module is the
canonical source; UI files will switch imports here in a future pass.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

try:
    from .platform_utils import get_os_id
except (ImportError, ValueError):
    from platform_utils import get_os_id


@dataclass(frozen=True)
class ToolSpec:
    """
    Metadata specification for an external tool managed by eSim.
    """

    id: str
    label: str
    category: str  # 'analog', 'digital', 'core', 'system'
    versions: List[str]
    default_version: str = "latest"
    executables: Dict[str, str] = field(default_factory=dict)  # OS id -> exe_name
    download_urls: Dict[str, str] = field(default_factory=dict)  # version -> URL
    install_scripts: Dict[str, str] = field(default_factory=dict)  # OS id -> script
    env_vars: List[str] = field(default_factory=list)
    description: str = ""
    is_experimental: bool = False

    def get_executable(self, os_id: Optional[str] = None) -> Optional[str]:
        """Returns the executable name for the specified or current OS."""
        target_os = os_id or get_os_id()
        return self.executables.get(target_os)

    def get_download_url(self, version: str) -> Optional[str]:
        """Returns the download URL for *version*, or None."""
        return self.download_urls.get(version)

    def get_install_script(self, os_id: Optional[str] = None) -> Optional[str]:
        """Returns the install script path for the specified or current OS."""
        target_os = os_id or get_os_id()
        return self.install_scripts.get(target_os)


# ====================================================================
# Centralised tool definitions — the single source of truth
# ====================================================================

TOOLS = {
    "esim": ToolSpec(
        id="esim",
        label="eSim",
        category="core",
        versions=["latest", "2.4", "2.3", "2.2"],
        executables={"win32": "eSim.bat", "linux": "esim", "darwin": "esim"},
        download_urls={
            "2.4": "https://static.fossee.in/esim/installation-files/"
                   "eSim-2.4_installer.exe",
            "2.3": "https://static.fossee.in/esim/installation-files/"
                   "eSim-2.3_installer.exe",
            "2.2": "https://static.fossee.in/esim/installation-files/"
                   "eSim-2.2_installer.exe",
            "latest": "https://static.fossee.in/esim/installation-files/"
                      "eSim-2.4_installer.exe",
        },
        description="The main eSim EDA platform.",
    ),
    "kicad": ToolSpec(
        id="kicad",
        label="KiCad",
        category="analog",
        versions=["latest", "9", "8", "7", "6"],
        executables={"win32": "kicad.exe", "linux": "kicad", "darwin": "kicad"},
        download_urls={
            "6.0.11": "https://github.com/KiCad/kicad-source-mirror/releases/"
                      "download/6.0.11/kicad-6.0.11-x86_64.exe",
            "6.0.10": "https://github.com/KiCad/kicad-source-mirror/releases/"
                      "download/6.0.10/kicad-6.0.10-x86_64.exe",
            "6.0.9": "https://github.com/KiCad/kicad-source-mirror/releases/"
                     "download/6.0.9/kicad-6.0.9-x86_64.exe",
        },
        install_scripts={
            "linux": "update-kicad-final.sh",
        },
        description="Schematic capture and PCB layout suite.",
    ),
    "ngspice": ToolSpec(
        id="ngspice",
        label="Ngspice",
        category="analog",
        versions=["latest", "42", "41", "39", "38", "37", "36", "35"],
        executables={"win32": "ngspice.exe", "linux": "ngspice", "darwin": "ngspice"},
        install_scripts={
            "linux": "nghdl/update-ngspice-final.sh",
        },
        description="General-purpose circuit simulator.",
    ),
    "ghdl": ToolSpec(
        id="ghdl",
        label="GHDL",
        category="digital",
        versions=["latest", "5.1.1", "5.0.0", "4.1.0", "4.0.0"],
        executables={"win32": "ghdl.exe", "linux": "ghdl", "darwin": "ghdl"},
        download_urls={
            "4.0.0": "https://github.com/ghdl/ghdl/releases/download/"
                     "v4.0.0/ghdl-MINGW32.zip",
            "4.1.0": "https://github.com/ghdl/ghdl/releases/download/"
                     "v4.1.0/ghdl-MINGW32.zip",
            "5.0.0": "https://github.com/ghdl/ghdl/releases/download/"
                     "v5.0.1/ghdl-mcode-5.0.1-mingw64.zip",
            "5.1.1": "https://github.com/ghdl/ghdl/releases/download/"
                     "v5.1.1/ghdl-mcode-5.1.1-mingw64.zip",
            "latest": "https://github.com/ghdl/ghdl/releases/download/"
                      "v5.1.1/ghdl-mcode-5.1.1-mingw64.zip",
        },
        install_scripts={
            "linux": "nghdl/update-ghdl-with-dependency.sh",
        },
        description="VHDL simulator.",
    ),
    "verilator": ToolSpec(
        id="verilator",
        label="Verilator",
        category="digital",
        versions=["latest", "5.032", "5.026", "5.018", "5.006"],
        executables={"win32": "verilator.exe", "linux": "verilator",
                     "darwin": "verilator"},
        install_scripts={
            "linux": "nghdl/update-verilator-final.sh",
        },
        description="Fast Verilog/SystemVerilog simulator.",
    ),
    "llvm": ToolSpec(
        id="llvm",
        label="LLVM",
        category="digital",
        versions=["latest", "19", "18", "17", "16", "15", "14", "13"],
        executables={"win32": "clang.exe", "linux": "clang", "darwin": "clang"},
        description="Collection of modular and reusable compiler and "
                    "toolchain technologies.",
    ),
    "chocolatey": ToolSpec(
        id="chocolatey",
        label="Chocolatey",
        category="system",
        versions=["latest"],
        executables={"win32": "choco.exe"},
        description="Package manager for Windows.",
    ),
}

# ====================================================================
# Convenience dicts matching the names used in main.py / gui_fixed.py
# (UI files currently define their own copies; these are the canonical ones.)
# ====================================================================

TOOL_LABELS: Dict[str, str] = {
    tid: spec.label for tid, spec in TOOLS.items()
}

TOOL_VERSIONS: Dict[str, str] = {
    tid: spec.default_version for tid, spec in TOOLS.items()
}

ANALOG_TOOLS: List[str] = ["esim", "kicad", "ngspice"]

DIGITAL_TOOLS: List[str] = [
    "esim", "kicad", "ngspice", "ghdl", "verilator", "llvm",
]

CATEGORIES: Dict[str, List[str]] = {
    "analog": list(ANALOG_TOOLS),
    "digital": list(DIGITAL_TOOLS),
}

KNOWN_STATES: set = {
    "installed", "not_installed", "wrong_version",
    "install_failed", "update_failed", "error",
    "not_supported", "uninstall_failed",
}

# ====================================================================
# Script mapping  (capitalised display name -> bash script path)
# Used by updater_gui.py; kept here as the canonical version.
# ====================================================================

SCRIPT_MAPPING: Dict[str, str] = {
    "KiCad": "update-kicad-final.sh",
    "Ngspice": "nghdl/update-ngspice-final.sh",
    "GHDL": "nghdl/update-ghdl-with-dependency.sh",
    "Verilator": "nghdl/update-verilator-final.sh",
}

# ====================================================================
# Windows search paths  (for finding already-installed executables)
# Moved from utils.py where they currently live.
# TODO: migrate into backends/windows.py in a future phase.
# ====================================================================

WIN_KICAD_PATHS: List[Tuple[str, str]] = [
    (r"C:\Program Files\KiCad\9.0\bin\kicad.exe", "9"),
    (r"C:\Program Files\KiCad\8.0\bin\kicad.exe", "8"),
    (r"C:\Program Files\KiCad\7.0\bin\kicad.exe", "7"),
    (r"C:\Program Files\KiCad\6.0\bin\kicad.exe", "6"),
    (r"C:\Program Files (x86)\KiCad\9.0\bin\kicad.exe", "9"),
    (r"C:\Program Files (x86)\KiCad\8.0\bin\kicad.exe", "8"),
    (r"C:\Program Files (x86)\KiCad\7.0\bin\kicad.exe", "7"),
    (r"C:\Program Files (x86)\KiCad\6.0\bin\kicad.exe", "6"),
]

WIN_NGSPICE_PATHS: List[str] = [
    r"C:\Program Files\ngspice\bin\ngspice.exe",
    r"C:\Program Files (x86)\ngspice\bin\ngspice.exe",
    r"C:\ngspice\bin\ngspice.exe",
]

WIN_LLVM_PATHS: List[str] = [
    r"C:\Program Files\LLVM\bin\clang.exe",
    r"C:\Program Files (x86)\LLVM\bin\clang.exe",
]

# ====================================================================
# Version-to-exact mappings from tool_manager_windows.py
# (Maps major/minor version keys to the exact string/archive used by
# the Windows backend.  TODO: migrate into backends/windows.py.)
# ====================================================================

VERILATOR_VERSIONS: Dict[str, Optional[str]] = {
    "5.006": "verilator-5.006.7z",
    "5.018": "verilator-5.018.7z",
    "5.026": "verilator-5.026.7z",
    "5.032": "verilator-5.032.7z",
    "latest": None,
}

KICAD_VERSIONS: Dict[str, Optional[List[str]]] = {
    "6": ["6.0.11", "6.0.10", "6.0.9", "6.0.8"],
    "7": ["7.0.11", "7.0.10", "7.0.9"],
    "8": ["8.0.9", "8.0.8", "8.0.7"],
    "9": ["9.0.7", "9.0.6", "9.0.5"],
    "latest": None,
}

NGSPICE_VERSIONS: Dict[str, Optional[str]] = {
    "35": "35", "36": "36", "37": "37", "38": "38",
    "39": "39", "40": "40", "41": "41", "42": "42",
    "latest": None,
}

LLVM_VERSIONS: Dict[str, Optional[str]] = {
    "13": "13.0.1", "14": "14.0.6", "15": "15.0.7",
    "16": "16.0.6", "17": "17.0.6", "18": "18.1.8",
    "19": "19.1.5",
    "latest": None,
}


# ====================================================================
# Query helpers
# ====================================================================

def get_tool_metadata(tool_id: str) -> Optional[ToolSpec]:
    """Retrieves metadata for a specific tool."""
    return TOOLS.get(tool_id)


def get_supported_tools() -> List[str]:
    """Returns a list of all supported tool IDs."""
    return list(TOOLS.keys())


def is_tool_supported(tool_id: str) -> bool:
    """Checks if a tool is supported by the registry."""
    return tool_id in TOOLS


def list_tools_by_category(category: str) -> List[ToolSpec]:
    """Returns a list of ToolSpec objects for a given category."""
    tool_ids = CATEGORIES.get(category, [])
    return [TOOLS[tid] for tid in tool_ids if tid in TOOLS]


def get_all_specs() -> Dict[str, ToolSpec]:
    """Returns the entire tool registry."""
    return TOOLS
