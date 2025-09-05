# eSim Tool Manager (ETM)

eSim Tool Manager (ETM) is a lightweight Python utility that automates the setup, installation, updating, and configuration of external tools required by eSim. It simplifies managing dependencies for tools like Ngspice, KiCad, Verilator, and GHDL, allowing you to focus on circuit design and simulation.

---

## Features 

- **Tool Installation** – Install supported tools via system package managers.
- **Update Management** – Check for and upgrade installed tools.
- **Configuration Handling** – Manage user-specific paths and environment variables.
- **Dependency Check** – Validate presence of essential tools like `git` and `python3`.
- **Cross-Platform** – Supports Linux, macOS, and Windows (where package managers are available).

---

## Usage

From the repository root, you can run:

```bash
python -m etm --help
```

### Common Commands

```bash
python -m etm list-tools        # List all supported tools
python -m etm status            # Show installation status of tools
python -m etm install ngspice   # Install Ngspice
python -m etm update kicad      # Update KiCad
python -m etm doctor            # Run dependency checks
```

---

## Configuration

Configuration is stored in a JSON file at an OS-appropriate location:

- **Linux/macOS**: `~/.config/esim-tool-manager/config.json`
- **Windows**: `%APPDATA%\esim-tool-manager\config.json`

### Manage Configuration

```bash
python -m etm show-config
python -m etm set-config --key esim_root --value "/opt/esim"
```

---

## Requirements

- Python 3.6+
- Internet connection (for installing/updating tools)
- Appropriate system package manager:
  - **Linux**: `apt`, `dnf`, `pacman`, etc.
  - **macOS**: `brew`
  - **Windows**: `choco`, `winget`
