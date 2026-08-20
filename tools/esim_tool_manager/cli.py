from .config import ConfigManager
from .dependency_checker import DependencyChecker
from .detector import ToolDetector
from .installer import ToolInstaller
from .logger import ToolManagerLogger
from .update_checker import UpdateChecker
from .upgrade_manager import UpgradeManager


class ToolManagerCLI:
    """Interactive command-line interface for eSim Tool Manager."""

    TOOLS = [
        "ngspice",
        "verilator",
        "ghdl",
        "kicad",
    ]

    def __init__(self) -> None:
        self.detector = ToolDetector()
        self.installer = ToolInstaller()
        self.dependency_checker = DependencyChecker()
        self.update_checker = UpdateChecker()
        self.upgrade_manager = UpgradeManager()
        self.config = ConfigManager()
        self.logger = ToolManagerLogger()

    def display_menu(self) -> None:
        """Display the main menu."""

        print("\n")
        print("=" * 60)
        print("             eSim Automated Tool Manager")
        print("=" * 60)
        print("1. Scan Tools")
        print("2. Install Tool")
        print("3. Dependency Check")
        print("4. System Information")
        print("5. Check Updates")
        print("6. Upgrade Tool")
        print("7. Configuration")
        print("8. View Logs")
        print("9. Exit")
        print("=" * 60)

    def scan_tools(self) -> None:
        """Display detected tools."""

        print("\neSim Tool Detection")
        print("=" * 60)

        for tool in self.detector.scan():
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

    def select_tool(self) -> str | None:
        """Ask the user to select a supported tool."""

        print("\nSelect Tool")
        print("-" * 40)

        for index, tool in enumerate(self.TOOLS, start=1):
            print(f"{index}. {tool}")

        choice = input("\nEnter choice: ").strip()

        try:
            number = int(choice)

            if 1 <= number <= len(self.TOOLS):
                return self.TOOLS[number - 1]

        except ValueError:
            pass

        print("Invalid tool selection.")
        return None

    def install_tool(self) -> None:
        """Install a selected tool."""

        tool = self.select_tool()

        if tool is None:
            return

        self.logger.install_start(tool)

        success = self.installer.install(tool)

        if success:
            status = self.detector.detect_tool(
                tool,
                self.installer.PACKAGES[tool],
            )

            version = status.version or "unknown"

            self.logger.install_success(
                tool,
                version,
            )
        else:
            self.logger.install_failed(tool)

    def dependency_check(self) -> None:
        """Run the dependency checker."""

        self.dependency_checker.check()

    def system_information(self) -> None:
        """Display basic system information."""

        import platform
        import sys

        print("\neSim System Information")
        print("=" * 60)
        print(f"Operating System : {platform.system()}")
        print(f"OS Version       : {platform.release()}")
        print(f"Architecture     : {platform.machine()}")
        print(f"Python Version   : {sys.version.split()[0]}")
        print(
            f"Package Manager  : "
            f"{self.config.get('system', 'package_manager')}"
        )
        print(
            f"eSim Path        : "
            f"{self.config.get('esim', 'installation_path')}"
        )

    def check_updates(self) -> None:
        """Check updates for all supported tools."""

        self.logger.update_check()

        print("\neSim Update Check")
        print("=" * 60)

        for status in self.update_checker.check_all():

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

    def upgrade_tool(self) -> None:
        """Upgrade a selected tool."""

        tool = self.select_tool()

        if tool is None:
            return

        self.logger.upgrade_start(tool)

        success = self.upgrade_manager.upgrade(tool)

        if success:
            version = (
                self.upgrade_manager
                ._get_package_version(
                    self.upgrade_manager.PACKAGES[tool]
                )
                or "unknown"
            )

            self.logger.upgrade_success(
                tool,
                version,
            )
        else:
            self.logger.upgrade_failed(tool)

    def configuration(self) -> None:
        """Display configuration."""

        self.config.display()

    def view_logs(self) -> None:
        """Display the tool manager log."""

        log_path = self.logger.log_path

        print("\neSim Tool Manager Logs")
        print("=" * 60)

        if not log_path.exists():
            print("No log file found.")
            return

        try:
            content = log_path.read_text(
                encoding="utf-8"
            )

            if content.strip():
                print(content)
            else:
                print("Log file is empty.")

        except OSError as error:
            print(f"Unable to read log file: {error}")

    def run(self) -> None:
        """Run the interactive CLI."""

        self.logger.info(
            "SYSTEM",
            "Tool Manager started",
        )

        while True:
            self.display_menu()

            choice = input(
                "Enter your choice: "
            ).strip()

            if choice == "1":
                self.scan_tools()

            elif choice == "2":
                self.install_tool()

            elif choice == "3":
                self.dependency_check()

            elif choice == "4":
                self.system_information()

            elif choice == "5":
                self.check_updates()

            elif choice == "6":
                self.upgrade_tool()

            elif choice == "7":
                self.configuration()

            elif choice == "8":
                self.view_logs()

            elif choice == "9":
                self.logger.info(
                    "SYSTEM",
                    "Tool Manager stopped",
                )

                print("\nExiting eSim Tool Manager...")
                break

            else:
                print(
                    "\nInvalid choice. "
                    "Please select 1-9."
                )


if __name__ == "__main__":
    ToolManagerCLI().run()
