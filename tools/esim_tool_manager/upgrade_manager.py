import shutil
import subprocess

from .detector import ToolDetector
from .update_checker import UpdateChecker


class UpgradeManager:
    """Upgrade eSim tools using APT."""

    PACKAGES = {
        "ngspice": "ngspice",
        "verilator": "verilator",
        "ghdl": "ghdl",
        "kicad": "kicad",
    }

    def __init__(self) -> None:
        self.detector = ToolDetector()
        self.update_checker = UpdateChecker()

    def upgrade(self, tool_name: str) -> bool:
        """Upgrade a supported tool."""

        tool_name = tool_name.lower()

        if tool_name not in self.PACKAGES:
            print(f"Unsupported tool: {tool_name}")
            return False

        if shutil.which("apt") is None:
            print("APT package manager is not available.")
            return False

        package = self.PACKAGES[tool_name]

        print(f"Checking updates for {tool_name}...")

        status = self.update_checker.check_tool(tool_name)

        if status.installed_version is None:
            print(
                f"{tool_name} is not installed. "
                "Use the installer first."
            )
            return False

        if status.available_version is None:
            print(
                f"Unable to determine the available "
                f"version for {tool_name}."
            )
            return False

        if not status.update_available:
            print(
                f"{tool_name} is already up to date "
                f"({status.installed_version})."
            )
            return True

        print(
            f"Updating {tool_name}: "
            f"{status.installed_version} -> "
            f"{status.available_version}"
        )

        try:
            result = subprocess.run(
                [
                    "sudo",
                    "apt",
                    "install",
                    "--only-upgrade",
                    "-y",
                    package,
                ],
                check=False,
            )

            if result.returncode != 0:
                print(f"Upgrade failed for {tool_name}.")
                return False

            print(f"{tool_name} upgrade completed.")

            return self.verify_upgrade(tool_name)

        except (OSError, subprocess.SubprocessError) as error:
            print(f"Upgrade error: {error}")
            return False

    def verify_upgrade(self, tool_name: str) -> bool:
        """Verify that the tool remains installed after upgrade."""

        tool_name = tool_name.lower()

        if tool_name not in self.PACKAGES:
            return False

        package = self.PACKAGES[tool_name]

        if shutil.which(package) is None:
            print(
                f"Verification failed: "
                f"{tool_name} is not available."
            )
            return False

        version = self._get_package_version(package)

        if version:
            print(
                f"Verification successful: "
                f"{tool_name} version {version}"
            )
            return True

        print(
            f"{tool_name} is installed, "
            "but its package version could not be determined."
        )

        return True

    @staticmethod
    def _get_package_version(package: str) -> str | None:
        """Get installed package version using dpkg-query."""

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

            return version or None

        except (OSError, subprocess.SubprocessError):
            return None


if __name__ == "__main__":
    manager = UpgradeManager()

    print("eSim Upgrade Manager")
    print("=" * 60)

    print("\nSupported tools:")

    for tool in manager.PACKAGES:
        print(f"- {tool}")

    print("\nExample:")
    print(
        "manager = UpgradeManager()"
    )
    print(
        "manager.upgrade('verilator')"
    )
