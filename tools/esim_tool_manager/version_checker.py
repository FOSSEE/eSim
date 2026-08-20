import subprocess
from dataclasses import dataclass
from typing import Optional

from .detector import ToolDetector


@dataclass
class VersionInfo:
    tool: str
    installed_version: Optional[str]
    available_version: Optional[str]


class VersionChecker:
    """Check installed and APT-available versions of eSim tools."""

    PACKAGES = {
        "ngspice": "ngspice",
        "verilator": "verilator",
        "ghdl": "ghdl",
        "kicad": "kicad",
    }

    def __init__(self) -> None:
        self.detector = ToolDetector()

    def get_available_version(
        self,
        package: str,
    ) -> Optional[str]:
        """Get the candidate version available through APT."""

        try:
            result = subprocess.run(
                ["apt-cache", "policy", package],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )

            for line in result.stdout.splitlines():
                if "Candidate:" in line:
                    version = line.split(":", 1)[1].strip()

                    if version and version != "(none)":
                        return version

            return None

        except (subprocess.SubprocessError, OSError):
            return None

    def check_tool(self, tool_name: str) -> VersionInfo:
        """Get installed and available versions for one tool."""

        tool_name = tool_name.lower()

        if tool_name not in self.PACKAGES:
            raise ValueError(
                f"Unsupported tool: {tool_name}"
            )

        status = self.detector.detect_tool(
            tool_name,
            self.PACKAGES[tool_name],
        )

        available_version = self.get_available_version(
            self.PACKAGES[tool_name]
        )

        return VersionInfo(
            tool=tool_name,
            installed_version=status.version,
            available_version=available_version,
        )

    def check_all(self) -> list[VersionInfo]:
        """Check versions of all supported tools."""

        return [
            self.check_tool(tool_name)
            for tool_name in self.PACKAGES
        ]


if __name__ == "__main__":
    checker = VersionChecker()

    print("eSim Version Checker")
    print("=" * 70)

    for info in checker.check_all():
        installed = info.installed_version or "Not installed"
        available = info.available_version or "Not available"

        print(f"\n{info.tool}")
        print(f"  Installed : {installed}")
        print(f"  APT       : {available}")

        if info.installed_version is None:
            print("  Status    : Not installed")
        elif info.available_version is None:
            print("  Status    : Unable to check")
        else:
            print("  Status    : Installed package detected")
