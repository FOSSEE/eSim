"""
esim_tool_manager.cli
----------------------
Simple, user-friendly command-line interface for the Automated Tool Manager.

Usage:
    python -m esim_tool_manager list
    python -m esim_tool_manager install ngspice
    python -m esim_tool_manager check-updates
    python -m esim_tool_manager update ngspice
    python -m esim_tool_manager check-deps ngspice
    python -m esim_tool_manager configure ngspice
    python -m esim_tool_manager logs
"""

import argparse
import sys

from .core import ToolManager, LOG_DIR


def _run_guarded(manager, fn, tool_name, *args, **kwargs):
    """Run a ToolManager method, converting unknown-tool errors into a
    clean, user-friendly CLI message instead of a raw traceback."""
    try:
        return fn(tool_name, *args, **kwargs)
    except ValueError as e:
        print(f"Error: {e}\n")
        print("Available tools:")
        for name in manager.config.registry:
            print(f"  {name}")
        sys.exit(1)


def print_table(rows):
    if not rows:
        print("No tools registered.")
        return
    name_w = max(len(r["name"]) for r in rows) + 2
    print(f"{'TOOL'.ljust(name_w)}{'INSTALLED'.ljust(15)}{'LATEST'.ljust(15)}{'UPDATE?'}")
    print("-" * (name_w + 40))
    for r in rows:
        update_flag = "YES" if r["update_available"] else "no"
        print(
            f"{r['name'].ljust(name_w)}"
            f"{str(r['installed_version']).ljust(15)}"
            f"{str(r['latest_known_version']).ljust(15)}"
            f"{update_flag}"
        )


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="esim-tool-manager",
        description="Automated Tool Manager for eSim external tools."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="List known tools, installed versions, and update availability.")

    p_install = sub.add_parser("install", help="Install a tool.")
    p_install.add_argument("tool")
    p_install.add_argument("--dry-run", action="store_true")

    sub.add_parser("check-updates", help="Check for available updates across all tools.")

    p_update = sub.add_parser("update", help="Update a specific tool.")
    p_update.add_argument("tool")
    p_update.add_argument("--dry-run", action="store_true")

    p_deps = sub.add_parser("check-deps", help="Check system dependencies for a tool.")
    p_deps.add_argument("tool")

    p_conf = sub.add_parser("configure", help="Configure PATH/environment for a tool.")
    p_conf.add_argument("tool")

    sub.add_parser("logs", help="Show path to the action log file.")

    args = parser.parse_args(argv)
    manager = ToolManager()

    if args.command == "list":
        print_table(manager.list_tools())

    elif args.command == "install":
        ok = _run_guarded(manager, manager.install, args.tool, dry_run=args.dry_run)
        sys.exit(0 if ok else 1)

    elif args.command == "check-updates":
        updates = manager.check_updates()
        if updates:
            print_table(updates)

    elif args.command == "update":
        ok = _run_guarded(manager, manager.update, args.tool, dry_run=args.dry_run)
        sys.exit(0 if ok else 1)

    elif args.command == "check-deps":
        ok = _run_guarded(manager, manager.check_dependencies, args.tool)
        sys.exit(0 if ok else 1)

    elif args.command == "configure":
        ok = _run_guarded(manager, manager.configure, args.tool)
        sys.exit(0 if ok else 1)

    elif args.command == "logs":
        print(f"Log file: {LOG_DIR / 'tool_manager.log'}")


if __name__ == "__main__":
    main()
