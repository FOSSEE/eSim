import argparse
from colorama import Fore, Style, init
from tool_manager.detector import check_tool
from tool_manager.dependency_checker import check_dependency
from tool_manager.installer import install_tool
from tool_manager.updater import check_update
from tool_manager.config_manager import is_in_path

init(autoreset=True)

def ok(msg): return Fore.GREEN + "✔ " + msg + Style.RESET_ALL
def bad(msg): return Fore.RED + "✖ " + msg + Style.RESET_ALL
def info(msg): return Fore.CYAN + "ℹ " + msg + Style.RESET_ALL

def main():
    parser = argparse.ArgumentParser(description="Automated Tool Manager for eSim")

    parser.add_argument("--check", action="store_true", help="Check tools and dependencies")
    parser.add_argument("--install", help="Install a tool (ngspice/kicad)")
    parser.add_argument("--update-check", help="Check if tool update is required")

    args = parser.parse_args()

    if args.check:
        print(info("Checking External Tools\n"))

        for tool, cmd in {
            "Ngspice": ["ngspice", "--version"],
            "KiCad": ["kicad", "--version"]
        }.items():
            installed, version = check_tool(tool, cmd)
            if installed:
                print(ok(f"{tool} installed"))
                print("  Version:", version)
            else:
                print(bad(f"{tool} not installed"))
                print("  Hint: Install and add to PATH")

        print(info("\nChecking System Dependencies\n"))
        print(ok("Python available") if check_dependency(["python", "--version"]) else bad("Python missing"))
        print(ok("Git available") if check_dependency(["git", "--version"]) else bad("Git missing"))

    if args.install:
        install_tool(args.install)

    if args.update_check:
        installed, version = check_tool(args.update_check, [args.update_check.lower(), "--version"])
        needs_update, rec = check_update(args.update_check, version)
        if needs_update:
            print(bad(f"{args.update_check} update recommended → version {rec}"))
        else:
            print(ok(f"{args.update_check} is up to date"))

if __name__ == "__main__":
    main()
