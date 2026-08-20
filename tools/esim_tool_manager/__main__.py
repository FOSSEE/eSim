from .cli import ToolManagerCLI


def main() -> None:
    """Start the eSim Tool Manager."""
    ToolManagerCLI().run()


if __name__ == "__main__":
    main()
