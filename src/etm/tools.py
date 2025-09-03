from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class Tool:
    name: str
    check_cmd: List[str]
    installers: Dict[str, List[str]]  # keys: linux-apt, mac-brew, win-choco
    updaters: Dict[str, List[str]]

TOOL_REGISTRY: Dict[str, Tool] = {
    "ngspice": Tool(
        name="ngspice",
        check_cmd=["ngspice","-v"],
        installers={
            "linux-apt":["apt-get","install","-y","ngspice"],
            "mac-brew":["brew","install","ngspice"],
            "win-choco":["choco","install","ngspice","-y"]
        },
        updaters={
            "linux-apt":["apt-get","install","-y","--only-upgrade","ngspice"],
            "mac-brew":["brew","upgrade","ngspice"],
            "win-choco":["choco","upgrade","ngspice","-y"]
        }
    ),
    "kicad": Tool(
        name="kicad",
        check_cmd=["kicad-cli","--version"],
        installers={
            "linux-apt":["apt-get","install","-y","kicad"],
            "mac-brew":["brew","install","kicad"],
            "win-choco":["choco","install","kicad","-y"]
        },
        updaters={
            "linux-apt":["apt-get","install","-y","--only-upgrade","kicad"],
            "mac-brew":["brew","upgrade","kicad"],
            "win-choco":["choco","upgrade","kicad","-y"]
        }
    ),
    "ghdl": Tool(
        name="ghdl",
        check_cmd=["ghdl","--version"],
        installers={
            "linux-apt":["apt-get","install","-y","ghdl"],
            "mac-brew":["brew","install","ghdl"],
            "win-choco":["choco","install","ghdl","-y"]
        },
        updaters={
            "linux-apt":["apt-get","install","-y","--only-upgrade","ghdl"],
            "mac-brew":["brew","upgrade","ghdl"],
            "win-choco":["choco","upgrade","ghdl","-y"]
        }
    ),
    "verilator": Tool(
        name="verilator",
        check_cmd=["verilator","--version"],
        installers={
            "linux-apt":["apt-get","install","-y","verilator"],
            "mac-brew":["brew","install","verilator"],
            "win-choco":["choco","install","verilator","-y"]
        },
        updaters={
            "linux-apt":["apt-get","install","-y","--only-upgrade","verilator"],
            "mac-brew":["brew","upgrade","verilator"],
            "win-choco":["choco","upgrade","verilator","-y"]
        }
    ),
}

def list_tool_names():
    return list(TOOL_REGISTRY.keys())

def get_tool(name: str) -> Optional[Tool]:
    return TOOL_REGISTRY.get(name.lower())
