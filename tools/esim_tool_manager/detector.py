import shutil
import subprocess
from dataclasses import dataclass
from typing import Optional


@dataclass
class ToolStatus:
    name: str
    command: str
    installed: bool
    version: Optional[str] = None


class ToolDetector:
    """Detect installed eSim external tools."""

    TOOLS = {
        "ngspice": "ngspice",
        "verilator": "verilator",
        "ghdl": "ghdl",
        "kicad": "kicad",
    }

    def detect_tool(self, name: str, command: str) -> ToolStatus:
        """Detect whether a tool is installed."""

        executable = shutil.which(command)

        if executable is None:
            return ToolStatus(
                name=name,
                command=command,
                installed=False,
            )

        if command == "kicad":
            version = self._get_kicad_version()
        else:
            version = self._get_version(command)

        return ToolStatus(
            name=name,
            command=command,
            installed=True,
            version=version,
        )

    def _get_version(self, command: str) -> Optional[str]:
        """Get the version of a standard command-line tool."""

        try:
            result = subprocess.run(
                [command, "--version"],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )

            output = result.stdout.strip() or result.stderr.strip()

            if not output:
                return None

            return output.splitlines()[0]

        except (subprocess.SubprocessError, OSError):
            return None

    def _get_kicad_version(self) -> Optional[str]:
        """
        Get KiCad version from the installed APT package.

        KiCad does not support the standard --version argument,
        so dpkg-query is used instead.
        """

        try:
            result = subprocess.run(
                [
                    "dpkg-query",
                    "-W",
                    "-f=${Version}",
                    "kicad",
                ],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )

            version = result.stdout.strip()

            if version:
                return version

        except (subprocess.SubprocessError, OSError):
            pass

        return None

    def scan(self) -> list[ToolStatus]:
        """Scan all supported eSim tools."""

        return [
            self.detect_tool(name, command)
            for name, command in self.TOOLS.items()
        ]


if __name__ == "__main__":
    detector = ToolDetector()

    print("eSim Tool Detection")
    print("=" * 60)

    for tool in detector.scan():
        if tool.installed:
            version = tool.version or "Version unknown"

            print(
                f"{tool.name:<12}: "
                f"Installed ({version})"
            )
        else:
            print(
                f"{tool.name:<12}: "
                "Not installed"
            )
