from .detector import ToolDetector


class DependencyChecker:
    """Check whether required eSim tools are available."""

    REQUIRED_TOOLS = [
        "ngspice",
        "verilator",
        "ghdl",
        "kicad",
    ]

    def __init__(self) -> None:
        self.detector = ToolDetector()

    def check(self) -> bool:
        """Check all required tools and return overall status."""

        results = self.detector.scan()
        all_available = True

        print("eSim Dependency Check")
        print("=" * 60)

        for tool in results:
            if tool.name not in self.REQUIRED_TOOLS:
                continue

            if tool.installed:
                version = tool.version or "Version unknown"
                print(
                    f"{tool.name:<12}: "
                    f"Installed ({version})"
                )
            else:
                print(
                    f"{tool.name:<12}: "
                    "Missing"
                )
                all_available = False

        print("=" * 60)

        if all_available:
            print("System Status: READY")
        else:
            print("System Status: MISSING DEPENDENCIES")

        return all_available


if __name__ == "__main__":
    checker = DependencyChecker()
    checker.check()
