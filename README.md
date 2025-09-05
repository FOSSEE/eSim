# eSim Tool Manager (ETM)

---

## Features
- **Tool Installation** — Install supported tools via system package managers.
- **Update Management** — Check for and upgrade installed tools.
- **Configuration Handling** — Manage user-specific paths and environment variables.
- **Dependency Check** — Validate presence of essentials like `git` and `python3`.
- **Cross-Platform** — Supports Linux, macOS, and Windows where package managers are available.

---

## Usage

From the repository root:

    python -m etm --help

Common commands:

    python -m etm list-tools       # List supported tools
    python -m etm status           # Show installed tool status
    python -m etm install ngspice  # Install a tool
    python -m etm update kicad     # Update a tool
    python -m etm doctor           # Run dependency checks

---

## Configuration

Configuration is stored in a JSON file at an OS-appropriate location:

- **Linux/macOS:** `~/.config/esim-tool-manager/config.json`  
- **Windows:** `%APPDATA%\esim-tool-manager\config.json`

View or update configuration values:

    python -m etm show-config
    python -m etm set-config --key esim_root --value "/opt/esim"

---
