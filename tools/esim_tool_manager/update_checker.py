import subprocess
from dataclasses import dataclass
from typing import Optional

from .version_checker import VersionChecker


@dataclass
class UpdateStatus:
    tool: str
    installed_version: Optional[str]
    available_version: Optional[str]
    update_available: bool


class UpdateChecker:
    """Check whether eSim tools have available APT updates."""

    PACKAGES = {
        "ngspice": "ngspice",
        "verilator": "verilator",
        "ghdl": "ghdl",
        "kicad": "kicad",
    }

    def __init__(self) -> None:
        self.version_checker = VersionChecker()

    def get_dpkg_version(
        self,
        package: str,
    ) -> Optional[str]:
        """Get the installed Debian package version."""

        try:
            result = subprocess.run(
                [
                    "dpkg-query",
                    "-W",
                    "-f=${Version}",
                    package,
                ],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )

            version = result.stdout.strip()

            if not version:
                return None

            return version

        except (subprocess.SubprocessError, OSError):
            return None

    def compare_versions(
        self,
        installed: Optional[str],
        available: Optional[str],
    ) -> bool:
        """Return True if the available version is newer."""

        if not installed or not available:
            return False

        try:
            result = subprocess.run(
                [
                    "dpkg",
                    "--compare-versions",
                    installed,
                    "lt",
                    available,
                ],
                check=False,
            )

            return result.returncode == 0

        except (subprocess.SubprocessError, OSError):
            return False

    def check_tool(
        self,
        tool_name: str,
    ) -> UpdateStatus:
        """Check update status for one tool."""

        tool_name = tool_name.lower()

        if tool_name not in self.PACKAGES:
            raise ValueError(
                f"Unsupported tool: {tool_name}"
            )

        package = self.PACKAGES[tool_name]

        installed_version = self.get_dpkg_version(
            package
        )

        available_version = (
            self.version_checker.get_available_version(
                package
            )
        )

        update_available = self.compare_versions(
            installed_version,
            available_version,
        )

        return UpdateStatus(
            tool=tool_name,
            installed_version=installed_version,
            available_version=available_version,
            update_available=update_available,
        )

    def check_all(self) -> list[UpdateStatus]:
        """Check update status for all supported tools."""

        return [
            self.check_tool(tool)
            for tool in self.PACKAGES
        ]


if __name__ == "__main__":
    checker = UpdateChecker()

    print("eSim Update Checker")
    print("=" * 70)

    for status in checker.check_all():

        print(f"\n{status.tool}")

        print(
            f"  Installed : "
            f"{status.installed_version or 'Not installed'}"
        )

        print(
            f"  Available : "
            f"{status.available_version or 'Not available'}"
        )

        if status.installed_version is None:
            print("  Status    : Not installed")

        elif status.available_version is None:
            print("  Status    : Unable to check")

        elif status.update_available:
            print("  Status    : Update available")

        else:
            print("  Status    : Up to date")	
