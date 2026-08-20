import logging
from pathlib import Path


class ToolManagerLogger:
    """Logging system for the eSim Tool Manager."""

    def __init__(
        self,
        log_path: str = "logs/tool_manager.log",
    ) -> None:
        self.log_path = Path(log_path)

        self.log_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.logger = logging.getLogger(
            "esim_tool_manager"
        )

        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:
            handler = logging.FileHandler(
                self.log_path,
                encoding="utf-8",
            )

            formatter = logging.Formatter(
                "%(asctime)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )

            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def info(self, event: str, message: str) -> None:
        """Record an informational event."""

        self.logger.info(
            "%s | %s",
            event,
            message,
        )

    def install_start(self, tool: str) -> None:
        self.info(
            "INSTALL_START",
            f"Installing {tool}",
        )

    def install_success(
        self,
        tool: str,
        version: str,
    ) -> None:
        self.info(
            "INSTALL_SUCCESS",
            f"{tool} installed version={version}",
        )

    def install_failed(
        self,
        tool: str,
    ) -> None:
        self.info(
            "INSTALL_FAILED",
            f"Failed to install {tool}",
        )

    def update_check(self) -> None:
        self.info(
            "UPDATE_CHECK",
            "Checking package updates",
        )

    def upgrade_start(self, tool: str) -> None:
        self.info(
            "UPGRADE_START",
            f"Upgrading {tool}",
        )

    def upgrade_success(
        self,
        tool: str,
        version: str,
    ) -> None:
        self.info(
            "UPGRADE_SUCCESS",
            f"{tool} upgraded version={version}",
        )

    def upgrade_failed(
        self,
        tool: str,
    ) -> None:
        self.info(
            "UPGRADE_FAILED",
            f"Failed to upgrade {tool}",
        )


if __name__ == "__main__":
    logger = ToolManagerLogger()

    logger.info(
        "SYSTEM",
        "Tool Manager logging initialized",
    )

    logger.install_start("Verilator")

    logger.install_success(
        "Verilator",
        "5.032",
    )

    logger.update_check()

    logger.upgrade_start("Verilator")

    logger.upgrade_success(
        "Verilator",
        "5.032",
    )

    print("Logging test completed.")
    print("Log file: logs/tool_manager.log")
