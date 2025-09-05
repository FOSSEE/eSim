# Design Document: eSim Tool Manager (ETM)

## 1. Purpose
The **eSim Tool Manager (ETM)** is a lightweight Python CLI designed to automate the installation, update, configuration, and dependency checks for external tools used by **eSim** (Ngspice, KiCad, Verilator, GHDL).  
The goal is to reduce manual environment setup and improve reproducibility.

---

## 2. Scope
This document covers:
- Overall architecture and design
- Module responsibilities
- Control flow for core operations (install, update, status, configure, doctor)
- Extensibility points
- Known limitations

---

## 3. High-Level Architecture
- **CLI Layer (`cli.py`)**: Parses user commands and routes them to the respective modules.  
- **Tool Registry (`tools.py`)**: Stores declarative mappings for supported tools and their commands.  
- **OS Abstraction (`os_ops.py`)**: Detects OS/package manager and executes system commands safely.  
- **Configuration (`config.py`)**: Persistent JSON-based configuration, stored per user.  
- **Dependency Checker (`dependency.py`)**: Validates required utilities and package managers.  
- **Logging (`logging_conf.py`)**: Centralized logging for console and file output.

---

## 4. Module Responsibilities
### `cli.py`
- Entry point (`python -m etm`)
- Subcommands:
  - `list-tools` – list supported tools
  - `status [tools...]` – show installation status and version
  - `install [tools...]` – install tools
  - `update [tools...]` – update tools
  - `configure` – update config and print PATH snippet
  - `doctor` – run dependency checks
  - `show-config` / `set-config` – inspect and modify config

### `tools.py`
- Contains `TOOL_REGISTRY` (dataclasses) with:
  - `name`, `check_cmd`, `installers`, `updaters`
- Helpers: `list_tool_names()`, `get_tool(name)`

### `os_ops.py`
- Detects OS (`platform`)
- Locates package managers (`apt-get`, `brew`, `choco`)
- Runs commands with `subprocess`
- Adds `sudo` prefix when needed
- Suggests installation steps for missing package managers

### `config.py`
- Manages JSON config at:
  - Linux/macOS → `~/.config/esim-tool-manager/config.json`
  - Windows → `%APPDATA%\esim-tool-manager\config.json`
- Functions: `load_config()`, `save_config()`

### `dependency.py`
- `check_basics()` ensures package managers (`apt`, `brew`, `choco`) and tools (`git`, `python3`, `curl`) are installed

### `logging_conf.py`
- Configures a logger (`etm`)
- Logs to both console and user-level log files

---

## 5. Control Flow Examples
### Install Flow (`python -m etm install ngspice`)
1. CLI parses `install` command and tool name.  
2. Detects OS and package manager.  
3. Retrieves tool entry from `TOOL_REGISTRY`.  
4. Ensures package manager exists.  
5. Runs installer command with `subprocess`.  
6. Logs and prints result.  

### Status Flow (`python -m etm status`)
1. CLI resolves `status`.  
2. For each tool, runs `check_cmd`.  
3. Parses return code to determine installation status.  
4. Prints version if available.  

### Configure Flow (`python -m etm configure`)
1. Loads config with `load_config()`.  
2. Ensures `esim_root` and other settings are present.  
3. Saves config back to disk.  
4. Prints PATH snippet if needed.  

---

## 6. Extensibility
- **Adding Tools**: Extend `TOOL_REGISTRY` in `tools.py`.  
- **New Package Managers**: Extend `os_ops.pkg_manager()` and update registry.  
- **Future Enhancements**: dry-run mode, parallel installs, version pinning, rollback, GUI wrapper.  

---

## 7. Security & Permissions
- Uses `sudo` on Unix-like systems when required.  
- On Windows, Chocolatey requires elevated shell.  
- ETM does not silently modify system files — only suggests PATH updates.  

---

## 8. Limitations
- Prototype-level installer/updater (assumes package names are consistent).  
- Version parsing is generic and may fail for certain tools.  
- Limited package manager support (apt, brew, choco).  

---

## 9. Testing
- Minimal unit tests (e.g., `test_registry.py`) ensure registry consistency.  
- Manual testing required across different OS/package manager combinations.  
