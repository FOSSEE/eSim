#!/usr/bin/env python3
"""
Tool Metadata Registry for eSim Tool Manager.
Consolidates tool definitions, versions, and platform support.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
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
    env_vars: List[str] = field(default_factory=list)
    description: str = ""
    is_experimental: bool = False

    def get_executable(self, os_id: Optional[str] = None) -> Optional[str]:
        """Returns the executable name for the specified or current OS."""
        target_os = os_id or get_os_id()
        return self.executables.get(target_os)


# Centralized tool definitions
TOOLS = {
    "esim": ToolSpec(
        id="esim",
        label="eSim",
        category="core",
        versions=["latest", "2.4", "2.3", "2.2"],
        executables={"win32": "eSim.bat", "linux": "esim", "darwin": "esim"},
        description="The main eSim EDA platform."
    ),
    "kicad": ToolSpec(
        id="kicad",
        label="KiCad",
        category="analog",
        versions=["latest", "9", "8", "7", "6"],
        executables={"win32": "kicad.exe", "linux": "kicad", "darwin": "kicad"},
        description="Schematic capture and PCB layout suite."
    ),
    "ngspice": ToolSpec(
        id="ngspice",
        label="Ngspice",
        category="analog",
        versions=["latest", "42", "41", "39", "38", "37", "36", "35"],
        executables={"win32": "ngspice.exe", "linux": "ngspice", "darwin": "ngspice"},
        description="General-purpose circuit simulator."
    ),
    "ghdl": ToolSpec(
        id="ghdl",
        label="GHDL",
        category="digital",
        versions=["latest", "5.1.1", "5.0.0", "4.1.0", "4.0.0"],
        executables={"win32": "ghdl.exe", "linux": "ghdl", "darwin": "ghdl"},
        description="VHDL simulator."
    ),
    "verilator": ToolSpec(
        id="verilator",
        label="Verilator",
        category="digital",
        versions=["latest", "5.032", "5.026", "5.018", "5.006"],
        executables={"win32": "verilator.exe", "linux": "verilator", "darwin": "verilator"},
        description="Fast Verilog/SystemVerilog simulator."
    ),
    "llvm": ToolSpec(
        id="llvm",
        label="LLVM",
        category="digital",
        versions=["latest", "19", "18", "17", "16", "15", "14", "13"],
        executables={"win32": "clang.exe", "linux": "clang", "darwin": "clang"},
        description="Collection of modular and reusable compiler and toolchain technologies."
    ),
    "chocolatey": ToolSpec(
        id="chocolatey",
        label="Chocolatey",
        category="system",
        versions=["latest"],
        executables={"win32": "choco.exe"},
        description="Package manager for Windows."
    ),
}

# Categories for grouping in UI
CATEGORIES = {
    "analog": ["esim", "kicad", "ngspice"],
    "digital": ["esim", "kicad", "ngspice", "ghdl", "verilator", "llvm"],
}


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
