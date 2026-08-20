import shutil
import subprocess
from typing import Optional

from .detector import ToolDetector


class ToolInstaller:
    """Install eSim external tools using APT."""

    PACKAGES = {
        "ngspice": "ngspice",
        "verilator": "verilator",
        "ghdl": "ghdl",
        "kicad": "kicad",
    }

    def __init__(self) -> None:
        self.detector = ToolDetector()

    def is_apt_available(self) -> bool:
        """Check whether APT is available on the system."""
        return shutil.which("apt") is not None

    def install(self, tool_name: str) -> bool:
        """Install a supported tool using APT."""

        tool_name = tool_name.lower()

        if tool_name not in self.PACKAGES:
            print(f"Unsupported tool: {tool_name}")
            return False

        if not self.is_apt_available():
            print("APT package manager is not available.")
            return False

        package = self.PACKAGES[tool_name]

        print(f"Installing {tool_name}...")
        print(f"APT package: {package}")

        try:
            result = subprocess.run(
                ["sudo", "apt", "update"],
                check=False,
            )

            if result.returncode != 0:
                print("Failed to update APT package information.")
                return False

            result = subprocess.run(
                ["sudo", "apt", "install", "-y", package],
                check=False,
            )

            if result.returncode != 0:
                print(f"Failed to install {tool_name}.")
                return False

            print(f"{tool_name} installation completed.")

            return self.verify_installation(tool_name)

        except (OSError, subprocess.SubprocessError) as error:
            print(f"Installation error: {error}")
            return False

    def verify_installation(self, tool_name: str) -> bool:
        """Verify that a tool is installed after installation."""

        tool_name = tool_name.lower()

        if tool_name not in self.PACKAGES:
            return False

        command = self.PACKAGES[tool_name]

        if shutil.which(command) is None:
            print(f"Verification failed: {tool_name} not found.")
            return False

        status = self.detector.detect_tool(
            tool_name,
            command,
        )

        if status.installed:
            print(
                f"Verification successful: "
                f"{tool_name} "
                f"({status.version or 'version unknown'})"
            )
            return True

        print(f"Verification failed: {tool_name}")
        return False

    def install_missing_tools(self) -> None:
        """Install all supported tools that are currently missing."""

        for tool_name in self.PACKAGES:
            command = self.PACKAGES[tool_name]

            if shutil.which(command):
                print(f"{tool_name}: already installed")
                continue

            print(f"{tool_name}: missing")
            self.install(tool_name)


if __name__ == "__main__":
    installer = ToolInstaller()

    print("eSim Tool Installer")
    print("=" * 60)

    print("\nSupported tools:")
    for tool in installer.PACKAGES:
        print(f"- {tool}")

    print("\nExample:")
    print("python3 -m tools.esim_tool_manager.installer")
