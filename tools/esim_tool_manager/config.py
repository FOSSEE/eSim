from configparser import ConfigParser
from pathlib import Path


class ConfigManager:
    """Manage eSim Tool Manager configuration."""

    DEFAULT_CONFIG = {
        "system": {
            "package_manager": "apt",
        },
        "esim": {
            "installation_path": "/opt/esim",
        },
        "updates": {
            "auto_check": "true",
        },
        "tools": {
            "ngspice": "ngspice",
            "verilator": "verilator",
            "ghdl": "ghdl",
            "kicad": "kicad",
        },
    }

    def __init__(self, config_path: str = "config/esim_manager.ini"):
        self.config_path = Path(config_path)
        self.config = ConfigParser()

        self._ensure_config_directory()
        self.load()

    def _ensure_config_directory(self) -> None:
        """Create the configuration directory if required."""

        self.config_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    def create_default_config(self) -> None:
        """Create a default configuration file."""

        self.config.clear()

        for section, values in self.DEFAULT_CONFIG.items():
            self.config[section] = values

        self.save()

    def load(self) -> None:
        """Load configuration or create defaults."""

        if not self.config_path.exists():
            self.create_default_config()
            return

        self.config.read(self.config_path)

    def save(self) -> None:
        """Save configuration to disk."""

        with self.config_path.open(
            "w",
            encoding="utf-8",
        ) as config_file:
            self.config.write(config_file)

    def get(
        self,
        section: str,
        option: str,
        fallback=None,
    ):
        """Get a configuration value."""

        return self.config.get(
            section,
            option,
            fallback=fallback,
        )

    def set(
        self,
        section: str,
        option: str,
        value: str,
    ) -> None:
        """Set and save a configuration value."""

        if not self.config.has_section(section):
            self.config.add_section(section)

        self.config.set(
            section,
            option,
            value,
        )

        self.save()

    def display(self) -> None:
        """Display all configuration settings."""

        print("eSim Tool Manager Configuration")
        print("=" * 60)

        for section in self.config.sections():
            print(f"\n[{section}]")

            for option, value in self.config.items(section):
                print(f"{option} = {value}")


if __name__ == "__main__":
    manager = ConfigManager()

    manager.display()
